from NikoKit.NikoQt.NQApplication import NQRuntime


class NQSatelliteRuntime(NQRuntime):
    class App(NQRuntime.App):
        admin_password = ""

    class Gui(NQRuntime.Gui):
        TrayIcon = None
        TrayMenu = None
        TrayMenuItems = None

        WinLogs = None
