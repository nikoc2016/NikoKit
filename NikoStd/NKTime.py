import datetime
from functools import wraps


class NKDatetime:
    DT_FORMAT = '%Y-%m-%d_%H:%M:%S'

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
            print(func.__name__ + " Execute Time: " + str(end_time - start_time))
            return result

        return inner
