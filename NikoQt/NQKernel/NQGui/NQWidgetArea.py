from NikoKit.NikoQt.NQAdapter import QGroupBox, QVBoxLayout
from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout_margin
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetArea(NQMixin, QGroupBox):
    def __init__(self, title, central_widget=None, central_layout=None, *args, **kwargs):
        # GUI Component
        self.central_layout = central_layout
        self.central_widget = central_widget

        super(NQWidgetArea, self).__init__(title=title, *args, **kwargs)

    def construct(self):
        self.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def setLayout(self, layout):
        if layout:
            self.central_layout = layout
        else:
            self.central_layout = QVBoxLayout()
        clear_layout_margin(self.central_layout, 5)
        super(NQWidgetArea, self).setLayout(self.central_layout)

    def setCentralWidget(self, widget):
        self.setLayout(self.central_layout)
        if widget:
            self.central_layout.addWidget(widget)
