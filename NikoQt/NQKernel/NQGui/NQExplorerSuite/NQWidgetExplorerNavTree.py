from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetTree import NQWidgetTree
from NikoKit.NikoStd.NKDataStructure import NKDataStructure


class NQWidgetExplorerNavTree(NQWidgetTree):
    signal_folder_clicked = Signal()

    class TreeNode(NKDataStructure):
        def __init__(self, nkfs_item=None, qtree_item=None, *args, **kwargs):
            super(NQWidgetExplorerNavTree.TreeNode, self).__init__(*args, **kwargs)
            self.nkfs_item = nkfs_item
            self.qtree_item = qtree_item
            self.children_dict = {}  # [folder_name] = TreeNode()

        def p_key(self):
            return self.nkfs_item.dir_name()

        def __setitem__(self, key, value):
            self.children_dict[key] = value

        def __getitem__(self, item):
            return self.children_dict[item]

        def __iter__(self):
            return iter(self.children_dict)

    def __init__(self, *args, **kwargs):
        super(NQWidgetExplorerNavTree, self).__init__(*args, **kwargs)

        # GUI Components

    def construct(self):
        pass

    def connect_signals(self):
        pass

    def set_folders(self, root_dir, folders):
        pass
