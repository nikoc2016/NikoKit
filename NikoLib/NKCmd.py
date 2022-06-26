import socket
import socketserver
import threading
import uuid

from NikoKit.NikoStd import NKConst
from NikoKit.NikoStd.NKDataStructure import NKDataStructure
from NikoKit.NikoStd.NKPrint import tprint
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin
from NikoKit.NikoStd.NKTime import NKDatetime


class NKCmdServer(NKPrintableMixin):
    # Instance
    host = ""
    port = 44444
    command_id_to_task = {}
    command_server = None
    command_to_help_text = {}
    handler_func = None
    udp_thread = None

    # Constants
    RESULT_SIGN_GOOD = "GOOD "
    RESULT_SIGN_FAIL = "FAIL "

    @classmethod
    def launch(cls, host, port, handler_func, silent_mode=False):
        cls.host = host
        cls.port = port
        cls.handler_func = handler_func
        cls.stop(silent_mode=True)
        cls.udp_thread = cls.UdpThread()
        cls.udp_thread.start()
        if not silent_mode:
            tprint("Cmd::Server OK.")

    @classmethod
    def stop(cls, silent_mode=False):
        try:
            cls.udp_thread.stop()
            cls.udp_thread.join()
        except:
            pass
        cls.udp_thread = None
        if not silent_mode:
            tprint("Cmd::Server Shutdown.")

    @classmethod
    def register_command(cls, command_keyword, help_text):
        cls.command_to_help_text[command_keyword] = help_text

    @classmethod
    def execute_command(cls,
                        command_line,
                        client_socket,
                        client_address):
        command_id = str(uuid.uuid4())
        command_task = cls.CommandTask(
            command_id=command_id,
            command_line=command_line,
            receive_datetime=NKDatetime.now(),
            client_socket=client_socket,
            client_address=client_address,
        )
        cls.command_id_to_task[command_id] = command_task

        # Check if command is registered
        is_registered = False
        for registered_command in cls.command_to_help_text.keys():
            if command_line.lower().startswith(registered_command.lower()):
                is_registered = True
                break

        if is_registered:
            cls.handler_func(command_id, command_line)
        elif command_line == "help":
            help_str = "\n"
            for command in cls.command_to_help_text.keys():
                help_str += ("%s - %s\n" % (command, cls.command_to_help_text[command]))
            cls.handler_func(command_id, command_line)
            cls.finish_command(command_id=command_id,
                               result_sign=cls.RESULT_SIGN_GOOD,
                               result_detail=help_str)

        elif command_line == "ping":
            help_str = "pong"
            cls.handler_func(command_id, command_line)
            cls.finish_command(command_id=command_id,
                               result_sign=cls.RESULT_SIGN_GOOD,
                               result_detail=help_str)
            
        else:
            cls.finish_command(command_id=command_id,
                               result_sign=cls.RESULT_SIGN_FAIL,
                               result_detail="Unknown Command `%s`" % str(command_line))

    @classmethod
    def finish_command(cls, command_id, result_sign, result_detail):
        command_task = cls.command_id_to_task[command_id]
        result_detail = str(result_detail)
        if command_task.result or command_task.send_datetime:
            tprint("Cmd::finish_command::Command %i is already finished. New result does not apply: %s" % (command_id,
                                                                                                          result_detail))
        else:
            command_task.result = result_detail
            command_task.send_datetime = NKDatetime.now()
            try:
                command_task.client_socket.sendto(bytes(result_sign + result_detail, NKConst.SYS_CHARSET),
                                                  command_task.client_address)
                command_task.client_socket = None
            except Exception as e:
                tprint(
                    "Cmd::finish_command::[Command %i: %s] Fail to send back: %s" % (command_id, result_detail, str(e)))

    class CommandTask(NKDataStructure):
        def __init__(self,
                     command_id,
                     command_line,
                     receive_datetime,
                     client_socket,
                     client_address,
                     result=None,
                     send_datetime=None,
                     *args, **kwargs):
            self.command_id = command_id
            self.command_line = command_line
            self.receive_datetime = receive_datetime
            self.client_socket = client_socket
            self.client_address = client_address
            self.result = result
            self.send_datetime = send_datetime

            super(NKCmdServer.CommandTask, self).__init__(*args, **kwargs)

        def p_key(self):
            return self.command_id

    class CommandHandler(socketserver.BaseRequestHandler):
        def handle(self):
            command_line = self.request[0].strip()
            try:
                command_line = command_line.decode()
            except:
                pass

            sock = self.request[1]

            NKCmdServer.execute_command(
                command_line=command_line,
                client_socket=sock,
                client_address=self.client_address
            )

    class UdpThread(threading.Thread):
        def __init__(self):
            super(NKCmdServer.UdpThread, self).__init__()
            self.udp_server = None

        def run(self):
            self.udp_server = socketserver.UDPServer((NKCmdServer.host,
                                                      NKCmdServer.port),
                                                     NKCmdServer.CommandHandler)
            self.udp_server.serve_forever()

        def stop(self):
            self.udp_server.server_close()


class NKCmdClient(NKPrintableMixin):
    def __init__(self, host, port, *args, **kwargs):
        super(NKCmdClient, self).__init__(*args, **kwargs)

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

    def launch_manual_mode(self):
        tprint("NKCmdClient")

        while True:
            user_input = input("$ ")
            try:
                self.sock.sendto(bytes(user_input, NKConst.SYS_CHARSET), (self.host, self.port))
                received = str(self.sock.recv(1024), NKConst.SYS_CHARSET)
                tprint(received)
            except Exception as e:
                tprint(repr(e))
