from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class NQThread(NKPrintableMixin, QThread):
    def __init__(self):
        super(NQThread, self).__init__()

        # Thread Flow Control
        self.stop_flag = False  # Flag raised, thread stops.
        self.pause_flag = False  # Flag raised, program paused.

        # Message
        self.error_list = []

        # Connect Signals
        self.finished.connect(self.slot_thread_done)

    def slot_thread_done(self):
        pass
