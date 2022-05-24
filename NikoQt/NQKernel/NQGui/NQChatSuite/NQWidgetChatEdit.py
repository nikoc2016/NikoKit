from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetChatEdit(QTextEdit, NQWidget):
    signal_message_send = Signal(str)
    signal_file_send = Signal(str)

    def __init__(self,
                 enable_file_browser=True,
                 *args,
                 **kwargs):
        self.enable_file_browser = enable_file_browser
        super(NQWidgetChatEdit, self).__init__(*args, **kwargs)

    def setText(self, text):
        pass

    def text(self):
        pass

    def slot_send(self):
        pass

    def slot_file_browse(self):
        pass

    def keyPressEvent(self, event):
        QTextEdit.keyPressEvent(self, event)
        print('press')
        if event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            cursor.clearSelection()
            cursor.deletePreviousChar()
            if self.toPlainText() != '':
                print('success')



