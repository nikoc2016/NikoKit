from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt import NQApplication
import time

STATUS_QUEUED = "STATUS_QUEUED"
STATUS_RUNNING = "STATUS_RUNNING"
STATUS_COMPLETED = "STATUS_COMPLETED"
STATUS_NOT_EXIST = "STATUS_NOT_EXIST"

class NQThreadWorker(QObject):
    """Base Worker class, users should inherit and implement their own task logic"""
    signal_started = Signal()  # Signal emitted when task starts
    signal_finished = Signal()  # Signal emitted when task ends
    signal_progress = Signal(int)  # Signal for task progress (optional)
    signal_error = Signal(str)  # Signal for task errors

    def __init__(self):
        super().__init__()
        self.stop_flag = False
        self.pause_flag = False

    def run(self):
        try:
            self.signal_started.emit()  # Emit task start signal
            while not self.stop_flag:
                if not self.pause_flag:
                    # Custom task logic goes here
                    raise NotImplementedError
                time.sleep(0.1)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            self.signal_error.emit(error_message)  # Emit error signal, OPTIONAL
        finally:
            self.signal_finished.emit()  # [CRITICAL] Must emit OR Thread permanent stuck!

    def log(self, log_channel, log_type, log_context):
        # [IMPORTANT] For NKPatrol-Butler to display task_logs properly, log_channel="task_id"
        NQApplication.Runtime.Service.NKLogger.log("NQTM_" + log_channel, log_type, log_context)

    def __repr__(self):
        return f"{id(self) % (10 ** 3)}-{self.__class__.__name__}"

