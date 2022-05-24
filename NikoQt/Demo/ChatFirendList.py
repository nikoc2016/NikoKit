from NikoKit.NikoLib.NKChat import NKChatConversation, NKChatUser
from NikoKit.NikoQt.NQAdapter import *

from NikoKit.NikoQt.NQApplication import Runtime
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
        Runtime.Gui.WinMain = NQWindow(w_width=370)
        main_lay = QVBoxLayout(Runtime.Gui.WinMain)
        chat_widget = NQWidgetChatFriendList()
        user0 = NKChatUser(user_id="000",
                           user_account="user000",
                           user_print_name="零号",
                           user_permission=0,
                           user_account_link_dict=None,
                           user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\0.ico"))
        chat_widget.tab_conv_widget.set_owner(user0)
        for i in range(10):
            chat_widget.tab_conv_widget.add_conversation(conversation=NKChatConversation.get_dummy())
        main_lay.addWidget(chat_widget)
        Runtime.Gui.WinMain.show()
        app.serve()


if __name__ == "__main__":
    DemoApp.launch_app()
