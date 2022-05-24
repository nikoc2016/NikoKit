import base64
import hashlib
import io
import os
import os.path as p

from NikoKit.NikoStd.NKDataStructure import NKDataStructure


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_base64_from_file(file_path):
    try:
        return base64.encodebytes(open(file_path, "rb").read())
    except:
        return base64.encodestring(open(file_path, "rb").read())


def get_file_from_base64(base_64):
    try:
        return io.BytesIO(base_64)
    except:
        return io.StringIO(base64.decodestring(base_64))


def scout(*target_paths):
    for target_path in target_paths:
        target_path = p.normpath(target_path)
        if p.splitext(target_path)[1]:
            target_dir = p.dirname(target_path)
        else:
            target_dir = target_path
        try:
            os.makedirs(target_dir)
        except:
            pass


class NKFile(NKDataStructure):
    def __init__(self,
                 path=None,
                 at=None,
                 ct=None,
                 byte=None,
                 *args,
                 **kwargs):
        self.path = path
        if at is None:
            try:
                self.at = p.getatime(path)
            except:
                pass
        else:
            self.at = at

        if ct is None:
            try:
                self.ct = p.getctime(path)
            except:
                pass
        else:
            self.ct = ct

        if byte is None:
            try:
                self.byte = p.getsize(path)
            except:
                pass
        else:
            self.byte = byte

        super(NKFile, self).__init__(*args, **kwargs)

    def p_key(self):
        return self.path

    def file_name(self):
        return p.splitext(self.file_name_full())[0]

    def file_ext(self):
        return p.splitext(self.file_name_full())[1]

    def file_name_full(self):
        return p.basename(self.path)


class NKDir(NKDataStructure):
    def __init__(self,
                 directory=None,
                 at=None,
                 ct=None,
                 *args,
                 **kwargs):
        self.directory = directory
        if at is None:
            try:
                self.at = p.getatime(directory)
            except:
                pass
        else:
            self.at = at

        if ct is None:
            try:
                self.ct = p.getctime(directory)
            except:
                pass
        else:
            self.ct = ct

        super(NKDir, self).__init__(*args, **kwargs)

    def p_key(self):
        return self.directory

    def dir_name(self):
        return p.basename(self.directory)
