import hashlib
import os
import os.path as p


def get_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def scout(path):
    path = p.normpath(path)
    if p.splitext(path)[1]:
        target_dir = p.dirname(path)
    else:
        target_dir = path
    try:
        os.makedirs(target_dir)
    except:
        pass
