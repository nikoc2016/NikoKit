import random
import datetime
import string

from NikoKit.NikoQt.NQAdapter import QPixmap, QMovie
from NikoKit.NikoStd import NKTime
from NikoKit.NikoStd.NKDataStructure import NKDataStructure
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin
from NikoKit.NikoStd.NKUser import NKUser


class NKChatUser(NKUser):
    def __init__(self,
                 user_pic_pixmap=None,
                 *args,
                 **kwargs):
        self.user_pic_pixmap = user_pic_pixmap
        super(NKChatUser, self).__init__(*args, **kwargs)

    @classmethod
    def get_dummy(cls, *args, **kwargs):
        user = NKChatUser()
        return user


class NKChatMessage(NKDataStructure):
    def __init__(self,
                 message_id=None,
                 user=None,
                 message_datetime=None,
                 message_file_path="",
                 message_text=None,
                 message_pixmap=None,
                 message_movie=None,
                 message_file_icon_pixmap=None,
                 *args,
                 **kwargs
                 ):
        self.message_id = message_id
        self.user = user
        self.message_datetime = message_datetime
        self.message_file_path = message_file_path
        self.message_text = message_text
        self.message_pixmap = message_pixmap
        self.message_movie = message_movie
        self.message_file_icon_pixmap = message_file_icon_pixmap
        super(NKChatMessage, self).__init__(*args, **kwargs)

    def p_key(self):
        return self.message_id

    @classmethod
    def get_dummy(cls,
                  message_type=None,
                  message_user=None,
                  message_datetime=None,
                  message_text=None,
                  message_file_path=None,
                  message_pixmap=None,
                  message_movie=None,
                  message_file_icon_pixmap=None,
                  *args,
                  **kwargs):

        if not message_type:
            message_type = random.randint(1, 4)  # 1为文本类型，其他为文件

        if not message_user:
            message_user = NKChatUser.get_dummy()

        message_id = "".join([random.choice(string.digits) for i in range(16)])

        if not message_datetime:
            year = random.randint(2020, 2022)
            month = random.randint(1, 12)
            day = random.randint(1, NKTime.NKDate.month_days_count(year, month))
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            message_datetime = datetime.datetime(year=year,
                                                 month=month,
                                                 day=day,
                                                 hour=hour,
                                                 minute=minute,
                                                 second=second)
        if message_type == 1:
            if message_text is not None:
                pass
            else:
                choices = []
                for j in range(random.randint(50, 100)):
                    choices.append(random.choice(string.ascii_letters + string.digits))
                message_text = "".join(choices)
            nk_message = NKChatMessage(message_id=message_id,
                                       user=message_user,
                                       message_datetime=message_datetime,
                                       message_text=message_text)

        elif message_type == 2:
            if message_file_path is not None:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_user,
                                           message_datetime=message_datetime,
                                           message_file_path=message_file_path,
                                           message_pixmap=QPixmap(message_pixmap)
                                           )
            else:
                paths = [r"L:\work\chat_test\pixmap\0.jpg",
                         r"L:\work\chat_test\pixmap\1.jpg",
                         r"L:\work\chat_test\pixmap\2.jpg",
                         r"L:\work\chat_test\pixmap\3.jpg",
                         r"L:\work\chat_test\pixmap\4.jpg",
                         r"L:\work\chat_test\pixmap\5.jpg",
                         r"L:\work\chat_test\pixmap\6.jpg",
                         r"L:\work\chat_test\pixmap\7.jpg",
                         r"L:\work\chat_test\pixmap\8.jpg",
                         r"L:\work\chat_test\pixmap\9.jpg"]

                random_path = paths[random.randint(0, len(paths) - 1)]
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_user,
                                           message_datetime=message_datetime,
                                           message_file_path=random_path,
                                           message_pixmap=QPixmap(random_path)
                                           )
        elif message_type == 3:
            if message_file_path is not None:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_user,
                                           message_datetime=message_datetime,
                                           message_file_path=message_file_path,
                                           message_movie=QMovie(message_pixmap)
                                           )
            else:
                paths = [r"L:\work\chat_test\movie\0.jpg",
                         r"L:\work\chat_test\movie\1.jpg",
                         r"L:\work\chat_test\movie\2.jpg",
                         r"L:\work\chat_test\movie\3.jpg",
                         r"L:\work\chat_test\movie\4.jpg",
                         r"L:\work\chat_test\movie\5.jpg",
                         r"L:\work\chat_test\movie\6.jpg",
                         r"L:\work\chat_test\movie\7.jpg",
                         r"L:\work\chat_test\movie\8.jpg",
                         r"L:\work\chat_test\movie\9.jpg"]

                random_path = paths[random.randint(0, len(paths) - 1)]
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_user,
                                           message_datetime=message_datetime,
                                           message_file_path=random_path,
                                           message_movie=QMovie(random_path)
                                           )
        else:
            if message_file_path is not None:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_user,
                                           message_datetime=message_datetime,
                                           message_file_path=message_file_path,
                                           message_movie=QMovie(message_pixmap)
                                           )
            else:
                file_paths = [r"L:\work\chat_test\file\0.json",
                              r"L:\work\chat_test\file\1.csv",
                              r"L:\work\chat_test\file\2.docx",
                              r"L:\work\chat_test\file\3.txt",
                              r"L:\work\chat_test\file\4.pptx",
                              r"L:\work\chat_test\file\5.html",
                              r"L:\work\chat_test\file\6.pdf",
                              r"L:\work\chat_test\file\7.mp4",
                              r"L:\work\chat_test\file\8.zip",
                              r"L:\work\chat_test\file\9.wav"]
                pixmap_paths = [r"L:\work\chat_test\icon\0.ico",
                                r"L:\work\chat_test\icon\1.ico",
                                r"L:\work\chat_test\icon\2.ico",
                                r"L:\work\chat_test\icon\3.ico",
                                r"L:\work\chat_test\icon\4.ico",
                                r"L:\work\chat_test\icon\5.ico",
                                r"L:\work\chat_test\icon\6.ico",
                                r"L:\work\chat_test\icon\7.ico",
                                r"L:\work\chat_test\icon\8.ico",
                                r"L:\work\chat_test\icon\9.ico"]
                random_file_path = file_paths[random.randint(0, len(file_paths) - 1)]
                random_pixmap_path = pixmap_paths[random.randint(0, len(pixmap_paths) - 1)]
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_user,
                                           message_datetime=message_datetime,
                                           message_file_path=random_file_path,
                                           message_file_icon_pixmap=QPixmap(random_pixmap_path))

        return nk_message


