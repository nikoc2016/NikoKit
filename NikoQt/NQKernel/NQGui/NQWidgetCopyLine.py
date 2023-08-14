from NikoKit.NikoQt.NQAdapter import QHBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout_margin
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetCopyLine(NQWidget):
    def __init__(self, prompt="Copy->"):
        self.prompt = prompt
        self.main_lay: QHBoxLayout = None
        self.prompt: QLabel = None
        self.line_edit: QLineEdit = None
        self.btn_copy: QPushButton = None

        super().__init__()

    def construct(self):
        super().construct()
        self.main_lay = QHBoxLayout()
        self.prompt = QLabel(self.prompt)
        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(True)
        self.btn_copy = QPushButton(self.lang("copy"))
        self.main_lay.addWidget(self.prompt)
        self.main_lay.addWidget(self.line_edit)
        self.main_lay.addWidget(self.btn_copy)
        clear_layout_margin(self.main_lay)
        self.setLayout(self.main_lay)

    def connect_signals(self):
        super().connect_signals()
        self.btn_copy.clicked.connect(self.slot_copy)

    def set_value(self, target_value):
        self.line_edit.setText(target_value)

    def get_value(self):
        return str(self.line_edit.text())

    def slot_copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.get_value())
