from NikoKit.NikoQt.NQAdapter import QWidget
from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin

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
class NQWidget(NQMixin, QWidget):
    def __init__(self, w_name="NQBasicWidget", w_title="NQBasicWidget", *args, **kwargs):
        super(NQWidget, self).__init__(w_name, w_title, *args, **kwargs)

    def to_ghost(self):
        my_ghost = NQGhost.new_ghost(self.__class__.__name__)
        my_ghost.update({
            "w_name": self.w_name,
            "w_title": self.w_title,
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
            w_title=ghost["w_title"],
            w_use_lang=ghost["w_use_lang"],
            # Call NQGhost.build(child_ghost) to append children
        )
