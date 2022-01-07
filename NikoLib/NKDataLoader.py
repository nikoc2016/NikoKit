import traceback

from NikoKit.NikoLib.NKAppDataManager import NKAppDataMixin
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
                     load_func=None,
                     reload_func=None,
                     clear_func=None,
                     status=None,
                     updated_datetime=None,
                     enabled=True,
                     auto_load=False,
                     auto_reload=False,
                     auto_reload_timeout_sec=60):
            self.name = name
            self.label = label
            self.load_func = load_func
            self.reload_func = reload_func
            self.clear_func = clear_func
            self.status = status
            if not self.status:
                self.status = NKDataLoader.UNLOAD
            self.updated_datetime = updated_datetime
            self.enabled = enabled
            self.auto_load = auto_load
            self.auto_reload = auto_reload
            self.auto_reload_current_sec = 0
            self.auto_reload_timeout_sec = auto_reload_timeout_sec

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

        def not_busy(self):
            if self.status not in (NKDataLoader.LOADING,
                                   NKDataLoader.UPDATING,
                                   NKDataLoader.CLEARING):
                return True
            return False

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

        def load(self):
            messages = []
            if self.not_busy():
                try:
                    self.load_func(self)
                except Exception as e:
                    messages.append(str(e))
                    messages.append(traceback.format_exc())
            return messages

        def reload(self):
            messages = []
            if self.not_busy():
                try:
                    self.reload_func(self)
                except Exception as e:
                    messages.append(str(e))
                    messages.append(traceback.format_exc())
            return messages

        def clear(self):
            messages = []
            if self.not_busy():
                try:
                    self.clear_func(self)
                except Exception as e:
                    messages.append(str(e))
                    messages.append(traceback.format_exc())
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
        self.auto_load_errors = []

    def slot_second_elapsed(self):
        for data_load_name, data_load in self.data_loads.items():
            auto_load_error = data_load.check()
            self.auto_load_errors.extend(auto_load_error)

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
