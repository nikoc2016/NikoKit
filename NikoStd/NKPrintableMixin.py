class NKPrintableMixin:
    def __init__(self, *args, **kwargs):
        super(NKPrintableMixin, self).__init__(*args, **kwargs)

    def __repr__(self):
        base_str = "<%s %s>"
        detail_str = ""
        for my_property in self.__dict__.keys():
            detail_str += my_property + ":" + str(self.__dict__[my_property]) + "; "
        return base_str % (self.__class__, detail_str)
