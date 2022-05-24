import os
import subprocess
import win32con

DISPLAY_MODE_HIDE = win32con.SW_HIDE
DISPLAY_MODE_NORMAL = win32con.SW_SHOWNORMAL
DISPLAY_MODE_MINIMIZED = win32con.SW_MINIMIZE
DISPLAY_MODE_MAXIMIZE = win32con.SW_MAXIMIZE


def run(command,
        cwd=None,
        display_mode=DISPLAY_MODE_HIDE,
        custom_env=None):
    """

    Args:
        command: Command or EXE path and Args
        cwd: EXE starting directory
        display_mode: Decides how the window is shown
        0 - SW_HIDE
        1 - SW_SHOWNORMAL | SW_NORMAL
        2 - SW_SHOWMINIMIZED
        3 - SW_MAXIMIZE
        custom_env:  Dict overrides sys.environ   ex. {"MAYA_PATH": "C:/Maya"}

    Returns:
            subprocess.Popen()
    """
    si = subprocess.STARTUPINFO()
    si.dwFlags = win32con.STARTF_USESHOWWINDOW
    si.wShowWindow = display_mode

    if not custom_env:
        custom_env = {}

    return subprocess.Popen(command,
                            startupinfo=si,
                            creationflags=subprocess.CREATE_NEW_CONSOLE,
                            env={**os.environ, **custom_env},
                            cwd=cwd
                            )


def run_pipe(command,
             cwd=None,
             custom_env=None):
    """

    Args:
        command: Command or EXE path and Args
        cwd: EXE starting directory
        custom_env:  Dict overrides sys.environ   ex. {"MAYA_PATH": "C:/Maya"}

    Returns:
            subprocess.Popen()
    """

    if not custom_env:
        custom_env = {}

    return subprocess.Popen(command,
                            creationflags=subprocess.CREATE_NO_WINDOW,
                            env={**os.environ, **custom_env},
                            cwd=cwd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )


def example_pipe_handling(process):
    """
    This is a example of how to deal with piping result in real-time

    Args:
        process: subprocess.Process

    Returns:

    """
    while process.poll() is None:
        new_line = process.stdout.readline().decode()
        if new_line == "Done":
            continue
        else:
            number = int(new_line)
            print("Progress: " + str(number))
            print("Result: " + str(number + number))


# import os, sys
# from time import sleep
#
# import LaunchExternal
#
# LaunchExternal.run(command=[r"D:\gvfpipe\experimental\Niko\LaunchExternal\TargetCode\exe_console.exe", "-superb"],
#                    cwd=r"D:\gvfpipe\experimental\Niko\LaunchExternal\TargetCode",
#                    display_mode=LaunchExternal.DISPLAY_MODE_NORMAL,
#                    custom_env={"LaunchExternal": "Superb", "LaunchExternal2": "Superb2"},
#                    )
#
# LaunchExternal.run(command=[r"D:\gvfpipe\experimental\Niko\LaunchExternal\TargetCode\exe_gui.exe", "-superb"],
#                    cwd=r"D:\gvfpipe\experimental\Niko\LaunchExternal\TargetCode",
#                    display_mode=LaunchExternal.DISPLAY_MODE_HIDE,
#                    custom_env={"LaunchExternal": "Superb", "LaunchExternal2": "Superb2"},
#                    )
#
# process = LaunchExternal.run_pipe(
#     command=[r"D:\gvfpipe\experimental\Niko\LaunchExternal\TargetCode\exe_counter.exe", "10"],
#     cwd=r"D:\gvfpipe\experimental\Niko\LaunchExternal\TargetCode",
#     custom_env={"LaunchExternal": "Superb", "LaunchExternal2": "Superb2"},
#     )
#
# LaunchExternal.example_pipe_handling(process)
# i = 0
# while True:
#     i += 1
#     sleep(1)