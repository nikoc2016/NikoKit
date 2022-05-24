from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetLabel(QLabel, NQWidget):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.clicked.emit()
        elif event.buttons() == Qt.RightButton:
            # self.pix_popup_menu()
            pass
