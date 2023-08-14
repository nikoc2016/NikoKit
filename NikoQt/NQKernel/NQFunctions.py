import html

from PySide2.QtWidgets import QWidget

from NikoKit.NikoQt.NQAdapter import QHBoxLayout, QVBoxLayout


def clear_layout(layout):
    if not layout:
        return
    for i in reversed(range(layout.count())):
        widget_to_remove = layout.itemAt(i).widget()
        layout.removeWidget(widget_to_remove)
        widget_to_remove.setParent(None)


def lay(contents, vertical=True, lead_stretch=True, end_stretch=True):
    base_lay = QVBoxLayout() if vertical else QHBoxLayout()
    if lead_stretch:
        base_lay.addStretch()
    for content in contents:
        try:
            base_lay.addWidget(content)
        except:
            base_lay.addLayout(content)
    if end_stretch:
        base_lay.addStretch()
    return base_lay


def clear_layout_margin(layout, space=0):
    layout.setSpacing(space)
    layout.setContentsMargins(space, space, space, space)


def text_to_html(text):
    return html.escape(str(text)).replace("\n", "<br/>").replace(" ", "&nbsp;")


def color_line(line, color_hex=None, change_line=True):
    if color_hex:
        line = '<font color="%s">%s</font>' % (color_hex, line)
    if change_line:
        line += "<br/>"
    return line
