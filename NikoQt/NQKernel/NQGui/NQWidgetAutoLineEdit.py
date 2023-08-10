from NikoKit.NikoQt.NQAdapter import QLineEdit, QFontMetrics, QSizePolicy


class NQWidgetAutoLineEdit(QLineEdit):
    def __init__(self, min_width=10, *args, **kwargs):
        super(NQWidgetAutoLineEdit, self).__init__(*args, **kwargs)
        self.min_width = min_width
        self.setMinimumWidth(min_width)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.textChanged.connect(self.adjust_width)
        self.adjust_width("")

    def adjust_width(self, text):
        # Get the current font metrics
        font_metrics = QFontMetrics(self.font())
        # Calculate the width of the text
        text_width = font_metrics.horizontalAdvance(text)
        # Add some padding to the width
        new_width = text_width + 10
        # Set the new width
        if new_width < self.min_width:
            new_width = self.min_width
        self.setFixedWidth(new_width)

    def keyPressEvent(self, event):
        super(NQWidgetAutoLineEdit, self).keyPressEvent(event)
        self.adjust_width(self.text())
