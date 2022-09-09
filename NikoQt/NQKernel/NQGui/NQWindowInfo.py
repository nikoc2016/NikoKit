from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow


class NQWindowInfo(NQWindow):
    def __init__(self, info_string, auto_change_line=True, on_top=True, *args, **kwargs):
        # Switches
        self.auto_change_line = auto_change_line

        # GUI Component
        self.main_lay = None
        self.message_text_edit = None
        self.understood_button = None

        super(NQWindowInfo, self).__init__(*args, **kwargs)
        if on_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.slot_show()
        self.set_info(info_string)

    def construct(self):
        super(NQWindowInfo, self).construct()
        main_lay = QVBoxLayout()
        message_text_edit = QTextEdit()
        message_text_edit.setReadOnly(True)
        if not self.auto_change_line:
            message_text_edit.setLineWrapMode(QTextEdit.NoWrap)
        button_lay = QHBoxLayout()
        button_lay.setAlignment(Qt.AlignHCenter)
        understood_button = QPushButton(self.lang("i_understand"))

        main_lay.addWidget(message_text_edit)
        main_lay.addLayout(button_lay)
        button_lay.addWidget(understood_button)

        self.main_lay = main_lay
        self.message_text_edit = message_text_edit
        self.understood_button = understood_button

        self.setLayout(self.main_lay)

    def connect_signals(self):
        super(NQWindowInfo, self).connect_signals()
        self.understood_button.clicked.connect(self.slot_close)

    def set_info(self, info_string):
        self.message_text_edit.setText(info_string)
