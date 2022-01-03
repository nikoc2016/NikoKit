import datetime
import random
import time


def random_datetime(fix_year=None, fix_month=None, fix_day=None):
    try:
        new_datetime = datetime.datetime.fromtimestamp(random.randint(1, int(time.time())))
        if fix_year:
            new_datetime = new_datetime.replace(year=fix_year)
        if fix_month:
            new_datetime = new_datetime.replace(month=fix_month)
        if fix_day:
            new_datetime = new_datetime.replace(day=fix_day)
    except:
        new_datetime = random_datetime(fix_year, fix_month, fix_day)

    return new_datetime
