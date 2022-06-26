import sys
import threading

PRINT_LOCK = threading.Lock()


def tprint(*args):
    with PRINT_LOCK:
        print(*args)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
