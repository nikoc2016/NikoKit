from NikoKit.NikoStd.NKVersion import NKVersion
import os.path as p


class NQLite:
    def __init__(self,
                 name,
                 name_short,
                 version,
                 version_tag,
                 entry_py_path,
                 config=None,
                 icon_res_name="",
                 runtime=None,
                 appdata_dir="",
                 log_dir=None,  # None -> appdata_dir; "" -> No Log; "url" -> custom log
                 use_dummy=False,
                 quit_on_last_window_closed=True,
                 enable_nk_logger=True,
                 enable_dark_theme=True,
                 enable_resource=True,
                 resource_patch=None,
                 enable_timer=True,
                 enable_window_manager=True,
                 enable_tray_manager=False,
                 enable_appdata_manager=True,
                 enable_data_loader=True,
                 enable_nk_language=True
                 ):
        # Storage
        self.QApplication = None
        self.Runtime = None

        # Validation
        name = str(name)
        name_short = str(name_short)
        if not isinstance(version, NKVersion):
            raise Exception("version must be a NKVersion()")
        version_tag = str(version_tag)

        # QApplication
        from NikoKit.NikoQt.NQAdapter import QApplication
        self.QApplication = QApplication()

        from NikoKit.NikoQt import NQApplication
        if runtime:
            self.Runtime = runtime
            NQApplication.Runtime = runtime
        else:
            self.Runtime = NQApplication.Runtime

        if not appdata_dir:
            appdata_dir = p.join(p.expanduser('~'), 'Documents', name)
        if log_dir is None:
            log_dir = p.join(appdata_dir, "Logs")

        NQApplication.Runtime.App.name = name
        NQApplication.Runtime.App.name_short = name_short
        NQApplication.Runtime.App.version = version
        NQApplication.Runtime.App.version_tag = version_tag
        NQApplication.Runtime.Config = config
        NQApplication.Runtime.App.use_dummy = use_dummy
        NQApplication.Runtime.Dir.appdata_dir = appdata_dir
        NQApplication.Runtime.Dir.log_dir = log_dir

        if icon_res_name:
            NQApplication.Runtime.App.icon_res_name = icon_res_name

        NQApplication.load_basic(entry_py_path)
        self.QApplication.setQuitOnLastWindowClosed(quit_on_last_window_closed)

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

    def serve(self):
        self.QApplication.exec_()

    def exit(self):
        from NikoKit.NikoQt import NQApplication
        try:
            NQApplication.Runtime.Service.NQTimer.stop_timer()
        except:
            pass
        self.QApplication.quit()
