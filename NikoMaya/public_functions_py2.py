# coding=utf8
# Copyright (c) 2019 GVF
import codecs
import errno
import getpass
import json
import locale
import logging
import os
import re
import sys
import traceback

sys.path.append(r"V:\TD\gvfpipe\utils")
try:
    import _winreg
except:
    import winreg as _winreg
import subprocess
from datetime import datetime
from gvf_globals import task_globals

FFMPEG_EXE = ""
FFPROBE_EXE = ""


def set_ffmpeg_path():
    global FFMPEG_DIR
    global FFMPEG_EXE
    global FFPROBE_EXE
    FFMPEG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core")
    FFMPEG_EXE = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
    FFPROBE_EXE = os.path.join(FFMPEG_DIR, "ffprobe.exe")


FONT_PATH = r"V:TD/gvfpipe/dcc_ops/maya/scripts/playblast_tool/msyhbd.ttc"
logging.basicConfig()
log = logging.getLogger("public_func")


# example_online_status = {
#      'tw_selected_project': None,
#      'tw_username': None,
#      'tw_available_projects': None,
#      'tw_password': None,
#      'last_updated_timestamp':u'2021-01-20 11:28:50'
# }
def get_gml_online_status():
    gml_conn = GMLConnector()
    online_status = {}
    try:
        online_status = gml_conn.get_login_status()
        tw_password = online_status.get("tw_password")
        password = online_status.get("password")
        if not tw_password and password:
            online_status["tw_password"] = password
        if not password and tw_password:
            online_status["password"] = tw_password

    except Exception as e:
        print(e)
        if e == GMLConnector.EXCEPTION_GML_NOT_RUNNING:
            # GML is not running, do something
            pass
        elif e == GMLConnector.EXCEPTION_GML_VERSION_EXPIRED:
            # GML is expired, do something
            pass
    return online_status


def is_rs_project():
    import gvf_globals
    current_project = gvf_globals.task_globals.current_project_env
    project_renderer_config = gvf_globals.proj_renderer
    using_redshift = False
    if current_project in project_renderer_config.keys() and project_renderer_config[current_project] == "RedShift":
        using_redshift = True
    return using_redshift


class GMLConnector(object):
    EXCEPTION_GML_NOT_RUNNING = Exception("GMLConnector Exception::GML is not running")
    EXCEPTION_GML_VERSION_EXPIRED = Exception("GMLConnector Exception::GML version is too low")

    def __init__(self):
        self.mydoc_dir = os.path.join(os.path.expanduser('~'), 'GML-1M') if 'Documents' in os.path.expanduser('~') \
            else os.path.join(os.path.expanduser('~'), 'Documents', 'GML-1M')
        self.mydoc_loginFile_path = os.path.join(self.mydoc_dir, 'login.json')
        self.mydoc_logFile_path = os.path.join(self.mydoc_dir, 'log.txt')
        self.mydoc_loginStatus_path = os.path.join(self.mydoc_dir, 'login_status.json')
        self.mydoc_awakeFile_path = os.path.join(self.mydoc_dir, 'awake.json')
        self.lock_name = "GML.lock"
        self.lock_path = os.path.join(self.mydoc_dir, self.lock_name)

    # Return: Bool
    def is_gml_running(self):
        try:
            try:
                os.makedirs(self.mydoc_dir)
            except:
                pass
            os.remove(self.lock_path)
            return False
        except OSError as e:
            if e.errno != errno.ENOENT:
                return True

    # Example Return Status
    def get_login_status(self):
        if not self.is_gml_running():
            raise GMLConnector.EXCEPTION_GML_NOT_RUNNING
        else:
            try:
                with open(self.mydoc_loginStatus_path, "r") as f:
                    online_status = json.load(f)
                    last_updated_timestamp = datetime.strptime(online_status["last_updated_timestamp"],
                                                               '%Y-%m-%d %H:%M:%S')

                    # if (datetime.now() - last_updated_timestamp).seconds > 15:
                    #     raise GMLConnector.EXCEPTION_GML_VERSION_EXPIRED

                    return online_status
            except:
                raise GMLConnector.EXCEPTION_GML_VERSION_EXPIRED


class GCopy:
    """
    Version: 1.0

    Example:

    GCopy.copy_file_to_dir(string Path-of-file,
                           string Copy-to-dir,
                           bool print_result)

    GCopy.copy_dir_to_dir(string Source-dir,
                          string Copy-to-dir,
                          bool print_result)

    GCopy.mirror_dir_to_dir(string Source-dir,
                            string Copy-to-dir,
                            bool print_result)

    If copy OK,  return str = ""
    If copy BAD, return str = "error detail"
    """

    @staticmethod
    def copy_file_to_dir(source_path, target_dir, print_result=False, default_shell=True):
        # Parse path
        file_name = os.path.basename(source_path)
        file_dir = os.path.dirname(source_path)

        # Run Command
        command_line = 'robocopy "%s" "%s" "%s"' % (file_dir, target_dir, file_name)
        ps = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=default_shell,
                              stderr=subprocess.STDOUT)
        error_message = GCopy.handle_stdout(ps, print_result)

        return error_message

    @staticmethod
    def copy_dir_to_dir(source_dir, target_dir, print_result=False, default_shell=True):
        if not os.path.isdir(source_dir):
            return "GCOPY::source dir not exists(%s)" % (source_dir,)

        # Run Command
        command_line = 'robocopy /E "%s" "%s" ' % (source_dir, target_dir)
        ps = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=default_shell,
                              stderr=subprocess.STDOUT)
        error_message = GCopy.handle_stdout(ps, print_result)

        return error_message

    @staticmethod
    def mirror_dir_to_dir(source_dir, target_dir, print_result=False, default_shell=True):
        if not os.path.isdir(source_dir):
            return "GCOPY::source dir not exists(%s)" % (source_dir,)

        # Run Command
        command_line = 'robocopy /MIR "%s" "%s" ' % (source_dir, target_dir)
        ps = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=default_shell,
                              stderr=subprocess.STDOUT)
        error_message = GCopy.handle_stdout(ps, print_result)

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
                data_decoded = data.decode(codecs.lookup(locale.getpreferredencoding()).name)

                # Printing Optimizing
                if "----" in data_decoded:
                    magic_number += 1

                elif print_result and magic_number >= 4:
                    print(data_decoded[0:-1])

                # Error Storage
                if u"错误" in data_decoded or "error" in data_decoded:
                    error_message = data_decoded

        return error_message


def get_os_one_dir():
    """
    get windows dir
    Returns:list - dir eg:["xxx"]

    """
    from dayu_widgets.qt import QFileDialog

    if sys.platform == "win32":
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        if file_dialog.exec_():
            paths = file_dialog.selectedFiles()
            return paths
    else:
        # TODO
        pass


def scan_file(folder, exclude_folders=None, exclude_files=None, exclude_ext=None, exact_type=None):
    """
    scan folder and return all files
    Args:
        folder: str - windows dir
        exclude_folders: list - folder name
        exclude_files: list - file name
        exclude_ext: list - file ext
    Returns:list - all files eg:["...",""]
    """
    import scandir
    file_path = []
    for root, dirs, files in scandir.walk(folder, topdown=True):
        if exclude_folders:
            dirs[:] = [folder_name for folder_name in dirs if folder_name not in exclude_folders]
        if exclude_files:
            files[:] = [name for name in files if os.path.splitext(name)[0] not in exclude_files]
        if exclude_ext:
            files[:] = [ext for ext in files if os.path.splitext(ext)[-1] not in exclude_ext]
        for file_name in files:
            if exact_type:
                if os.path.splitext(file_name)[-1] == exact_type:
                    file_path.append(os.path.join(root, file_name))
            else:
                file_path.append(os.path.join(root, file_name))
    return file_path


def get_maya_main_window():
    """
    Attach qt widget to maya as mayaMainWindow
    Returns:QtWidget.QWidget - The actual widget associated with maya
    不要再使用这个，请使用下面的get_main_window
    """
    from dayu_widgets.qt import QWidget
    import maya.OpenMayaUI as omui
    try:
        from shiboken2 import wrapInstance
    except ImportError:
        from shiboken import wrapInstance
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(long(maya_main_window_ptr), QWidget)
    return maya_main_window


def get_main_window(engine):
    """
    Attach qt widget to dcc
    Returns:QtWidget.QWidget - The actual widget associated with dcc
    """
    from dayu_widgets.qt import QWidget, QApplication
    app = QApplication.instance()
    main_window = None
    engine = engine.lower()
    if engine == "maya":
        import maya.OpenMayaUI as omui
        try:
            from shiboken2 import wrapInstance
        except ImportError:
            from shiboken import wrapInstance
        main_window_ptr = omui.MQtUtil.mainWindow()
        main_window = wrapInstance(long(main_window_ptr), QWidget)
    elif engine == "nuke":
        for widgets in app.topLevelWidgets():
            if widgets.metaObject().className() == "Foundry::UI::DockMainWindow":
                main_window = widgets
    elif engine == "houdini":
        import hou
        main_window = hou.qt.mainWindow()
    return main_window


def delete_existed_maya_window(ui_win):
    """
    Delete the maya window if it exists
    Args:
        ui_win: str - The object name of the window

    Returns:

    """
    import maya.cmds as cmds
    if cmds.window(ui_win, q=True, exists=True):
        try:
            cmds.deleteUI(ui_win)
        except Exception as e:
            pass


def delete_existed_houdini_window(ui_win):
    """
    Delete the maya window if it exists
    Args:
        ui_win: str - The object name of the window

    Returns:

    """
    from PySide2.QtWidgets import QWidget

    main_window = get_main_window("houdini")
    window_list = main_window.findChildren(QWidget, ui_win)
    for window in window_list:
        window.close()


def check_existed_maya_window(ui_win):
    """
    Check whether the maya window exists
    Args:
        ui_win: str - The object name of the window

    Returns:

    """
    import maya.cmds as cmds
    return cmds.window(ui_win, q=True, exists=True)


def get_pc_info():
    """
    get current user and pc ip address
    Returns:
        user_name:str - current user name
        ip_address:str - ip

    """
    user_name = getpass.getuser()
    import socket
    pc_name = socket.getfqdn(socket.gethostname())
    ip_address = socket.gethostbyname(pc_name)
    return user_name, ip_address


def copy_file_with_md5(source_file_path, targe_file_path, shell=True):
    """
    copy file with file md5
    Args:
        source_file_path: source path
        targe_file_path: tartge path
        shell: bool - use shell to run the copy command if true
    Returns:

    """
    try:
        if os.path.isfile(source_file_path) and os.path.isfile(targe_file_path):
            import hashlib
            source_file = hashlib.md5()
            targe_file = hashlib.md5()
            with open(source_file_path)as source_f:
                source_file.update(source_f.read())
            with open(targe_file_path) as targe_f:
                targe_file.update(targe_f.read())
            if source_file.hexdigest() != targe_file.hexdigest():
                # return copy_file(source_file_path, targe_file_path)
                result_code = GCopy.copy_file_to_dir(source_file_path, os.path.dirname(targe_file_path),
                                                     default_shell=shell)
                if not result_code:
                    return 0
                else:
                    return result_code
            else:
                return 0
        else:
            # return copy_file(source_file_path, targe_file_path)
            if not GCopy.copy_file_to_dir(source_file_path, os.path.dirname(targe_file_path), default_shell=shell):
                return 0
    except Exception as e:
        log.error(e)
        return 1


