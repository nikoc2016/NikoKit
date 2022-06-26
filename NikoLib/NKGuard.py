import threading
import time
import traceback

import psutil as psutil

from NikoKit.NikoStd.NKPrint import eprint, tprint


class NKGuard:
    def __init__(self, auto_quit=False):
        self.guard_thread = None
        self.pid_to_launcher = {}
        self.auto_quit = auto_quit

    def protect(self, pid, launcher):
        self.pid_to_launcher[pid] = launcher

    def unprotect(self, pid):
        del self.pid_to_launcher[pid]

    def launch(self, silent_mode=False):
        self.stop(silent_mode=True)
        self.guard_thread = self.NKGuardThread(self)
        self.guard_thread.start()
        if not silent_mode:
            tprint("Guard::Protection Started")

    def stop(self, silent_mode=False):
        try:
            self.guard_thread.stop()
            self.guard_thread.join()
        except:
            pass
        self.guard_thread = None
        if not silent_mode:
            tprint("Guard::Protection Stopped")

    class NKGuardThread(threading.Thread):
        def __init__(self, parent):
            self.parent = parent

            self.pause_flag = False
            self.stop_flag = False

            super(NKGuard.NKGuardThread, self).__init__()

        def run(self):
            while not self.stop_flag:
                if not self.pause_flag:
                    if not self.parent.pid_to_launcher and self.parent.auto_quit:
                        self.parent.stop()
                    delete_reservation = []
                    for pid, launcher in self.parent.pid_to_launcher.items():
                        if not psutil.pid_exists(pid):
                            delete_reservation.append(pid)
                            try:
                                launcher()
                            except:
                                eprint(traceback.format_exc())
                    for pid in delete_reservation:
                        del self.parent.pid_to_launcher[pid]

                for i in range(10):
                    if not self.stop_flag:
                        time.sleep(0.1)
                    else:
                        break

        def stop(self):
            self.stop_flag = True
