import os
import os.path as p

from NikoKit.NikoStd import NKConst, NKLaunch

from NikoKit.NikoLib.NKFileSystem import boom_dir


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

    NKRoboCopy.mirror_with_exclusion(string Source-dir,
                                     string Copy-to-dir,
                                     list<str> excludes,  # Relative files or dirs
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
    def mirror_with_exclusion(source_dir, target_dir, excludes, silent_mode=True):
        # Normalize Path
        source_dir = p.abspath(source_dir)
        target_dir = p.abspath(target_dir)

        # Boom it
        boom_dir(target_dir)
        os.makedirs(target_dir, exist_ok=True)

        # Prevent infinite loop if target_dir is inside source_dir
        excludes.append(target_dir)

        exclude_files = []
        exclude_dirs = []

        for rel_path in excludes:
            abs_path = rel_path
            if not p.isabs(rel_path):
                abs_path = p.abspath(p.join(source_dir, rel_path))

            if p.exists(abs_path):
                if p.isdir(abs_path):
                    exclude_dirs.append(abs_path)
                else:
                    exclude_files.append(abs_path)
            else:
                if rel_path.endswith("/") or rel_path.endswith("\\"):
                    exclude_dirs.append(abs_path)
                else:
                    exclude_files.append(abs_path)

        # Construct robocopy command using absolute paths
        command_line = ['robocopy', '/R:0', '/W:0', '/MIR', source_dir, target_dir]

        for d in exclude_dirs:
            command_line += ['/XD', d]
        for f in exclude_files:
            command_line += ['/XF', f]

        # Run
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
