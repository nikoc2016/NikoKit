from NikoKit.NikoLib.NKChat import NKChatUser, NKChatConversation, NKChatMessage
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChatFriendList import NQWidgetChatFriendList
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChatHistory import NQWidgetChatHistory
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChatInputPanel import NQWidgetChatInputPanel
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetChat(NQWidget):
    def __init__(self, *args, **kwargs):

        self.friend_list = None

        self.history_text_edit = None
        self.input_panel = None

        super(NQWidgetChat, self).__init__(*args, **kwargs)

    def construct(self):
        main_lay = QHBoxLayout()

        friend_list = NQWidgetChatFriendList()

        v2 = QVBoxLayout()

        history_text_edit = NQWidgetChatHistory()
        input_panel = NQWidgetChatInputPanel()
        input_panel.setMaximumHeight(200)

        main_lay.addWidget(friend_list)
        main_lay.addLayout(v2, 1)

        v2.addWidget(history_text_edit)
        v2.addWidget(input_panel, 1)

        self.setLayout(main_lay)

        self.friend_list = friend_list

        self.history_text_edit = history_text_edit
        self.input_panel = input_panel

        self.update_data()

    def update_data(self):
        user0 = NKChatUser(user_id="000",
                           user_account="user000",
                           user_print_name="零号",
                           user_permission=0,
                           user_account_link_dict=None,
                           user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\0.ico"))
        self.friend_list.tab_conv_widget.set_owner(user0)
        for i in range(10):
            self.friend_list.tab_conv_widget.add_conversation(conversation=NKChatConversation.get_dummy())

        chats = {}
        for i in range(9):
            new_message = NKChatMessage.get_dummy()
            chats[new_message.message_id] = new_message
        self.history_text_edit.render_chats(chats)
