from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetLabel(NQMixin, QLabel):
    clicked = Signal()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.clicked.emit()
        elif event.buttons() == Qt.RightButton:
            # self.pix_popup_menu()
            pass
