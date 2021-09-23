class Type2Widget:
    pass


class Ghost:
    @staticmethod
    def build(ghost):
        return ghost

    @staticmethod
    def extract(nk_widget):
        return nk_widget.to_ghost()


class NWidgetInterface:
    @classmethod
    def new_ghost(cls):
        return {
            "w_type": "NWidgetInterface",
            "w_id": "",
            "w_class": "",
            "w_label": "",
            "w_value": None,
            "ghost_children": []
        }

    @classmethod
    def from_ghost(cls, ghost):
        base_ghost = cls.new_ghost()
        if ghost["w_type"] != base_ghost["w_type"]:
            raise Exception("from_ghost::Error w_type not match.")
        base_ghost.update(ghost)
        return cls(**ghost)

    def __init__(self,
                 w_type="NWidgetInterface",
                 w_id="",
                 w_class="",
                 w_label="",
                 w_value=None,
                 ghost_children=None
                 ):
        self.w_type = w_type
        self.w_id = w_id
        self.w_class = w_class
        self.w_label = w_label
        self.w_value = w_value
        self.w_children = []

        if ghost_children:
            for ghost_child in ghost_children:
                w_child = Ghost.build(ghost_child)
                self.add_child(w_child)

    def add_child(self, child_widget):
        self.w_children.append(child_widget)

    def remove_child(self, child_widget):
        self.w_children.remove(child_widget)

    def to_ghost(self):
        ghost = self.new_ghost()
        for attr_name in ghost.keys():
            try:
                ghost[attr_name] = self.__dict__[attr_name]
            except:
                pass

        for child in self.w_children:
            ghost["ghost_children"].append(child.to_ghost())


class NWidgetManager:
    def __init__(self):
        pass
