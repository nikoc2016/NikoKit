import os

from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQComponent.NQResource import NQResource
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetLabel import NQWidgetLabel
from NikoKit.NikoStd.NKTime import NKDatetime
from NikoKit.NikoStd import NKConst, NKStyleSheet


class NQWidgetChatHistory(NQWidget):
    signal_file_clicked = Signal(str)  # FilePath
    signal_fetch_more = Signal()  # Requests More Content

    class ChatMessageWidget(NQWidget):
        def __init__(self,
                     message=None,
                     mode_selection=False,
                     media_width=250,
                     *args,
                     **kwargs):

            # Private Storage
            self.message = message
            self.mode_selection = mode_selection
            self.media_width = media_width

            # GUI Component
            self.main_lay = None
            self.selection_check_box = None

            super(NQWidgetChatHistory.ChatMessageWidget, self).__init__(*args, **kwargs)

        def construct(self):
            # Widgets
            main_lay = QHBoxLayout()

            pixmap_label = QLabel()
            pixmap_label.setPixmap(NQResource.scale(self.message.user.user_pic_pixmap,
                                                    20,
                                                    compress=True))

            message_lay = QVBoxLayout()
            message_lay.setMargin(0)

            time_label = QLabel("%s  %s" % (self.message.user.user_print_name,
                                            NKDatetime.datetime_to_str(self.message.message_datetime)))

            time_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                        color=NKConst.COLOR_GREY,
                                                        font_size="10px"))

            message_widget = self.create_message_content()

            selection_check_box = QCheckBox()

            # Relationships
            main_lay.addWidget(pixmap_label, alignment=Qt.AlignTop)
            main_lay.addLayout(message_lay, 1)
            main_lay.addWidget(selection_check_box, alignment=Qt.AlignRight)

            message_lay.addWidget(time_label, alignment=Qt.AlignLeft)
            message_lay.addWidget(message_widget, 1, alignment=Qt.AlignLeft)

            # Storage
            self.setLayout(main_lay)

            self.main_lay = main_lay

            self.selection_check_box = selection_check_box
            if self.mode_selection:
                pass
            else:
                self.selection_check_box.hide()

        def connect_signals(self):
            pass

        def create_message_content(self):
            content_label = None
            if self.message.message_text:
                content_label = QLabel(self.message.message_text)
                content_label.setStyleSheet(NKStyleSheet.build(selector="QLabel",
                                                               font_size="13px"))
                content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            elif self.message.message_file_path:
                if self.message.message_pixmap:
                    content_label = NQWidgetLabel()
                    content_label.setPixmap(NQResource.scale_by_width(self.message.message_pixmap,
                                                                      self.media_width,
                                                                      compress=True))
                    content_label.clicked.connect(self.clicked_message_widget)
                elif self.message.message_movie:
                    content_label = NQWidgetLabel()
                    movie = self.message.message_movie
                    # movie = NQResource.scale_by_width(movie,
                    #                                   self.media_width,
                    #                                   stretch=True)
                    movie.setCacheMode(QMovie.CacheAll)
                    movie.setSpeed(100)
                    content_label.setMovie(movie)
                    movie.start()
                    content_label.clicked.connect(self.clicked_message_widget)
                elif self.message.message_file_path:
                    content_label = NQWidgetLabel()
                    html = '''
                        <html>
                            <head/>
                            <body>
                                <p>
                                    <img src="%s" width="50" height="50" style="vertical-align:middle;"/>
                                    <span style="font-size:14px;vertical-align:middle;">%s</span>
                                </p>
                            </body>
                        </html>
                    ''' % (self.message.message_file_icon_pixmap, os.path.split(self.message.message_file_path)[1])
                    content_label.setText(html)
                    content_label.clicked.connect(self.clicked_message_widget)
            return content_label

        def clicked_message_widget(self):
            os.startfile(self.message.message_file_path)

    def __init__(self,
                 chats_dict=None,
                 auto_scroll=True,
                 *args,
                 **kwargs):

        # Private Storage

        # GUI Component
        self.main_lay = None

        self.auto_scroll = auto_scroll

        # Initialization
        super(NQWidgetChatHistory, self).__init__(*args, **kwargs)

    def construct(self):
        # Widgets
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_lay = QVBoxLayout()

        main_widget = QWidget()

        main_lay = QVBoxLayout(main_widget)
        main_lay.setSizeConstraint(QLayout.SetFixedSize)

        more_label = QLabel("more_message")

        # Relationships

        scroll_lay.addWidget(more_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        scroll_area.setWidget(main_widget)

        scroll_lay.addWidget(scroll_area)

        # Storage
        self.setLayout(scroll_lay)
        self.setMinimumHeight(300)
        self.setMinimumWidth(300)

        self.main_lay = main_lay

    def connect_signals(self):
        pass

    def render_chats(self, chats_dict):
        self.clear_chats()
        for chat_id in chats_dict:
            new_chat_item = self.ChatMessageWidget(message=chats_dict[chat_id])
            self.main_lay.addWidget(new_chat_item, 1)

    def clear_chats(self):
        NQFunctions.clear_layout(self.main_lay)
