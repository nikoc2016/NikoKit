from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoQt.NQAdapter import Signal, QEvent, Qt
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQBasicWidget


class NQWindowManager:
    @classmethod
    def register(cls, window):
        Runtime.Gui.Wins[window.w_id] = window

    @classmethod
    def get(cls, w_id):
        return Runtime.Gui.Wins[w_id]

    @classmethod
    def remove_by_w_id(cls, w_id):
        try:
            Runtime.Gui.Wins[w_id].close()
        except:
            pass

        del Runtime.Gui.Wins[w_id]

    @classmethod
    def remove(cls, window):
        cls.remove_by_w_id(window.w_id)

    @classmethod
    def show(cls, w_id):
        Runtime.Gui.Wins[w_id].slot_show()

    @classmethod
    def hide(cls, w_id):
        Runtime.Gui.Wins[w_id].slot_hide()


class NQWindow(NQBasicWidget):
    signal_close = Signal(str)  # Window-UUID
    signal_minimize = Signal(str)  # Window-UUID
    signal_maximize = Signal(str)  # Window-UUID
    signal_done = Signal(str, object)  # Window-UUID, Window-Result

    def __init__(self,
                 w_title="NQWindow",
                 w_icon=None,
                 w_width=1024,
                 w_height=768,
                 w_margin_x=0,
                 w_margin_y=0,
                 **kwargs):
        # Storage
        self.w_title = w_title
        self.w_icon = w_icon

        # Parent Construction
        super(NQWindow, self).__init__(**kwargs)

        # Init
        self.init_geo(w_width, w_height, w_margin_x, w_margin_y)

        # Register
        Runtime.Gui.WinMgr.register(self)

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
        super(NQWindow, self).construct()
        if self.w_icon:
            self.setWindowIcon(self.w_icon)
        self.setWindowTitle(self.lang(self.w_title))

    def slot_show(self):
        self.show()

    def slot_hide(self):
        self.hide()

    def slot_close(self):
        self.close()

    def closeEvent(self, event):
        self.signal_close.emit(self.w_id)
        Runtime.Gui.WinMgr.remove(self)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if event.oldState() and Qt.WindowMinimized:
                self.signal_minimize.emit(self.w_id)
            elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
                self.signal_maximize.emit(self.w_id)
