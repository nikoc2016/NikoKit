from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from NikoKit.NikoWidgets.Kernel import NWidgetInterface


class NWLineInput(NWidgetInterface, QWidget):
    def __init__(self,
                 w_id="",
                 w_class="",
                 w_label="",
                 w_value=None,
                 w_children=None
                 ):
        super(NWLineInput, self).__init__(
            w_type="NWLineInput",
            w_id=w_id,
            w_class=w_class,
            w_label=w_label,
            w_value=w_value,
            w_children=w_children
        )

        # GUI Component
        self.main_lay = None
        self.label = None
        self.line_edit = None

        # Construct
        self.construct()

        # Connect Signals
        self.connect_signals()

    def construct(self):
        main_lay = QVBoxLayout()
        label = QLabel(self.w_label)
        line_edit = QLineEdit()

        main_lay.addWidget(label)
        main_lay.addWidget(line_edit)

        self.main_lay = main_lay
        self.label = label
        self.line_edit = line_edit

        self.setLayout(main_lay)

    def connect_signals(self):
        pass

