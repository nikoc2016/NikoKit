from NikoKit.NikoQt.NQAdapter import Signal, Qt, QLineEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetConsoleLineEdit(NQMixin, QLineEdit):
    upPressed = Signal()
    downPressed = Signal()

    def __init__(self):
        self.cmd_history = [""]
        self.cmd_ptr = 0
        super(NQWidgetConsoleLineEdit, self).__init__()

    def connect_signals(self):
        super(NQWidgetConsoleLineEdit, self).connect_signals()
        self.upPressed.connect(self.slot_previous_command)
        self.downPressed.connect(self.slot_next_command)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Up:
            self.upPressed.emit()
        if event.key() == Qt.Key_Down:
            self.downPressed.emit()

    def slot_save_history(self, clear=True):
        self.cmd_history[-1] = self.text()
        self.cmd_history.append("")
        self.cmd_ptr = len(self.cmd_history) - 1
        if clear:
            self.setText("")

    def slot_previous_command(self):
        self.cmd_ptr -= 1
        if self.cmd_ptr < 0:
            self.cmd_ptr = len(self.cmd_history) - 1
        self.setText(self.cmd_history[self.cmd_ptr])

    def slot_next_command(self):
        self.cmd_ptr += 1
        if self.cmd_ptr == len(self.cmd_history):
            self.cmd_ptr = 0
        self.setText(self.cmd_history[self.cmd_ptr])

    def slot_clear_history(self):
        self.cmd_history = [""]
        self.cmd_ptr = 0
