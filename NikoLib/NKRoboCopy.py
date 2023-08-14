import os
import os.path as p

from NikoKit.NikoStd import NKConst, NKLaunch


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
    def copy_file_to_dir(source_path, target_dir, silent_mode=True):
        # Parse path
        file_name = os.path.basename(source_path)
        file_dir = os.path.dirname(source_path)

        # Run Command
        command_line = ['robocopy', '/R:0', '/W:0', file_dir, target_dir, file_name]
        process = NKLaunch.run_pipe(command_line)
        error_message = NKRoboCopy.handle_stdout(process=process, silent_mode=silent_mode)

        return error_message

    @staticmethod
    def copy_dir_to_dir(source_dir, target_dir, except_dirs=None, silent_mode=True):
        if not p.isdir(source_dir):
            print(f"NKRoboCopy::Source dir not exists({source_dir})")

        # Run Command
        command_line = ['robocopy', '/R:0', '/W:0', '/E', source_dir, target_dir]
        if isinstance(except_dirs, list) and len(except_dirs) > 0:
            command_line.append(r"/XD")
            for except_dir in except_dirs:
                command_line.append(except_dir)
        process = NKLaunch.run_pipe(command_line)
        error_message = NKRoboCopy.handle_stdout(process=process, silent_mode=silent_mode)
        print(error_message)

        return error_message

    @staticmethod
    def mirror_dir_to_dir(source_dir, target_dir, silent_mode=True):
        if not p.isdir(source_dir):
            print(f"NKRoboCopy::Source dir not exists({source_dir})")

        # Run Command
        command_line = ['robocopy', '/R:0', '/W:0', '/MIR', source_dir, target_dir]
        process = NKLaunch.run_pipe(command_line)
        error_message = NKRoboCopy.handle_stdout(process=process, silent_mode=silent_mode)

        return error_message

    @staticmethod
    def handle_stdout(process, silent_mode=True):
        magic_number = 0
        error_message = ""

        while process.poll() is None:
            new_line = process.stdout.readline().decode(NKConst.SYS_CHARSET)
            if "----" in new_line:
                magic_number += 1

            elif not silent_mode and magic_number >= 4:
                print(new_line[0:-1])

            # Error Storage
            if u"错误" in new_line or "error" in new_line:
                error_message += new_line

        return error_message
