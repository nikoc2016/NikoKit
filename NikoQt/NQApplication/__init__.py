import sys
import os.path as p

from NikoKit.NikoQt.NQApplication.NQRuntimeInterfaces import RuntimeDefault
from NikoKit.NikoQt.NQAdapter import *

Runtime = RuntimeDefault


def load_basic():
    if getattr(sys, 'frozen', False):
        Runtime.App.compiled = True
        Runtime.App.my_dir = p.dirname(sys.executable)
        Runtime.App.my_file_name = p.splitext(p.basename(sys.executable))[0]
        Runtime.App.my_file_ext = p.splitext(p.basename(sys.executable))[1]
    else:
        Runtime.App.compiled = False
        Runtime.App.my_dir = p.dirname(p.abspath(__file__))
        Runtime.App.my_filename = p.splitext(p.basename(__file__))[0]
        Runtime.App.my_file_ext = p.splitext(p.basename(__file__))[1]


def load_service_timer():
    from NikoKit.NikoQt.NQKernel.NQComponent.NQTimer import NQTimer
    Runtime.Service.timer = NQTimer()


def load_window_manager():
    from NikoKit.NikoQt.NQKernel.NQGui.NQWindow import NQWindowManager
    Runtime.Gui.win_mgr = NQWindowManager


def apply_dark_theme():
    app = QApplication.instance()
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(200, 200, 200).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
