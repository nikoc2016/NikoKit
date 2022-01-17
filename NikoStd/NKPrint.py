import threading

PRINT_LOCK = threading.Lock()


def tprint(*args, **kwargs):
    with PRINT_LOCK:
        print(*args, **kwargs)
