def clear_layout(layout):
    if not layout:
        return
    for i in reversed(range(layout.count())):
        widget_to_remove = layout.itemAt(i).widget()
        layout.removeWidget(widget_to_remove)
        widget_to_remove.setParent(None)


def clear_layout_margin(layout, space=0):
    layout.setSpacing(space)
    layout.setContentsMargins(space, space, space, space)


def color_line(line, color_hex=None, change_line=True):
    if color_hex:
        line = '<font color="%s">%s</font>' % (color_hex, line)
    if change_line:
        line += "<br/>"
    return line
