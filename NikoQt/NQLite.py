from NikoKit.NikoStd.NKVersion import NKVersion
import os.path as p


class NQLite:
    def __init__(self,
                 name,
                 name_short,
                 version,
                 version_tag,
                 runtime=None,
                 appdata_dir="",
                 enable_dark_theme=True,
                 enable_timer=True,
                 enable_window_manager=True,
                 enable_appdata_manager=True,
                 enable_nk_language=True,
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

        NQApplication.Runtime.App.name = name
        NQApplication.Runtime.App.name_short = name_short
        NQApplication.Runtime.App.version = version
        NQApplication.Runtime.App.version_tag = version_tag
        NQApplication.Runtime.Path.appdata_dir = appdata_dir

        if not appdata_dir:
            NQApplication.Runtime.Path.appdata_dir = p.join(p.expanduser('~'), 'Documents', name)

        NQApplication.load_basic()
        if enable_appdata_manager:
            NQApplication.load_service_appdata_manager()
        if enable_nk_language:
            NQApplication.load_service_nk_language()
        if enable_timer:
            NQApplication.load_service_timer()
        if enable_window_manager:
            NQApplication.load_window_manager()
        if enable_dark_theme:
            NQApplication.apply_dark_theme()

    def serve(self):
        self.QApplication.exec_()