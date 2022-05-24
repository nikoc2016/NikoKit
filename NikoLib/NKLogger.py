import sys
from NikoKit.NikoLib import NKFileSystem
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin
from NikoKit.NikoStd.NKTime import NKDate, NKDatetime
import os.path as p

STD_IN = "STD_IN"
STD_OUT = "STD_OUT"
STD_ERR = "STD_ERR"


class NKLog(NKPrintableMixin):
    def __init__(self, log_datetime_str=None, log_context=None, log_type=None):
        super(NKLog, self).__init__()
        self.log_datetime_str = log_datetime_str
        self.log_context = log_context
        self.log_type = log_type


class NKLoggerBuffer:
    def __init__(self, logger, log_type, *args, **kwargs):
        super(NKLoggerBuffer, self).__init__(*args, **kwargs)
        self.logger = logger
        self.log_type = log_type

    def write(self, message):
        now_datetime_str = NKDatetime.datetime_to_str(NKDatetime.now())
        datetime_log = None

        if now_datetime_str not in self.logger.logged_datetime_hints[self.log_type]:
            datetime_log = NKLog(log_datetime_str=now_datetime_str,
                                 log_context=now_datetime_str + "\n",
                                 log_type=self.log_type)
            self.logger.logs.append(datetime_log)
            self.logger.logged_datetime_hints[self.log_type].add(now_datetime_str)

        new_log = NKLog(log_datetime_str=now_datetime_str, log_context=message, log_type=self.log_type)
        self.logger.logs.append(new_log)

        try:
            self.logger.default_terminals[self.log_type].write(message)
        except:
            pass

        try:
            file_path = self.logger.log_file_paths[self.log_type]
            if file_path:
                NKFileSystem.scout(file_path)
                with open(file_path, "a") as f:
                    if datetime_log:
                        f.write(datetime_log.log_context)
                    if new_log:
                        f.write(new_log.log_context)
        except:
            pass

    def flush(self):
        try:
            self.logger.default_terminals[self.log_type].flush()
        except:
            pass


class NKLogger:
    def __init__(self, log_dir):
        self.logs = []
        self.logged_datetime_hints = {
            STD_OUT: set(),
            STD_ERR: set(),
        }

        self.default_terminals = {
            STD_OUT: sys.stdout,
            STD_ERR: sys.stderr,
        }

        if log_dir:
            NKFileSystem.scout(log_dir)
            today_str = NKDate.date_to_str(NKDate.now())
            self.log_file_paths = {
                STD_OUT: p.join(log_dir, "%s_%s.log" % (today_str, STD_OUT)),
                STD_ERR: p.join(log_dir, "%s_%s.log" % (today_str, STD_ERR)),
            }
        else:
            self.log_file_paths = {
                STD_OUT: None,
                STD_ERR: None,
            }

        self.custom_buffers = {
            STD_OUT: NKLoggerBuffer(self, STD_OUT),
            STD_ERR: NKLoggerBuffer(self, STD_ERR),
        }

        sys.stdout = self.custom_buffers[STD_OUT]
        sys.stderr = self.custom_buffers[STD_ERR]
