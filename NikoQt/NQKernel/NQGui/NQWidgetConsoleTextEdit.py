from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetConsoleTextEdit(QTextEdit, NQMixin):
    def __init__(self, auto_scroll=True, *args, **kwargs):
        self.auto_scroll = auto_scroll
        self.ready_to_scroll = False
        self.html_cache = ""
        self.text_cache = ""

        super(NQWidgetConsoleTextEdit, self).__init__(*args, **kwargs)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(True)

    def setHtml(self, html):
        if self.html_cache != html:
            self.smart_scroll_prepare()
            self.html_cache = html
            super(NQWidgetConsoleTextEdit, self).setHtml(html)
            self.smart_scroll()

    def setText(self, text):
        if self.text_cache != text:
            self.smart_scroll_prepare()
            self.text_cache = text
            super(NQWidgetConsoleTextEdit, self).setText(text)
            self.smart_scroll()

    def smart_scroll_prepare(self):
        if self.scroll_bar_at_bottom():
            self.ready_to_scroll = True
        else:
            self.ready_to_scroll = False

    def scroll_bar_at_bottom(self):
        scroll_bar = self.verticalScrollBar()
        is_at_bottom = scroll_bar.value() >= scroll_bar.maximum() - 4
        return is_at_bottom

    def smart_scroll(self):
        if self.auto_scroll and self.ready_to_scroll and not self.scroll_bar_at_bottom():
            self.moveCursor(QTextCursor.End)
            self.ensureCursorVisible()
