from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQBasicWidget
from NikoKit.NikoStd.NKLanguage import tran


class NQWindow(NQBasicWidget):
    def __init__(self,
                 w_title="NQWindow",
                 w_icon=None,
                 w_width=1024,
                 w_height=768,
                 w_margin_x=0,
                 w_margin_y=0,
                 **kwargs):
        super(NQWindow, self).__init__(**kwargs)
        # Storage
        self.w_title = w_title
        self.w_icon = w_icon

        # Init
        self.init_geo(w_width, w_height, w_margin_x, w_margin_y)
        self.construct()

        # Register
        Runtime.Gui.win_mgr.register(self)

    def init_geo(self,
                 w_width=1024,
                 w_height=768,
                 w_margin_x=0,
                 w_margin_y=0):
        if w_margin_x or w_margin_y:
            self.setGeometry(w_margin_x, w_margin_y, w_width, w_height)
        else:
            self.resize(w_width, w_height)

    def construct(self):
        if self.w_icon:
            self.setWindowIcon(self.w_icon)
        if self.w_use_lang:
            self.setWindowTitle(tran(self.w_title))
        else:
            self.setWindowTitle(self.w_title)

    def slot_show(self):
        self.show()

    def closeEvent(self, event):
        Runtime.Gui.win_mgr.remove(self)


class NQWindowManager:
    @classmethod
    def register(cls, window):
        Runtime.Gui.wins[window.w_id] = window

    @classmethod
    def get(cls, w_id):
        return Runtime.Gui.wins[w_id]

    @classmethod
    def remove_by_w_id(cls, w_id):
        try:
            Runtime.Gui.wins[w_id].close()
        except:
            pass

        del Runtime.Gui.wins[w_id]

    @classmethod
    def remove(cls, window):
        cls.remove_by_w_id(window.w_id)

    @classmethod
    def show(cls, w_id):
        Runtime.Gui.wins[w_id].slot_show()

    @classmethod
    def hide(cls, w_id):
        Runtime.Gui.wins[w_id].slot_hide()