def copy_file_with_mtime(source_file_path, target_file_path, shell=True):
    """

    Args:
        source_file_path: str - source path
        target_file_path: str - target path
        shell: bool - use shell to run the copy command if true

    Returns:

    """
    try:
        if os.path.isfile(source_file_path) and os.path.isfile(target_file_path):
            if os.stat(source_file_path).st_mtime > os.stat(target_file_path).st_mtime:
                GCopy.copy_file_to_dir(source_file_path, os.path.dirname(target_file_path), default_shell=shell)
        else:
            GCopy.copy_file_to_dir(source_file_path, os.path.dirname(target_file_path), default_shell=shell)
        return 0
    except Exception as e:
        log.error(e)
        return 1


def copy_file(source_file_path, targe_file_path):
    """
    Copy files using window Xcopy command
    Args:
        source_file_path:str - source path
        targe_file_path:str - tartge path

    Returns:int - xcopy return code
        0      Files were copied without error.
        1      No files were found to copy.
        2      The user pressed CTRL+C to terminate xcopy.
        4      Initialization error occurred. There is not
               enough memory or disk space, or you entered
               an invalid drive name or invalid syntax on
               the command line.
        5      Disk write error occurred.

    """
    if replace_path(source_file_path) == replace_path(targe_file_path):
        return 0
    return_code = subprocess.call(
        "echo F|xcopy /Y \"{}\" \"{}\"".format(replace_path(source_file_path), replace_path(targe_file_path)),
        shell=True)
    return return_code


def copy_dir(source_dir, target_dir):
    """

    Args:
        source_dir:source dir in window
        target_dir:target dir in window

    Returns:

    """
    if replace_path(source_dir) == replace_path(target_dir):
        return 0
    return_code = subprocess.call(
        "echo D|xcopy /E /Y \"{}\" \"{}\"".format(replace_path(source_dir), replace_path(target_dir)),
        shell=True)
    return return_code


def maya_get_dir(index):
    """

    Args:
        index: 	Indicate what the dialog is to return.
                0 Any file, whether it exists or not.
                1 A single existing file.
                2 The name of a directory. Both directories and files are displayed in the dialog.
                3 The name of a directory. Only directories are displayed in the dialog.
                4 Then names of one or more existing files.

    Returns:

    """
    import maya.cmds as cmds
    path = cmds.fileDialog2(fm=index, okc="load")
    if path:
        return path[0]


def fetch_all(section, section_value, table, info_filter="*"):
    from std_maya import get_mysql
    mysql = get_mysql.SqlDatabase(host="10.10.20.12", port=3306, user="Toolkit", passwd="123456", db="dcc_workflow")
    command = "SELECT %s FROM %s WHERE %s ='%s'" % (info_filter, table, section, section_value)
    info = mysql.search(command)
    return info


def check_video_fps(input_mov_path):
    """
    check fps
    Args:
        input_mov_path: str - input mov path

    Returns:str - fps

    """
    set_ffmpeg_path()
    command = "{} -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 " \
              "-show_entries stream=r_frame_rate {}".format(FFPROBE_EXE, input_mov_path)
    p = subprocess.Popen("{} ".format(command), stdout=subprocess.PIPE, shell=True)
    while p.poll() is None:
        if not p.stdout:
            continue
        line = p.stdout.readline().strip()
        if line:
            fps = line.split("/")[0]
            return fps


def check_video_with_24fps(input_mov_path):
    """
    get total video frames with 24 fps
    Args:
        input_mov_path:str - input mov path

    Returns:str - total frames

    """
    set_ffmpeg_path()
    command = "{} -v error -count_frames -select_streams v:0 -show_entries " \
              "stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 {}".format(FFPROBE_EXE, input_mov_path)
    p = subprocess.Popen("{} ".format(command), stdout=subprocess.PIPE, shell=True)
    while p.poll() is None:
        if not p.stdout:
            continue
        line = p.stdout.readline().strip()
        if line:
            return line


def get_video_thumbnail(input_mov_path, output_image_path=os.environ["TMP"]):
    """
    get video thumbnail on frame 1
    Args:
        input_mov_path:str - input mov path
        output_image_path:str - save thumbnail image path

    Returns:str - thumbnail image path

    """
    set_ffmpeg_path()
    file_name = os.path.splitext(os.path.basename(input_mov_path))[0]
    thumbnail_image_name = os.path.join(output_image_path, "{}_{}.jpg".format(file_name, "thumbnail"))
    command = "{} -v 1 -i {} -f image2 {} -y".format(FFMPEG_EXE, input_mov_path, thumbnail_image_name)
    return_code = subprocess.call("{} ".format(command), shell=True)
    if return_code:
        return thumbnail_image_name


def get_file_md5(file_path):
    import hashlib
    file_md5 = hashlib.md5()
    with open(file_path, "rb")as f:
        data = f.read()
        file_md5.update(data)
    return file_md5.hexdigest()


def replace_path(path):
    """
    replace the "//","/" as "\\"
    Args:
        path:

    Returns:

    """
    return path.replace("//", "/").replace("/", "\\")


def get_camera():
    import pymel.core as pm
    try:
        focus_panel = pm.getPanel(withFocus=1)
        camera = pm.modelPanel(focus_panel, q=1, camera=1)  # unicode string
    except RuntimeError:
        return

    try:
        camera_shape = pm.listRelatives(camera, c=1)[0]
        focal_length = str(camera_shape.focalLength.get())
    except IndexError:
        camera_shape = camera
        camera = str(pm.listRelatives(camera_shape, p=1)[0])
        focal_length = str(pm.camera(camera_shape, q=1, fl=1))

    return camera, focal_length


def commit_playblast(team_leader_name, artist_name, target_dir=u"", s_time=u"", e_time=u""):
    """
    commit playblast function in maya
    Args:
        team_leader_name(unicode): The leader's name
        artist_name(unicode): The artist's name
        target_dir(unicode): The target directory, default is current workspace
        s_time(unicode): The start frame of current scene, default is the minimum time in PlayBackSlider
        e_time(unicode): The end frame of current scene, efault is the maximum time in PlayBackSlider
    Notes:
        Note that the first three arguments passed must be in unicode format

    Examples:
        commit_playblast(u"张三", u"李四")

    """
    set_ffmpeg_path()
    import gvf_globals
    from gvf_globals import task_globals
    import json
    PLAYBLAST_CONFIG = r"D:/gvfpipe/dcc_ops/maya/scripts/playblast_tool_v2/playblast.json" if is_debug_mode() \
        else r"V:/TD/gvfpipe/dcc_ops/maya/scripts/playblast_tool_v2/playblast.json"
    with open(PLAYBLAST_CONFIG, "r") as f:
        playblast_config_dict = json.load(f)
    current_project_env = task_globals.current_project_env
    if current_project_env in gvf_globals.JunYiXin_projects:
        current_project_env = "JunYiXin_projects"
    playblast_config = playblast_config_dict.get(current_project_env, playblast_config_dict["default"])
    if playblast_config:
        return commit_playblast_external(playblast_config)

    from dayu_widgets.qt import QMessageBox
    import shutil
    import subprocess
    import pymel.core as pm
    import maya.mel as mel

    team_leader_name = team_leader_name.encode('utf-8')

    artist_name = artist_name.replace(",", "/").encode('utf-8')
    start_time = s_time.encode('utf-8') if s_time else str(int(pm.playbackOptions(minTime=1, q=1)))
    end_time = e_time.encode('utf-8') if e_time else str(int(pm.playbackOptions(maxTime=1, q=1)))
    target_dir, tmp_dir = os.environ["TMP"], os.path.join(os.environ["TMP"], "playblast_tmp")
    # scene_name = os.path.splitext(cmds.file(q=1, sn=1, shn=1))[0].encode('utf-8')
    # result, data = get_playblast_version(os.path.splitext(cmds.file(q=1, sn=1, shn=1))[0].encode('utf-8'))
    result, data = get_playblast_version()

    if not result:
        QMessageBox.warning(None, "warning", data, QMessageBox.Ok)
        return
    scene_name = data.encode('utf-8')

    try:
        camera, focal_length = get_camera()
    except TypeError:
        log.error(u"获取相机面板失败，请点击操作视图再重新尝试")
        return
    camera = camera.encode('utf-8')
    focal_length = focal_length.encode('utf-8')
    target_file = target_dir + "/" + scene_name + ".mov"
    total_frame = str(int(end_time) - int(start_time) + 1)
    if scene_name == "":
        QMessageBox.warning(None, "warning", "当前场景为空", QMessageBox.Ok)
        return
    elif target_dir == "":
        QMessageBox.warning(None, "warning", "拍屏文件导出路径为空", QMessageBox.Ok)
        return
    else:
        if not os.path.exists(tmp_dir):  # os.path can't check an existed path that contains Chinese
            try:
                os.makedirs(tmp_dir)
            except WindowsError:
                QMessageBox.warning(None, "warning", "无权限创建临时文件，请联系技术部人员", QMessageBox.Ok)
                return

        # if team_leader_name == "":
        #     QtWidgets.QMessageBox.warning(None, "warning", "组长姓名为空", QtWidgets.QMessageBox.Ok)
        if artist_name == "":
            QMessageBox.warning(None, "warning", "艺术家姓名为空", QMessageBox.Ok)
            return
        else:
            filename = tmp_dir + "\\" + "img"

        if os.path.exists(target_file):
            backup_dir = os.path.join(target_dir, "backup")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            try:
                shutil.move(target_file, backup_dir)
            except WindowsError and IOError and shutil.Error:
                os.remove(os.path.join(backup_dir, scene_name + ".mov"))
                try:
                    shutil.move(target_file, backup_dir)
                except WindowsError:
                    QMessageBox.warning(None, "warning", "另一个程序正在使用此文件", QMessageBox.Ok)
                    return

        time_slider = mel.eval("$gPlayBackSlider=$gPlayBackSlider")
        audio = pm.timeControl(time_slider, q=1, sound=1)
        sound = ""
        if audio:
            sound = audio
        pm.playblast(fmt="qt", f=filename, fo=1, sqt=0, cc=0, v=0, orn=0, os=1, fp=4, p=100, c="png", qlt=100,
                     wh=[1280, 544], st=start_time, et=end_time, sound=sound)
        try:
            source_file = mel.eval("file -q -sn")
            source_path = source_file.encode('utf-8')
        except:
            source_path = ""
        # type of command is utf-8
        fps = mel.eval('currentTimeUnitToFPS')
        command = FFMPEG_EXE + " -r " + str(
            fps) + r" -y -i " + tmp_dir + r"\img.mov" + r" -s 1280x544 -acodec copy -metadata comment=" + source_path + " -c:v libx264 -x264opts b_pyramid=0 -profile:v baseline -q:v 2 -b:v 500m -crf 2 -pix_fmt yuv420p -vf [in]drawtext=fontfile=" + FONT_PATH + r":text='Leader\:':fontcolor=0x64f538:fontsize=16:x=0.1*w:y=0.04*h,drawtext=fontfile=" + FONT_PATH + r":text=" + team_leader_name + r":fontcolor=white:fontsize=16:x=0.1*w+70:y=0.04*h,drawtext=fontfile=" + FONT_PATH + r":text=" + scene_name + r":fontcolor=white:fontsize=16:x=(w-text_w)/2:y=0.04*h,drawtext=fontfile=" + FONT_PATH + r":text='Artist\:':fontcolor=0x64f538:fontsize=16:x=0.75*w:y=0.04*h,drawtext=fontfile=" + FONT_PATH + r":text=" + artist_name + r":fontcolor=white:fontsize=16:x=0.75*w+70:y=0.04*h,drawtext=fontfile=" + FONT_PATH + r":text='Date\:':fontcolor=0x64f538:fontsize=16:x=0.1*w:y=0.94*h,drawtext=fontfile=" + FONT_PATH + r":text='%{localtime\:%Y\-%m\-%d}':fontcolor=white:fontsize=16:x=0.1*w+50:y=0.94*h,drawtext=fontfile=" + FONT_PATH + r":text='Camera\:':fontcolor=0x64f538:fontsize=16:x=(w-text_w)/2-130:y=0.94*h,drawtext=fontfile=" + FONT_PATH + r":text=" + camera + r"/" + focal_length + r":fontcolor=white:fontsize=16:x=(w-text_w)/2+60:y=0.94*h,drawtext=fontfile=" + FONT_PATH + r":text='Frame\:':fontcolor=0x64f538:fontsize=16:x=0.8*w:y=0.94*h,drawtext=fontfile=" + FONT_PATH + r":text='%{eif\:n+1\:d}/'" + total_frame + r":fontcolor=white:fontsize=16:x=0.8*w+60:y=0.94*h,drawtext=fontfile=" + FONT_PATH + r":text='24fps':fontcolor=white:fontsize=16:x=0.8*w+140:y=0.94*h[out] " + target_file
        gbk_command = command.decode('utf-8').encode('gbk')
        try:
            ffmpeg = subprocess.Popen(gbk_command, shell=True)
        except Exception as e:
            log.error(e)
        ffmpeg.wait()
        shutil.rmtree(tmp_dir)
        return target_file


