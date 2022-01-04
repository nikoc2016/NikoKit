import json
import os
import os.path as p

from NikoKit.NikoStd.NKPrintableClass import NKPrintableClass
from NikoKit.NikoLib.NKFileSystem import scout


class NKAppDataManager(NKPrintableClass):
    def __init__(self, appdata_root):
        self.appdata_root = appdata_root
        self.appdata_objects = {}
        self.appdata_ext = ".nkappdata"

    def get(self, appdata_name):
        if appdata_name in self.appdata_objects.keys():
            return self.appdata_objects[appdata_name]
        else:
            return None

    def set(self, appdata_name, appdata_object):
        self.appdata_objects[appdata_name] = appdata_object

    def save(self, appdata_name):
        appdata_path = p.join(self.appdata_root, appdata_name + self.appdata_ext)
        scout(appdata_path)
        with open(appdata_path, "w", encoding="utf-8") as f:
            json.dump(self.appdata_objects[appdata_name], f, ensure_ascii=False)

    def load(self, appdata_name):
        appdata_path = p.join(self.appdata_root, appdata_name + self.appdata_ext)
        scout(appdata_path)
        with open(appdata_path, "r", encoding="utf-8") as f:
            self.appdata_objects[appdata_name] = json.load(f)

    def save_all(self):
        for appdata_name in self.appdata_objects.keys():
            self.save(appdata_name)

    def load_all(self):
        scout(self.appdata_root)
        for appdata_filename in os.listdir(self.appdata_root):
            if p.splitext(appdata_filename)[1] == self.appdata_ext and p.isfile(p.join(self.appdata_root,
                                                                                       appdata_filename)):
                self.load(appdata_name=p.splitext(appdata_filename)[0])
