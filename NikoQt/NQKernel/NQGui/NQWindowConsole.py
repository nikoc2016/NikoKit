import html

from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoLib import NKLogger
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetConsoleLineEdit import NQWidgetConsoleLineEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetConsoleTextEdit import NQWidgetConsoleTextEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow
from NikoKit.NikoStd import NKConst


class NQWindowConsole(NQWindow):
    def __init__(self, allow_execute=False, *args, **kwargs):
        # Variable
        self.allow_execute = allow_execute
        self.cmd_history = [""]
        self.cmd_ptr = 0

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
        self.command_line_edit.upPressed.connect(self.slot_previous_command)
        self.command_line_edit.downPressed.connect(self.slot_next_command)
        NQApplication.Runtime.Signals.tick_passed.connect(self.load_logs)

    def slot_clear(self):
        self.slot_clear_command_line()
        self.slot_clear_log()

    def slot_clear_command_line(self):
        self.command_line_edit.setText("")

    def slot_clear_log(self):
        self.log_text_edit.setHtml("")

    def slot_clear_history(self):
        self.cmd_history = [""]
        self.cmd_ptr = 0

    def slot_execute(self):
        cmd = self.command_line_edit.text()
        self.cmd_history[-1] = cmd
        self.cmd_history.append("")
        self.cmd_ptr = len(self.cmd_history) - 1
        self.run_command(cmd)

    def slot_previous_command(self):
        self.cmd_ptr -= 1
        if self.cmd_ptr < 0:
            self.cmd_ptr = len(self.cmd_history) - 1
        self.command_line_edit.setText(self.cmd_history[self.cmd_ptr])

    def slot_next_command(self):
        self.cmd_ptr += 1
        if self.cmd_ptr == len(self.cmd_history):
            self.cmd_ptr = 0
        self.command_line_edit.setText(self.cmd_history[self.cmd_ptr])

    def load_logs(self):
        pass

    def run_command(self, command):
        pass


class NQWindowPythonConsole(NQWindowConsole):
    def __init__(self, allow_execute=False, custom_commands=None, *args, **kwargs):
        self.log_records_count = 0
        self.exec_dict = {"Runtime": NQApplication.Runtime, "log": NQApplication.Runtime.Service.NKLogger.log}
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
                log_raw_str = html.escape(str(log.log_context)).replace("\n", "<br/>").replace(" ", "&nbsp;")

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
        self.slot_clear_command_line()
