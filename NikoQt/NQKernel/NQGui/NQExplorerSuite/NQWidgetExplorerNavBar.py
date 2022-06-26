from NikoKit.NikoQt.NQKernel.NQGui.NQWidget import NQWidget
from NikoKit.NikoQt.NQAdapter import *


class NQWidgetExplorerNavBar(NQWidget):
    signal_dir_changed = Signal(str, str)  # Caller-Id, New Dir
    signal_refresh_hit = Signal(str, str)  # Caller-Id, New Dir
    signal_search_changed = Signal(str, str)  # Caller-Id, New Dir
    signal_search_hit = Signal(str, str)  # Caller-Id, New Dir
