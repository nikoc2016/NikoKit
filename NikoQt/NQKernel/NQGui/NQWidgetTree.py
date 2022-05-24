from PySide2.QtWidgets import QTreeWidget

from NikoKit.NikoQt.NQKernel.NQGui.NQMixin import NQMixin


class NQWidgetTree(NQMixin, QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(NQWidgetTree, self).__init__(*args, **kwargs)
