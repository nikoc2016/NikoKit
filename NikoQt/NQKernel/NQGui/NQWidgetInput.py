import re

from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoQt.NQAdapter import Signal, QLabel, QHBoxLayout, QSizePolicy, Qt
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetAutoLineEdit import NQWidgetAutoLineEdit


class NQWidgetInput(NQWidget):
    MODE_TEXT = 0
    MODE_INT = 1
    MODE_DOUBLE = 2

    signal_changed = Signal()

    def __init__(self,
                 prompt="Question:",
                 mode=MODE_TEXT,
                 default_value="",
                 min_value=None,
                 max_value=None,
                 min_width=10,
                 stretch_in_the_end=False):

        # Variables
        self.mode = mode
        self.prompt = prompt
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.last_valid_input = ""

        # GUI Components
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setAlignment(Qt.AlignCenter)
        self.line_edit = NQWidgetAutoLineEdit(min_width=min_width)
        if self.prompt:
            prompt = QLabel(self.prompt)
            prompt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
            self.layout.addWidget(prompt)
        self.layout.addWidget(self.line_edit)
        if stretch_in_the_end:
            self.layout.addStretch()

        # Default Value
        if not self.default_value:
            if self.mode == self.MODE_TEXT:
                self.default_value = ""
            elif self.mode == self.MODE_INT:
                self.default_value = "0"
            elif self.mode == self.MODE_DOUBLE:
                self.default_value = "0.0"
        self.set_value(str(self.default_value))

        super().__init__()

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.setLayout(self.layout)
        self.normalize(no_signal=True)

    def connect_signals(self):
        super().connect_signals()
        self.line_edit.editingFinished.connect(self.normalize)

    def drop_urls(self, urls):
        if len(urls) == 1:
            self.set_value(urls[0])
        else:
            self.set_value(",".join(['"' + url + '"' for url in urls]))

    def set_value(self, value):
        self.line_edit.setText(value)
        self.normalize(no_signal=True)

    def get_value(self):
        return self.last_valid_input

    def normalize(self, no_signal=False):
        text = self.line_edit.text()

        if self.mode == self.MODE_INT:
            # Replace all non-digit characters except a leading negative sign
            if "-" in text:
                text = "-" + re.sub(r'\D', '', text)
            else:
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

        if self.line_edit.text() != self.last_valid_input:
            self.last_valid_input = self.line_edit.text()
            if not no_signal:
                self.signal_changed.emit()
