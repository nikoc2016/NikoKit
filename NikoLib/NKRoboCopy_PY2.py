# encoding=utf-8
import os
import subprocess

from NikoKit.NikoStd import NKConst


class NKRoboCopy:
    """
    NKRoboCopy.copy_file_to_dir(string Path-of-file,
                                string Copy-to-dir,
                                bool print_result)

    NKRoboCopy.copy_dir_to_dir(string Source-dir,
                               string Copy-to-dir,
                               bool print_result)

    NKRoboCopy.mirror_dir_to_dir(string Source-dir,
                                 string Copy-to-dir,
                                 bool print_result)

    If copy OK,  return str = ""
    If copy BAD, return str = "error detail"
    """

    @staticmethod
    def copy_file_to_dir(source_path, target_dir, print_result=False, default_shell=False):
        # Parse path
        file_name = os.path.basename(source_path)
        file_dir = os.path.dirname(source_path)

        # Run Command
        command_line = 'robocopy "%s" "%s" "%s"' % (file_dir, target_dir, file_name)
        ps = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=default_shell,
                              stderr=subprocess.STDOUT)
        error_message = NKRoboCopy.handle_stdout(ps, print_result)

        return error_message

    @staticmethod
    def copy_dir_to_dir(source_dir, target_dir, print_result=False, default_shell=False):
        if not os.path.isdir(source_dir):
            return "GCOPY::source dir not exists(%s)" % (source_dir,)

        # Run Command
        command_line = 'robocopy /E "%s" "%s" ' % (source_dir, target_dir)
        ps = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=default_shell,
                              stderr=subprocess.STDOUT)
        error_message = NKRoboCopy.handle_stdout(ps, print_result)

        return error_message

    @staticmethod
    def mirror_dir_to_dir(source_dir, target_dir, print_result=False, default_shell=False):
        if not os.path.isdir(source_dir):
            return "GCOPY::source dir not exists(%s)" % (source_dir,)

        # Run Command
        command_line = 'robocopy /MIR "%s" "%s" ' % (source_dir, target_dir)
        ps = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=default_shell,
                              stderr=subprocess.STDOUT)
        error_message = NKRoboCopy.handle_stdout(ps, print_result)

        return error_message

    @staticmethod
    def handle_stdout(stdout_obj, print_result):
        magic_number = 0
        error_message = ""

        while True:
            data = stdout_obj.stdout.readline()
            if data == b'':
                if stdout_obj.poll() is not None:
                    break
            else:
                data_decoded = data.decode(NKConst.SYS_CHARSET)

                # Printing Optimizing
                if "----" in data_decoded:
                    magic_number += 1

                elif print_result and magic_number >= 4:
                    print(data_decoded[0:-1])

                # Error Storage
                if u"错误" in data_decoded or "error" in data_decoded:
                    error_message = data_decoded

        return error_message
