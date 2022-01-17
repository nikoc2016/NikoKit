from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow


class NQWindowInfo(NQWindow):
    def __init__(self, info_string, auto_change_line=True, *args, **kwargs):
        # Switches
        self.auto_change_line = auto_change_line

        # Data
        self.info_string = info_string

        # GUI Component
        self.main_lay = None
        self.message_text_edit = None
        self.understood_button = None

        super(NQWindowInfo, self).__init__(*args, **kwargs)

        self.slot_show()

    def construct(self):
        super(NQWindowInfo, self).construct()
        main_lay = QVBoxLayout()
        message_text_edit = QTextEdit()
        message_text_edit.setReadOnly(True)
        if not self.auto_change_line:
            message_text_edit.setLineWrapMode(QTextEdit.NoWrap)
        message_text_edit.setText(self.info_string)
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
