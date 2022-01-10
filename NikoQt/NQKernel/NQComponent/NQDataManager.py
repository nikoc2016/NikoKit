from NikoKit.NikoQt.NQAdapter import *
from NikoKit.NikoQt.NQKernel.NQComponent.NQThread import NQThread


class NQDataManager(QObject):
    thread = None

    # Things To Override
    class LoadThread(NQThread):
        def __init__(self, data_load):
            super(NQDataManager.LoadThread, self).__init__()
            self.data_cache = None
            self.data_load = data_load

    class ReloadThread(LoadThread):
        pass

    class DumpThread(LoadThread):
        pass

    class IncludeCondition:
        pass

    class ExcludeCondition(IncludeCondition):
        pass

    @classmethod
    def get_all(cls):
        return {}

    # Default Functions not required to change
    BUSY = "Thread Busy, Operation Cancelled."

    @classmethod
    def reserve_thread(cls):
        if cls.thread and cls.thread.isFinished():
            cls.thread = None
        if cls.thread is None:
            return True
        else:
            return False

    @classmethod
    def run_thread(cls, data_load, thread_class):
        messages = []
        if cls.reserve_thread():
            cls.thread = thread_class(data_load)
            cls.thread.start()
        return messages

    @classmethod
    def loader(cls, data_load):
        return cls.run_thread(data_load, cls.LoadThread)

    @classmethod
    def reloader(cls, data_load):
        return cls.run_thread(data_load, cls.ReloadThread)

    @classmethod
    def dumper(cls, data_load):
        return cls.run_thread(data_load, cls.DumpThread)

    @classmethod
    def is_loaded(cls):
        return cls.get_all() is None

    @classmethod
    def get(cls, condition):
        all_data_dict = cls.get_all()
        valid_data_dict = {}

        for data_idx, data in all_data_dict.items():
            condition_match = True
            condition_dict = vars(condition)
            for condition_key, condition_value in condition_dict.items():
                if condition_value and data.__dict__[condition_key] != condition_value:
                    condition_match = False
                    break
            if condition_match:
                valid_data_dict[data_idx] = data

        return valid_data_dict

    @classmethod
    def get_by_conditions(cls, conditions):
        valid_data_dict = {}

        for condition in conditions:
            conditional_data_dict = cls.get(condition)
            if isinstance(condition, cls.IncludeCondition):
                valid_data_dict.update(conditional_data_dict)
            elif isinstance(condition, cls.ExcludeCondition):
                for key in conditional_data_dict.keys():
                    del valid_data_dict[key]
            else:
                raise Exception("Unknown Exception Type")

        return valid_data_dict
