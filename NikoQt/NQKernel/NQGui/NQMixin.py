# Note: Remember to register your widget by modifying NQGui.register_all_widgets()
from uuid import uuid4

from NikoKit.NikoQt import NQApplication
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class NQMixin(NKPrintableMixin):
    def __init__(self, w_name="NQMixin", w_title="NQMixin", w_use_lang=True, w_icon=None, *args, **kwargs):
        super(NQMixin, self).__init__(*args, **kwargs)
        self.w_id = str(uuid4())
        self.w_name = w_name
        self.w_title = w_title
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
            result = ""
            for arg in args:
                result += NQApplication.Runtime.Service.NKLang.tran(arg)
            return result
        else:
            return ''.join(args)
