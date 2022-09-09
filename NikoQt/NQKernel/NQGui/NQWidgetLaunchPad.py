from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel import NQFunctions
from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetArea import NQWidgetArea
from NikoKit.NikoStd.NKDataStructure import NKDataStructure


class NQWidgetLaunchPad(NQWidget):
    signal_launch = Signal(str)

    class LaunchTarget(NKDataStructure):
        def __init__(self,
                     value="",
                     label="",
                     tooltip="",
                     group="",
                     group_display_name="",
                     size=150,
                     icon=None,
                     enabled=True):
            self.value = value
            self.label = label
            self.tooltip = tooltip
            self.group = group
            self.group_display_name = group_display_name
            self.size = size
            self.icon = icon
            self.enabled = enabled

            super(NQWidgetLaunchPad.LaunchTarget, self).__init__()

    class LaunchButton(QToolButton):
        def __init__(self,
                     launch_target):
            super(NQWidgetLaunchPad.LaunchButton, self).__init__()
            self.value = launch_target.value
            self.setEnabled(launch_target.enabled)
            self.setIcon(launch_target.icon)
            self.setToolTip(launch_target.tooltip)
            self.setIconSize(QSize(launch_target.size - 40, launch_target.size - 40))
            self.setFixedSize(QSize(launch_target.size, launch_target.size))
            self.setText(launch_target.label)
            self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def __init__(self,
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

        super(NQWidgetLaunchPad, self).__init__(*args, **kwargs)

    def construct(self):
        main_lay = QVBoxLayout()
        main_lay.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.main_lay = main_lay
        self.setLayout(main_lay)

    def slot_launch_button_clicked(self):
        self.signal_launch.emit(self.sender().value)

    def render_buttons(self):
        NQFunctions.clear_layout(self.main_lay)

        groups = {}
        for launch_value, launch_target in self.launch_targets.items():
            if launch_target.group not in groups:
                group_lay = QGridLayout()
                group_area = NQWidgetArea(title=launch_target.group_display_name,
                                          central_layout=group_lay)

                groups[launch_target.group] = {
                    "group": launch_target.group,
                    "group_display_name": launch_target.group_display_name,
                    "group_main_widget": group_area,
                    "group_layout": group_lay,
                    "group_row_idx": 0,
                    "group_col_idx": 0
                }

            new_launch_button = self.LaunchButton(launch_target)
            new_launch_button.clicked.connect(self.slot_launch_button_clicked)
            grid_lay = groups[launch_target.group]["group_layout"]
            grid_lay.addWidget(new_launch_button,
                               groups[launch_target.group]["group_row_idx"],
                               groups[launch_target.group]["group_col_idx"], 1, 1)
            groups[launch_target.group]["group_col_idx"] += 1
            if groups[launch_target.group]["group_col_idx"] >= self.launch_btn_col_count:
                groups[launch_target.group]["group_col_idx"] = 0
                groups[launch_target.group]["group_row_idx"] += 1

        for group_name, group_dict in groups.items():
            self.main_lay.addWidget(group_dict["group_main_widget"])

    def add_launch_target(self, launch_target, skip_render=False):
        self.launch_targets[launch_target.value] = launch_target
        if not skip_render:
            self.render_buttons()

    def add_launch_targets(self, launch_targets):
        for launch_target in launch_targets:
            self.add_launch_target(launch_target=launch_target, skip_render=True)
        self.render_buttons()

    def set_launch_target_enabled(self, value, enabled):
        try:
            self.launch_targets[value].enabled = enabled
            self.render_buttons()
            return True
        except:
            return False

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
