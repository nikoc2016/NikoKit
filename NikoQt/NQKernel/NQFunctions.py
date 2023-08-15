import html

from PySide2.QtWidgets import QWidget, QLayout

from NikoKit.NikoQt.NQAdapter import QHBoxLayout, QVBoxLayout
from NikoKit.NikoStd.NKPrint import eprint


def clear_layout(layout):
    if not layout:
        return
    for i in reversed(range(layout.count())):
        widget_to_remove = layout.itemAt(i).widget()
        layout.removeWidget(widget_to_remove)
        widget_to_remove.setParent(None)


def lay_adaptor(custom_layout):
    adapter = QWidget()
    adapter.setLayout(custom_layout)
    return adapter


def lay(contents, major_item=None, vertical=True, lead_stretch=True, end_stretch=True, margin=-1):
    base_lay = QVBoxLayout() if vertical else QHBoxLayout()
    if margin > -1:
        clear_layout_margin(base_lay, margin)
    if lead_stretch:
        base_lay.addStretch()
    for content in contents:
        if isinstance(content, QWidget):
            base_lay.addWidget(content)
        elif isinstance(content, QLayout):
            base_lay.addLayout(content)
        else:
            eprint(f"lay(Invalid Type:{type(content)}). Detail: {repr(content)}")
    if end_stretch:
        base_lay.addStretch()
    if major_item is not None:
        base_lay.setStretchFactor(major_item, 1)
    return base_lay


def clear_layout_margin(layout, space=0):
    layout.setSpacing(space)
    layout.setContentsMargins(space, space, space, space)


def text_to_html(text):
    return html.escape(str(text)).replace("\n", "<br/>").replace(" ", "&nbsp;")


def color_line(line: str, color_hex: str = None, change_line: bool = True):
    if color_hex:
        line = '<font color="%s">%s</font>' % (color_hex, line)
    if change_line:
        line += "<br/>"
    return line
