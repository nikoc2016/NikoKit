from NikoKit.NikoQt.NQAdapter import QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, Signal
from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout_margin
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQDropMixin
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
import os


class NQWidgetUrlSelector(NQWidget):
    MODE_PATH = 1
    MODE_DIR = 2
    # MODE_ALL = 3 Deprecated because of Qt unsupported

    signal_changed = Signal(str)

    def __init__(self, title="URL:", url="", mode=MODE_PATH):
        super().__init__()

        self.mode = mode

        self.main_lay = QHBoxLayout()
        clear_layout_margin(self.main_lay, 2)
        self.setLayout(self.main_lay)

        self.label = QLabel(title)
        self.main_lay.addWidget(self.label)

        self.url_lineedit = DroppableLineEdit(url)
        self.main_lay.addWidget(self.url_lineedit)

        self.slot_browse_button = QPushButton(self.lang("browse"))
        self.main_lay.addWidget(self.slot_browse_button)

        self.url_lineedit.url_dropped.connect(self.set_url)
        self.slot_browse_button.clicked.connect(self.slot_browse)
        self.url_lineedit.textChanged.connect(self.signal_changed.emit)
        self.main_lay.setStretchFactor(self.url_lineedit, 1)

    def drop_urls(self, urls):
        self.set_url(urls[-1])

    def norm_url(self):
        if self.url_lineedit.text().strip() != "":
            self.url_lineedit.setText(os.path.normpath(self.url_lineedit.text()))

    def get_url(self):
        self.norm_url()
        return self.url_lineedit.text()

    def set_url(self, url):
        self.url_lineedit.setText(url)
        self.norm_url()

    def slot_browse(self):
        if self.mode == self.MODE_PATH:
            file_dialog = QFileDialog.getOpenFileName(self, "Select File", self.get_url())
            if file_dialog[0]:
                self.set_url(file_dialog[0])
        elif self.mode == self.MODE_DIR:
            file_dialog = QFileDialog.getExistingDirectory(self, "Select Directory", self.get_url())
            if file_dialog:
                self.set_url(file_dialog)
        self.norm_url()


class DroppableLineEdit(NQDropMixin, QLineEdit):
    url_dropped = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drop_urls(self, urls):
        if urls:
            self.url_dropped.emit(urls[-1])
