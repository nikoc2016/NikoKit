import datetime
import random

from NikoKit.NikoQt.NQAdapter import *

from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChatInputPanel import NQWidgetChatInputPanel
from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindow
from NikoKit.NikoQt.NQLite import NQLite
from NikoKit.NikoStd.NKVersion import NKVersion


class DemoApp:
    @classmethod
    def launch_app(cls):
        app = NQLite(
            name="Demo",
            name_short="DM",
            version=NKVersion("1.0.0"),
            version_tag=NKVersion.ALPHA
        )

        # Main Window
        Runtime.Gui.WinMain = NQWindow(w_width=700,
                                       w_height=300)
        main_lay = QVBoxLayout(Runtime.Gui.WinMain)
        chat_widget = NQWidgetChatInputPanel()
        main_lay.addWidget(chat_widget)
        Runtime.Gui.WinMain.show()
        app.serve()


if __name__ == "__main__":
    DemoApp.launch_app()
