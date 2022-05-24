import time

from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQComponent.NQResource import NQResource
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoStd import NKStyleSheet, NKConst


class NQWidgetChatFriendList(NQWidget):
    signal_tab_conv_clicked = Signal(str)  # Widget UUID
    signal_tab_friend_clicked = Signal(str)  # Widget UUID
    signal_tab_group_clicked = Signal(str)  # Widget UUID
    signal_tab_org_clicked = Signal(str)  # Widget UUID
    signal_user_clicked = Signal(object)

    class SearchBar(NQWidget):

        def __init__(self,
                     *args,
                     **kwargs):
            # Private Storage

            # GUI Component
            self.search_line_edit = None

            super(NQWidgetChatFriendList.SearchBar, self).__init__(
                *args,
                **kwargs)

        def construct(self):
            # Widgets
            main_lay = QHBoxLayout()

            search_line_edit = QLineEdit()

            # search_btn = QPushButton("搜索")
            search_btn = QPushButton(search_line_edit)
            search_btn.setCursor(Qt.PointingHandCursor)
            search_btn.setFixedSize(22, 22)
            search_btn.setToolTip("搜索")
            search_btn.setFlat(True)
            # search_btn.setIcon(QIcon(r"L:\work\chat_test\ico\4.ico"))
            search_btn.setText("🔎")

            # 防止文本框输入内容位于按钮之下
            margins = search_line_edit.textMargins()
            search_line_edit.setTextMargins(margins.left(), margins.top(), search_btn.width(), margins.bottom())
            search_line_edit.setPlaceholderText("请输入搜索内容")

            search_lay = QHBoxLayout(search_line_edit)
            search_lay.addStretch()
            search_lay.addWidget(search_btn)
            search_lay.setSpacing(0)
            search_lay.setContentsMargins(0, 0, 0, 0)

            # Relationships
            main_lay.addWidget(search_line_edit)

            # Storage
            self.setLayout(main_lay)

            self.search_line_edit = search_line_edit

        def search(self):
            pass

    class AvatarLabel(NQMixin, QLabel):
        def __init__(self,
                     avatar_pixmap=None,
                     unread_count=0,
                     show_unread=False,
                     show_unread_count=False,
                     *args,
                     **kwargs):

            # Private Storage
            self.avatar = avatar_pixmap
            self.unread_count = unread_count
            self.show_unread = show_unread
            self.show_unread_count = show_unread_count

            # GUI Component
            self.unread_label = None

            # Initialization
            super(NQWidgetChatFriendList.AvatarLabel, self).__init__(
                *args,
                **kwargs)

            self.setAttribute(Qt.WA_StyledBackground, True)

            self.setFixedSize(40, 40)

        def construct(self):
            # Widgets
            main_lay = QVBoxLayout()

            unread_label = QLabel()
            unread_label.setFixedSize(8, 8)
            # unread_label.setStyleSheet("QLabel{background-color:red;border-radius:25px;border:1px solid red;}")
            unread_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                          border_radius="4px",
                                                          border="1px solid red",
                                                          background_color="red"))

            # Relationships
            main_lay.addWidget(unread_label, alignment=Qt.AlignTop | Qt.AlignRight)
            main_lay.setMargin(0)

            # Storage
            self.setLayout(main_lay)

            self.unread_label = unread_label

            self.reset_unread_label()

        def connect_signals(self):
            pass

        def set_unread_count(self, count):
            self.unread_count = count
            self.reset_unread_label()

        def reset_unread_label(self):
            if self.show_unread:
                self.unread_label.show()
                if self.show_unread_count:
                    if self.unread_count > 99:
                        self.unread_label.setText("99+")
                    else:
                        self.unread_label.setText(str(self.unread_count))
                    self.unread_label.setFixedSize(16, 16)
                    self.unread_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                                       border_radius="8px",
                                                                       border="1px solid red",
                                                                       background_color="red"
                                                                       ))

                else:
                    self.unread_label.setText("")
                    self.unread_label.setFixedSize(8, 8)
                    self.unread_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                                       border_radius="4px",
                                                                       border="1px solid red",
                                                                       background_color="red"))
            else:
                self.unread_label.setText("")
                self.unread_label.hide()

        def get_grayscale_avatar(self):
            return NQResource.get_grayscale_pixmap(self.user.user_pic_pixmap)

        def set_grayscale_avatar(self, is_grayscale):
            if is_grayscale:
                self.setPixmap(self.get_grayscale_avatar().scaled(40, 40))
            else:
                self.setPixmap(self.avatar_pixmap.scaled(40, 40))

        # def unread_count_changed2(self):
        #
        #     # user_pic = self.user.user_pic_pixmap.scaled(256, 256)
        #     user_pic = NQResource.scale(self.message.user.user_pic_pixmap,
        #                                 256,
        #                                 stretch=True,
        #                                 compress=True)
        #     if self.unread_count == 0:
        #         pass
        #     else:
        #         if self.show_unread:
        #             ellipse_rx, ellipse_ry = 30, 30
        #             text_point = QPoint(170, 100)
        #             display_str = str(self.unread_count)
        #             if self.unread_count < 10:
        #                 ellipse_rx, ellipse_ry = 30, 30
        #                 text_point = QPoint(170, 100)
        #                 display_str = str(self.unread_count)
        #             elif 10 <= self.unread_count < 100:
        #                 ellipse_rx, ellipse_ry = 40, 30
        #                 text_point = QPoint(160, 100)
        #                 display_str = str(self.unread_count)
        #             elif 100 <= self.unread_count:
        #                 ellipse_rx, ellipse_ry = 50, 30
        #                 text_point = QPoint(150, 100)
        #                 display_str = "99+"
        #
        #             painter = QPainter()
        #             painter.begin(user_pic)
        #             painter.setBrush(QColor("#FA5151"))  # Set the circle color
        #
        #             center = QPoint(180, 90)  # 椭圆圆心位置
        #             painter.drawEllipse(center, ellipse_rx, ellipse_ry)  # 画椭圆（椭圆圆心，宽，高）
        #
        #             font = painter.font()
        #             font.setPointSize(30)  # 设置字体大小
        #
        #             pen = painter.pen()
        #             pen.setColor(Qt.white)  # Set the text color
        #
        #             painter.setPen(pen)
        #             painter.setFont(font)
        #             painter.drawText(text_point, display_str)  # 画文本（坐标点（80，100），内容）
        #             painter.end()
        #         else:
        #             ellipse_rx, ellipse_ry = 20, 20
        #
        #             painter = QPainter()
        #             painter.begin(user_pic)
        #             painter.setBrush(QColor("#FA5151"))  # Set the circle color
        #
        #             center = QPoint(190, 80)  # 椭圆圆心位置
        #             painter.drawEllipse(center, ellipse_rx, ellipse_ry)  # 画椭圆（椭圆圆心，宽，高）
        #
        #             painter.end()
        #
        #     icon = QIcon()
        #     icon.addPixmap(user_pic, QIcon.Normal, QIcon.Off)
        #     self.pixmapBtn.setIcon(icon)

    class ConversationWidget(NQWidget):
        class ConversationItemWidget(NQWidget):
            def __init__(self,
                         owner=None,
                         conversation=None,
                         offline=False,
                         avatar_pixmap=None,
                         unread_count=0,
                         show_unread=False,
                         *args,
                         **kwargs
                         ):

                # Private Storage
                self.owner = owner
                self.conversation = conversation
                self.offline = offline
                self.avatar_pixmap = avatar_pixmap
                self.unread_count = unread_count
                self.show_unread = show_unread
                self.conversation_name = None
                self.conversation_last_content = None

                # GUI Component
                self.avatar_label = None

                self.conversation_name_label = None

                self.conversation_content_label = None

                # Initialization
                super(NQWidgetChatFriendList.ConversationWidget.ConversationItemWidget, self).__init__(
                    *args,
                    **kwargs
                )
                # self.

            def construct(self):

                # Widgets
                main_lay = QHBoxLayout()

                avatar_label = NQWidgetChatFriendList.AvatarLabel(show_unread=True,
                                                                  unread_count=15,
                                                                  show_unread_count=True)
                # avatar_label = QLabel()
                # avatar_label.setPixmap(QPixmap(r"L:\work\chat_test\ico\7.ico"))

                v2_lay = QVBoxLayout()

                conversation_name_label = QLabel()
                conversation_name_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                                         font_size="20"))

                conversation_content_label = QLabel()
                conversation_name_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                                         font_size="10"))

                # Relationships
                main_lay.addWidget(avatar_label, alignment=Qt.AlignVCenter)
                main_lay.addLayout(v2_lay)

                v2_lay.addWidget(conversation_name_label, alignment=Qt.AlignLeft)
                v2_lay.addWidget(conversation_content_label, alignment=Qt.AlignLeft)

                # Storage
                self.setLayout(main_lay)

                self.avatar_label = avatar_label

                self.conversation_name_label = conversation_name_label

                self.conversation_content_label = conversation_content_label

            def set_offline(self, offline_status):
                self.offline = offline_status
                self.update_offline()

            def update_offline(self):
                if self.offline:
                    self.set_avatar(NQResource.get_grayscale_pixmap(self.conversation.conversation_pic_pixmap))
                else:
                    if self.show_unread and self.unread_count:
                        self.set_avatar(self.conversation.conversation_unread_pic_pixmap)
                    else:
                        self.set_avatar(self.conversation.conversation_pic_pixmap)

            def update_conversation(self, conversation):
                self.conversation = conversation
                self.update_avatar()
                if self.conversation.group_name:
                    self.update_group_name()
                else:
                    self.update_user_name()
                self.update_content()

            def set_avatar_pixmap(self, pixmap):
                self.avatar_pixmap = pixmap

            def update_avatar_pixmap(self):
                self.avatar_label.setPixmap(self.avatar_pixmap.scaled(40, 40))

            def update_content(self):
                self.conversation_content_label.setText(self.conversation_last_content)

            def update_conversation_name_label(self):
                self.conversation_name_label.setText(self.conversation_name)

            def set_conversation_name(self, new_conversation_name):
                self.conversation_name = new_conversation_name

            def update_data(self):
                if len(self.conversation.users) == 2:
                    for user_id in self.conversation.users.keys():
                        if user_id != self.owner.user_id:
                            self.conversation_name = self.conversation.users[user_id].user_print_name
                            self.set_avatar_pixmap(self.conversation.users[user_id].user_pic_pixmap)
                            self.conversation_last_content = self.conversation.get_last_content()
                else:
                    self.conversation_name = self.conversation.group_name
                    self.set_avatar_pixmap(self.conversation.conversation_group_pic_pixmap)

            def refresh(self):
                self.update_data()
                self.update_avatar_pixmap()
                self.update_conversation_name_label()
                self.update_content()

        class ConversationItem(QListWidgetItem):

            def __init__(self,
                         parent=None,
                         item_widget=None,
                         *args,
                         **kwargs
                         ):

                self.parent = parent
                self.item_widget = item_widget

                # Initialization
                super(NQWidgetChatFriendList.ConversationWidget.ConversationItem, self).__init__(
                    *args,
                    **kwargs
                )
                # self.setForeground(QBrush(NKConst.COLOR_GREEN))

            def get_last_time(self):
                return self.item_widget.conversation.last_conversation_time
                # return self.parent.itemWidget(self).conversation.last_conversation_time

            def __lt__(self, other):
                try:
                    return self.get_last_time() < other.get_last_time()
                except Exception:
                    return QListWidgetItem.__lt__(self, other)

        def __init__(self,
                     owner=None,
                     conversations=None,
                     *args,
                     **kwargs):

            # Private Storage
            if conversations is None:
                conversations = {}
            self.owner = owner
            self.conversations = conversations

            # GUI Component
            self.conversation_list_widget = None

            # Initialization
            super(NQWidgetChatFriendList.ConversationWidget, self).__init__(
                *args,
                **kwargs)

        def construct(self):
            # Widgets
            main_lay = QVBoxLayout()

            conversation_list_widget = QListWidget()
            conversation_list_widget.setStyleSheet(NKStyleSheet.build(selector="QListWidget::item:selected",
                                                                      background_color=NKConst.COLOR_GREY))

            # Relationships
            main_lay.addWidget(conversation_list_widget)

            # Storage
            self.setLayout(main_lay)

            self.conversation_list_widget = conversation_list_widget

        def set_owner(self, user):
            self.owner = user

        def add_conversation(self, conversation):
            self.conversations[conversation.conversation_id] = conversation
            new_conversation_item_widget = self.ConversationItemWidget(owner=self.owner,
                                                                       conversation=conversation)
            new_conversation_item_widget.refresh()
            self.add_item(new_conversation_item_widget)
            self.sort_conversations()

        def add_conversations(self, conversations):
            for conversation_id in conversations.keys():
                self.conversations[conversation_id] = conversations[conversation_id]
                new_conversation_item_widget = self.ConversationItemWidget(owner=self.owner,
                                                                           conversation=conversations[conversation_id])
                new_conversation_item_widget.refresh()
                self.add_item(new_conversation_item_widget)
            self.sort_conversations()

        def add_item(self, item_widget):
            new_conversation_item = self.ConversationItem(parent=self, item_widget=item_widget)
            new_conversation_item.setSizeHint(QSize(200, 50))
            self.conversation_list_widget.addItem(new_conversation_item)
            self.conversation_list_widget.setItemWidget(new_conversation_item, item_widget)

        def update_conversation(self, conversation):
            self.conversations[conversation.conversation_id] = conversation
            self.get_conversation_item(conversation.conversation_id).update_item()
            self.sort_conversations()

        def del_conversation(self, conversation_id):
            for row in range(self.conversation_list_widget.count()):
                row_item = self.conversation_list_widget.item(row)
                if row_item.conversation.conversation_id == conversation_id:
                    self.conversation_list_widget.takeItem(row)
                    break

        def get_conversation_item(self, conversation_id):
            conversation_item = None
            for row in range(self.conversation_list_widget.count()):
                row_item = self.conversation_list_widget.item(row)
                if row_item.conversation.conversation_id == conversation_id:
                    conversation_item = row_item
                    break
            return conversation_item

        def sort_conversations(self):
            self.conversation_list_widget.sortItems(Qt.DescendingOrder)

    def __init__(self,
                 *args,
                 **kwargs):

        # Private Storage

        # GUI Component
        self.tab_conv_widget = None

        super(NQWidgetChatFriendList, self).__init__(
            *args,
            **kwargs)

    def construct(self):
        # Widgets
        main_lay = QVBoxLayout()

        search_bar = self.SearchBar()

        chat_tab = QTabWidget()

        tab_conv_widget = self.ConversationWidget()
        tab_friend_widget = QWidget()
        tab_group_widget = QWidget()
        tab_org_widget = QWidget()

        chat_tab.addTab(tab_conv_widget, "聊天")
        chat_tab.addTab(tab_friend_widget, "好友")
        chat_tab.addTab(tab_group_widget, "群组")
        chat_tab.addTab(tab_org_widget, "组织")

        # Relationships
        main_lay.addWidget(search_bar)
        main_lay.addWidget(chat_tab, 1)

        # Storage
        self.setLayout(main_lay)

        self.tab_conv_widget = tab_conv_widget

    def set_users(self, user_dict):
        pass

    def add_user(self, user):
        pass

    def clear_users(self):
        pass

    def slot_user_clicked(self):
        pass
