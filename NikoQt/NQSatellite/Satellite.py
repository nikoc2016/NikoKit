import sys
import traceback

from NikoKit.NikoLib.NKHardwareSpec import NKHardwareSpec
from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowConsole import NQWindowPythonConsole
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowLogin import NQWindowLogin
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowLogs import NQWindowLogs
from NikoKit.NikoQt.NQSatellite.Runtime import NQSatelliteRuntime
from NikoKit.NikoStd.NKPrint import eprint
from NikoKit.NikoStd.NKVersion import NKVersion
from NikoKit.NikoQt import NQApplication
import os.path as p


def admin_validator(username, password):
    if password == NQApplication.Runtime.App.admin_password:
        return True
    else:
        return False


class NQSatellite:
    def __init__(self,
                 name,
                 name_short,
                 version,
                 version_tag,
                 entry_py_path,
                 admin_password="sudo",
                 before_exit_callback=None,
                 icon_res_name="NQSatelliteLogo.png",
                 runtime=None,
                 appdata_dir="",
                 log_dir="",
                 plugin_loader=None,
                 use_dummy=False,
                 scan_machine_spec=True,
                 enable_nk_logger=True,
                 enable_dark_theme=True,
                 enable_resource=True,
                 resource_patch=None,
                 enable_timer=True,
                 enable_window_manager=True,
                 enable_appdata_manager=True,
                 enable_data_loader=True,
                 enable_nk_language=True,
                 enable_cmd_server=True,
                 enable_nk_guard=True
                 ):
        # Storage
        self.QApplication = None
        self.Runtime = None
        self.before_exit_callback = before_exit_callback

        # Validation
        name = str(name)
        name_short = str(name_short)
        if not isinstance(version, NKVersion):
            raise Exception("version must be a NKVersion()")
        version_tag = str(version_tag)

        # QApplication
        from NikoKit.NikoQt.NQAdapter import QApplication
        self.QApplication = QApplication()
        self.QApplication.setQuitOnLastWindowClosed(False)

        if runtime:
            self.Runtime = runtime
            NQApplication.Runtime = runtime
        else:
            self.Runtime = NQSatelliteRuntime
            NQApplication.Runtime = NQSatelliteRuntime

        if not appdata_dir:
            appdata_dir = p.join(p.expanduser('~'), 'Documents', name)
        if not log_dir:
            log_dir = p.join(appdata_dir, "Logs")

        # Machine Spec
        if scan_machine_spec:
            NQApplication.Runtime.Machine.hardware_snapshot = NKHardwareSpec().get_snapshot()

        NQApplication.Runtime.App.name = name
        NQApplication.Runtime.App.name_short = name_short
        NQApplication.Runtime.App.version = version
        NQApplication.Runtime.App.version_tag = version_tag
        NQApplication.Runtime.App.use_dummy = use_dummy
        NQApplication.Runtime.App.admin_password = admin_password
        NQApplication.Runtime.Dir.appdata_dir = appdata_dir
        NQApplication.Runtime.Dir.log_dir = log_dir

        if icon_res_name:
            NQApplication.Runtime.App.icon_res_name = icon_res_name

        NQApplication.load_basic(entry_py_path)
        if enable_nk_logger:
            NQApplication.load_service_nk_logger(log_dir)
        if enable_resource:
            NQApplication.load_service_nq_resource(resource_patch)
        if enable_appdata_manager:
            NQApplication.load_service_appdata_manager()
        if enable_nk_language:
            NQApplication.load_service_nk_language()
        if enable_timer:
            NQApplication.load_service_timer()
        if enable_window_manager:
            NQApplication.load_service_window_manager()
        if enable_data_loader:
            NQApplication.load_service_data_loader()
        if enable_dark_theme:
            NQApplication.apply_dark_theme()
        if enable_cmd_server:
            NQApplication.load_service_cmd_server()
        if enable_nk_guard:
            NQApplication.load_service_nk_guard()

        NQApplication.Runtime.Gui.WinLogs = NQWindowLogs(nk_logger=NQApplication.Runtime.Service.NKLogger,
                                                         w_title="Logs")

        self.build_tray()
        self.build_tray_menu()

        if callable(plugin_loader):
            try:
                plugin_loader()
            except Exception as e:
                eprint("NQSatellite::Plugin Loader Failure\n%s" % traceback.format_exc())

    def build_tray(self):
        NQApplication.Runtime.Gui.TrayIcon = QSystemTrayIcon()
        NQApplication.Runtime.Gui.TrayIcon.setIcon(
            NQApplication.Runtime.Data.Res.QIcon(NQApplication.Runtime.App.icon_res_name)
        )
        NQApplication.Runtime.Gui.TrayIcon.activated.connect(self.slot_tray_clicked)
        NQApplication.Runtime.Gui.TrayIcon.show()

    def build_tray_menu(self):
        NQApplication.Runtime.Gui.TrayMenuItems = []

        # EXAMPLE: Register an action
        action_show_logs = QAction(NQApplication.Runtime.Service.NKLang.tran("logs"))
        action_show_logs.triggered.connect(self.slot_show_logs)
        action_console = QAction(NQApplication.Runtime.Service.NKLang.tran("console"))
        action_console.triggered.connect(self.slot_new_console)
        action_quit = QAction(NQApplication.Runtime.Service.NKLang.tran("quit"))
        action_quit.triggered.connect(self.slot_exit)
        NQApplication.Runtime.Gui.TrayMenuItems.append(action_show_logs)
        NQApplication.Runtime.Gui.TrayMenuItems.append(action_console)
        NQApplication.Runtime.Gui.TrayMenuItems.append(action_quit)

        NQApplication.Runtime.Gui.TrayMenu = QMenu()
        NQApplication.Runtime.Gui.TrayMenu.addAction(action_show_logs)
        NQApplication.Runtime.Gui.TrayMenu.addAction(action_console)
        NQApplication.Runtime.Gui.TrayMenu.addSeparator()
        NQApplication.Runtime.Gui.TrayMenu.addAction(action_quit)

        NQApplication.Runtime.Gui.TrayIcon.setContextMenu(NQApplication.Runtime.Gui.TrayMenu)

    def slot_tray_clicked(self):
        pass

    @classmethod
    def slot_show_logs(cls):
        NQApplication.Runtime.Gui.WinLogs.show()

    @classmethod
    def slot_new_console(cls):
        NQWindowLogin(
            admin_validator,
            w_width=300,
            w_height=100,
            w_title="Auth",
            appdata_name="AdminAuth",
            ignore_auto_login=True,
            require_username=False,
            require_password=True,
            allow_remember_me=False,
            allow_auto_login=False,
            success_callback=cls.slot_new_console_admin_verified
        ).show()

    @classmethod
    def slot_new_console_admin_verified(cls):
        NQWindowPythonConsole(w_title="Python Console", allow_execute=True).show()

    def slot_exit(self):
        NQWindowLogin(
            admin_validator,
            w_width=300,
            w_height=100,
            w_title="Auth",
            appdata_name="AdminAuth",
            ignore_auto_login=True,
            require_username=False,
            require_password=True,
            allow_remember_me=False,
            allow_auto_login=False,
            success_callback=self.exit
        ).show()

    def serve(self):
        self.QApplication.exec_()

    def exit(self):
        try:
            NQApplication.Runtime.Service.NQTimer.stop_timer()
        except:
            pass
        if self.before_exit_callback:
            self.before_exit_callback()
        self.QApplication.quit()
