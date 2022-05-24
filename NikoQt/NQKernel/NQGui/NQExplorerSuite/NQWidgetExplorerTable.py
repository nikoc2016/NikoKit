from NikoKit.NikoQt.NQKernel.NQGui.NQWidgetTable import NQWidgetTable
from NikoKit.NikoQt.NQAdapter import *


class NQWidgetExplorerTable(NQWidgetTable):
    signal_file_selected = Signal(object)
    signal_dir_selected = Signal(object)

    def __init__(self, *args, **kwargs):
        super(NQWidgetExplorerTable, self).__init__(*args, **kwargs)
        self.data_list = []  # [NKFile, NKDir]
        self.header = [self.lang(row_title) for row_title in ["name", "ctime", "atime", "size", "path"]]

    def set_data(self, nkfs_object_list):
        self.data_list = nkfs_object_list
        self.refresh()

    def refresh(self):
        # Convert self.data_list to top_headers, left_headers, table_data
        # Use super()._set_data() to render
        pass
