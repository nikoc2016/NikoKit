import sys
import os.path as p
from NikoKit.NikoLib import NKFileSystem
from NikoKit.NikoStd.NKDataStructure import NKDataStructure
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin
from NikoKit.NikoStd.NKTime import NKDate, NKDatetime

STD_IN = "STD_IN"
STD_OUT = "STD_OUT"
STD_ERR = "STD_ERR"
STD_WARNING = "STD_WARNING"
CHANNEL_SYS = "CHANNEL_SYS"


class NKLog(NKDataStructure):
    def __init__(self, log_datetime_str=None, log_context=None, log_type=None):
        super(NKLog, self).__init__()
        self.log_datetime_str = log_datetime_str
        self.log_context = log_context
        self.log_type = log_type


class NKLogger(NKPrintableMixin):
    def __init__(self, log_dir=""):
        self.logs = {CHANNEL_SYS: []}  # {"CHANNEL_SYS": [NKLog, NKLog..], "CHANNEL_CUSTOM": [NKLog...]}
        self.exist_datetime = {}  # {"CHANNEL_SYS": {"STD_OUT":[datetime, datetime...], "STD_ERR":[datetime...]}}
        self.log_dir = log_dir
        self.default_buffers = {
            STD_OUT: sys.stdout,
            STD_ERR: sys.stderr,
        }
        self.custom_buffers = {
            STD_OUT: NKLoggerBuffer(logger=self, log_channel=CHANNEL_SYS, log_type=STD_OUT),
            STD_ERR: NKLoggerBuffer(logger=self, log_channel=CHANNEL_SYS, log_type=STD_ERR)
        }

        sys.stdout = self.custom_buffers[STD_OUT]
        sys.stderr = self.custom_buffers[STD_ERR]

        super(NKLogger, self).__init__()

    def log(self, log_channel, log_type, log_context):
        datetime_log = None
        now_datetime_str = NKDatetime.datetime_to_str(NKDatetime.now())

        # Init if channel not exists
        if log_channel not in self.logs.keys():
            self.logs[log_channel] = []
        if log_channel not in self.exist_datetime.keys():
            self.exist_datetime[log_channel] = {STD_OUT: set(), STD_ERR: set(), STD_WARNING: set()}

        # Log Datetime
        if now_datetime_str not in self.exist_datetime[log_channel][log_type]:
            datetime_log = NKLog(log_datetime_str=now_datetime_str,
                                 log_context=now_datetime_str + "\n",
                                 log_type=log_type)
            self.logs[log_channel].append(datetime_log)
            self.exist_datetime[log_channel][log_type].add(now_datetime_str)

        # Log Context
        new_log = NKLog(log_datetime_str=now_datetime_str, log_context=log_context, log_type=log_type)
        self.logs[log_channel].append(new_log)

        # Print Service
        try:
            if log_channel == CHANNEL_SYS:
                self.default_buffers[log_type].write(log_context)
        except:
            pass

        # Write Service
        try:
            if self.log_dir:
                today_str = NKDate.date_to_str(NKDate.now())
                file_path = p.join(self.log_dir, log_channel, f"{today_str}_{log_type}.log")
                NKFileSystem.scout(file_path)
                with open(file_path, "a") as f:
                    if datetime_log:
                        f.write(datetime_log.log_context)
                    if new_log:
                        f.write(new_log.log_context)
        except:
            pass


class NKLoggerBuffer:
    def __init__(self, logger, log_channel, log_type):
        self.logger = logger
        self.log_channel = log_channel
        self.log_type = log_type

    def write(self, log_context):
        self.logger.log(log_channel=self.log_channel, log_type=self.log_type, log_context=log_context)

    def flush(self):
        try:
            self.logger.default_buffers[self.log_type].flush()
        except:
            pass
