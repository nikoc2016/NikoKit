import html
import os
import sys

import select
import socket

from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoLib import NKLogger, NKCmd
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetConsoleLineEdit import NQWidgetConsoleLineEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetConsoleTextEdit import NQWidgetConsoleTextEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow
from NikoKit.NikoStd import NKConst
from NikoKit.NikoStd.NKDataStructure import NKDataStructure
from NikoKit.NikoStd.NKTime import NKDatetime


class NQWindowConsole(NQWindow):
    def __init__(self, allow_execute=False, *args, **kwargs):
        # Variable
        self.allow_execute = allow_execute

        # GUI Components
        self.main_lay = None
        self.command_lay = None
        self.log_text_edit = None
        self.command_line_edit = None
        self.execute_button = None

        super(NQWindowConsole, self).__init__(*args, **kwargs)

        self.show()

    def construct(self):
        super(NQWindowConsole, self).construct()

        main_lay = QVBoxLayout()
        command_lay = QHBoxLayout()

        log_text_edit = NQWidgetConsoleTextEdit()
        command_line_edit = NQWidgetConsoleLineEdit()
        execute_button = QPushButton(self.lang("execute"))

        main_lay.addWidget(log_text_edit)
        main_lay.addLayout(command_lay)

        command_lay.addWidget(command_line_edit)
        command_lay.addWidget(execute_button)
        command_lay.setStretchFactor(command_line_edit, 1)

        self.setLayout(main_lay)
        self.main_lay = main_lay
        self.command_lay = command_lay
        self.log_text_edit = log_text_edit
        self.command_line_edit = command_line_edit
        self.execute_button = execute_button

        if not self.allow_execute:
            self.command_line_edit.setDisabled(True)
            self.execute_button.setDisabled(True)

    def connect_signals(self):
        super(NQWindowConsole, self).connect_signals()
        self.execute_button.clicked.connect(self.slot_execute)
        self.command_line_edit.returnPressed.connect(self.slot_execute)
        NQApplication.Runtime.Signals.tick_passed.connect(self.load_logs)

    def slot_clear(self):
        self.slot_clear_command_line()
        self.slot_clear_log()

    def slot_clear_command_line(self):
        self.command_line_edit.setText("")

    def slot_save_and_clear_command_line(self):
        self.command_line_edit.slot_save_history()

    def slot_clear_log(self):
        self.log_text_edit.setHtml("")

    def slot_execute(self):
        cmd = self.command_line_edit.text()
        self.run_command(cmd)
        self.slot_save_and_clear_command_line()

    def load_logs(self):
        pass

    def run_command(self, command):
        pass


class NQWindowPythonConsole(NQWindowConsole):
    def __init__(self, allow_execute=False, custom_commands=None, *args, **kwargs):
        self.log_records_count = 0
        self.exec_dict = {"Runtime": NQApplication.Runtime,
                          "log": NQApplication.Runtime.Service.NKLogger.log,
                          "p": os.path,
                          "os": os,
                          "sys": sys}
        if isinstance(custom_commands, dict):
            self.exec_dict.update(custom_commands)
        super(NQWindowPythonConsole, self).__init__(allow_execute, *args, **kwargs)

    def load_logs(self):
        log_str = ""
        logs = NQApplication.Runtime.Service.NKLogger.logs[NKLogger.CHANNEL_SYS]
        if len(logs) != self.log_records_count:
            self.log_records_count = len(logs)
            self.slot_clear_log()
            for log in logs:
                log_raw_str = NQFunctions.html_escape(log.log_context)

                if log.log_type == NKLogger.STD_OUT:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_STD_OUT,
                                                      change_line=False)
                elif log.log_type == NKLogger.STD_ERR:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_STD_ERR,
                                                      change_line=False)
                elif log.log_type == NKLogger.STD_WARNING:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_STD_WARNING,
                                                      change_line=False)
                else:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_GREY,
                                                      change_line=False)
            self.log_text_edit.setHtml(log_str)

    def run_command(self, command):
        exec(command, self.exec_dict)


class NQWindowNKCmdConsole(NQWindowConsole):
    def __init__(self, host, port, allow_execute=False, *args, **kwargs):
        self.logs = []
        self.logs_count_cache = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        self.host = host
        self.port = port

        super(NQWindowNKCmdConsole, self).__init__(allow_execute, *args, **kwargs)

    class CmdLog(NKDataStructure):
        CREATOR_ME = "CREATOR_ME"
        CREATOR_TARGET = "CREATOR_TARGET"

        def __init__(self, log_creator, log_context, log_datetime=None):
            self.log_creator = log_creator
            self.log_context = log_context
            if log_datetime:
                self.log_datetime = log_datetime
            else:
                self.log_datetime = NKDatetime.now()
            super(NQWindowNKCmdConsole.CmdLog, self).__init__()

    def load_logs(self):
        read_ready, ready_write, exceptional = select.select([self.sock], [], [], 0)
        if len(read_ready):
            try:
                received = str(self.sock.recv(1024), NKConst.SYS_CHARSET)
            except WindowsError as e:
                if e.winerror == 10054:
                    received = "FAIL Server Offline"
                else:
                    received = "FAIL " + str(e)
            self.logs.append(self.CmdLog(log_creator=self.CmdLog.CREATOR_TARGET,
                                         log_context=received))

        log_str = ""

        if len(self.logs) != self.logs_count_cache:
            self.logs_count_cache = len(self.logs)
            self.slot_clear_log()
            for log in self.logs:
                log_raw_str = NQFunctions.html_escape(log.log_context)

                if log.log_creator == self.CmdLog.CREATOR_ME:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_GOLD,
                                                      change_line=True)

                elif log.log_creator == self.CmdLog.CREATOR_TARGET and \
                        log.log_context.startswith(NKCmd.NKCmdServer.RESULT_SIGN_GOOD):
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_GREEN,
                                                      change_line=True)

                elif log.log_creator == self.CmdLog.CREATOR_TARGET and \
                        log.log_context.startswith(NKCmd.NKCmdServer.RESULT_SIGN_FAIL):
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_RED,
                                                      change_line=True)
                else:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_GREY,
                                                      change_line=True)

            self.log_text_edit.setHtml(log_str)

    def run_command(self, command):
        try:
            self.logs.append(self.CmdLog(log_creator=self.CmdLog.CREATOR_ME,
                                         log_context=command))
            self.sock.sendto(bytes(command, NKConst.SYS_CHARSET), (self.host, self.port))
        except Exception as e:
            self.logs.append(self.CmdLog(log_creator=self.CmdLog.CREATOR_TARGET,
                                         log_context=NKCmd.NKCmdServer.RESULT_SIGN_FAIL + repr(e)))