class NKChatConversation(NKDataStructure):
    def __init__(self,
                 conversation_id=None,
                 group_name=None,
                 users=None,
                 messages=None,
                 last_conversation_time=None,
                 conversation_group_pic_pixmap=None,
                 *args,
                 **kwargs
                 ):
        super(NKChatConversation, self).__init__(
            *args,
            **kwargs
        )

        self.conversation_id = conversation_id
        self.group_name = group_name
        self.users = users
        self.messages = messages
        self.last_conversation_time = last_conversation_time
        self.conversation_group_pic_pixmap = conversation_group_pic_pixmap

    def get_sorted_messages(self):
        messages_list = sorted(self.messages, key=lambda x: self.messages[x].message_datetime, reverse=False)
        return messages_list

    def set_last_conversation_time(self, conversation_time):
        self.last_conversation_time = conversation_time

    def get_last_content(self):
        last_message = self.messages[self.get_sorted_messages()[-1]]
        if last_message.message_text:
            if self.group_name:
                return "%s: %s" % (last_message.user.user_print_name, last_message.message_text)
            else:
                return last_message.message_text
        elif last_message.message_file_path:
            if last_message.message_pixmap:
                return "[图片]"
            elif last_message.message_movie:
                return "[动图]"
            elif last_message.message_file_path:
                return "[文件]"

    @classmethod
    def get_dummy(cls, *args, **kwargs):
        user0 = NKChatUser(user_id="000",
                           user_account="user000",
                           user_print_name="零号",
                           user_permission=0,
                           user_account_link_dict=None,
                           user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\0.ico"))
        users = [NKChatUser(user_id="111",
                            user_account="user111",
                            user_print_name="壹号",
                            user_permission=0,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\1.ico")),

                 NKChatUser(user_id="222",
                            user_account="user222",
                            user_print_name="贰号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\2.ico")),

                 NKChatUser(user_id="333",
                            user_account="user333",
                            user_print_name="叁号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\3.ico")),

                 NKChatUser(user_id="444",
                            user_account="user444",
                            user_print_name="肆号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\4.ico")),

                 NKChatUser(user_id="555",
                            user_account="user555",
                            user_print_name="伍号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\5.ico")),

                 NKChatUser(user_id="666",
                            user_account="user666",
                            user_print_name="陆号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\6.ico")),

                 NKChatUser(user_id="777",
                            user_account="user777",
                            user_print_name="柒号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\7.ico")),

                 NKChatUser(user_id="888",
                            user_account="user888",
                            user_print_name="捌号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\8.ico")),

                 NKChatUser(user_id="999",
                            user_account="user777",
                            user_print_name="玖号",
                            user_permission=1,
                            user_account_link_dict=None,
                            user_pic_pixmap=QPixmap(r"L:\work\chat_test\ico\9.ico"))
                 ]

        groups = ["广式烧味", "上海外滩", "广西靓仔", "韩式烤肉", "重庆辣妹", "东北大哥", "深圳华强北", "广州小蛮腰", "黄金右脚",
                  "南拳北腿"]
        pixmaps = [QPixmap(r"L:\work\chat_test\ico\1.ico"),
                   QPixmap(r"L:\work\chat_test\ico\2.ico"),
                   QPixmap(r"L:\work\chat_test\ico\3.ico"),
                   QPixmap(r"L:\work\chat_test\ico\4.ico"),
                   QPixmap(r"L:\work\chat_test\ico\5.ico"),
                   QPixmap(r"L:\work\chat_test\ico\6.ico"),
                   QPixmap(r"L:\work\chat_test\ico\7.ico"),
                   QPixmap(r"L:\work\chat_test\ico\8.ico"),
                   QPixmap(r"L:\work\chat_test\ico\9.ico")
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
        id_num = 0
        for i in range(16):
            id_num = 10 * id_num + random.randint(0, 9)
        conversation_id = str(id_num)
        is_group = random.randint(0, 1)
        if is_group:
            group_num = random.randint(0, len(groups) - 1)
            group_name = groups[group_num]
            groups.pop(group_num)
            conversation_users = [user for user in users if random.randint(1, 3) == 1]
            conversation_users.append(user0)
            conversation_group_pic_pixmap = pixmaps[random.randint(0, len(pixmaps) - 1)]
        else:
            conversation_users = [user0, users[random.randint(0, len(users) - 1)]]

        last_time = datetime.datetime(2022, 3, 9, 14, random.randint(0, 59), 0)

        message_id = conversation_id
        message_use = conversation_users[random.randint(0, len(conversation_users) - 1)]
        message_type = random.randint(1, 4)
        if message_type == 1:
            nk_message = NKChatMessage(message_id=message_id,
                                       user=message_use,
                                       message_datetime=last_time,
                                       message_text="chat_test_text%s" % message_use.user_print_name)
        else:
            file_type = random.randint(0, 2)
            if message_type == 2:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_use,
                                           message_datetime=last_time,
                                           message_file_path=pixmap_list[file_type][1],
                                           message_pixmap=pixmap_list[file_type][0]
                                           )
            elif message_type == 3:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_use,
                                           message_datetime=last_time,
                                           message_file_path=movie_list[file_type][1],
                                           message_movie=movie_list[file_type][0]
                                           )
            else:
                nk_message = NKChatMessage(message_id=message_id,
                                           user=message_use,
                                           message_datetime=last_time,
                                           message_file_path=file_list[file_type][1],
                                           message_file_icon_pixmap=file_list[file_type][0]
                                           )
        conversation_user_dict = {
            conversation_user.user_id: conversation_user for conversation_user in conversation_users
        }
        conversation_messages = {nk_message.message_id: nk_message}
        if is_group:
            return NKChatConversation(conversation_id=conversation_id,
                                      group_name=group_name,
                                      users=conversation_user_dict,
                                      messages=conversation_messages,
                                      last_conversation_time=last_time,
                                      conversation_group_pic_pixmap=conversation_group_pic_pixmap)
        else:
            return NKChatConversation(conversation_id=conversation_id,
                                      users=conversation_user_dict,
                                      messages=conversation_messages,
                                      last_conversation_time=last_time,
                                      )


class NKChatEngine(NKPrintableMixin):

    @staticmethod
    def example_config():
        """This function returns an example/template CONFIG

        Returns:
            A template config dictionary

        """
        return {
            'mongo-ip': None,
            'mongo-port': None,
            'mongo_collection': None,
            'mongo-username': None,
            'mongo-password': None,
            'redis-ip': None,
            'redis-port': None,
            'redis-id': None,
            'redis-username': None,
            'redis-password': None,
        }

    def __init__(self, *args, **kwargs):
        super(NKChatEngine, self).__init__(*args, **kwargs)

    def beta_get_all_friends(self):
        pass