class NQThreadManager(QObject):
    signal_task_started = Signal(object)  # Signal emitted when a task starts; object is NQThreadWorker
    signal_task_finished = Signal(object)  # Signal emitted when a task finishes; object is NQThreadWorker
    signal_task_error = Signal(object, str)  # Signal emitted when a task encounters an error; object is NQThreadWorker, str is error message

    def __init__(self, threads_count=4):
        super().__init__()
        self.threads_count = threads_count
        self.qthreads_to_worker = {}  # {qthread: worker}
        self.workers_queue = []  # [(priority, worker)]
        self.paused = False

        # Initialize QThreads
        for _ in range(threads_count):
            qthread = QThread()
            qthread.start()
            self.qthreads_to_worker[qthread] = None

    def run(self, worker, priority=0):
        # Add worker to the queue with priority, maintaining order
        self.workers_queue.append((priority, worker))
        self._arrange_tasks()

    def run_on_duplicate_ignore(self, worker, priority=0):
        # Check if worker exists in the queue or is currently running
        if any(queued_worker == worker for _, queued_worker in self.workers_queue):
            return  # Ignore if worker already in the queue
        if any(active_worker == worker for active_worker in self.qthreads_to_worker.values()):
            return  # Ignore if worker is already running

        self.run(worker, priority)

    def pause(self):
        self.paused = True
        for _, worker in self.qthreads_to_worker.items():
            if isinstance(worker, NQThreadWorker):
                worker.pause_flag = True

    def resume(self):
        self.paused = False
        for _, worker in self.qthreads_to_worker.items():
            if isinstance(worker, NQThreadWorker):
                worker.pause_flag = False
        self._arrange_tasks()

    def get_threads_status(self):
        # Return a dictionary of thread and worker status
        threads_status = []
        for _, worker in self.qthreads_to_worker.items():
            if worker is not None:
                worker_info = repr(worker)
            else:
                worker_info = None
            threads_status.append(worker_info)
        return threads_status

    def get_worker_status(self, worker):
        if not isinstance(worker, NQThreadWorker):
            return STATUS_NOT_EXIST

        # Check if the worker exists in any thread
        for qthread, active_worker in self.qthreads_to_worker.items():
            if active_worker == worker:
                return STATUS_RUNNING

        # Check if the worker is in the queue
        for _, queued_worker in self.workers_queue:
            if queued_worker == worker:
                return STATUS_QUEUED

        # Check if the worker has finished (signal already emitted)
        if worker.stop_flag and not any(worker == active_worker for active_worker in self.qthreads_to_worker.values()):
            return STATUS_COMPLETED

        return STATUS_NOT_EXIST

    def get_tasks_ahead(self, worker):
        # Count the number of workers ahead of the given worker based on queue order
        worker_priority = None
        for priority, queued_worker in self.workers_queue:
            if queued_worker == worker:
                worker_priority = priority
                break
        if worker_priority is None:
            return 0

        count = 0
        for priority, queued_worker in self.workers_queue:
            if queued_worker == worker:
                break
            if priority >= worker_priority:
                count += 1
        return count

    def shutdown(self, wait_sec=0, wait_forever=False):
        # Gracefully stop all workers
        for qthread, worker in self.qthreads_to_worker.items():
            if worker:
                worker.stop_flag = True

        if wait_forever:
            for qthread in self.qthreads_to_worker:
                qthread.wait()
        else:
            end_time = time.time() + wait_sec
            while time.time() < end_time:
                if all(worker is None for worker in self.qthreads_to_worker.values()):
                    break
                time.sleep(0.1)

        # Forcefully terminate remaining threads
        for qthread in self.qthreads_to_worker:
            qthread.terminate()  # terminate for forceful shutdown
            qthread.wait()

    def _arrange_tasks(self):
        if self.paused:
            return

        # Continue assigning workers while there are available threads and queued workers
        while True:
            # Check for an available QThread
            available_thread = None
            for qthread, worker in self.qthreads_to_worker.items():
                if worker is None:
                    available_thread = qthread
                    break

            if available_thread is None:
                return  # No available threads

            # Find the worker with the highest priority and earliest position without sorting
            if not self.workers_queue:
                return  # No workers in queue

            target_index = 0
            target_priority, target_worker = self.workers_queue[0]
            for i, (priority, worker) in enumerate(self.workers_queue):
                if priority > target_priority:
                    target_priority, target_worker = priority, worker
                    target_index = i

            # Assign worker to thread
            self.workers_queue.pop(target_index)
            self.qthreads_to_worker[available_thread] = target_worker
            self._start_worker(available_thread, target_worker)

    def _start_worker(self, thread, worker):
        # Move the worker to the thread and start it
        worker.moveToThread(thread)
        worker.signal_started.connect(lambda: self.signal_task_started.emit(worker))
        worker.signal_finished.connect(lambda: self._clean_up(worker, thread))
        worker.signal_error.connect(lambda error_message: self.signal_task_error.emit(worker, error_message))
        worker.signal_finished.connect(lambda: self.signal_task_finished.emit(worker))

        # Start the worker in the thread
        QTimer.singleShot(0, worker.run)  # QTimer.singleShot schedules the worker's run method

    def _clean_up(self, worker=None, thread=None):
        # Clean up after a worker has finished its task
        if thread in self.qthreads_to_worker:
            self.qthreads_to_worker[thread] = None

        if worker:
            try:
                worker.deleteLater()
            except:
                pass

        # Try to arrange the next worker
        self._arrange_tasks()

# Example usage
if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    manager = NQThreadManager(threads_count=4)

    class ExampleWorker(NQThreadWorker):
        def run(self):
            try:
                self.signal_started.emit()
                for i in range(5):
                    if self.stop_flag:
                        break
                    time.sleep(1)  # Simulate work
                    # self.signal_progress.emit((i + 1) * 20)
                    print((i + 1) * 20)
                if not self.stop_flag:
                    self.signal_finished.emit()
            except Exception as e:
                self.signal_error.emit(str(e))

    # Create and run some workers
    worker1 = ExampleWorker()
    worker2 = ExampleWorker()
    worker3 = ExampleWorker()

    manager.run(worker1, priority=1)
    manager.run(worker2, priority=2)
    manager.run(worker3, priority=0)

    sys.exit(app.exec_())
