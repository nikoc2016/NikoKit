from NikoKit.NikoQt.NQAdapter import Signal, Qt, QLineEdit


class NQWidgetConsoleLineEdit(QLineEdit):
    upPressed = Signal()
    downPressed = Signal()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Up:
            self.upPressed.emit()
        if event.key() == Qt.Key_Down:
            self.downPressed.emit()
