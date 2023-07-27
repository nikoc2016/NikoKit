from typing import List, Tuple, Union

import html as htool
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin
from NikoKit.NikoQt.NQKernel.NQFunctions import color_line


class NQWidgetConsoleTextEdit(QTextEdit, NQMixin):
    def __init__(self, auto_scroll=True, *args, **kwargs):
        self.scroll_bar_value = 0
        self.auto_scroll = auto_scroll
        self.ready_to_scroll = False
        self.html_cache = ""
        self.text_cache = ""

        super(NQWidgetConsoleTextEdit, self).__init__(*args, **kwargs)

        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(True)

    # [(str_line, str_color_hex), ...] Smart Rendering
    def render_lines(self, lines: List[Tuple[str, Union[str, None]]]):
        html = ""
        for line, color_hex in lines:
            line = htool.escape(line).replace("\r\n", "<br>").replace("\n", "<br>")
            html += color_line(line,
                               color_hex=color_hex,
                               change_line=True)
        self.setHtml(html)

    def setHtml(self, html_text):
        if self.html_cache != html_text:
            self.smart_scroll_prepare()
            self.html_cache = html_text
            super(NQWidgetConsoleTextEdit, self).setHtml(html_text)
            self.smart_scroll()

    def setText(self, text):
        if self.text_cache != text:
            self.smart_scroll_prepare()
            self.text_cache = text
            super(NQWidgetConsoleTextEdit, self).setText(text)
            self.smart_scroll()

    def smart_scroll_prepare(self):
        self.scroll_bar_value = self.verticalScrollBar().value()
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
        else:
            self.verticalScrollBar().setValue(self.scroll_bar_value)
