from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQApplication import Runtime


class NQTimer(QObject):
    def __init__(self):
        super(NQTimer, self).__init__()

        # Private Storage
        self.previous_month = 0
        self.previous_day = 0
        self.previous_hour = 0
        self.previous_minute = 0
        self.previous_second = 0
        self.previous_has_initiated = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.slot_timeout)
        self.timer.start(1000)

    def slot_timeout(self):
        # Extract Current Time
        curr_datetime = QDateTime.currentDateTime()
        curr_month = int(curr_datetime.toString('MM'))
        curr_day = int(curr_datetime.toString('dd'))
        curr_hour = int(curr_datetime.toString('hh'))
        curr_minute = int(curr_datetime.toString('mm'))
        curr_second = int(curr_datetime.toString('ss'))

        # Emit Signals
        if self.previous_has_initiated:
            if self.previous_month != curr_month:
                Runtime.Signals.month_passed.emit(curr_month)
            if self.previous_day != curr_day:
                Runtime.Signals.day_passed.emit(curr_day)
            if self.previous_hour != curr_hour:
                Runtime.Signals.hour_passed.emit(curr_hour)
            if self.previous_minute != curr_minute:
                Runtime.Signals.minute_passed.emit(curr_minute)
            if self.previous_second != curr_second:
                Runtime.Signals.second_passed.emit(curr_second)

        # Cache Current Time
        self.previous_month = curr_month
        self.previous_day = curr_day
        self.previous_hour = curr_hour
        self.previous_minute = curr_minute
        self.previous_second = curr_second
        self.previous_has_initiated = True
