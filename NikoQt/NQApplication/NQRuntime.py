import getpass
import socket

from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoStd.NKVersion import NKVersion


class DefaultSignals(QObject):
    tick_passed = Signal()
    second_passed = Signal(int)  # Range 0-59
    minute_passed = Signal(int)  # Range 0-59
    hour_passed = Signal(int)  # Range 0-23
    day_passed = Signal(int)  # Range 1-31
    month_passed = Signal(int)  # Range 1-12
    tray_clicked = Signal(object)  # reason


class NQRuntime(QObject):
    Signals = DefaultSignals()
    Config = None

    class Dir:
        appdata_dir = None  # MyDoc\AppName
        log_dir = None  # MyDoc\AppName\Logs

    class File:
        yaml_config = "config.yaml"

    class App:
        name = "NikoQt"
        name_short = "NQ"
        version = NKVersion("1.0.0")
        version_tag = NKVersion.ALPHA
        cmd_server_host = "localhost"
        cmd_server_port = 0
        compiled = False
        my_dir = ""
        my_file_name = ""
        my_file_ext = ""
        use_dummy = False
        icon_res_name = "NikoKitLogo.png"

    class Data:
        Res = None

    class Threads:
        pass

    class Service:
        NQTimer = None
        AppDataMgr = None
        NKLang = None
        DataLoader = None
        NKLogger = None
        NKCmd = None
        NKGuard = None

    class Gui:
        Wins = {}
        WinMgr = None
        WinDataLoader = None
        WinLogs = None
        TrayIcon = None
        TrayIconMgr = None

    class Database:
        Conn = None
        Create = None
        Update = None
        Retrieve = None
        Delete = None

    class Machine:
        pc_name = socket.gethostname()
        ip = socket.gethostbyname(pc_name)
        username = str(getpass.getuser())
        fqdn = socket.getfqdn()
        fqdn_parts = fqdn.split(".")
        active_directory = fqdn_parts[1] if len(fqdn_parts) > 1 else fqdn
        hardware_snapshot = None
