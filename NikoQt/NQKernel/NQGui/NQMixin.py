# Note: Remember to register your widget by modifying NQGui.register_all_widgets()
from uuid import uuid4
import os.path as p
from NikoKit.NikoQt import NQApplication
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class NQMixin(NKPrintableMixin):
    def __init__(self, w_name=None, w_title=None, w_use_lang=True, w_icon=None, *args, **kwargs):
        super(NQMixin, self).__init__(*args, **kwargs)
        self.w_id = str(uuid4())
        self.w_name = w_name
        if not self.w_name:
            self.w_name = self.__class__.__name__
        self.w_title = w_title
        if not self.w_title:
            self.w_title = self.__class__.__name__
        self.w_use_lang = w_use_lang
        self.w_icon = w_icon

        # Initialization Procedure
        self.construct()
        self.connect_signals()

    def construct(self):
        pass

    def connect_signals(self):
        pass

    def lang(self, *args):
        if self.w_use_lang:
            return NQApplication.Runtime.Service.NKLang.tran(*args)
        else:
            return ' '.join(args)


class NQDropMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.drop_urls([p.normpath(url.toLocalFile()) for url in event.mimeData().urls()])

    def drop_urls(self, urls):
        print(self.__class__, urls)
