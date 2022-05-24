import datetime
import time


def run_forever(entry, logging=True, run_now=True, days=0, hours=0, minutes=0, seconds=0):
    time_delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    first_run = True

    while True:
        if not first_run or (first_run and run_now):
            if logging:
                print("Running...")
            entry()

        first_run = False
        previous_update_datetime = datetime.datetime.now()
        next_update_datetime = previous_update_datetime + time_delta
        if logging:
            print("This run:%s, Next run:%s" % (previous_update_datetime, next_update_datetime))

        while datetime.datetime.now() < next_update_datetime:
            time.sleep(1)
