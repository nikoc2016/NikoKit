from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQAdapter import Signal, QEvent, Qt
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWindowManager:
    @classmethod
    def register(cls, window):
        NQApplication.Runtime.Gui.Wins[window.w_id] = window

    @classmethod
    def get(cls, w_id):
        return NQApplication.Runtime.Gui.Wins[w_id]

    @classmethod
    def remove_by_w_id(cls, w_id):
        try:
            NQApplication.Runtime.Gui.Wins[w_id].close()
        except:
            pass

        try:
            del NQApplication.Runtime.Gui.Wins[w_id]
        except:
            print(f"NQWindow(w_id:{w_id}) not in WINDOW-MANAGER. Release your own pointer.")

    @classmethod
    def remove(cls, window):
        cls.remove_by_w_id(window.w_id)

    @classmethod
    def show(cls, w_id):
        NQApplication.Runtime.Gui.Wins[w_id].slot_show()

    @classmethod
    def hide(cls, w_id):
        NQApplication.Runtime.Gui.Wins[w_id].slot_hide()


class NQWindow(NQWidget):
    signal_close = Signal(str)  # Window-UUID
    signal_minimize = Signal(str)  # Window-UUID
    signal_maximize = Signal(str)  # Window-UUID
    signal_hide = Signal(str)  # Window-UUID
    signal_done = Signal(str, object)  # Window-UUID, Window-Result

    def __init__(self,
                 w_width=1024,
                 w_height=768,
                 w_margin_x=None,
                 w_margin_y=None,
                 *args,
                 **kwargs):
        # Parent Construction
        super(NQWindow, self).__init__(*args, **kwargs)

        # Init
        self.init_geo(w_width, w_height, w_margin_x, w_margin_y)

        # Register
        NQApplication.Runtime.Gui.WinMgr.register(self)

    def init_geo(self,
                 w_width=1024,
                 w_height=768,
                 w_margin_x=None,
                 w_margin_y=None):
        if isinstance(w_margin_x, int) or isinstance(w_margin_y, int):
            self.setGeometry(w_margin_x, w_margin_y, w_width, w_height)
        else:
            self.resize(w_width, w_height)

    def construct(self):
        super(NQWindow, self).construct()
        if self.w_icon:
            self.setWindowIcon(self.w_icon)
        else:
            self.setWindowIcon(NQApplication.Runtime.Data.Res.QIcon(NQApplication.Runtime.App.icon_res_name))
        self.setWindowTitle(self.lang(self.w_title))

    def slot_show(self):
        self.show()

    def slot_hide(self):
        self.hide()

    def slot_close(self):
        self.close()

    def hideEvent(self, event):
        self.signal_hide.emit(self.w_id)

    def closeEvent(self, event):
        self.signal_close.emit(self.w_id)
        NQApplication.Runtime.Gui.WinMgr.remove(self)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if event.oldState() and Qt.WindowMinimized:
                self.signal_minimize.emit(self.w_id)
            elif event.oldState() == Qt.WindowNoState or self.windowState() == Qt.WindowMaximized:
                self.signal_maximize.emit(self.w_id)
