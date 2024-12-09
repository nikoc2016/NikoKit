import datetime
import calendar
from functools import wraps

from NikoKit.NikoStd.NKPrint import tprint


class NKDatetime:
    DT_FORMAT = '%Y-%m-%d_%H-%M-%S'

    @staticmethod
    def now():
        return datetime.datetime.now()

    @staticmethod
    def datetime_to_str(target_datetime):
        if not target_datetime:
            return ""
        return target_datetime.strftime(NKDatetime.DT_FORMAT)

    @staticmethod
    def str_to_datetime(target_datetime_str):
        if not target_datetime_str:
            return None
        return datetime.datetime.strptime(target_datetime_str, NKDatetime.DT_FORMAT)

    @staticmethod
    def if_datetime_expired(target_datetime, expiration_seconds):
        now_datetime = NKDatetime.now()
        if now_datetime < target_datetime or (now_datetime - target_datetime).seconds < expiration_seconds:
            return True
        return False

    @staticmethod
    def secs_to_dhms(seconds):
        days = seconds // (24 * 3600)
        seconds %= (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return days, hours, minutes, seconds

    @staticmethod
    def dhms_to_secs(days, hours, minutes, seconds):
        total_seconds = (days * 24 * 3600) + (hours * 3600) + (minutes * 60) + seconds
        return total_seconds


class NKDate:
    DT_FORMAT = '%Y-%m-%d'

    @staticmethod
    def now():
        return datetime.date.today()

    @staticmethod
    def date_to_str(target_date):
        if not target_date:
            return ""
        return target_date.strftime(NKDate.DT_FORMAT)

    @staticmethod
    def str_to_date(target_date_str):
        if not target_date_str:
            return None
        return datetime.datetime.strptime(target_date_str, NKDate.DT_FORMAT).date()

    @staticmethod
    def if_datetime_expired(target_date, expiration_days):
        now_date = NKDate.now()
        if now_date < target_date or (now_date - target_date).days <= expiration_days:
            return True
        return False

    @classmethod
    def month_days_count(cls, year, month):
        return calendar.monthrange(year, month)[1]

    @classmethod
    def month_dates_all(cls, year, month):
        return [datetime.date(year, month, day + 1) for day in range(cls.month_days_count(year, month))]

    @classmethod
    def month_dates_workdays(cls, year, month):
        return [month_date for month_date in cls.month_dates_all(year, month) if 0 <= month_date.weekday() <= 4]

    @classmethod
    def month_dates_weekends(cls, year, month):
        return [month_date for month_date in cls.month_dates_all(year, month) if 5 <= month_date.weekday() <= 6]

    @classmethod
    def gap_dates(cls, *dates):
        gap_dates = []
        sort_dates = sorted(dates)
        gap_date = sort_dates[0]
        while gap_date <= sort_dates[-1]:
            gap_dates.append(gap_date)
            gap_date += datetime.timedelta(days=1)
        return gap_dates


class TimeMeasure:
    def __init__(self):
        self.base_datetime = None
        self.elapse_deltas = []

    def clear(self):
        self.base_datetime = None
        self.elapse_deltas = []

    def start(self):
        if not self.base_datetime:
            self.base_datetime = datetime.datetime.now()

    def stop(self):
        current_datetime = datetime.datetime.now()
        self.elapse_deltas.append(current_datetime - self.base_datetime)
        self.base_datetime = None

    def check(self):
        self.stop()
        self.start()

    def get_length(self):
        elapse_delta_sum = datetime.timedelta()
        for elapse_delta in self.elapse_deltas:
            elapse_delta_sum = elapse_delta_sum + elapse_delta
        return elapse_delta_sum

    def get_lengths(self):
        return self.elapse_deltas

    @staticmethod
    def time_measure_decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start_time = datetime.datetime.now()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            tprint("Execute time<%s.%s>: %s" % (str(func.__module__), str(func.__qualname__), str(end_time - start_time)))
            return result

        return inner
