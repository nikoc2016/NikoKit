from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoStd.NKVersion import NKVersion


class Signals(QObject):
    second_passed = Signal(int)  # Range 0-59
    minute_passed = Signal(int)  # Range 0-59
    hour_passed = Signal(int)  # Range 0-23
    day_passed = Signal(int)  # Range 1-31
    month_passed = Signal(int)  # Range 1-12


class App:
    name = "NikoQt"
    name_short = "NQ"
    version = NKVersion("1.0.0")
    version_tag = NKVersion.ALPHA
    compiled = False
    my_dir = ""
    my_file_name = ""
    my_file_ext = ""


class Data:
    pass


class Threads:
    pass


class Service:
    timer = None


class Gui:
    wins = {}
    win_mgr = None


class RuntimeDefault:
    Signals = Signals()
    App = App
    Data = Data
    Threads = Threads
    Service = Service
    Gui = Gui
