from NikoKit.NikoQt.NQAdapter import QGroupBox, QVBoxLayout, QWidget, Qt, QHBoxLayout, QToolButton, QLabel
from NikoKit.NikoQt.NQKernel.NQFunctions import clear_layout_margin
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetArea(NQMixin, QGroupBox):
    def __init__(self, title, central_widget=None, central_layout=None, collapsable=True, *args, **kwargs):
        # Data
        self._collapsed = False
        self.title = title
        self.collapsable = collapsable

        # GUI Component
        self._main_lay = QVBoxLayout()
        self._title_lay = QHBoxLayout()  # Hide\Show Arrow, Bold Title, Additional ToolButtons
        self._title_label = QLabel()  # Post-change of title
        self.collapse_btn = QToolButton()  # Toggle to hide\show body_adaptor
        self.collapse_btn.setArrowType(Qt.DownArrow)
        self.collapse_btn.setStyleSheet("QToolButton { background-color: transparent; border: none; }")
        self._body_adaptor = QWidget()  # Adaptor for central_layout
        self.central_layout = central_layout  # User Custom Layout
        self.central_widget = central_widget  # User Custom Central Widget

        self.set_title(title)
        super(NQWidgetArea, self).__init__(*args, **kwargs)  # Will call construct and connect_signals from parent.

    def construct(self):
        super().construct()

        self._main_lay.addLayout(self._title_lay)
        self._main_lay.addWidget(self._body_adaptor)

        clear_layout_margin(self._title_lay, 3)
        self._title_lay.setSpacing(5)
        if self.collapsable:
            self._title_lay.addWidget(self.collapse_btn)
        self._title_lay.addWidget(self._title_label)

        clear_layout_margin(self._main_lay)
        super(NQWidgetArea, self).setLayout(self._main_lay)

        self.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

    def connect_signals(self):
        self.collapse_btn.clicked.connect(self.toggle_collapsed)

    def setLayout(self, layout):
        if layout:
            self.central_layout = layout
        else:
            self.central_layout = QVBoxLayout()
        clear_layout_margin(self.central_layout, 5)
        self._body_adaptor.setLayout(self.central_layout)

    def setCentralWidget(self, widget):
        self.setLayout(self.central_layout)
        if widget:
            self.central_layout.addWidget(widget)

    def set_collapsed(self, collapsed):
        self._collapsed = collapsed
        self._body_adaptor.setVisible(not self._collapsed)
        self.collapse_btn.setArrowType(Qt.DownArrow if not self._collapsed else Qt.RightArrow)

    def get_collapsed(self):
        return self._collapsed

    def toggle_collapsed(self):
        self.set_collapsed(not self._collapsed)

    def set_title(self, title_str):
        self.title = title_str
        self._title_label.setText("<b>{}</b>".format(self.title))