from NikoKit.NikoQt.NQAdapter import QSystemTrayIcon
from NikoKit.NikoQt import NQApplication
from NikoKit.NikoQt.NQKernel.NQComponent.NQMenu import NQMenuGenerator


class NQTrayIconManager:
    tray_q_icon = NQApplication.Runtime.Data.Res.QIcon(NQApplication.Runtime.App.icon_res_name)
    tray_menu_generator = NQMenuGenerator()

    @classmethod
    def init_tray(cls):
        if not NQApplication.Runtime.Gui.TrayIcon:
            NQApplication.Runtime.Gui.TrayIcon = QSystemTrayIcon()
            NQApplication.Runtime.Gui.TrayIcon.activated.connect(slot_tray_clicked)
        NQApplication.Runtime.Gui.TrayIcon.setIcon(cls.tray_q_icon)

    @classmethod
    def rebuild(cls):
        if not NQApplication.Runtime.Gui.TrayIcon:
            cls.init_tray()
        NQApplication.Runtime.Gui.TrayIcon.setContextMenu(
            cls.tray_menu_generator.to_menu()
        )

    @classmethod
    def show_tray_icon(cls):
        if not NQApplication.Runtime.Gui.TrayIcon:
            cls.init_tray()
        NQApplication.Runtime.Gui.TrayIcon.show()

    @classmethod
    def hide_tray_icon(cls):
        if not NQApplication.Runtime.Gui.TrayIcon:
            cls.init_tray()
        NQApplication.Runtime.Gui.TrayIcon.hide()


def slot_tray_clicked(reason):
    NQApplication.Runtime.Signals.tray_clicked.emit(reason)
