from NikoKit.NikoQt.NQAdapter import Signal

from NikoKit.NikoQt.NQApplication.NQRuntime import NQRuntime, DefaultSignals


class NQSatelliteSignals(DefaultSignals):
    cmd_broadcast = Signal(str, str)  # cmd_id, cmd_line
    awake = Signal(str)  # Awake Signal


class NQSatelliteRuntime(NQRuntime):
    class App(NQRuntime.App):
        admin_password = ""

    Signals = NQSatelliteSignals()
