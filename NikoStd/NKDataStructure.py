from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class NKDataStructure(NKPrintableMixin):
    def __init__(self, *args, **kwargs):
        super(NKDataStructure, self).__init__(*args, **kwargs)

    def p_key(self):
        return None

    def update(self, data):
        if isinstance(data, self.__class__):
            for attr_name in vars(data):
                if data.__dict__[attr_name]:
                    self.__dict__[attr_name] = data.__dict__[attr_name]
        else:
            raise Exception(self.__class__, " can't update with ", data.__class__)

    @classmethod
    def get_dummy(cls, *args, **kwargs):
        return cls()

    @classmethod
    def corrupt(cls, data, possibility, *args, **kwargs):
        return cls()
