import html

from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoLib import NKLogger
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow
from NikoKit.NikoStd import NKConst


class NQWindowConsole(NQWindow):
    def __init__(self, allow_execute=False, *args, **kwargs):
        # Variable
        self.allow_execute = allow_execute
        self.log_records_count = 0
        self.exec_dict = {"Runtime": NQApplication.Runtime}

        # Switches
        self.enable_auto_scroll = True

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

        log_text_edit = QTextEdit()
        log_text_edit.setLineWrapMode(QTextEdit.NoWrap)
        log_text_edit.setReadOnly(True)
        command_line_edit = QLineEdit()
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
        NQApplication.Runtime.Signals.tick_passed.connect(self.slot_refresh)

    def slot_clear(self):
        self.slot_clear_command_line()
        self.slot_clear_log()

    def slot_clear_command_line(self):
        self.command_line_edit.setText("")

    def slot_clear_log(self):
        self.log_text_edit.setHtml("")

    def slot_refresh(self):
        self.auto_scroll_check()
        if self.isVisible() and self.enable_auto_scroll:
            self.load_logs()
        self.auto_scroll()

    def scroll_bar_at_bottom(self):
        scroll_bar = self.log_text_edit.verticalScrollBar()
        is_at_bottom = scroll_bar.value() >= scroll_bar.maximum() - 4
        return is_at_bottom

    def auto_scroll_check(self):
        if self.scroll_bar_at_bottom():
            self.enable_auto_scroll = True
        else:
            self.enable_auto_scroll = False

    def auto_scroll(self):
        if self.enable_auto_scroll and not self.scroll_bar_at_bottom():
            self.log_text_edit.moveCursor(QTextCursor.End)
            self.log_text_edit.ensureCursorVisible()

    def load_logs(self):
        pass

    def slot_execute(self):
        pass


class NQWindowPythonConsole(NQWindowConsole):
    def load_logs(self):
        log_str = ""
        logs = NQApplication.Runtime.Service.NKLogger.logs
        if len(logs) > self.log_records_count:
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
                else:
                    log_str += NQFunctions.color_line(line=log_raw_str,
                                                      color_hex=NKConst.COLOR_GREY,
                                                      change_line=False)
            self.log_text_edit.setHtml(log_str)

    def slot_execute(self):
        exec(self.command_line_edit.text(), self.exec_dict)
        self.slot_clear_command_line()
