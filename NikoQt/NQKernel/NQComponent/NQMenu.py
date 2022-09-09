from NikoKit.NikoQt.NQAdapter.NQPySide2 import QAction

from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQAdapter import QMenu


class NQMenuOption:
    def __init__(self,
                 name,
                 display_name,
                 slot_callback,
                 icon=None,
                 hotkey=None):
        self.name = name,
        self.display_name = display_name
        self.slot_call_back = slot_callback
        self.icon = icon
        self.hotkey = hotkey

        super(NQMenuOption, self).__init__()

    def __repr__(self):
        return "<NQMenuOption %s %s>" % (self.name, self.display_name)


class NQMenuSubMenu:
    def __init__(self,
                 name,
                 display_name,
                 children_list):
        self.name = name,
        self.display_name = display_name
        self.children_list = children_list
        if not self.children_list:
            self.children_list = []

        super(NQMenuSubMenu, self).__init__()

    def __repr__(self):
        return "<NQMenuSubMenu %s %s> Children: %s" % (self.name, self.display_name, self.children_list)


class NQMenuLineSeparator:
    def __repr__(self):
        return "<NQMenuLineSeparator>"


def example_slot():
    print("Action Triggered.")


def example_content_list():
    return [
        NQMenuOption(name="option_1", display_name="Option1", slot_callback=example_slot),
        NQMenuOption(name="option_2", display_name="Option2", slot_callback=example_slot),
        NQMenuSubMenu(name="menu_1", display_name="Menu1", children_list=[
            NQMenuOption(name="option_3", display_name="Option3", slot_callback=example_slot),
            NQMenuOption(name="option_4", display_name="Option4", slot_callback=example_slot),
        ]),
        NQMenuLineSeparator(),
        NQMenuOption(name="exit", display_name="Exit", slot_callback=example_slot)
    ]


class NQMenuGenerator:
    def __init__(self, content_list=None):
        self.content_list = content_list
        if not self.content_list:
            self.content_list = example_content_list()

    def set_content_list(self, content_list):
        self.content_list = content_list

    def to_menu(self, title=""):
        return self._compile(self.content_list, menu_name=title)

    def _compile(self, content_list, menu_name=""):
        menu = QMenu(menu_name)
        menu.nq_cache_list = []
        for menu_item in content_list:
            if isinstance(menu_item, NQMenuLineSeparator):
                menu.addSeparator()
            elif isinstance(menu_item, NQMenuOption):
                if menu_item.icon:
                    new_action = QAction(icon=menu_item.icon, text=menu_item.display_name)
                else:
                    new_action = QAction(text=menu_item.display_name)
                if menu_item.hotkey:
                    new_action.setShortcut(menu_item.hotkey)
                new_action.triggered.connect(menu_item.slot_call_back)
                menu.nq_cache_list.append(new_action)
                menu.addAction(new_action)
            elif isinstance(menu_item, NQMenuSubMenu):
                sub_menu = self._compile(menu_item.children_list, menu_item.display_name)
                menu.addMenu(sub_menu)
            else:
                raise Exception("Unable to handle NQMenu Item with type " + type(menu_item))
        return menu
