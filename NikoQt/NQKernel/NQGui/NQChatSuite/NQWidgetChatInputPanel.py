from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQChatSuite.NQWidgetChatEdit import NQWidgetChatEdit
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetChatInputPanel(NQWidget):
    signal_post_chat = Signal()

    class NQWidgetChatInputToolWidget(NQWidget):
        def __init__(self,
                     *args,
                     **kwargs):
            # Private Storage

            # GUI Component
            self.main_lay = None

            super(NQWidgetChatInputPanel.NQWidgetChatInputToolWidget, self).__init__(
                *args,
                **kwargs)

        def add_tool(self, text=None, icon=None, function=None, hotkey=None):
            tool_btn = QToolButton()
            if text is not None:
                tool_btn.setText(text)
            else:
                tool_btn.setIcon(icon)

            # if function is not None:
            #     tool_btn.clicked.connect(function)

            self.main_lay.addWidget(tool_btn)

        def construct(self):
            # Widgets
            main_lay = QVBoxLayout()

            # Relationships

            # Storage
            self.setLayout(main_lay)

            self.main_lay = main_lay

    def __init__(self,
                 *args,
                 **kwargs):
        # Private Storage

        # GUI Component
        self.input_text_edit = None

        super(NQWidgetChatInputPanel, self).__init__(
            *args,
            **kwargs)

    def construct(self):
        # Widgets
        main_lay = QVBoxLayout()

        tool_widget = self.NQWidgetChatInputToolWidget()

        tool_widget.add_tool(text=self.lang("selection") + self.lang("file"))

        input_text_edit = NQWidgetChatEdit()

        send_btn = QToolButton()
        send_btn.setText(self.lang("send"))

        # Relationships
        main_lay.addWidget(tool_widget)
        main_lay.addWidget(input_text_edit)
        main_lay.addWidget(send_btn, alignment=Qt.AlignRight)

        # Storage
        self.setLayout(main_lay)

        self.input_text_edit = input_text_edit