def commit_playblast_external(playblast_config, artist_name="", s_time="", e_time="", width="", height="",
                              subtitle_mode="", format=""):
    set_ffmpeg_path()
    import pymel.core as pm
    import maya.mel as mel
    import maya.cmds as cmds
    from PySide2 import QtCore
    from dayu_widgets.qt import QMessageBox
    import shutil
    HUD_MEL = r"V:/TD/gvfpipe/dcc_ops/maya/scripts/playblast_tool_v2/SW6HUD.mel"

    start_time = s_time if s_time else str(int(pm.playbackOptions(minTime=1, q=1)))
    end_time = e_time if e_time else str(int(pm.playbackOptions(maxTime=1, q=1)))
    format = format if e_time else playblast_config["format"]
    width = width if width else playblast_config["width"]
    height = height if height else playblast_config["height"]
    subtitle_mode = subtitle_mode if subtitle_mode else playblast_config["subtitle_mode"]
    target_dir = os.path.join(os.environ["TMP"], "playblast_tmp")
    result, scene_name = get_playblast_version()
    scene_name = scene_name.rsplit("_", 1)[0]
    cfgs = QtCore.QSettings("GVF_Pipeline", "playblast_tool")
    # leader_name = cfgs.value("leader_name")
    artist_name = cfgs.value("artist_name")

    if not result:
        QMessageBox.warning(None, "warning", scene_name, QMessageBox.Ok)
        return

    try:
        camera, focal_length = get_camera()
    except TypeError:
        log.error(u"获取相机面板失败，请点击操作视图再重新尝试")
        return
    if scene_name == "":
        QMessageBox.warning(None, "warning", "当前场景为空", QMessageBox.Ok)
        return
    elif target_dir == "":
        QMessageBox.warning(None, "warning", "拍屏文件导出路径为空", QMessageBox.Ok)
        return
    tmp_dir = os.path.join(os.getenv('TEMP'), "playblast_tmp")
    if not os.path.exists(tmp_dir):  # os.path can't check an existed path that contains Chinese
        try:
            os.mkdir(tmp_dir)
        except Exception:
            QMessageBox.warning(None, "warning", "无权限创建临时文件，请联系技术部人员", QMessageBox.Ok)
    tmp_mov = tmp_dir + "/" + "tmp_" + scene_name + "." + format
    target_file = target_dir + "/" + scene_name + "." + format
    if os.path.exists(target_file):
        backup_dir = os.path.join(target_dir, "backup")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        try:
            shutil.move(target_file, backup_dir)
        except WindowsError and IOError and shutil.Error:
            os.remove(os.path.join(backup_dir, scene_name + ".mov"))
            try:
                shutil.move(target_file, backup_dir)
            except WindowsError:
                QMessageBox.warning(None, "warning", "另一个程序正在使用此文件", QMessageBox.Ok)
                return

    time_slider = mel.eval("$gPlayBackSlider=$gPlayBackSlider")
    audio = pm.timeControl(time_slider, q=1, sound=1)

    if subtitle_mode == "original":
        # if leader_name == "":
        #     QMessageBox.warning(None, "warning", "组长姓名为空", QMessageBox.Ok)
        #     return
        if artist_name == "":
            QMessageBox.warning(None, "warning", "艺术家姓名为空", QMessageBox.Ok)
            return

        prev_HUD = {}
        if cmds.headsUpDisplay(listHeadsUpDisplays=True):
            for headsup in cmds.headsUpDisplay(listHeadsUpDisplays=True):
                if headsup.startswith("PlayblastHud"):
                    cmds.headsUpDisplay(headsup, remove=True)
                else:
                    vis = cmds.headsUpDisplay(headsup, q=True, vis=True)
                    prev_HUD[headsup] = vis
                    cmds.headsUpDisplay(headsup, e=True, vis=False)

        heads_up_display()
        if format == "mov":
            if cmds.about(v=True) == "2018" and audio:
                pm.playblast(fmt="qt", f=tmp_mov, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             c="png",
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
            elif audio:
                pm.playblast(fmt="qt", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             c="png",
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time, sound=audio)
            else:
                pm.playblast(fmt="qt", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             c="png",
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
        else:
            if cmds.about(v=True) == "2018" and audio:
                pm.playblast(fmt="avi", f=tmp_mov, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
            elif audio:
                pm.playblast(fmt="avi", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time, sound=audio)
            else:
                pm.playblast(fmt="avi", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)

        if cmds.headsUpDisplay(listHeadsUpDisplays=True):
            for i in cmds.headsUpDisplay(listHeadsUpDisplays=True):
                if i.startswith("PlayblastHud"):
                    cmds.headsUpDisplay(i, remove=True)

        for headsup in prev_HUD:
            cmds.headsUpDisplay(headsup, e=True, vis=prev_HUD[headsup])

    elif subtitle_mode == "outsource":
        # HUD of outsourcing mode
        mel_script = 'source "{}";'.format(HUD_MEL)
        mel.eval(mel_script)
        if format == "mov":
            if cmds.about(v=True) == "2018" and audio:
                pm.playblast(fmt="qt", f=tmp_mov, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             c="png",
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
            elif audio:
                pm.playblast(fmt="qt", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             c="png",
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time, sound=audio)
            else:
                pm.playblast(fmt="qt", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             c="png",
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
        elif format == "avi":
            if cmds.about(v=True) == "2018" and audio:
                pm.playblast(fmt="avi", f=tmp_mov, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
            elif audio:
                pm.playblast(fmt="avi", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time, sound=audio)
            else:
                pm.playblast(fmt="avi", f=target_file, fo=1, sqt=0, cc=0, v=0, orn=1, os=1, fp=4, p=100,
                             qlt=100,
                             wh=[int(width), int(height)], st=start_time, et=end_time)
    if cmds.about(v=True) == "2018" and audio:
        audio_node = cmds.ls(audio)[0]
        audio_path = cmds.getAttr(audio_node + ".filename")
        audio_opt = " -i " + audio_path
        audio_start = cmds.getAttr(audio_node + ".sourceStart")
        audio_end = cmds.getAttr(audio_node + ".sourceEnd")
        audio_duration = cmds.getAttr(audio_node + ".duration")
        audio_time = audio_end - audio_start
        total_frame = int(end_time) - int(start_time) + 1
        if not os.path.exists(audio_path):
            audio_opt = ""
        elif " " in audio_path:
            QMessageBox.warning(None, "warning", u"请检查音频文件是否有空格.", QMessageBox.Ok)
            return
        try:
            source_file = mel.eval("file -q -sn")
            source_path = source_file.replace(" ", "_").encode('utf-8')
        except:
            source_path = ""
        if audio_time > total_frame and int(audio_duration) + 1 > total_frame:
            shortest = " -shortest"
        else:
            shortest = ""
        fps = mel.eval('currentTimeUnitToFPS')
        command = FFMPEG_EXE + " -r " + str(
            fps) + r" -i " + tmp_mov + audio_opt + shortest + " -vcodec copy -acodec copy -metadata comment=" + source_path + " " + target_file + " -y "
        gbk_command = command.decode('utf-8').encode('gbk')
        try:
            ffmpeg = subprocess.Popen(gbk_command, shell=True)
            ffmpeg.wait()
        except Exception as e:
            log.error(e)

    return target_file


def get_leader():
    from PySide2 import QtCore
    cfgs = QtCore.QSettings("GVF_Pipeline", "playblast_tool")
    leader_name = cfgs.value("leader_name")
    return leader_name


def get_scene_name():
    import maya.cmds as cmds
    scene_name = os.path.splitext(cmds.file(q=1, sn=1, shn=1))[0]
    return scene_name


def get_artist():
    from PySide2 import QtCore
    cfgs = QtCore.QSettings("GVF_Pipeline", "playblast_tool")
    artist_name = cfgs.value("artist_name")
    return artist_name


def get_frame():
    import maya.mel as mel
    import maya.cmds as cmds
    import pymel.core as pm
    start_time = int(pm.playbackOptions(minTime=1, q=1))
    end_time = int(pm.playbackOptions(maxTime=1, q=1))
    total_frame = end_time - start_time + 1
    fps = mel.eval('currentTimeUnitToFPS')  # 返回的是一个float
    currentframe = cmds.currentTime(q=1)
    currentTime_get = "{} / {}    {}fps".format(int(currentframe), total_frame, int(fps))
    return currentTime_get


def get_date():
    import maya.cmds as cmds
    currentDate = cmds.date()
    currentDate = currentDate.split(" ")[0].replace("/", "-")
    return currentDate


def get_cam_info():
    import pymel.core as pm
    focus_panel = pm.getPanel(withFocus=1)
    camera_name = pm.modelPanel(focus_panel, q=1, camera=1)
    camera_shape = pm.listRelatives(camera_name, c=1)[0]
    focal_length = camera_shape.focalLength.get()
    cam_get = "{} / {}".format(camera_name, focal_length)
    return cam_get


def heads_up_display():
    import maya.cmds as cmds
    try:
        cmds.displayPref(fm=2, sfs=12, dfs=16)
    except:
        pass
    cmds.displayColor("headsUpDisplayLabels", 14, dormant=1)
    cmds.displayColor("headsUpDisplayValues", 16, dormant=1)

    block01 = cmds.headsUpDisplay(nextFreeBlock=0)
    cmds.headsUpDisplay('PlayblastHudLeader01', allowOverlap=1, section=0, block=block01, blockSize='small',
                        label=' ', labelFontSize='small', dataFontSize='small')
    block0 = cmds.headsUpDisplay(nextFreeBlock=0)
    cmds.headsUpDisplay('PlayblastHudLeader', allowOverlap=1, section=0, block=block0, blockSize='large',
                        label='Leader:', command=get_leader, attachToRefresh=True,
                        labelFontSize='large', dataFontSize='large')

    block21 = cmds.headsUpDisplay(nextFreeBlock=2)
    cmds.headsUpDisplay('PlayblastHudScene21', allowOverlap=1, section=2, block=block21, blockSize='small',
                        label=' ',
                        labelFontSize='small', dataFontSize='small')
    block2 = cmds.headsUpDisplay(nextFreeBlock=2)
    cmds.headsUpDisplay('PlayblastHudScene', allowOverlap=1, section=2, block=block2, blockSize='large',
                        labelFontSize='large', dataFontSize='large', command=get_scene_name, attachToRefresh=True)

    block41 = cmds.headsUpDisplay(nextFreeBlock=4)
    cmds.headsUpDisplay('PlayblastHudArtist41', allowOverlap=1, section=4, block=block41, blockSize='small',
                        label=' ', labelFontSize='small', dataFontSize='small')
    block4 = cmds.headsUpDisplay(nextFreeBlock=4)
    cmds.headsUpDisplay('PlayblastHudArtist', allowOverlap=1, section=4, block=block4, blockSize='large',
                        label='Artist:', command=get_artist,
                        labelFontSize='large', dataFontSize='large', attachToRefresh=True)

    block5 = cmds.headsUpDisplay(nextFreeBlock=5)
    cmds.headsUpDisplay('PlayblastHudDate', allowOverlap=1, section=5, block=block5, blockSize='large', label='Date:',
                        labelFontSize='large',
                        dataFontSize='large', command=get_date, attachToRefresh=True)
    block7 = cmds.headsUpDisplay(nextFreeBlock=7)
    cmds.headsUpDisplay('PlayblastHudCam', allowOverlap=1, section=7, block=block7, blockSize='large', label='Camera:',
                        labelFontSize='large', dataFontSize='large', command=get_cam_info, attachToRefresh=True)
    block9 = cmds.headsUpDisplay(nextFreeBlock=9)
    cmds.headsUpDisplay('PlayblastHudFrame', allowOverlap=1, section=9, block=block9, blockSize='large', label='Frame:',
                        labelFontSize='large', dataFontSize='large', command=get_frame,
                        attachToRefresh=True)


def text_input(original_file, target_file, left_up, middle_up, right_up, left_bottom, middle_bottom, right_bottom,
               width, height):
    video = original_file
    # 读取视频
    import cv2
    from playblast_tool_v2 import playblast_tool_dialog2
    cap = cv2.VideoCapture(video)
    # 获取视频帧率
    fps_video = cap.get(cv2.CAP_PROP_FPS)
    # 设置写入视频的编码格式
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # 获取视频宽度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 获取视频高度
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    videoWriter = cv2.VideoWriter(target_file, fourcc, fps_video, (frame_width, frame_height))
    fps = int(fps_video)
    color1 = (255, 255, 255)
    color2 = (55, 255, 155)
    text_size = 14
    frame_id = 0
    date1 = datetime.now().strftime("%Y-%m-%d")
    tff_path = r"V:/TD/gvfpipe/dcc_ops/maya/scripts/playblast_tool_v2/msyh.ttf"
    ft = playblast_tool_dialog2.put_chinese_text(tff_path)
    width = float(width)
    height = float(height)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame_id += 1
            f = u'%s/ ' % frame_id
            image1 = ft.draw_text(frame, (int(width * 0.093), int(height * 0.015)), u"Leader :", text_size,
                                  color2)
            image1 = ft.draw_text(image1, (int(width * 0.148), int(height * 0.015)), left_up, text_size, color1)
            image1 = ft.draw_text(image1, (int(width * 0.42), int(height * 0.015)), middle_up, text_size, color1)
            image1 = ft.draw_text(image1, (int(width * 0.78), int(height * 0.015)), u"Artist :", text_size, color2)
            image1 = ft.draw_text(image1, (int(width * 0.83), int(height * 0.015)), right_up, text_size, color1)

            image1 = ft.draw_text(image1, (int(width * 0.093), int(height * 0.919)), u"Date :", text_size, color2)
            image1 = ft.draw_text(image1, (int(width * 0.148), int(height * 0.919)), date1, text_size, color1)
            image1 = ft.draw_text(image1, (int(width * 0.414), int(height * 0.919)), u"Camera :", text_size, color2)
            image1 = ft.draw_text(image1, (int(width * 0.468), int(height * 0.919)),
                                  u" " + left_bottom + u'/ ' + middle_bottom, text_size, color1)
            image1 = ft.draw_text(image1, (int(width * 0.78), int(height * 0.919)), u"Frame :", text_size, color2)
            image1 = ft.draw_text(image1, (int(width * 0.83), int(height * 0.919)),
                                  f + right_bottom + u"      %s" % fps + u" fps", text_size, color1)

            videoWriter.write(image1)
        else:
            videoWriter.release()
            break
    return target_file


def check_asset_legality():
    """

    Returns:

    """
    import maya.cmds as cmds
    for ref_file in cmds.file(q=1, r=1):
        if cmds.referenceQuery(ref_file, il=1):
            file_md5 = get_file_md5(ref_file)
            sql_result = fetch_all(table="task_publish", section="md5", section_value=file_md5)
            if not sql_result:
                return ref_file


def check_ma_asset(dirs, exclude=None):
    """

    Args:
        dirs:window dir - str
        exclude:

    Returns:

    """
    if exclude:
        ma_asset_list = [file_name for file_name in os.listdir(dirs) if
                         os.path.splitext(file_name)[-1] == ".ma" and exclude not in os.path.splitext(file_name)[
                             0] and re.match(r"\w*_\D*_[H|L]_v\d{3}.ma", file_name)]
        return ma_asset_list
    else:
        ma_asset_list = [file_name for file_name in os.listdir(dirs) if
                         os.path.splitext(file_name)[-1] == ".ma" and re.match(r"\w*_\D*_[H|L]_v\d{3}.ma", file_name)]
        return ma_asset_list


def get_unique_renderable_camera():
    import maya.cmds as cmds

    cam = cmds.ls(type="camera")
    error_info = ""
    result = None

    def is_true(cam):
        return cmds.getAttr("{}.renderable".format(cam)) is True

    active_cam = filter(is_true, cam)
    temp = active_cam[:]
    default_camera = ["frontShape", "perspShape", "sideShape", "topShape"]
    for ac in temp:
        if ac in default_camera:
            temp.remove(ac)
    # if len(active_cam) == 0:
    #     result = False
    #     error_info = u"Have not specified a renderable camera yet!"
    # elif len(active_cam) > 1:
    #     result = False
    #     error_info = u"More than one renderable camera exist!"
    if len(temp) == 0:
        result = False
        error_info = u"Selected default camera as a renderable camera!"
    elif len(temp) == 1:
        result = temp[0]
    return result, error_info


def open_maya_standalone(file_path):
    import maya.standalone
    maya.standalone.initialize()
    import maya.cmds as cmds
    cmds.file(file_path, f=1, o=1)


def get_playblast_version():
    from gvf_globals import task_globals
    from tw_toolkit.cgtw_task_list import func_tool
    from tw_toolkit.GvfPublishTool import publish_sql
    from PySide2 import QtWidgets
    import maya.cmds as cmds
    config_table = func_tool.get_config_table()

    if not task_globals.task_id:
        # msg = "请先在任务系统选择对应镜头任务"
        # return False, msg
        scene_name = cmds.file(q=1, sn=1, shn=1)
        if scene_name:
            return True, scene_name.split(".")[0]
        else:
            return False, "当前场景未保存"
    # elif not re.match(r"sc([0-9]{3})([a-z]?)_shot([0-9]{3,})([a-z]?)_[a-z]+_v([0-9]{3})", scene_name):
    #     msg = "当前文件命名非法，请使用任务系统保存文件"
    #     return False, msg

    if func_tool.get_file_save_status(task_globals.engine):
        msg = "是否保存当前文件？"
        message = QtWidgets.QMessageBox.warning(None, "warning", msg, QtWidgets.QMessageBox.Ok,
                                                QtWidgets.QMessageBox.Cancel)
        if message == QtWidgets.QMessageBox.Ok:
            cmds.file(s=1)
        else:
            return False, "拍屏审核失败，请确认保存文件"

    pb_ver = publish_sql.get_publish_version(task_globals.task_id)  # get the latest publish version
    pipeline = config_table.get(task_globals.pipeline).get("abbreviation")
    scene_name = "_".join([task_globals.scene, task_globals.shot, pipeline, pb_ver])
    return True, scene_name


def count_modified_interval(file_path):
    import time
    current_time = time.time()
    ctime = time.ctime(os.path.getctime(file_path))
    return abs(current_time - ctime)


def check_ascii_error(text):
    """

    Args:
        text: unicode/str - The string to be checked whether contains Chinese words

    Returns:
        bool: True for containing Chinese words, otherwise false
    """
    if not isinstance(text, unicode):
        try:
            text = text.decode('utf8')
        except UnicodeDecodeError:
            text = text.decode('gbk')

    return re.compile(u'[\u4e00-\u9fa5]').search(text)


def automatic_switching_reference():
    """
    自动转换文件参考里的低模变高模，如果有surface则转换为surface
    Returns:

    """
    import maya.cmds as cmds
    ref_file = cmds.file(q=1, r=1)  # 获取所有参考节点
    for file_path in ref_file:
        ref_path = ""
        # 查询是否加载该参考
        if cmds.referenceQuery(file_path, il=1):
            # 获取参考文件名和参考节点
            ref_node = cmds.file(file_path, q=1, rfn=1)
            # 将参考路径由本地替换为网盘
            file_path = file_path.replace("l:", "X:").replace("L:", "X:")
            current_ref_file_name = os.path.basename(file_path)
            # 拆分文件名:ella_rig_L_v015.ma 只截取资产名:ella_rig
            if "Low" in file_path:
                asset_name = re.search(r"(.*?)_L_v\d{3}", current_ref_file_name).group(1)
                # 替换高低摸路径
                new_ref_file_path = file_path.replace("Low", "High")
                # 材质
                base_name = os.path.basename(new_ref_file_path)
                current_ns = cmds.referenceQuery(ref_node, ns=1)[1:]
                new_name_space = ""
                assets_list, surface_flag = get_matched_asset(new_ref_file_path, is_mat(base_name))
                if assets_list:
                    source_dir = os.path.dirname(new_ref_file_path)
                    if surface_flag:
                        if "Surfacing" not in source_dir:
                            mod_index = source_dir.rfind("/Mod")
                            source_dir = os.path.join(source_dir[:mod_index], "Surfacing").replace("\\", "/")
                            new_name_space = asset_name.split("_")[0] + "_surf"
                    else:
                        new_name_space = current_ns.replace("rig_L", "rig_H")
                    ref_path = os.path.join(source_dir, assets_list[-1])
                    # 新空间名
                    # 分析现有空间名是否正确
                    if current_ns != new_name_space:
                        # 解算乱来，不管了
                        # if new_name_space in cmds.namespaceInfo(lon=1):
                        #     suffix_num = 1
                        #     while True:
                        #         if "{}{}".format(new_name_space, str(suffix_num)) not in cmds.namespaceInfo(lon=1):
                        #             new_name_space = "{}{}".format(new_name_space, str(suffix_num))
                        #             break
                        #         else:
                        #             suffix_num = suffix_num + 1
                        # 重命名空间名
                        if cmds.namespace(ex=new_name_space):
                            cmds.namespace(rm=new_name_space, mnr=1)
                        print (current_ns, new_name_space)
                        cmds.namespace(ren=(current_ns, new_name_space))
                    try:
                        cmds.file(ref_path, lr=ref_node)
                    except RuntimeError:
                        pass


def clean_maya_file():
    import maya.cmds as cmds
    for plugin in cmds.unknownPlugin(q=1, list=1) or []:
        try:
            cmds.unknownPlugin(plugin, remove=1)
        except Exception:
            pass
    for node in cmds.ls(type="unknown") or []:
        try:
            cmds.lockNode(node, lock=0)
            cmds.delete(node)
        except Exception:
            pass


def get_texture_from_text(file_path):
    _buffer = []
    tex_path_list = []
    with open(file_path, "r") as f:
        while True:
            content = f.readline()
            if not content:
                break
            if ".ftn" in content:
                _buffer.append(content.strip())
    if _buffer:
        tex_path_list = [_clip.split().pop().replace(";", "").replace("\"", "").replace("//", "/") for _clip in
                         _buffer]

    return list(set(tex_path_list))


def get_udim_texture_sequence(base_texture, blank_flag=False, igcase_flag=True):
    """
    查找序列贴图
    Args:
        base_texture: str - 基础贴图路径
        :param base_texture:
        :param blank_flag: bool - 找不到返回[]
        :param igcase_flag:
    Returns: list - 匹配文件路径列表


    """
    base_name = os.path.basename(base_texture)
    try:
        # X:/Projects/BXS/Publish/Assets/Char/ZhouTianXing_ShaoNian/Sourceimages/ZhouTianXing_ShangYi_Normal.<UDIM>.png
        if igcase_flag:
            texture_index = re.match(r".*(<UDIM>|\d{4})", base_name, re.IGNORECASE).group(1)  # 获取贴图序号
        else:
            texture_index = re.match(r".*(<UDIM>|\d{4})", base_name).group(1)  # 获取贴图序号
    except AttributeError as e:
        log.error(e)
        print(u"error file:{}".format(base_texture))
        return []

    regular = base_name.replace(texture_index, r"\d{4}")  # 构建正则匹配表达式
    dir_name = os.path.dirname(base_texture)
    # 获取匹配文件列表
    if igcase_flag:
        match_full_path_list = [concat_path_with_slash(dir_name, each_texture_name) for each_texture_name in os.listdir(dir_name)
                                if re.match(regular, each_texture_name, re.IGNORECASE)]
    else:
        match_full_path_list = [concat_path_with_slash(dir_name, each_texture_name) for each_texture_name in os.listdir(dir_name)
                                if re.match(regular, each_texture_name)]
    if not match_full_path_list:
        if blank_flag:
            return match_full_path_list
        match_full_path_list.append(base_texture)
    return sorted(match_full_path_list)


def get_ass_sequence(base_ass):
    """
    查找ass代理序列
    Args:
        base_ass: str - 基础ass路径

    Returns:

    """
    base_name = os.path.basename(base_ass)
    try:
        ass_reg = re.match(r".*\.(\d{4})", base_name) or re.match(r".*\.(####)", base_name) or re.match(r".*_(\d{4})",
                                                                                                        base_name) or re.match(
            r".*_(####)", base_name)
        ass_index = ass_reg.group(1)
    except AttributeError:
        raise AttributeError(u"error_file:{}".format(base_ass))
    regular = base_name.replace(ass_index, r"\d{4}")  # 构建正则匹配表达式
    dir_name = os.path.dirname(base_ass)
    # 获取匹配文件列表
    match_full_path_list = [os.path.join(dir_name, each_ass_name).replace("\\", "/") for each_ass_name in
                            os.listdir(dir_name)
                            if re.match(regular, each_ass_name)]
    if not match_full_path_list:
        # match_full_path_list.append(ass_index)
        return []
    return match_full_path_list


def get_format_time(sec, t_format="%Y-%m-%d %H:%M:%S"):
    import time
    return time.strftime(t_format, time.localtime(sec))


def commit_gcopy(source_path, target_path, mod, shell=True):
    """

    Args:
        source_path: str - file path in mod1, dir path in mod2 and mod3
        target_path: str - file path in mod1, dir path in mod2 and mod3
        mod: 1 - commit copy_file_with_md5
             2 - commit copy_dir_to_dir
             3 - commit mirror_dir_to_dir
             4 - commit copy_file_with_mtime
        shell: bool - use shell to run the command if true
    Returns:
    Examples:
        commit_gcopy("X:/Projects/texture/image.png", "L:/Projects/texture/image.png", mod=1)
        commit_gcopy("X:/Projects/texture", "L:/Projects/texture", mod=2)
        commit_gcopy("X:/Projects/texture", "L:/Projects/texture", mod=3)
        commit_gcopy("X:/Projects/proxy/tree.ass", "L:/Projects/proxy/tree.ass", mod=4)
    """
    if mod == 1:
        copy_file_with_md5(source_path, target_path, shell=shell)
    elif mod == 2:
        GCopy.copy_dir_to_dir(source_path, target_path, default_shell=shell)
    elif mod == 3:
        GCopy.mirror_dir_to_dir(source_path, target_path, default_shell=shell)
    elif mod == 4:
        copy_file_with_mtime(source_path, target_path, shell=shell)


class Register(object):
    def __init__(self):
        self.maya_reg_path = "SOFTWARE\\Autodesk\\Maya\\{}\\Setup\\InstallPath"
        self.maya_reg_item = "MAYA_INSTALL_LOCATION"

        self.cgt_reg_path = "SOFTWARE\\CgTeamWork\\6"
        self.cgt_reg_item = "InstallPath"

    def get_install_path(self, key, item):
        value, type_id = _winreg.QueryValueEx(key, item)
        return value

    def list_all_value(self, key_group, path):
        """
        list values owned by this registry key
        :return:
        """
        key = self.get_key(key_group, path)
        if key:
            value_list = []
            try:
                index = 0
                while 1:
                    value_item = _winreg.EnumValue(key, index)
                    index += 1
                    value_list.append(value_item)
            except WindowsError:
                return value_list

    def get_regedit(self, key_group, path, name):
        """

        :param path:
        :param name:
        :return:
        """
        key = self.get_key(key_group, path)
        value, type_id = _winreg.QueryValueEx(key, name)
        return value

    @staticmethod
    def get_key(key_group, path):
        """

        :param path: regedit path
        :return: key
        """
        # _winreg.QueryInfoKey(key_group)
        try:
            return _winreg.OpenKey(key_group, path)
        except:
            pass

    def get_maya_lib_path(self, version):
        maya_bin_folder = self.get_maya_install_path(version)
        if maya_bin_folder:
            return os.path.join(maya_bin_folder, "Python/DLLs").replace("\\", "/")

    def get_maya_py_path(self, version):
        version = int(version)
        maya_bin_folder = self.get_maya_install_path(version)
        if maya_bin_folder:
            executor = "mayapy2.exe" if version >= 2022 else "mayapy.exe"
            return os.path.join(maya_bin_folder, "bin", executor).replace("\\", "/")

    def get_maya_batch_path(self, version):
        maya_bin_folder = self.get_maya_install_path(version)
        if maya_bin_folder:
            return os.path.join(maya_bin_folder, "bin/mayabatch.exe").replace("\\", "/")

    def get_maya_install_path(self, version):
        """
            :param version: available:[2017 - 2020]
            :return: maya install path
        """
        key = self.get_key(_winreg.HKEY_LOCAL_MACHINE, self.maya_reg_path.format(version))
        if key:
            return self.get_install_path(key, self.maya_reg_item).replace("\\", "/")
        else:
            print "fetch regedit value failed: maya{} is not found!".format(version)

    def get_cgt_install_path(self):
        """
            :return: cgt install path
        """
        key = self.get_key(_winreg.HKEY_CURRENT_USER, self.cgt_reg_path)
        if key:
            return self.get_install_path(key, self.cgt_reg_item).replace("\\", "/")
        else:
            print "fetch regedit value failed: CGT6 is not found!"

    def get_cgt_base_lib(self):
        cgt_bin_folder = self.get_cgt_install_path()
        if cgt_bin_folder:
            base_lib_folder = os.path.join(os.path.dirname(cgt_bin_folder), "base").replace("\\", "/")
            return base_lib_folder


def open_resource_explorer(base_dir=None, title=None, parent=None):
    from pylibs.tkinter import Tk
    from pylibs.tkinter import filedialog

    root = Tk()  # 创建一个Tkinter.Tk()实例
    root.withdraw()  # 将Tkinter.Tk()实例隐藏
    root.focus_force()

    parm_dict = {
        "title": title if title else "选择文件",
    }
    if base_dir:
        parm_dict["initialdir"] = base_dir
    if parent:
        parm_dict["parent"] = parent

    file_path = filedialog.askopenfilename(**parm_dict)
    return file_path


def get_latest_version_assembly(path):
    import os
    import re
    dir_list = os.listdir(path)
    pattern = r"assembly_v([0-9]*)"
    latest_version = 0
    latest_dir = None
    for dir_name in dir_list:
        result = re.match(pattern, dir_name)
        if result:
            version = int(result.group(1))
            if version > latest_version:
                latest_version = version
                latest_dir = dir_name
    if not latest_dir:
        raise Exception("No assembly directory")
    return os.path.join(path, latest_dir)


def create_houdini_node(parent_node, node_type, input_list=None, parm_dict=None, node_name=None):
    node = parent_node.createNode(node_type, node_name) if node_name else parent_node.createNode(node_type)
    if input_list:
        for index, input_node in enumerate(input_list):
            node.setInput(index, input_node)
    if parm_dict:
        node.setParms(parm_dict)
    return node


def get_file_name_type(path):
    full_file_name = os.path.basename(path)
    file_name, _, file_type = full_file_name.rpartition(".")
    return file_name, file_type


def exist_json_file(path):
    if not os.path.exists(path):
        try:
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with open(path, "w"):
                pass
        except Exception as e:
            return False
    return True


def write_json(path, pattern_data):
    if exist_json_file(path):
        with open(path, "w") as f:
            try:
                json.dump(pattern_data, f, indent=4)
            except IOError as e:
                print(e)
                return False
            return True


def read_json(path):
    if exist_json_file(path):
        with open(path, "r") as f:
            print("read from {}".format(path))
            try:
                pattern_data = json.load(f)
            except (IOError, ValueError) as e:
                print(e)
                return {}
            return pattern_data


def get_maya_version(ma_file):
    if ma_file.endswith("mb"):
        with open(ma_file, 'rb') as f:
            for line in read_fileline_generator(f):
                search_version = re.search(b'Maya (\d{4})', line, re.S)
                if search_version:
                    return int(search_version.group(1))
    else:
        with open(ma_file, "r") as f:
            pattern = r"Maya.*(20\d{2})"
            for line in read_fileline_generator(f):
                match_version_result = re.search(pattern, line)
                if match_version_result:
                    return int(match_version_result.group(1))
    raise Exception("cannot match maya version")


def get_correct_case_path(source_path):
    import glob
    r = glob.glob(re.sub(r'([^:/\\])(?=[/\\]|$)', r'[\1]', source_path))
    return r and r[0] or source_path


def copy_xgen_tex_mat(ref_path, net_tex_path):
    # 参考工具参考高模时，没有拷贝贴图。
    if re.search(r'High', os.path.dirname(ref_path)):
        # 拷贝xgen数据文件
        net_xgen_path = os.path.dirname(ref_path).split('High')[0].replace('Rig', 'Xgen')
        local_xgen_path = net_xgen_path.replace('X:', 'L:')
        GCopy.mirror_dir_to_dir(net_xgen_path, local_xgen_path, default_shell=True)

        # 拷贝xgen配置文件
        scene_name = os.path.splitext(os.path.basename(ref_path))[0]
        source_dir = os.path.dirname(ref_path)
        xgen_configure = ""
        for each_file in os.listdir(source_dir):
            if re.match("{}\w+\.xgen".format(scene_name), each_file):
                xgen_configure = os.path.join(source_dir, each_file).replace("\\", "/")
                break
        if xgen_configure:
            local_xgen_configure = xgen_configure.replace("X:/", "L:/")
            copy_file_with_md5(xgen_configure, local_xgen_configure)

        # 拷贝mat文件
        net_mat_path = os.path.join(os.path.dirname(ref_path), 'mat').replace('Rig', 'Mod').replace('\\', '/')
        local_mat_path = net_mat_path.replace('X:', 'L:')
        if not os.path.isfile(local_mat_path):
            GCopy.mirror_dir_to_dir(net_mat_path, local_mat_path, default_shell=True)
    else:
        # 拷贝部分贴图文件
        if net_tex_path:
            for tex in net_tex_path:
                local_tex = convert_path_from_net_to_local(tex)
                copy_file_with_md5(tex, local_tex)


def get_surface_file(source_dir, mat):
    if "Surfacing" not in source_dir:
        mod_index = source_dir.rfind("/Mod") if "/Mod" in source_dir else source_dir.rfind("/Rig")
        surface_folder = os.path.join(source_dir[:mod_index], "Surfacing").replace("\\", "/")
    else:
        surface_folder = source_dir
    try:
        if mat:
            if "mat" not in surface_folder:
                surface_folder = os.path.join(surface_folder, "mat")
            surface_file_list = sorted([file_name for file_name in os.listdir(surface_folder)
                                        if is_mat(file_name)])
        else:
            surface_file_list = sorted([file_name for file_name in os.listdir(surface_folder)
                                        if is_asset(file_name)])
    except WindowsError:
        surface_file_list = []
    return surface_file_list


def is_abc(file_name):
    return re.match(r".*_(H|L|surf)_geom_grp.abc({\d*})?$", file_name)


def is_asset(file_name):
    return re.match(r".*_(H|L|surf)_v\d{3}.ma({\d*})?$", file_name)


def is_mat(file_name):
    return re.match(r".*_(H|L|surf)_v\d{3}_mat.ma({\d*})?$", file_name)


def open_explorer(dir_path):
    try:
        os.startfile(os.path.realpath(dir_path))
    except WindowsError:
        return False
    return True


def open_explorer_on_file(file_path):
    subprocess.Popen(r'explorer /select,%s' % os.path.realpath(file_path))


def is_updated(source_dir, fetched_dir):
    """
    compare version from two path

    Returns:

    """
    group1 = re.search(r"/?(\w*)_v([\d]{3})", source_dir).groups()
    group2 = re.search(r"/?(\w*)_v([\d]{3})", fetched_dir).groups()
    if group1[0] != group2[0]:
        # 必须保持结构一致才能比较版本
        return False
    return fetched_dir if int(group1[1]) < int(group2[1]) else False


def get_scene_info(file_path):
    reg = re.match("X:/Projects/(\w+)/Publish/Sequence/Assembly/(\w+)/(\w+)", file_path)
    if reg:
        return reg.group(1), reg.group(2), reg.group(3)
    else:
        return None, None, None


def fetch_latest_assembly(project, eps, shot):
    """
    Args:
        project: str - The selected project
        eps: str - The specified scene
        shot: str - The specified shot

    Returns:
        assembly_lgt_dir: iter - The latest assembly directory and version if exist, else return None
    """
    assembly_root_dir = "X:/Projects/{}/Publish/Sequence/Assembly".format(project)
    try:
        assembly_scene_dir = os.path.join(assembly_root_dir, eps, shot).replace("/", "\\")
        if assembly_scene_dir and os.listdir(assembly_scene_dir):
            assembly_latest_version = sorted(os.listdir(assembly_scene_dir)).pop()
            assembly_publish_dir = os.path.join(assembly_scene_dir, assembly_latest_version)
            assembly_lgt_dir = os.path.join(assembly_publish_dir, os.listdir(assembly_publish_dir)[0])

            return assembly_publish_dir.replace("\\", "/"), assembly_latest_version
    except Exception as e:
        print e
        return None, None


def get_abc_geo_name_space(mat_name_space):
    import maya.cmds as cmds
    top_dag_name = cmds.ls(assemblies=1)
    name_space_list = []
    if top_dag_name:
        for ref_dag in top_dag_name:
            # 返回找到的Group名字
            if re.match(".*?:geom_grp", ref_dag):
                name_space = ref_dag.split(":geom_grp")[0]
                if name_space.split("_")[0] == mat_name_space.split("_")[0]:
                    name_space_list.append(name_space)
    return name_space_list


def get_matched_asset(ref_file_path, mat, check_update=True):
    import maya.cmds as cmds
    matched_assets_list = []
    ref_dir = os.path.dirname(ref_file_path).replace("\\", "/")
    ref_file_name = os.path.basename(ref_file_path)
    project, eps, shot = get_scene_info(ref_file_path)
    surface_flag = False
    if "abc_files" in ref_dir:
        if project:
            lgt_dir, assembly_ver = fetch_latest_assembly(project, eps, shot)
            lgt_file_path = concat_path_with_slash(lgt_dir, "abc_files", ref_file_name)
            if lgt_dir:
                if not os.path.isfile(lgt_file_path) or is_updated(ref_dir, lgt_dir):
                    matched_assets_list = [(lgt_dir, assembly_ver, eps, shot)]

                #     ref_ns = cmds.referenceQuery(ref_file_path, ns=1).split(":")[-1]
                #     cmds.file(ref_file_path, rr=1)
                #     if cmds.namespace(ex=ref_ns):
                #         cmds.namespace(rm=ref_ns, dnc=1)
                #
                # if is_updated(ref_dir, lgt_dir):
                #     matched_assets_list = [(lgt_dir, assembly_ver, eps, shot)]

    else:
        if "Low" in ref_file_path or "Rig" in ref_file_path and check_update:
            surface_file_list = []
        else:
            surface_file_list = get_surface_file(ref_dir, mat)
        if surface_file_list:
            matched_assets_list = surface_file_list
            surface_flag = True
        else:
            if mat:
                matched_assets_list = sorted([file_name for file_name in os.listdir(ref_dir) if is_mat(file_name)])
            else:
                matched_assets_list = sorted([file_name for file_name in os.listdir(ref_dir) if is_asset(file_name)])
        if not matched_assets_list:
            return matched_assets_list, surface_flag
        latest_file = sorted(matched_assets_list)[-1]
        ref_file_base = os.path.basename(ref_file_path)
        # 如果存在重复文件序号则去掉
        try:
            duplicate_num = re.match(r".*_(H|L|surf)_v\d{3}.ma({\d*})?$", ref_file_base).group(2)
            if duplicate_num:
                ref_file_base = ref_file_base.replace(duplicate_num, "")
        except Exception as e:
            pass
        if check_update:
            if not is_updated(ref_file_base, latest_file) and latest_file == ref_file_base:
                # 单从版本号无法判断surf流程的文件，加入文件名不同来区分
                matched_assets_list = []
    return sorted(matched_assets_list), surface_flag


def is_debug_mode():
    from gvf_globals import task_globals
    td_flag = False
    try:
        with open(task_globals.gvf_mod_file, "r") as f:
            file_content = f.read()
        if "D:\gvfpipe" in file_content:
            td_flag = True
    except Exception as e:
        print(str(e))
    return td_flag


def get_xgen_info():
    import xgenm as xg
    xgen_collection_list = xg.palettes()
    xgen_info_dict = {}
    for collection in xgen_collection_list:
        xgen_info_dict.update({collection: xg.descriptions(collection)})
    return xgen_collection_list, xgen_info_dict


def import_xgen_curve():
    import maya.cmds as cmds
    import xgenm as xg
    from gvf_globals import task_globals

    # X:\Projects\test2\Publish\Sequence\Cfx\sc001\shot001\cache\cfx_v004\xgen_abc
    base_path = os.path.join("X:/Projects", task_globals.current_project_env, "Publish/Sequence/Cfx",
                             task_globals.scene, task_globals.shot, "cache").replace("\\", "/")
    if not os.listdir(base_path):
        return False, u"导入失败：相应cfx发布路径下无可用缓存"

    latest_version = sorted([folder for folder in os.listdir(base_path)])[-1]
    curve_file_path = ""
    for dir, sub_dir, file in os.walk(os.path.join(base_path, latest_version)):
        if dir.endswith("xgen_abc"):
            curve_file_path = dir

    xgen_collection_name, xgen_layer_info = get_xgen_info()
    if not xgen_collection_name:
        return False, u"导入失败：当前场景无xgen毛发"

    # collection_name ：在ma文件中的曲线文件夹---'ella_rig_H:Ella_TF_COLL'
    if os.path.isdir(curve_file_path):
        for collection_name in xgen_collection_name:
            dec_path_dict = {}
            char_name = re.match(r"(.*):(.*)?", collection_name).group(1)

            # xgen.abc文件所在路径
            xgen_abc_info_path = os.path.join(curve_file_path, char_name)
            if os.path.isdir(xgen_abc_info_path):
                for root, dirs, files in os.walk(xgen_abc_info_path):
                    for file in files:
                        if file.endswith('.abc'):
                            filename, extenison = os.path.splitext(file)
                            dict_curve_dec = char_name + ":" + filename
                            new_path = os.path.join(root, file).replace("\\", "/")
                            dec_path_dict[dict_curve_dec] = new_path

                for description_name in xgen_layer_info[collection_name]:
                    if description_name in dec_path_dict:
                        set_path = dec_path_dict[description_name]

                        xg.setAttr("useCache", "true", str(collection_name), str(description_name),
                                   "SplinePrimitive")
                        xg.setAttr("liveMode", "flase", str(collection_name), str(description_name),
                                   "SplinePrimitive")
                        xg.setAttr("cacheFileName", str(set_path), str(collection_name), str(description_name),
                                   "SplinePrimitive")
                        cmds.xgmSetActive(d=str(description_name), o="RandomGenerator")
            else:
                print(u"{}无毛发缓存".format(char_name))

    else:
        return False, u"导入失败：相应目录下没有xgen_abc文件夹"
    return True, ""


try:
    import GCloudService


    class FtpHandler:
        @staticmethod
        def upload_download_handler(src_path, dst_path, method, drive=GCloudService.DRIVE_PROJ):
            """
            网盘路径只能使用全路径，方便判断源路径与目标路径对象是不是一致，只能同为文件或是目录，以源路径为基准
            :param src_path: 源路径，指向可以是文件或是目录
            :param dst_path: 目标路径，指向可以是文件或是目录
            :param method: "upload" or "download"，指定操作是上传或是下载
            :param drive: 操作的网盘，默认是X盘
            :return: 操作成功返回 "success", True；失败返回 错误信息， False
            """
            # 文件
            if os.path.isfile(src_path):
                if os.path.isdir(dst_path):
                    dst_path = os.path.join(dst_path, os.path.basename(src_path))
                if method == "upload":
                    return FtpHandler.upload_file(src_path, dst_path, drive)
                elif method == "download":
                    return FtpHandler.download_file(src_path, dst_path, drive)

            # 目录
            elif os.path.isdir(src_path):
                if os.path.isfile(dst_path):
                    dst_path = os.path.dirname(dst_path)
                if method == "upload":
                    return FtpHandler.upload_dir(src_path, dst_path, drive)
                elif method == "download":
                    return FtpHandler.download_dir(src_path, dst_path, drive)

        @staticmethod
        def upload_file(src_file, dst_file, drive=GCloudService.DRIVE_PROJ):
            ftp = GCloudService.Ftp(drive=drive)  # 指定要交互的盘符

            try:
                ftp.upload_file(
                    local_file_path=src_file,  # 本地的路径
                    save_to_nas_path=dst_file  # 网盘文件路径
                )
            except Exception as e:
                return e, False
            finally:
                ftp.disconnect()
            return "success", True

        @staticmethod
        def upload_dir(src_dir, dst_dir, drive=GCloudService.DRIVE_PROJ):
            ftp = GCloudService.Ftp(drive=drive)  # 指定要交互的盘符

            # 扫描目标所有 文件，文件夹
            file_list, dir_list = ftp.scan_local_dir(local_dir=src_dir)

            try:
                # 创建空文件夹
                for relative_dir in dir_list:
                    absolute_dir = os.path.join(dst_dir, relative_dir)
                    ftp.make_dirs(absolute_dir)

                # 上传所有文件
                for file_meta in file_list:
                    ftp.upload_file(
                        local_file_path=os.path.join(src_dir, file_meta["file_path"]),
                        save_to_nas_path=os.path.join(dst_dir, file_meta["file_path"])
                    )
            except Exception as e:
                return e, False
            finally:
                ftp.disconnect()
            return "success", True

        @staticmethod
        def download_file(src_file, dst_file, drive=GCloudService.DRIVE_PROJ):
            ftp = GCloudService.Ftp(drive=drive)  # 指定要交互的盘符

            try:
                ftp.download_file(
                    nas_file_path=src_file,  # 网盘文件路径
                    save_to_path=dst_file  # 本地的路径
                )
            except Exception as e:
                return e, False
            finally:
                ftp.disconnect()
            return "success", True

        @staticmethod
        def download_dir(src_dir, dst_dir, drive=GCloudService.DRIVE_PROJ):
            ftp = GCloudService.Ftp(drive=drive)  # 指定要交互的盘符

            # 扫描目标所有 文件，文件夹
            file_list, dir_list = ftp.scan_remote_dir(nas_dir=src_dir)

            # 创建空文件夹
            for relative_dir in dir_list:
                absolute_dir = os.path.join(dst_dir, relative_dir)
                try:
                    os.makedirs(absolute_dir)
                except:
                    pass

            # 下载所有文件
            for file_meta in file_list:
                try:
                    ftp.download_file(
                        nas_file_path=os.path.join(src_dir, file_meta["file_path"]),
                        save_to_path=os.path.join(dst_dir, file_meta["file_path"])
                    )
                except Exception as e:
                    return e, False
            return "success", True

except:
    pass


class StayOnTopMessageBox:
    from dayu_widgets.qt import QMessageBox, Qt

    def __init__(self):
        pass

    @staticmethod
    def create_message_box(icon, title, content, button, parent, window_flags, block_flag=False):

        """
        @param icon: such as QMessageBox.Information,QMessageBox.Warning
        @param title: title of the message box
        @param content: content of the message box
        @param button: first button in message box
        @param parent: parent Qt object
        @param block_flag: 是否阻塞
        """
        from dayu_widgets.qt import QMessageBox, Qt
        msg_box = QMessageBox(icon, title, content, button, parent, window_flags)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
        if block_flag:
            return msg_box.exec_()
        else:
            return msg_box.open()

    # 以下三个方法指定按键有概率会出问题，建议只传parent, title, content三个参数
    @classmethod
    def information(cls, parent, title, content, button=QMessageBox.NoButton, icon=QMessageBox.Information,
                    window_flags=Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint, block_flag=False):
        cls.create_message_box(icon, title, content, button, parent, window_flags, block_flag)

    @classmethod
    def question(cls, parent, title, content, button=QMessageBox.Yes | QMessageBox.No, icon=QMessageBox.Question,
                 window_flags=Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint, block_flag=False):
        return cls.create_message_box(icon, title, content, button, parent, window_flags, block_flag)

    @classmethod
    def warning(cls, parent, title, content, button=QMessageBox.NoButton, icon=QMessageBox.Warning,
                window_flags=Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint, block_flag=False):
        cls.create_message_box(icon, title, content, button, parent, window_flags, block_flag)


def convert_path_from_net_to_local(path, reverse=False, local_disk="L:"):
    import gvf_globals
    if not reverse:
        for net_disk in gvf_globals.net_disk_list:
            path = path.replace(net_disk, local_disk).replace("\\", "/")
    else:
        net_disk, project = get_project_disk(path)
        path = path.replace(local_disk, net_disk).replace("\\", "/")
    return path


def get_project_disk(project_file_path):
    import gvf_globals
    project = "default"
    for project_name in gvf_globals.proj_disk_dict.keys():
        if project_name in project_file_path:
            project = project_name
    project_disk = gvf_globals.proj_disk_dict.get(project)
    if project == "default":
        # "X:/Projects/BXS/Publish/Assets/Char/GongLu/Rig/Low/GongLu_rig_L_v002.ma"
        try:
            project = project_file_path.split("/", 3)[2]
        except Exception as e:
            print "invalid file path:{}".format(project_file_path)
            raise e
    return project_disk, project


def get_project_folder(project_file_path):
    project_disk, project_name = get_project_disk(project_file_path)
    project_end_index = project_file_path.index(project_name) + len(project_name)
    project_folder = project_file_path[:project_end_index]
    return project_folder


def get_custom_material_list():
    import maya.cmds as cmds
    sg_list = cmds.ls(type="shadingEngine")
    default_sg_list = [u'initialParticleSE', u'initialShadingGroup']
    custom_sg_list = []
    for sg in sg_list:
        if sg not in default_sg_list:
            custom_sg_list.append(sg)
    custom_material_list = cmds.ls(cmds.listConnections(custom_sg_list), materials=1)
    return custom_material_list


def get_custom_top_node_list(node_type=None):
    if node_type is None:
        node_type = []
    import maya.cmds as cmds
    available_node_type_list = ["transform"]
    available_node_type_list.extend(node_type)
    default_node_list = [u"persp", u"front", u"back", u"top", u"bottom", u"side", u"left", u"right", u'animBot']
    custom_top_node_list = []
    for top_node in cmds.ls(assemblies=1):
        if top_node not in default_node_list and cmds.nodeType(top_node) in available_node_type_list:
            custom_top_node_list.append(top_node)
    return custom_top_node_list


def recursive_merge_dict(source_dict, update_dict):
    """
        递归合并字典
        :param source_dict: {"a": {"c": 2, "d": 1}, "b": 2}
        :param update_dict: {"a": {"c": 1, "f": {"zzz": 2}}, "c": 3, }
        :return: {'a': {'c': 1, 'd': 1, 'f': {'zzz': 2}}, 'b': 2, 'c': 3}
        """
    for key, value in update_dict.items():
        if key not in source_dict:
            source_dict[key] = value
        else:
            if isinstance(value, dict):
                recursive_merge_dict(source_dict[key], value)
            else:
                source_dict[key] = value
    return source_dict


def get_toolkit_base_dir():
    toolkit_name = "gvfpipe"
    current_path = __file__
    root_folder = os.path.dirname(current_path)
    if not root_folder.endswith(toolkit_name):
        root_folder = os.path.dirname(root_folder)
    return root_folder


def add_lib_path(mode=None):
    # LIB_FOLDER_DICT = {
    #     "dev": "D:",
    #     "prod": "V:/TD"
    # }
    # debug_flag = is_debug_mode()
    # if not mode or mode not in LIB_FOLDER_DICT.keys():
    #     mode = "dev" if debug_flag else "prod"
    # root_folder = LIB_FOLDER_DICT[mode]
    root_folder = get_toolkit_base_dir()
    import_path = [
        root_folder + "/dcc_ops/maya/scripts",
        root_folder + "/plugins",
        root_folder + "/pylibs",
        root_folder + "/utils",
        root_folder + "/bin",
        root_folder + "/bin/images",
        root_folder,
    ]
    for path in import_path:
        if path not in sys.path:
            sys.path.insert(0, path)


def time_struct_to_date_str(time_struct):
    # return time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
    return time_struct.isoformat(" ")


def get_file_update_date(file_path):
    timestamp = os.path.getmtime(file_path)
    time_struct = datetime.fromtimestamp(timestamp)
    return time_struct


def check_file_if_latest(source_path, target_path):
    # 比较两个文件的修改日期
    if not os.path.isfile(target_path):
        print "file path:{} not exists.".format(target_path)
        return False
    source_file_date = get_file_update_date(source_path)
    target_file_date = get_file_update_date(target_path)
    print(" ".join([source_path, time_struct_to_date_str(source_file_date)]))
    print(" ".join([target_path, time_struct_to_date_str(target_file_date)]))
    return target_file_date >= source_file_date


def concat_path_with_slash(*args):
    # 跟os.path.join一样，但是返回的路径是/而不是\
    path_str_list = []
    for arg in args:
        try:
            path_str_list.append(ur"{}".format(arg.decode("gbk")))
        except:
            path_str_list.append(arg)
    return os.path.join(*path_str_list).replace("\\", "/")


def solve_uvset_issue(root=None):
    import maya.cmds as cmds
    # 如果原物体的uvset名不为默认名map1，abc导出后会存在两个uvset，虽然选择的uvset是正确的，但是材质效果会出错。
    # 解决方法：在导出abc前 1、如果有默认uv集则将正确的uv集数据复制到默认uv集上 2、如果没有默认uv集则将当前uv集改名为默认uv集
    print "[Fix uvset]"
    default_uv_set = u"map1"
    if root:
        mesh_list = [child for child in cmds.listRelatives(root, ad=1, f=1) if cmds.nodeType(child) == "mesh"]
    else:
        mesh_list = cmds.ls(type="mesh", l=1)
    try:
        for mesh in mesh_list:
            current_uvset = cmds.polyUVSet(mesh, q=1, currentUVSet=1)[0]
            if default_uv_set in cmds.polyUVSet(mesh, q=1, allUVSets=1):
                if current_uvset != default_uv_set:
                    print "copy method............"
                    print mesh, "before uvset:{}".format(current_uvset)
                    cmds.polyUVSet(mesh, copy=1, newUVSet=default_uv_set)
                    try:
                        # cmds.polyUVSet(mesh, delete=True, uvSet=current_uvset)
                        cmds.polyUVSet(currentUVSet=True, uvSet=default_uv_set)
                    except:
                        print "Error occur when delete uvset:{}".format(current_uvset)
                    print mesh, "after uvset:{}".format(cmds.polyUVSet(mesh, q=1, currentUVSet=1)[0])
            else:
                print "rename method............"
                print mesh, "before uvset:{}".format(current_uvset)
                cmds.polyUVSet(mesh, rename=True, uvSet=current_uvset, newUVSet=default_uv_set)
                print mesh, "after uvset:{}".format(cmds.polyUVSet(mesh, q=1, currentUVSet=1)[0])
    except:
        pass


def set_rs_version_env(rs_version="3.0.45", maya_version="2018"):
    # TODO 似乎3.0.5的rs用户不能直接用2.5.48的rs开后台，待测试
    # 主要是用来设置低版本的rs来适配其他机器的环境，所以环境变量中maya的版本号还是默认为18，毕竟maya20也用不了rs2.5..
    # 该函数主要是应对启动maya后环境变量中动态的值就无法再改变了，如果是在没有启动maya的环境下想单独修改rs版本，只需要简单的如下一句
    # os.environ["REDSHIFT_COREDATAPATH"] = "V:/TD/Redshift/2.6.41/Redshift"
    import os
    rs_env_path = r"V:\TD\gvfpipe\dcc_ops\maya\modules\Maya.env"
    rs_root_dir = r"V:\TD\plugins\Redshift\{}\Redshift".format(rs_version)
    env_dict = {}
    maya_version = str(maya_version)
    with open(rs_env_path, "r") as f_read:
        for line_content in f_read.readlines():
            line_content = line_content.strip().replace(" ", "")
            line_content = line_content.replace("{RS_ROOT_DIR}", rs_root_dir)
            line_content = line_content.replace("{VERSION}", maya_version)
            k, v = line_content.split("=")
            env_dict[k] = v

    merged_env_dict = os.environ
    net_rs_path = env_dict["REDSHIFT_COREDATAPATH"]
    local_rs_path = os.environ.get("REDSHIFT_COREDATAPATH", "")
    if local_rs_path:
        for k, v in env_dict.items():
            old_value = os.environ.get(k, "")
            if old_value and local_rs_path in old_value:
                try:
                    merged_env_dict[k] = str(old_value.replace(local_rs_path, net_rs_path))
                except:
                    merged_env_dict[k] = old_value.replace(local_rs_path, net_rs_path)
    else:
        merged_env_dict["REDSHIFT_COREDATAPATH"] = rs_root_dir
    return merged_env_dict


def get_reference_info_from_text(ma_path, read_line_limit=400):
    ref_info_dict = {}
    i = 1
    with open(ma_path, "r") as f_read:
        partial_content = ""
        while i < read_line_limit:
            line_content = f_read.readline().rstrip()
            if not line_content.endswith(";") and line_content.startswith("file"):
                partial_content += line_content
            else:
                full_content = partial_content + line_content
                partial_content = ""
                ref_prefix_pattern = r'file.*-ns "(\w+)".*-rfn "(.+)".*-typ "mayaAscii" "(.*)";'
                match_result = re.match(ref_prefix_pattern, full_content.replace("\t", ""), re.IGNORECASE)
                if match_result:
                    ref_ns, ref_node, ref_file = match_result.groups()
                    ref_info_dict[ref_ns] = ref_file
            i += 1
    return ref_info_dict


def get_custom_camera():
    """
    Determines whether the camera in 'cams' has a named camera that satisfies the regular expression.
    Returns:True/False, true_camera/None

    """
    import maya.cmds as cmds
    cam_list = []
    for cam in cmds.listCameras():
        if cmds.nodeType(cam) == "camera":
            cam = cmds.listRelatives(cam, parent=1)[0]
        cam_list.append(cam)

    default_camera_list = [u"persp", u"front", u"back", u"top", u"bottom", u"side", u"left", u"right"]
    true_camera = cam_list[:]
    for cam in true_camera[:]:
        if cam.split("|")[-1] in default_camera_list:
            true_camera.remove(cam)
    return true_camera


def clean_unknown_transform():
    import maya.cmds as cmds
    for node in cmds.ls(type="unknownTransform") or []:
        grand_parent_node = cmds.listRelatives(node, p=1)
        for child_node in cmds.listRelatives(node, c=1) or []:
            if grand_parent_node:
                cmds.parent(child_node, grand_parent_node)
            else:
                cmds.parent(child_node, w=1)
        try:
            cmds.lockNode(node, lock=0)
            cmds.delete(node)
        except Exception:
            pass


def get_texture_path():
    # be careful udim
    import maya.cmds as cmds
    path_dict = {}
    textures_list = cmds.ls(type="file")
    try:
        rs_list = cmds.ls(type=["RedshiftNormalMap", "RedshiftSprite"])
    except:
        rs_list = []

    for file_node in textures_list:
        file_path = cmds.getAttr(file_node + ".ftn")
        path_dict[file_node + ".ftn"] = file_path
    for rs_node in rs_list:
        file_path = cmds.getAttr(rs_node + ".tex0")
        path_dict[rs_node + ".tex0"] = file_path

    return path_dict


def get_folder_latest_file(source_folder):
    filename_date_list = [(file_name, get_file_update_date(os.path.join(source_folder, file_name))) for file_name in
                          os.listdir(source_folder)]
    filename_date_list = sorted(filename_date_list, key=lambda container: container[-1])
    return filename_date_list[-1][0]


def get_publish_version(publish_folder):
    version_list = []
    for sub_name in os.listdir(publish_folder):
        match_result = re.match(".*v(\d{3}).*", sub_name)
        if match_result:
            version_list.append(int(match_result.group(1)))
    version_list.sort()
    publish_version_num = version_list[-1] + 1 if version_list else 1
    return "v{:03d}".format(publish_version_num)


def force_del(file_name):
    command_line = 'del /a /f /q "%s"' % (file_name)
    subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                     stderr=subprocess.STDOUT)
    print(command_line)


def ssh_scp_copy(source_file_path, targe_file_path):
    user_name = getpass.getuser()  # 获取当前用户名
    dot_ssh_path = 'C:/Users/' + user_name + '/.ssh'
    rsa_file = "/".join([dot_ssh_path, "id_rsa"])
    source_file_path = source_file_path.replace('\\', '/').replace('//', '/')
    targe_file_path = targe_file_path.replace('\\', '/').replace('//', '/').replace("X:/", "")
    targe_file_path = "/".join(["root@10.10.20.102:/mnt/jcdatabak/Projects", targe_file_path])
    if not os.path.exists(rsa_file):
        if not os.path.exists(os.path.dirname(rsa_file)):
            os.mkdir(os.path.dirname(rsa_file))
        import shutil
        shutil.copyfile("V:/TD/gvfpipe/plugins/tw_toolkit/GvfPublishTool/id_rsa", rsa_file)
    command_line = 'scp -p -i "%s" -o StrictHostKeyChecking=no "%s" "%s"' % (
        rsa_file, source_file_path, targe_file_path)
    proc = subprocess.Popen(command_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True,
                            stderr=subprocess.STDOUT)
    while proc.poll() is None:
        try:
            line = proc.stdout.readline()
        except:
            line = proc.stdout.readline().decode("gb18030", errors="ignore")
        if u"系统找不到指定的文件" in line or "No such file or directory" in line:
            print(targe_file_path)
            raise Exception("source_file_path or targe_file_path may be wrong.")  # 目标文件夹也应该存在


def read_fileline_generator(file, size=1024 * 1024):
    while 1:
        data = file.read(size)
        if not data:
            break
        yield data


def fix_ref_edit_history():
    import maya.cmds as cmds
    for ref_node in cmds.ls(rf=1):
        for edit_history in cmds.referenceQuery(ref_node, editStrings=1, failedEdits=1, successfulEdits=1):
            texture_suffix = "fileTextureName"
            weight_suffix = "skinCluster"
            if texture_suffix in edit_history or weight_suffix in edit_history:
                edit_content_list = edit_history.replace('"', "").split(" ")
                edit_command = edit_content_list[0]
                edit_attr = edit_content_list[1] if edit_command != "disconnectAttr" else edit_content_list[2]
                cmds.referenceEdit(edit_attr, failedEdits=1, successfulEdits=1, editCommand=edit_command, removeEdits=1)


def set_anim_file_path_to_net(file_path):
    new_content_list = []
    with open(file_path, "r") as f_read:
        for old_content in f_read.readlines():
            new_content_list.append(get_new_content(old_content))
    with open(file_path, "w") as f_write:
        f_write.writelines(new_content_list)


def get_new_content(old_content):
    new_content = old_content
    if task_globals.current_project_env == "WGJS":
        pattern = r'"([LXP]:)/WGJS_FJ_Project/WGJS_FJ/Project/Assets/\w+/\w+/mod/\w+.ma"'
        match_result = re.search(pattern, new_content, re.I)
        if match_result:
            reference_path = match_result.group().strip('"')
            old_disk = match_result.group(1)
            net_reference_path = convert_path_from_net_to_local(reference_path, True, old_disk)
            if task_globals.pipeline == "Anim":
                # 动画替换高模
                net_reference_path = net_reference_path.replace("_lowrig", "_rig")
            new_content = old_content.replace(reference_path, net_reference_path)
    else:
        pattern = r'"[L|X]:/Projects/(\w+)/Publish/Assets/(\w+)/(\w+)/.*.ma"'
        match_result = re.search(pattern, old_content, re.IGNORECASE)
        if match_result:
            old_asset_path = match_result.group().strip('"')
            net_asset_path = convert_path_from_net_to_local(old_asset_path, True)
            new_asset_folder = os.path.dirname(net_asset_path)
            print new_asset_folder
            try:
                new_asset_name = \
                    sorted([file_name for file_name in os.listdir(new_asset_folder) if file_name.endswith(".ma")])[
                        -1]
                new_asset_path = concat_path_with_slash(new_asset_folder, new_asset_name)
                new_content = new_content.replace(old_asset_path, new_asset_path)
                print new_asset_path
            except:
                print "no file in folder:{}".format(new_asset_folder)
    return new_content


if __name__ == '__main__':
    # print is_updated(r"X:\Projects\LittleEmma\Publish\Sequence\Assembly\sc009\shot013\assembly_v001\sc009_shot013_ani_v003_lighting",
    #                  r"X:\Projects\LittleEmma\Publish\Sequence\Assembly\sc009\shot013\assembly_v002")
    # print get_matched_asset(r"X:/Projects/LittleEmma/Publish/Assets/Char/Emma/Mod/High\Emma_mod_H_v021__Wbear_mod_H_v006__bear_COLL.xgen",
    source_file_path = r"X:\Projects\LittleEmma\Publish\Sequence\Assembly\sc017c\shot009\assembly_v003\sc017c_shot009_ani_v003__BirdA_rig_H__ns__Feather_COLL.abc"
    target_file_path = r"X:\Projects\LittleEmma\Work\Sequence\Lgt\sc017c\shot009\sc017c_shot009_lgt_bg_101_137_v002__BirdA_rig_H__ns__Feather_COLL.abc"
    print os.stat(source_file_path).st_mtime
    print os.stat(target_file_path).st_mtime
