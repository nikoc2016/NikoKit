from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget


class NQWidgetLaunchPad(NQWidget):
    signal_launch = Signal(str)

    class LaunchTarget:
        def __init__(self,
                     value="",
                     label="",
                     size=150,
                     icon=None,
                     enabled=True):
            self.value = value
            self.label = label
            self.size = size
            self.icon = icon
            self.enabled = enabled

    class LaunchButton(QToolButton):
        def __init__(self,
                     launch_target):
            super(NQWidgetLaunchPad.LaunchButton, self).__init__()
            self.value = launch_target.value
            self.setEnabled(launch_target.enabled)
            self.setIcon(launch_target.icon)
            self.setIconSize(QSize(launch_target.size - 40, launch_target.size - 40))
            self.setFixedSize(QSize(launch_target.size, launch_target.size))
            self.setText(launch_target.label)
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def __init__(self,
                 w_name="NQWidgetLaunchPad",
                 w_title="NQWidgetLaunchPad",
                 launch_btn_size=150,
                 launch_btn_col_count=3,
                 *args,
                 **kwargs):
        # Private Storage
        self.launch_btn_size = launch_btn_size
        self.launch_btn_col_count = launch_btn_col_count

        # GUI Component
        self.main_lay = None
        self.launch_targets = {}

        super(NQWidgetLaunchPad, self).__init__(w_name, w_title, *args, **kwargs)

    def construct(self):
        main_lay = QGridLayout()
        main_lay.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.main_lay = main_lay
        self.setLayout(main_lay)

    def slot_launch_button_clicked(self):
        self.signal_launch.emit(self.sender().value)

    def render_buttons(self):
        NQFunctions.clear_layout(self.main_lay)
        row_idx = 0
        col_idx = 0
        for launch_value, launch_target in self.launch_targets.items():
            new_launch_button = self.LaunchButton(launch_target)
            new_launch_button.clicked.connect(self.slot_launch_button_clicked)
            self.main_lay.addWidget(new_launch_button, row_idx, col_idx, 1, 1)
            col_idx += 1
            if col_idx >= self.launch_btn_col_count:
                col_idx = 0
                row_idx += 1

    def add_launch_target(self, launch_target, skip_render=False):
        self.launch_targets[launch_target.value] = launch_target
        if not skip_render:
            self.render_buttons()

    def add_launch_targets(self, launch_targets):
        for launch_target in launch_targets:
            self.add_launch_target(launch_target=launch_target, skip_render=True)
        self.render_buttons()

    def set_launch_target_enabled(self, value, enabled):
        self.launch_targets[value].enabled = enabled
        self.render_buttons()

    def remove_launch_target(self, value, skip_render=False):
        del self.launch_targets[value]
        if not skip_render:
            self.render_buttons()

    def remove_launch_targets(self, values):
        for value in values:
            self.remove_launch_target(value=value, skip_render=True)
        self.render_buttons()

    def clear_launch_targets(self):
        self.launch_targets = {}
        self.render_buttons()
