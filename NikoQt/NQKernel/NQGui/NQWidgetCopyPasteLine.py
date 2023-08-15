from NikoKit.NikoQt.NQAdapter import QHBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout_margin
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetCopyPasteLine(NQWidget):
    def __init__(self, prompt="CopyPaste->", no_copy=False, no_paste=False, read_only=True):
        self.prompt = prompt
        self.no_copy = no_copy
        self.no_paste = no_paste
        self.read_only = read_only
        self.main_lay: QHBoxLayout = None
        self.prompt: QLabel = None
        self.line_edit: QLineEdit = None
        self.btn_copy: QPushButton = None
        self.btn_paste: QPushButton = None

        super().__init__()

    def construct(self):
        super().construct()
        self.main_lay = QHBoxLayout()
        self.prompt = QLabel(self.prompt)
        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(self.read_only)
        self.btn_copy = QPushButton(self.lang("copy"))
        if self.no_copy:
            self.btn_copy.hide()
        self.btn_paste = QPushButton(self.lang("paste"))
        if self.no_paste:
            self.btn_paste.hide()
        self.main_lay.addWidget(self.prompt)
        self.main_lay.addWidget(self.line_edit)
        self.main_lay.addWidget(self.btn_copy)
        self.main_lay.addWidget(self.btn_paste)
        clear_layout_margin(self.main_lay)
        self.setLayout(self.main_lay)

    def connect_signals(self):
        super().connect_signals()
        self.btn_copy.clicked.connect(self.slot_copy)
        self.btn_paste.clicked.connect(self.slot_paste)

    def set_value(self, target_value):
        self.line_edit.setText(target_value)

    def get_value(self):
        return str(self.line_edit.text())

    def slot_copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.get_value())

    def slot_paste(self):
        clipboard = QApplication.clipboard()
        self.set_value(clipboard.text())
