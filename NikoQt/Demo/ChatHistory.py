import datetime
import random

from NikoKit.NikoQt.NQAdapter import *

from NikoKit.NikoLib.NKChat import NKChatUser, NKChatMessage
from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoQt.NQKernel.NQGui.NQChat.NQWidgetChatHistory import NQWidgetChatHistory
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

        users = [NKChatUser(user_id="111",
                            user_account="user111",
                            user_print_name="壹号",
                            user_permission=0,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"D:\Users\picture\avatar.png")),

                 NKChatUser(user_id="222",
                            user_account="user222",
                            user_print_name="贰号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"D:\Users\picture\luck.png"))
                 ]
        pixmap_list = [(QPixmap(r"L:\work\chat_test\pixmap\1.jpg"), r"L:\work\chat_test\pixmap\1.jpg"),
                       (QPixmap(r"L:\work\chat_test\pixmap\2.jpg"), r"L:\work\chat_test\pixmap\2.jpg"),
                       (QPixmap(r"L:\work\chat_test\pixmap\3.jpg"), r"L:\work\chat_test\pixmap\3.jpg")]

        movie_list = [(QMovie(r"L:\work\chat_test\movie\1.gif"), r"L:\work\chat_test\movie\1.gif"),
                      (QMovie(r"L:\work\chat_test\movie\2.gif"), r"L:\work\chat_test\movie\2.gif"),
                      (QMovie(r"L:\work\chat_test\movie\3.gif"), r"L:\work\chat_test\movie\3.gif")]

        file_list = [(r"L:\work\chat_test\ico\1.ico", r"L:\work\chat_test\file\1.csv"),
                     (r"L:\work\chat_test\ico\2.ico", r"L:\work\chat_test\file\2.docx"),
                     (r"L:\work\chat_test\ico\3.ico", r"L:\work\chat_test\file\3.txt")]

        chats = {}
        for i in range(9):
            message_id = ("%s" % i) * 5
            user_index = random.randint(0, len(users) - 1)
            message_type = random.randint(1, 4)
            if message_type == 1:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=users[user_index],
                                           message_datetime=datetime.datetime(2022, 2, 24, 14, i, 0),
                                           message_text="chat_test_text%s" % i)
            else:
                file_type = random.randint(0, 2)
                if message_type == 2:
                    nk_message = NKChatMessage(message_id=message_id,
                                               user=users[user_index],
                                               message_datetime=datetime.datetime(2022, 2, 24, 14, i, 0),
                                               message_file_path=pixmap_list[file_type][1],
                                               message_pixmap=pixmap_list[file_type][0]
                                               )
                elif message_type == 3:
                    nk_message = NKChatMessage(message_id=message_id,
                                               user=users[user_index],
                                               message_datetime=datetime.datetime(2022, 2, 24, 14, i, 0),
                                               message_file_path=movie_list[file_type][1],
                                               message_movie=movie_list[file_type][0]
                                               )
                else:
                    nk_message = NKChatMessage(message_id=message_id,
                                               user=users[user_index],
                                               message_datetime=datetime.datetime(2022, 2, 24, 14, i, 0),
                                               message_file_path=file_list[file_type][1],
                                               message_file_icon_pixmap=file_list[file_type][0]
                                               )
            chats[message_id] = nk_message

        # Main Window
        Runtime.Gui.WinMain = NQWindow()
        main_lay = QVBoxLayout(Runtime.Gui.WinMain)
        chat_widget = NQWidgetChatHistory()
        chat_widget.render_chats(chats)
        main_lay.addWidget(chat_widget)
        Runtime.Gui.WinMain.show()
        app.serve()


if __name__ == "__main__":
    DemoApp.launch_app()
