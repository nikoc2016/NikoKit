import os
import os.path as p

from NikoKit.NikoLib.NKFileSystem import NKFile, NKDir
from NikoKit.NikoStd.NKPrintableMixin import NKPrintableMixin


class FSAdapter(NKPrintableMixin):
    def __init__(self, *args, **kwargs):
        super(FSAdapter, self).__init__(*args, **kwargs)

    def get_files(self, url):
        if p.isdir(url):
            file_paths = [p.join(url, f) for f in os.listdir(url) if p.isfile(p.join(url, f))]
            return [NKFile(path=path) for path in file_paths]
        else:
            return []

    def get_folders(self, url):
        if p.isdir(url):
            folder_dirs = [p.join(url, f) for f in os.listdir(url) if p.isdir(p.join(url, f))]
            return [NKDir(directory=directory) for directory in folder_dirs]
        else:
            return []

    def get_all(self, url):
        folders = self.get_folders(url=url)
        files = self.get_files(url=url)
        folders.extend(files)
        return folders
