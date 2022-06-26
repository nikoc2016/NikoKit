import sys
import os.path as p

from NikoKit.NikoLib.NKFileSystem import get_exe_info
from NikoKit.NikoQt.NQApplication.NQRuntime import NQRuntime
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowLogs import NQWindowLogs

Runtime = NQRuntime


def load_basic(entry_py_path):
    Runtime.App.compiled, Runtime.App.my_dir, Runtime.App.my_file_name, Runtime.App.my_file_ext = get_exe_info(entry_py_path)

    if not Runtime.Dir.appdata_dir:
        Runtime.Dir.appdata_dir = p.join(p.expanduser('~'), 'Documents', 'NQAppdata')


def load_service_nk_logger(log_dir):
    from NikoKit.NikoLib.NKLogger import NKLogger
    Runtime.Service.NKLogger = NKLogger(log_dir=log_dir)


def load_service_nq_resource(res_patch=None):
    from NikoKit.NikoQt.NQKernel.NQComponent.NQResource import NQResource
    Runtime.Data.Res = NQResource(res_patch)


def load_service_nk_language():
    from NikoKit.NikoStd.NKLanguage import NKLanguage
    Runtime.Service.NKLang = NKLanguage()


def load_service_timer():
    from NikoKit.NikoQt.NQKernel.NQComponent.NQTimer import NQTimer
    Runtime.Service.NQTimer = NQTimer()


def load_service_appdata_manager():
    from NikoKit.NikoLib.NKAppDataManager import NKAppDataManager
    Runtime.Service.AppDataMgr = NKAppDataManager(appdata_root=Runtime.Dir.appdata_dir)
    Runtime.Service.AppDataMgr.load_all()


def load_service_window_manager():
    from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindowManager
    Runtime.Gui.WinMgr = NQWindowManager


def load_service_data_loader():
    from NikoKit.NikoLib.NKDataLoader import NKDataLoader
    Runtime.Service.DataLoader = NKDataLoader(appdata_mgr=Runtime.Service.AppDataMgr)
    Runtime.Signals.second_passed.connect(Runtime.Service.DataLoader.slot_second_elapsed, Qt.QueuedConnection)
    from NikoKit.NikoQt.NQKernel.NQGui.NQWindowDataLoader import NQWindowDataLoader
    Runtime.Gui.WinDataLoader = NQWindowDataLoader(w_icon=Runtime.Data.Res.QIcon(Runtime.App.icon_res_name),
                                                   data_loader=Runtime.Service.DataLoader)
    Runtime.Signals.tick_passed.connect(Runtime.Gui.WinDataLoader.slot_refresh)


def load_service_nk_guard(auto_quit=False):
    from NikoKit.NikoLib.NKGuard import NKGuard
    Runtime.Service.NKGuard = NKGuard(auto_quit=auto_quit)


def load_service_cmd_server():
    from NikoKit.NikoLib.NKCmd import NKCmdServer
    Runtime.Service.NKCmd = NKCmdServer()


def apply_dark_theme():
    app = QApplication.instance()
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(60, 63, 65))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(42, 42, 42))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, QColor(169, 183, 198))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(200, 200, 200).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
