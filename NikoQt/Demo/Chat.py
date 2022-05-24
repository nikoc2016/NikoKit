from NikoKit.NikoLib.NKChat import NKChatConversation, NKChatUser
from NikoKit.NikoQt.NQAdapter import *

from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChat import NQWidgetChat
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChatFriendList import NQWidgetChatFriendList
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
        Runtime.Gui.WinMain = NQWindow(w_width=1024, w_height=720, w_title="NKChat")
        main_lay = QVBoxLayout(Runtime.Gui.WinMain)
        chat_widget = NQWidgetChat()
        main_lay.addWidget(chat_widget)
        Runtime.Gui.WinMain.show()
        app.serve()


if __name__ == "__main__":
    DemoApp.launch_app()
