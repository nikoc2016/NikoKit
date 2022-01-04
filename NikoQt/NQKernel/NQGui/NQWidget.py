from uuid import uuid4

from NikoKit.NikoQt.NQAdapter import QWidget
from NikoKit.NikoQt.NQApplication import Runtime
from NikoKit.NikoStd.NKPrintableClass import NKPrintableClass

NQWidgetRegistry = set()


class NQGhost:
    @classmethod
    def new_ghost(cls, w_type_str):
        return {
            "w_type_str": w_type_str
        }

    @classmethod
    def build(cls, ghost):
        for NQWidgetClass in NQWidgetRegistry:
            if NQWidgetClass.__name__ == ghost["w_type_str"]:
                return NQWidgetClass.from_ghost(ghost)


# Note: Remember to register your widget by modifying NQGui.register_all_widgets()
class NQBasicWidget(NKPrintableClass, QWidget):
    def __init__(self, w_name="NQBasicWidget", w_use_lang=True):
        super(NQBasicWidget, self).__init__()
        self.w_id = str(uuid4())
        self.w_name = w_name
        self.w_use_lang = w_use_lang

        # Initialization Procedure
        self.construct()
        self.connect_signals()

    def construct(self):
        pass

    def connect_signals(self):
        pass

    def lang(self, raw_str):
        if self.w_use_lang:
            return Runtime.Service.NKLang.tran(raw_str)
        else:
            return raw_str

    def to_ghost(self):
        my_ghost = NQGhost.new_ghost(self.__class__.__name__)
        my_ghost.update({
            "w_name": self.w_name,
            "w_use_lang": self.w_use_lang
        })
        return my_ghost

    def to_ghost_recursive(self):
        my_ghost = self.to_ghost()
        # Implement Child Elements
        return my_ghost

    @classmethod
    def from_ghost(cls, ghost):
        return cls(
            w_name=ghost["w_name"],
            w_use_lang=ghost["w_use_lang"]
            # Call NQGhost.build(child_ghost) to append children
        )
