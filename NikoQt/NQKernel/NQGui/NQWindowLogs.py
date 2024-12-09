import html
import time
import traceback

from NikoKit.NikoQt.NQAdapter import QHBoxLayout, QStackedWidget
from NikoKit.NikoQt import NQApplication
from NikoKit.NikoLib import NKLogger
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetArea import NQWidgetArea
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetCheckList import NQWidgetCheckList
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetConsoleTextEdit import NQWidgetConsoleTextEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow
from NikoKit.NikoStd import NKConst


class NQWindowLogs(NQWindow):
    def __init__(self, nk_logger=None, *args, **kwargs):
        # Data
        if nk_logger:
            self.nk_logger = nk_logger
        else:
            self.nk_logger = NQApplication.Runtime.Service.NKLogger
        self.channel_to_console = {}
        self.channel_to_log_count = {}

        # GUI Components
        self.main_lay = None
        self.channel_area = None
        self.channel_checklist = None
        self.console_stack = None

        super(NQWindowLogs, self).__init__(*args, **kwargs)

    def construct(self):
        super(NQWindowLogs, self).construct()

        main_lay = QHBoxLayout()
        channel_area = NQWidgetArea(title=self.lang("channel"))
        channel_checklist = NQWidgetCheckList(exclusive=True)
        console_stack = QStackedWidget()

        main_lay.addWidget(channel_area)
        main_lay.addWidget(console_stack)
        main_lay.setStretchFactor(console_stack, 1)
        channel_area.setCentralWidget(channel_checklist)

        self.setLayout(main_lay)

        self.main_lay = main_lay
        self.channel_area = channel_area
        self.channel_checklist = channel_checklist
        self.console_stack = console_stack

    def connect_signals(self):
        super(NQWindowLogs, self).connect_signals()
        NQApplication.Runtime.Signals.tick_passed.connect(self.slot_refresh)

    def slot_refresh(self):
        for channel in self.nk_logger.logs.keys():
            if channel not in self.channel_to_console.keys():
                console = NQWidgetConsoleTextEdit()
                self.channel_to_console[channel] = console
                self.channel_to_log_count[channel] = 0
                self.console_stack.addWidget(console)
                self.channel_checklist.add_option(option_name=channel, display_text=channel, checked=True)

        selected_channel = self.channel_checklist.get_checked()
        self.console_stack.setCurrentWidget(self.channel_to_console[selected_channel])

        try:
            logs = self.nk_logger.logs[selected_channel]
            if len(logs) != self.channel_to_log_count[selected_channel]:
                self.channel_to_log_count[selected_channel] = len(logs)
                log_str = ""
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
                self.channel_to_console[selected_channel].setHtml(log_str)
        except Exception as e:
            err_msg = NQFunctions.html_escape(traceback.format_exc())
            self.channel_to_console[selected_channel].setHtml(
                NQFunctions.color_line(line="FAIL::CONNECT TO NKLOGGER CHANNEL <br/> %s " % err_msg,
                                       color_hex=NKConst.COLOR_RED,
                                       change_line=False))
