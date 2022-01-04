from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoStd.NKVersion import NKVersion


class DefaultSignals(QObject):
    second_passed = Signal(int)  # Range 0-59
    minute_passed = Signal(int)  # Range 0-59
    hour_passed = Signal(int)  # Range 0-23
    day_passed = Signal(int)  # Range 1-31
    month_passed = Signal(int)  # Range 1-12


class DefaultPath:
    appdata_dir = None  # MyDoc\AppName


class DefaultApp:
    name = "NikoQt"
    name_short = "NQ"
    version = NKVersion("1.0.0")
    version_tag = NKVersion.ALPHA
    compiled = False
    my_dir = ""
    my_file_name = ""
    my_file_ext = ""


class DefaultData:
    pass


class DefaultThreads:
    pass


class DefaultService:
    NKTimer = None
    AppDataMgr = None
    NKLang = None


class DefaultGui:
    Wins = {}
    WinMgr = None


class DefaultRuntime:
    Signals = DefaultSignals()
    Path = DefaultPath
    App = DefaultApp
    Data = DefaultData
    Threads = DefaultThreads
    Service = DefaultService
    Gui = DefaultGui
