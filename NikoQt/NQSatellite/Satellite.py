import os
import sys
import traceback

from NikoKit.NikoLib import NKCmd
from NikoKit.NikoLib.NKHardwareSpec import NKHardwareSpec
from NikoKit.NikoQt.NQKernel.NQComponent.NQMenu import NQMenuOption, NQMenuSubMenu, NQMenuLineSeparator
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowConsole import NQWindowPythonConsole, NQWindowNKCmdConsole
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowLogin import NQWindowLogin
from NikoKit.NikoQt.NQKernel.NQGui.NQWindowLogs import NQWindowLogs
from NikoKit.NikoQt.NQSatellite.Runtime import NQSatelliteRuntime
from NikoKit.NikoStd import NKLaunch
from NikoKit.NikoStd.NKPrint import eprint
from NikoKit.NikoStd.NKVersion import NKVersion
from NikoKit.NikoQt import NQApplication
import os.path as p


def admin_validator(username, password):
    if password == NQApplication.Runtime.App.admin_password:
        return True
    else:
        return False


def register_commands():
    NQApplication.Runtime.Service.NKCmd.register_command("awake", "awake [Target]")


def cmd_handler(command_id, command_line):
    if command_line.startswith("awake"):
        NQApplication.Runtime.Signals.awake.emit(command_line[5:].strip())
        NQApplication.Runtime.Service.NKCmd.finish_command(command_id=command_id,
                                                           result_sign=NKCmd.NKCmdServer.RESULT_SIGN_GOOD,
                                                           result_detail="Awake Received")
    else:
        NQApplication.Runtime.Signals.cmd_broadcast.emit(command_id, command_line)


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
                 log_dir=None,  # None -> appdata_dir; "" -> No Log; "url" -> custom log
                 use_dummy=False,
                 scan_machine_spec=True,
                 cmd_server_port=0,
                 enable_nk_logger=True,
                 enable_dark_theme=True,
                 enable_resource=True,
                 resource_patch=None,
                 enable_timer=True,
                 enable_window_manager=True,
                 enable_tray_manager=True,
                 enable_appdata_manager=True,
                 enable_data_loader=True,
                 enable_nk_language=True,
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
        if log_dir is None:
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
            NQApplication.load_service_nk_logger()
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
        if enable_tray_manager:
            NQApplication.load_service_tray_manager()
        if enable_data_loader:
            NQApplication.load_service_data_loader()
        if enable_dark_theme:
            NQApplication.apply_dark_theme()
        if enable_nk_guard:
            NQApplication.load_service_nk_guard()

        if cmd_server_port:
            NQApplication.Runtime.App.cmd_server_port = cmd_server_port
            NQApplication.load_service_cmd_server()
            NQApplication.Runtime.Service.NKCmd.launch(host=NQApplication.Runtime.App.cmd_server_host,
                                                       port=NQApplication.Runtime.App.cmd_server_port,
                                                       handler_func=cmd_handler,
                                                       silent_mode=False)
            register_commands()

        NQApplication.Runtime.Gui.WinLogs = NQWindowLogs(nk_logger=NQApplication.Runtime.Service.NKLogger,
                                                         w_title="Logs")

        lang = NQApplication.Runtime.Service.NKLang

        NQApplication.Runtime.Gui.TrayIconMgr.tray_menu_generator.set_content_list([
            NQMenuOption(name="logs", display_name=lang.tran("logs"), slot_callback=self.slot_show_logs),
            NQMenuSubMenu(name="console_menu",
                          display_name=lang.tran("console"),
                          children_list=[
                              NQMenuOption(name="python_console",
                                           display_name=lang.tran("Python", "console"),
                                           slot_callback=self.slot_python_console),
                              NQMenuOption(name="gml_cmd_console",
                                           display_name=lang.tran("GML-CMD", "console"),
                                           slot_callback=self.slot_cmd_console),
                          ]),
            NQMenuLineSeparator(),
            NQMenuOption(name="exit", display_name=lang.tran("quit"), slot_callback=self.slot_exit)
        ])
        NQApplication.Runtime.Gui.TrayIconMgr.rebuild()

    @classmethod
    def slot_show_logs(cls):
        NQApplication.Runtime.Gui.WinLogs.show()

    @classmethod
    def slot_python_console(cls):
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
            success_callback=cls.slot_new_python_console_admin_verified
        ).show()

    @classmethod
    def slot_cmd_console(cls):
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
            success_callback=cls.slot_new_cmd_console_admin_verified
        ).show()

    @classmethod
    def slot_new_python_console_admin_verified(cls):
        NQWindowPythonConsole(w_title="Python Console", allow_execute=True).show()

    @classmethod
    def slot_new_cmd_console_admin_verified(cls):
        NQWindowNKCmdConsole(host=NQApplication.Runtime.App.cmd_server_host,
                             port=NQApplication.Runtime.App.cmd_server_port,
                             w_title="CMD Console",
                             allow_execute=True).show()

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

    def exit(self, *args, **kwargs):
        try:
            NQApplication.Runtime.Service.NQTimer.stop_timer()
        except:
            pass

        try:
            self.before_exit_callback(*args, **kwargs)
        except:
            eprint(traceback.format_exc())

        self.QApplication.exit()
        sys.exit()
