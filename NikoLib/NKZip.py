import os
import os.path as p
import uuid
from NikoKit.NikoStd import NKLaunch
from NikoKit.NikoStd.NKDataStructure import NKDataStructure

PATH_7ZA_EXE = p.normpath(p.join(p.dirname(__file__), "bin", "7za.exe"))


class CompressProcess(NKDataStructure):
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

    def __init__(self, compress_id="", popen_proc_obj=None, std_out=None, std_err=None, *args, **kwargs):
        super(CompressProcess, self).__init__(*args, **kwargs)
        self.compress_id = compress_id
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
    # Recommend: Use this only when is_finished triggered
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
            line = line.decode()
            if line != os.linesep:
                self.std_out.append(line.replace(os.linesep, ""))

    def cache_std_err(self):
        lines = self.popen_proc_obj.stderr.readlines()
        for line in lines:
            line = line.decode()
            if line != os.linesep:
                self.std_err.append(line.replace(os.linesep, ""))

    def p_key(self):
        return self.compress_id


def compress(compress_target, zip_path, zip_type="7z", password="", hide_names=True):
    """
    Args:
        compress_target: File or Folder path
        zip_path: the .zip that will be created
        zip_type: zip, rar, 7z(Default)
        password: zip password
        hide_names: only works with 7z

    Returns:
        CompressProcess object
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
        CompressProcess object
    """
    command = ["x", zip_path]
    if password:
        command.append("-p" + str(password))
    command.extend(["-y", "-o" + extract_dir])

    return free_7z_command(command)


def free_7z_command(parameter_list):
    """
    Args:
        parameter_list: ex. ["x", "C:\a.exe", "-p123", "C:\a_Folder"]

    Returns:
        CompressProcess object
    """
    if not isinstance(parameter_list, list):
        raise Exception("Parameters must be a list")
    command = [PATH_7ZA_EXE] + parameter_list
    popen_process = NKLaunch.run_pipe(command=command)
    return CompressProcess(compress_id=str(uuid.uuid4()), popen_proc_obj=popen_process)


# cp = compress(compress_target=r"D:\NKZipTest\toPack", zip_path=r"D:\NKZipTest\a.7z", password="123")
# while not cp.is_finished():
#     time.sleep(1)
# print(cp.info())
#
# ep = extract(zip_path=r"D:\NKZipTest\a.7z", extract_dir=r"D:\NKZipTest\extracted", password="123")
# while not ep.is_finished():
#     time.sleep(1)
# print(ep.info())
