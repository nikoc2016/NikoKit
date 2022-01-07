import base64
import hashlib
import io
import os
import os.path as p


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
