import os
import subprocess
import tempfile
import os.path as p
from uuid import uuid4

from NikoKit.NikoLib import NKFileSystem
from NikoKit.NikoStd import NKConst

# Copy from win32con
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_NORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_MAXIMIZE = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
SW_FORCEMINIMIZE = 11
SW_MAX = 11

DISPLAY_MODE_HIDE = SW_HIDE
DISPLAY_MODE_NORMAL = SW_SHOWNORMAL
DISPLAY_MODE_MINIMIZED = SW_MINIMIZE
DISPLAY_MODE_MAXIMIZE = SW_MAXIMIZE


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
    si.dwFlags = subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = display_mode

    if not custom_env:
        custom_env = {}

    return subprocess.Popen(command,
                            startupinfo=si,
                            creationflags=subprocess.CREATE_NEW_CONSOLE,
                            env={**os.environ, **custom_env},
                            cwd=cwd
                            )


def run_system(command, pause=False):
    """
    You can *NOT* manipulate subprocess with this method
    The child process is launched as SYSTEM process
    Use only when normal run() won't work

    Args:
        command: Command String that executes in cmd.exe
        pause: Pausing the script in the end

    Returns:
            subprocess.Popen()
    """

    target_dir = p.join(tempfile.gettempdir(), "NKLaunchProxy")
    NKFileSystem.delete_try(target_dir)
    NKFileSystem.scout(target_dir)
    bat_path = p.join(target_dir, str(uuid4()) + ".bat")

    # Convert List To String
    if isinstance(command, list):
        segments = []
        for segment in command:
            if " " in segment:
                segments.append(f'"{segment}"')
            else:
                segments.append(segment)
        command = " ".join(segments)
    else:
        command = str(command)

    if pause:
        command += "\npause"

    # Write to Bat
    with open(bat_path, "w") as f:
        f.write(f"@echo off\n" + command)
        run(command=["explorer.exe", bat_path])


def run_system_sequential(commands, pause=False):
    """
    You can *NOT* manipulate subprocess with this method
    The child process is launched as SYSTEM process
    Use only when normal run() won't work

    Args:
        commands: Multiple or single lines that will execute in cmd.exe
        pause: Pausing the script in the end

    Returns:
            subprocess.Popen()
    """
    target_dir = p.join(tempfile.gettempdir(), "NKLaunchProxy")
    NKFileSystem.delete_try(target_dir)
    NKFileSystem.scout(target_dir)
    bat_path = p.join(target_dir, str(uuid4()) + ".bat")

    bat_content = "@echo off\n"

    # Convert List To String
    for command in commands:
        if isinstance(command, list):
            segments = []
            for segment in command:
                if " " in segment:
                    segments.append('"' + str(segment) + '"')
                else:
                    segments.append(segment)
            command = " ".join(segments)
            bat_content += command + "\n"
        else:
            bat_content += str(command) + "\n"

    if pause:
        bat_content += "\npause"

    # Write to Bat
    with open(bat_path, "w") as f:
        f.write(bat_content)
        run(command=["explorer.exe", bat_path])


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
        new_line = process.stdout.readline().decode(NKConst.SYS_CHARSET)
        if new_line == "Done":
            continue
        else:
            number = int(new_line)
            print("Progress: " + str(number))
            print("Result: " + str(number + number))

# import os, sys
# from time import sleep
#
# import NKLaunch
#
# NKLaunch.run(command=[r"D:\NKLaunch\TargetCode\exe_console.exe", "-superb"],
#                    cwd=r"D:\NKLaunch\TargetCode",
#                    display_mode=NKLaunch.DISPLAY_MODE_NORMAL,
#                    custom_env={"NKLaunch": "Superb", "NKLaunch2": "Superb2"},
#                    )
#
# NKLaunch.run(command=[r"D:\NKLaunch\TargetCode\exe_gui.exe", "-superb"],
#                    cwd=r"D:\NKLaunch\TargetCode",
#                    display_mode=NKLaunch.DISPLAY_MODE_HIDE,
#                    custom_env={"NKLaunch": "Superb", "NKLaunch2": "Superb2"},
#                    )
#
# NKLaunch.run(...).wait() # Blocking
#
# NKLaunch.run_system([r"D:\NKZipTest\args.exe", "hello", "destination is here"])
#
# process = NKLaunch.run_pipe(
#     command=[r"D:\NKLaunch\TargetCode\exe_counter.exe", "10"],
#     cwd=r"D:\NKLaunch\TargetCode",
#     custom_env={"NKLaunch": "Superb", "NKLaunch2": "Superb2"},
#     )
#
# NKLaunch.example_pipe_handling(process)
# i = 0
# while True:
#     i += 1
#     sleep(1)
