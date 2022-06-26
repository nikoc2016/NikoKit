import os
import os.path as p
import tempfile
import time
import uuid
from time import sleep

from NikoKit.NikoLib import NKFileSystem
from NikoKit.NikoStd import NKLaunch, NKConst
from NikoKit.NikoStd.NKDataStructure import NKDataStructure
from NikoKit.NikoLib.bin import bin_7z

PATH_7ZA_EXE = "7z"
PATH_7ZA_DLL = "7z"


def prepare_7z_binaries(extract_dir=None):
    global PATH_7ZA_EXE
    global PATH_7ZA_DLL
    if not extract_dir:
        extract_dir = tempfile.gettempdir()
    PATH_7ZA_EXE = p.normpath(p.join(extract_dir, "7z.exe"))
    PATH_7ZA_DLL = p.normpath(p.join(extract_dir, "7z.dll"))
    try:
        NKFileSystem.write_file_from_base64(file_path=PATH_7ZA_EXE, base_64=bin_7z.res["7z.exe"])
    except Exception as e:
        print("7z.exe write failure, is it in use? [%s]" % e)
    try:
        NKFileSystem.write_file_from_base64(file_path=PATH_7ZA_DLL, base_64=bin_7z.res["7z.dll"])
    except Exception as e:
        print("7z.dll write failure, is it in use? [%s]" % e)


def compress(compress_target, zip_path, zip_type="7z", password="", hide_names=True):
    """
    Args:
        compress_target: File or Folder path
        zip_path: the .zip that will be created
        zip_type: zip, rar, 7z(Default)
        password: zip password
        hide_names: only works with 7z

    Returns:
        SevenZipProcess object
    """
    command = ["a", zip_path, "-t" + str(zip_type)]
    if password:
        command.append("-p" + str(password))
        if zip_type == "7z" and hide_names:
            command.append("-mhe=on")
    command.append(compress_target)

    return free_7z_command(command)


def extract(zip_path, extract_dir, password=""):
    """
    Args:
        zip_path: The extract target zip
        extract_dir: the folder which files extract to
        password: zip password

    Returns:
        SevenZipProcess object
    """
    command = ["x", zip_path]
    if password:
        command.append("-p" + str(password))
    command.extend(["-y", "-o" + extract_dir])

    return free_7z_command(command)


def extract_try(zip_path, extract_dir, password_list=None, password_generator=None):
    """
    Args:
        zip_path:           The extract target zip
        extract_dir:        The folder which files extract to
        password_list:      str password OR list<str> password
        password_generator: def generator(zip_file_path) -> list OR str

    Returns:
        SevenZipProcess, None: (Success OR Fail) task, NO password found
        None, None:            (Encrypted)       task, NO password found
        SevenZipProcess, str:  (Success OR Fail) task,    password found

    SYNC LAG WARNING
        This function will RETURN when extraction is FINISHED.
        Advance: Use this in a thread
    """
    if not is_encrypted(zip_path):
        extract_process = extract(zip_path=zip_path, extract_dir=extract_dir)
        while not extract_process.is_finished():
            pass
        extract_process.info()
        return extract_process, None

    brute_force_list = []
    if isinstance(password_list, list):
        brute_force_list.extend(password_list)
    elif isinstance(password_list, str):
        brute_force_list.append(password_list)
    if callable(password_generator):
        generated_password = password_generator(zip_path)
        if isinstance(generated_password, list):
            brute_force_list.extend(generated_password)
        elif isinstance(generated_password, str):
            brute_force_list.append(generated_password)

    for try_password in brute_force_list:
        extract_process = extract(zip_path=zip_path, extract_dir=extract_dir, password=try_password)
        while not extract_process.is_finished():
            pass

        wrong_password = False
        for line in extract_process.info()["std_err"]:
            if "Wrong password" in line:
                wrong_password = True
                break

        if not wrong_password:
            return extract_process, try_password

    return None, None


