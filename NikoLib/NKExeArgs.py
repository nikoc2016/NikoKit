import os
import sys
import os.path as p

from NikoKit.NikoLib.NKFileSystem import get_exe_info
from NikoKit.NikoLib.NKLogger import NKLogger
from NikoKit.NikoStd.NKTime import NKDatetime


class ExeRuntime:
    compiled = None
    my_dir = None
    my_file_name = None
    my_file_ext = None
    logger = None


def main():
    ExeRuntime.compiled, ExeRuntime.my_dir, ExeRuntime.my_file_name, ExeRuntime.my_file_ext = get_exe_info(__file__)
    ExeRuntime.logger = NKLogger(log_dir=p.join(ExeRuntime.my_dir, ExeRuntime.my_file_name + "_LOGS"))
    print(f"NKExeArgs {NKDatetime.datetime_to_str(NKDatetime.now())}\n"
          f"Args:{sys.argv}\n"
          f"Compiled:{ExeRuntime.compiled}\n"
          f"Dir:{ExeRuntime.my_dir}\n"
          f"File:{ExeRuntime.my_file_name + ExeRuntime.my_file_ext}")
    os.system("pause>nul")


if __name__ == "__main__":
    main()
