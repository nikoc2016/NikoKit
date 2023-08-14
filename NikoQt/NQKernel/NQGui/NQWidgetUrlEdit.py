from PySide2.QtCore import Signal
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
import os.path as p

from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout_margin
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQDropMixin
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetConsoleTextEdit import NQWidgetConsoleTextEdit


class NQWidgetUrlEdit(NQWidget):
    MODE_ALL = "MODE_ALL"
    MODE_FILE_ONLY = "MODE_FILE_ONLY"
    MODE_DIR_ONLY = "MODE_DIR_ONLY"

    # Mode only affect drop behaviors and validate button
    def __init__(self, mode=MODE_ALL, auto_scroll=True, *args, **kwargs):
        self.mode = mode
        self.auto_scroll = auto_scroll
        self.main_lay: QHBoxLayout = None
        self.url_edit: UrlEdit = None
        self.btn_lay: QVBoxLayout = None
        self.btn_clear: QPushButton = None
        self.btn_remove_invalid_urls: QPushButton = None

        super().__init__(*args, **kwargs)

    def construct(self):
        super().construct()
        self.main_lay = QHBoxLayout()
        clear_layout_margin(self.main_lay)
        self.url_edit = UrlEdit(auto_scroll=self.auto_scroll)
        self.url_edit.setReadOnly(False)
        self.url_edit.setPlaceholderText(self.lang("drag_and_drop"))
        self.btn_lay = QVBoxLayout()
        self.btn_clear = QPushButton(self.lang("clear"))
        self.btn_remove_invalid_urls = QPushButton(self.lang("remove_invalid_urls"))
        if self.mode == self.MODE_ALL:
            self.url_edit.setPlaceholderText(self.lang("drag_and_drop_file_or_dir"))
        elif self.mode == self.MODE_FILE_ONLY:
            self.url_edit.setPlaceholderText(self.lang("drag_and_drop_file"))
        elif self.mode == self.MODE_DIR_ONLY:
            self.url_edit.setPlaceholderText(self.lang("drag_and_drop_dir"))

        self.setLayout(self.main_lay)
        self.main_lay.addWidget(self.url_edit)
        self.main_lay.addLayout(self.btn_lay)
        self.btn_lay.addWidget(self.btn_clear)
        self.btn_lay.addWidget(self.btn_remove_invalid_urls)
        self.btn_lay.addStretch()

    def connect_signals(self):
        super().connect_signals()
        self.btn_remove_invalid_urls.clicked.connect(self.slot_remove_invalid_urls)
        self.btn_clear.clicked.connect(self.slot_clear)
        self.url_edit.url_dropped.connect(self.slot_url_dropped)

    def slot_remove_invalid_urls(self):
        self.set_urls(self.validate_urls(self.get_urls()))

    def get_urls(self):
        return [url for url in self.url_edit.toPlainText().split("\n") if url.strip() != ""]

    def set_urls(self, urls):
        unique_urls = set()
        for url in urls:
            unique_urls.add(url)
        unique_urls = sorted(list(unique_urls))
        self.url_edit.setText("\n".join(unique_urls))

    def add_urls(self, urls):
        existing_urls = self.get_urls()
        self.set_urls(existing_urls + urls)

    def slot_url_dropped(self, urls):
        self.add_urls(self.validate_urls(urls))

    def slot_clear(self):
        self.url_edit.clear()

    def validate_urls(self, urls):
        valid_urls = []
        for url in urls:
            if self.mode == self.MODE_ALL:
                if p.exists(url):
                    valid_urls.append(url)
            elif self.mode == self.MODE_DIR_ONLY:
                if p.isdir(url):
                    valid_urls.append(url)
            elif self.mode == self.MODE_FILE_ONLY:
                if p.isfile(url):
                    valid_urls.append(url)
            else:
                raise Exception(f"NQWidgetUrlEdit.validate_urls Unknown mode {self.mode}")
        return valid_urls


class UrlEdit(NQDropMixin, NQWidgetConsoleTextEdit):
    url_dropped = Signal(object)

    def __init__(self, auto_scroll=True, *args, **kwargs):
        super().__init__(auto_scroll=auto_scroll, *args, **kwargs)

    def drop_urls(self, urls):
        self.url_dropped.emit(urls)