def is_encrypted(zip_path):
    check_process = free_7z_command(["l", "-slt", zip_path, "-p" + str(uuid.uuid4())])
    while not check_process.is_finished():
        pass

    encrypted = False
    check_process.info()
    for line in check_process.std_out:
        if line == "Encrypted = +":
            encrypted = True
            break
    for line in check_process.std_err:
        if "Wrong password" in line:
            encrypted = True
            break
    return encrypted


def free_7z_command(parameter_list):
    """
    Args:
        parameter_list: ex. ["x", "C:\a.exe", "-p123", "C:\a_Folder"]

    Returns:
        SevenZipProcess object
    """
    if not isinstance(parameter_list, list):
        raise Exception("Parameters must be a list")
    command = [PATH_7ZA_EXE] + parameter_list
    popen_process = NKLaunch.run_pipe(command=command)
    return SevenZipProcess(transaction_id=str(uuid.uuid4()), popen_proc_obj=popen_process)


class SevenZipProcess(NKDataStructure):
    """
    Features:
        Manage compress process and provide functions to check status

    Members:
        compress_id               A uuid represent a compress transaction
        popen_proc_obj            A popen process object
        std_out                   A custom stdout cache list, Default=None
        std_err                   A custom stderr cache list, Default=None

    APIs:
        is_finished()             Boolean
        is_finished_properly()    Boolean
        return_code()             int or None(When still running)
        info()                    {"std_out": [Lines], "std_err": [Lines]}
    """

    def __init__(self, transaction_id="", popen_proc_obj=None, std_out=None, std_err=None, *args, **kwargs):
        super(SevenZipProcess, self).__init__(*args, **kwargs)
        self.transaction_id = transaction_id
        self.popen_proc_obj = popen_proc_obj
        if std_out:
            self.std_out = std_out
        else:
            self.std_out = []
        if std_err:
            self.std_err = std_err
        else:
            self.std_err = []

    def is_finished(self):
        return self.popen_proc_obj.poll() is not None

    def is_finished_properly(self):
        return self.popen_proc_obj.poll() == 0

    def return_code(self):
        return self.popen_proc_obj.poll()

    # SYNC LAG WARNING
    # Recommend: Use this only when is_finished() triggered
    # Advance: Use this in a thread
    def info(self):
        self.cache_std_out()
        self.cache_std_err()
        return {
            "std_out": self.std_out[:],
            "std_err": self.std_err[:],
            "return_code": self.return_code()
        }

    def cache_std_out(self):
        lines = self.popen_proc_obj.stdout.readlines()
        for line in lines:
            try:
                line = line.decode()
            except:
                line = line.decode(NKConst.SYS_CHARSET)

            if line != os.linesep:
                line = line.replace(os.linesep, "")
                self.std_out.append(line)

    def cache_std_err(self):
        lines = self.popen_proc_obj.stderr.readlines()
        for line in lines:
            try:
                line = line.decode()
            except:
                line = line.decode(NKConst.SYS_CHARSET)
            if line != os.linesep:
                line = line.replace(os.linesep, "")
                self.std_err.append(line)

    def p_key(self):
        return self.transaction_id


# EXTRACTING EXE TO TEMP, NO NEED IF `7Z` IS OS COMMAND ALREADY
# prepare_7z_binaries()

# cp = compress(compress_target=r"D:\NKZipTest\toPack", zip_path=r"D:\NKZipTest\a.7z", password="123")
# while not cp.is_finished():
#     time.sleep(1)
# print(cp.info())


# ep = extract(zip_path=r"D:\NKZipTest\a.7z", extract_dir=r"D:\NKZipTest\extracted", password="123")
# while not ep.is_finished():
#     time.sleep(1)
# print(ep.info())


# def interesting(file_name):
#     return ["abc", "123"]
#
#
# ep, password = extract_try(zip_path=r"D:\NKZipTest\plain.rar",
#                            extract_dir=r"D:\NKZipTest\extracted",
#                            password_list=["124", "155"],
#                            password_generator=interesting)
# print(password)


# result = free_7z_command(["x", r"D:\NKZipTest\big_123.7z", "-p12345"])
# while not result.is_finished():
#     time.sleep(1)
# print(result.info())
