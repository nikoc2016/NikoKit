"""
check_list = NQWidgetCheckList(exclusive=[True/False], read_only=[True/False])

Signals
changed = Signal(str)  # passing selected option name

Add/Remove
check_list.add_option(option_name, display_name, checked, at_index)
check_list.remove_option(option_name)
check_list.remove_all_options()

Save/Load
check_list.to_list()
check_list.from_list(data_list)

Query
check_list.is_checked(option_name)
check_list.set_read_only([True/False])
check_list.get_options_status() -> dict
check_list.set_options_status(dict options_status)
check_list.get_checked() -> str OR list
check_list.set_checked([str/list] option_names, uncheck_others=[True/False])

Protected
check_list.slot_click()
check_list.render_options()
check_list.set_focus(option_name, set_check=True)
check_list.toggle_focus(option_name)
"""
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class NQWidgetCheckList(NQMixin, QListWidget):
    changed = Signal(str)

    char_checked = "☑"
    char_unchecked = "☐"

    class Option(NKPrintableMixin):
        def __init__(self,
                     option_name="",
                     display_text="",
                     checked=False,
                     *args,
                     **kwargs):
            self.option_name = option_name
            self.display_text = display_text
            self.checked = checked

            super(NQWidgetCheckList.Option, self).__init__(*args, **kwargs)

        def to_list(self):
            return [self.option_name, self.display_text, self.checked][:]

        def from_list(self, data_list):
            self.option_name = data_list[0]
            self.display_text = data_list[1]
            self.checked = data_list[2]

    def __init__(self, exclusive=False, read_only=False, *args, **kwargs):
        # Mode
        self.exclusive = exclusive
        self.read_only = read_only

        # Color
        self.checked_color = "#FFFFFF"
        self.unchecked_color = "#AAAAAA"
        self.disabled_color = "#555555"

        # Variable
        self.name_to_option = {}
        self.order_of_option = []
        self.list_widget_items = []

        super(NQWidgetCheckList, self).__init__(*args, **kwargs)

    def connect_signals(self):
        # Signals
        self.clicked.connect(self.slot_click)

    def add_option(self,
                   option_name,
                   display_text="",
                   checked=True,
                   at_index=None):

        if option_name in self.name_to_option.keys():
            return False

        option = self.Option(
            option_name=option_name,
            display_text=display_text,
            checked=False
        )

        if at_index is not None:
            self.order_of_option.insert(at_index, option)
        else:
            self.order_of_option.append(option)

        self.name_to_option[option_name] = option

        self.set_focus(option_name=option_name, set_check=checked)

        self.render_options()

        return True

    def remove_option(self, option_name, bypass_render=False):
        try:
            option = self.name_to_option[option_name]
            del self.name_to_option[option_name]
            self.order_of_option.remove(option)
            if not bypass_render:
                self.render_options()
            return True
        except:
            return False

    def remove_all_options(self):
        option_name_to_remove = list(self.name_to_option.keys())
        for option_name in option_name_to_remove:
            self.remove_option(option_name, bypass_render=True)
        self.render_options()

    def is_checked(self, option_name):
        return self.name_to_option[option_name].checked

    def set_read_only(self, bool_read_only):
        self.read_only = bool_read_only
        self.render_options()

    def get_options_status(self):
        result_dict = {}
        for option in self.order_of_option:
            result_dict[option.option_name] = option.checked
        return result_dict

    def set_options_status(self, options_status):
        for option_name, checked in options_status.items():
            self.name_to_option[option_name] = checked

    def get_checked(self):
        checked = []
        for option in self.order_of_option:
            if option.checked:
                checked.append(option.option_name)
        if self.exclusive:
            return checked[0]
        else:
            return checked

    def set_checked(self, option_names, uncheck_others=True):
        if type(option_names) is str:
            option_names = [option_names]

        if uncheck_others:
            for option in self.order_of_option:
                option.checked = False

        for option_name in option_names:
            self.name_to_option[option_name].checked = True

        self.render_options()

    def slot_click(self, index):
        if not self.read_only:
            row_num = index.row()
            option_name = self.order_of_option[row_num].option_name
            self.toggle_focus(option_name)
            self.render_options()
            self.changed.emit(self.order_of_option[row_num].option_name)

    def render_options(self):
        # Synchronize Recycling ListWidget
        widget_count_diff = len(self.order_of_option) - len(self.list_widget_items)

        if widget_count_diff < 0:
            self.clear()
            self.list_widget_items = []
            widget_count_diff = len(self.order_of_option) - len(self.list_widget_items)

        if widget_count_diff > 0:
            for i in range(widget_count_diff):
                new_list_widget_item = QListWidgetItem()
                self.list_widget_items.append(new_list_widget_item)
                self.addItem(new_list_widget_item)

        # Update Values to ListWidgetItems
        for idx, option in enumerate(self.order_of_option):
            check_status_char = self.char_checked
            color_str = self.checked_color
            if not option.checked:
                check_status_char = self.char_unchecked
                color_str = self.unchecked_color

            if self.read_only:
                color_str = self.disabled_color

            self.list_widget_items[idx].setText("%s %s" % (check_status_char, option.display_text))
            self.list_widget_items[idx].setTextColor(QColor(color_str))

    def set_focus(self, option_name, set_check=True):
        # Exclusive
        if self.exclusive:
            for option in self.order_of_option:
                if option.option_name == option_name:
                    option.checked = True
                else:
                    option.checked = False

        # Normal
        else:
            self.name_to_option[option_name].checked = set_check

        # Render
        self.render_options()

    def toggle_focus(self, option_name):
        # Exclusive
        if self.exclusive:
            for option in self.order_of_option:
                if option.option_name == option_name:
                    option.checked = True
                else:
                    option.checked = False

        # Normal
        else:
            self.name_to_option[option_name].checked = not self.name_to_option[option_name].checked

        # Render
        self.render_options()

    def to_list(self):
        result_list = []
        for option in self.order_of_option:
            result_list.append(option.to_list())
        return result_list

    def from_list(self, data_list):
        self.remove_all_options()
        for option_data_list in data_list:
            new_option = self.Option()
            new_option.from_list(option_data_list)
            self.order_of_option.append(new_option)
            self.name_to_option[new_option.option_name] = new_option
        self.render_options()
