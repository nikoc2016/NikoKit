import re

from PySide2.QtCore import Signal

from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget

from PySide2.QtWidgets import QLabel, QLineEdit, QHBoxLayout
from PySide2.QtGui import QIntValidator, QDoubleValidator, QValidator


class NQWidgetInput(NQWidget):
    MODE_TEXT = 0
    MODE_INT = 1
    MODE_DOUBLE = 2

    signal_done = Signal()

    def __init__(self, prompt="Question:", mode=MODE_TEXT, default_value="", min_value=None, max_value=None):

        # Variables
        self.mode = mode
        self.prompt = prompt
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value

        # GUI Components
        self.layout = QHBoxLayout()
        self.label = QLabel(self.prompt)
        self.line_edit = QLineEdit()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)

        # Default Value
        if not self.default_value:
            if self.mode == self.MODE_TEXT:
                self.default_value = ""
            elif self.mode == self.MODE_INT:
                self.default_value = "0"
            elif self.mode == self.MODE_DOUBLE:
                self.default_value = "0.0"
        self.line_edit.setText(str(self.default_value))

        super().__init__()

        self.setLayout(self.layout)
        self.normalize(no_signal=True)

    def connect_signals(self):
        super().connect_signals()
        self.line_edit.editingFinished.connect(self.normalize)

    def set_value(self, value):
        self.line_edit.setText(value)
        self.normalize(no_signal=True)

    def get_value(self):
        self.normalize(no_signal=True)
        return self.line_edit.text()

    def normalize(self, no_signal=False):
        text = self.line_edit.text()

        if self.mode == self.MODE_INT:
            # Remove all non-numeric characters
            text = re.sub(r'\D', '', text)
            if not text:  # If there is no number after normalization, use min_value
                if self.min_value is not None:
                    text = str(self.min_value)
                else:
                    text = str(0)
            else:
                num = int(text)
                if self.min_value is not None and num < self.min_value:
                    num = self.min_value
                if self.max_value is not None and num > self.max_value:
                    num = self.max_value
                text = str(num)
            self.line_edit.setText(text)

        elif self.mode == self.MODE_DOUBLE:
            # Remove all non-numeric characters except the first dot
            text = re.sub(r'[^0-9.]', '', text)
            parts = text.split('.')
            if len(parts) > 1:
                # Join the parts with only one dot
                text = parts[0] + '.' + ''.join(parts[1:]).replace('.', '')
            if not text:  # If there is no number after normalization, use min_value
                if self.min_value is not None:
                    text = str(self.min_value)
                else:
                    text = str(0.0)
            else:
                num = float(text)
                if self.min_value is not None and num < self.min_value:
                    num = float(self.min_value)
                if self.max_value is not None and num > self.max_value:
                    num = float(self.max_value)
                text = str(num)
            self.line_edit.setText(text)

        elif self.mode == self.MODE_TEXT:
            pass

        if not no_signal:
            self.signal_done.emit()
