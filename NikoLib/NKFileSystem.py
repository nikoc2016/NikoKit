import base64
import errno
import hashlib
import io
import json
import os
import os.path as p
import shutil
import sys
import tempfile

import psutil

from NikoKit.NikoStd.NKDataStructure import NKDataStructure


class NKHDLock:
    lock_handles = {}
    lock_dir = p.join(tempfile.gettempdir(), "NKHDLock")
    lock_ext = ".lock"

    @classmethod
    def lock(cls, lock_name):
        if not cls.is_locked(lock_name):
            scout(cls.lock_dir)
            lock_handle = open(p.join(cls.lock_dir, lock_name + cls.lock_ext), "w")
            cls.lock_handles[lock_name] = lock_handle
            return True
        return False

    @classmethod
    def unlock(cls, lock_name):
        if lock_name in cls.lock_handles:
            cls.lock_handles[lock_name].close()
            return True
        return False

    @classmethod
    def is_locked(cls, lock_name):
        try:
            os.remove(p.join(cls.lock_dir, lock_name + cls.lock_ext))
            return False
        except OSError as e:
            if e.errno != errno.ENOENT:
                return True


# Call with __file__ and it will work
def get_exe_info(entry_py_path):
    # Get Exe or Py Info
    if getattr(sys, 'frozen', False):
        compiled = True
        my_dir = p.dirname(sys.executable)
        my_file_name = p.splitext(p.basename(sys.executable))[0]
        my_file_ext = p.splitext(p.basename(sys.executable))[1]
    else:
        compiled = False
        my_dir = p.dirname(p.abspath(entry_py_path))
        my_file_name = p.splitext(p.basename(entry_py_path))[0]
        my_file_ext = p.splitext(p.basename(entry_py_path))[1]

    return compiled, my_dir, my_file_name, my_file_ext


def is_proc_running(process_name):
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False



def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Encode a list or dictionary to BASE64
def datastructure_to_base64(data):
    json_str = json.dumps(data, ensure_ascii=False)
    base64_bytes = base64.b64encode(json_str.encode("utf-8"))
    base64_str = base64_bytes.decode("utf-8")
    return base64_str


# Restore BASE64-encoded string to its original form
def base64_to_datastructure(base64_str):
    base64_bytes = base64_str.encode("utf-8")
    json_bytes = base64.b64decode(base64_bytes)
    json_str = json_bytes.decode("utf-8")
    data = json.loads(json_str)
    return data


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


def write_file_from_base64(file_path, base_64):
    try:
        os.makedirs(p.dirname(file_path))
    except:
        pass

    try:
        os.remove(file_path)
    except:
        pass

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base_64))


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


def delete_try(url):
    try:
        os.remove(url)
    except:
        pass

    try:
        boom_dir(url)
    except:
        pass


def boom_dir(target_dir, remove_root=True):
    if not p.isdir(target_dir):
        return True
    is_empty_folder = True
    if target_dir[-1] == os.sep:
        target_dir = target_dir[:-1]

    files = os.listdir(target_dir)
    for file in files:
        if file == '.' or file == '..':
            continue
        path = os.path.join(target_dir, file)
        if os.path.isdir(path):
            is_empty_recursive_child = boom_dir(path)
            if not is_empty_recursive_child:
                is_empty_folder = False
        else:
            try:
                os.remove(path)
            except Exception as e:
                is_empty_folder = False
    if is_empty_folder and remove_root:
        os.rmdir(target_dir)
    return is_empty_folder


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
                if not isinstance(self.byte, int):
                    self.byte = -1
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

    def dir_url(self):
        return p.dirname(self.path)


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
