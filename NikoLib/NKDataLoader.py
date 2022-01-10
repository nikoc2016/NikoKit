import datetime
import traceback

from NikoKit.NikoLib.NKAppDataManager import NKAppDataMixin
from NikoKit.NikoStd import NKTime
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class NKDataLoader(NKAppDataMixin, NKPrintableMixin):
    UNLOAD = "UNLOAD"
    LOADING = "LOADING"
    UPDATING = "UPDATING"
    CLEARING = "CLEARING"
    LOADED = "LOADED"
    LOAD_ERROR = "LOAD_ERROR"

    class DataLoad:
        def __init__(self,
                     name,
                     label,
                     loader=None,
                     reloader=None,
                     dumper=None,
                     status=None,
                     updated_datetime=None,
                     enabled=True,
                     auto_load=False,
                     auto_reload=False,
                     auto_reload_timeout_sec=60,
                     logs=None):
            self.name = name
            self.label = label
            self.loader = loader
            self.reloader = reloader
            self.dumper = dumper
            self.status = status
            if not self.status:
                self.status = NKDataLoader.UNLOAD
            self.updated_datetime = updated_datetime
            self.enabled = enabled
            self.auto_load = auto_load
            self.auto_reload = auto_reload
            self.auto_reload_current_sec = 0
            self.auto_reload_timeout_sec = auto_reload_timeout_sec
            self.logs = logs
            if not logs:
                self.logs = []

        def set_unload(self):
            self.status = NKDataLoader.UNLOAD

        def set_loading(self):
            self.status = NKDataLoader.LOADING

        def set_updating(self):
            self.status = NKDataLoader.UPDATING

        def set_clearing(self):
            self.status = NKDataLoader.CLEARING

        def set_loaded(self):
            self.status = NKDataLoader.LOADED

        def set_load_error(self):
            self.status = NKDataLoader.LOAD_ERROR

        def log_message(self, messages):
            if messages is None:
                return
            elif isinstance(messages, str):
                self.logs.append(NKTime.NKDatetime.datetime_to_str(datetime.datetime.now()) + " " + str(messages))
            elif isinstance(messages, list):
                for message in messages:
                    self.logs.append(NKTime.NKDatetime.datetime_to_str(datetime.datetime.now()) + " " + str(message))

        def execute_callbacks(self, callback):
            messages = []
            try:
                callback_message = callback(self)
                if callback_message:
                    messages.extend(callback_message)
            except Exception as e:
                messages.append(str(e))
                messages.append(traceback.format_exc())
                self.set_load_error()

            self.log_message(messages)
            return messages

        def load(self):
            return self.execute_callbacks(self.loader)

        def reload(self):
            return self.execute_callbacks(self.reloader)

        def clear(self):
            return self.execute_callbacks(self.dumper)

        def check(self):
            messages = []
            if self.status != NKDataLoader.LOADED and self.auto_load:
                results = self.load()
                messages.extend(results)
            else:
                self.auto_reload_current_sec += 1
                if self.auto_reload_timeout_sec <= self.auto_reload_current_sec:
                    self.auto_reload_current_sec = 0
                    if self.status == NKDataLoader.LOADED and self.auto_reload:
                        results = self.reload()
                        messages.extend(results)
            return messages

        def get_pref(self):
            return {
                "auto_load": self.auto_load,
                "auto_reload": self.auto_reload,
                "auto_reload_timeout_sec": self.auto_reload_timeout_sec,
            }

        def set_pref(self, pref):
            self.auto_load = pref["auto_load"]
            self.auto_reload = pref["auto_reload"]
            self.auto_reload_timeout_sec = pref["auto_reload_timeout_sec"]

    def __init__(self, appdata_mgr, appdata_name="NKDataLoader", *args, **kwargs):
        super(NKDataLoader, self).__init__(appdata_mgr=appdata_mgr, appdata_name=appdata_name, *args, **kwargs)
        self.data_loads = {}
        self.logs = []

    def slot_second_elapsed(self):
        for data_load_name, data_load in self.data_loads.items():
            messages = data_load.check()
            self.logs.extend(messages)

    def add_data_load(self, data_load, skip_appdata_load=False):
        self.data_loads[data_load.name] = data_load
        if not skip_appdata_load:
            self.apply_appdata(self.load_appdata())

    def add_data_loads(self, data_loads):
        for data_load in data_loads:
            self.add_data_load(data_load, skip_appdata_load=True)
        self.apply_appdata(self.load_appdata())

    def set_data_load_enabled(self, name, enabled):
        self.data_loads[name].enabled = enabled

    def remove_data_load(self, name):
        del self.data_loads[name]

    def remove_data_loads(self, names):
        for name in names:
            self.remove_data_load(name)

    def clear_data_loads(self):
        self.data_loads = {}

    def extract_appdata(self):
        appdata = self.new_appdata()
        for name in self.data_loads.keys():
            appdata[name] = self.data_loads[name].get_pref()
        return appdata

    def apply_appdata(self, appdata):
        for name in appdata.keys():
            try:
                self.data_loads[name].set_pref(appdata[name])
            except:
                pass
