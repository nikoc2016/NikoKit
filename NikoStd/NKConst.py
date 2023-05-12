import codecs
import locale

COLOR_RED = "#FF4500"
COLOR_BLUE = "#80C8FF"
COLOR_GREEN = "#80FF80"
COLOR_GOLD = "#FFD700"
COLOR_GREY = "#9E9E9E"
COLOR_LIME = "#26CA19"
COLOR_STD_OUT = "#CCCCCC"
COLOR_STD_ERR = "#FA6967"
COLOR_STD_WARNING = "#C19C00"
COLOR_EASY_RED = "#C0504D"
COLOR_EASY_BLUE = "#4F81BD"

ZH_CN = "ZH_CN"
EN_US = "EN_US"

YEAR = "YEAR"
MONTH = "MONTH"
WEEK = "WEEK"
DAY = "DAY"

ALL = "ALL"
GLOBAL = "GLOBAL"
UNGROUPED = "UNGROUPED"

SYS_CHARSET = codecs.lookup(locale.getpreferredencoding()).name
FILETYPES = {
    "FILETYPE_IMAGE": ['pef', 'hv3', 'cbr', 'webp', 'bmp', 'jfif', 'cbz', 'j2k', 'tif', 'crw', 'raf',
                       'rw2', 'png', 'jp2', 'arw', 'cb7', 'ugoria', 'jpeg', 'sr2', 'exif', 'j2c', 'jpf',
                       'psd', 'wdp', 'tga', 'jpm', 'erf', 'mef', 'jpe', 'tiff', 'pnm', 'nrw', 'dng',
                       'gif', 'apng', 'jpc', 'pbm', 'jpx', 'orf', 'cbt', 'mos', 'x3f', 'mrw', '3fr',
                       'heif', 'bpg', 'jxr', 'srw', 'hdr', 'cr2', 'ppm', 'kdc', 'pcx', 'hdp', 'pgm',
                       'dds', 'jpg', 'psb', 'nef'],
    "FILETYPE_VIDEO": ["avi", "wmv", "wmp", "wm", "asf", "mpg", "mpeg", "mpe", "m1v", "m2v", "mpv2",
                       "mp2v", "ts", "tp", "tpr", "trp", "vob", "ifo", "ogm", "ogv", "mp4", "m4v",
                       "m4p", "m4b", "3gp", "3gpp", "3g2", "3gp2", "mkv", "rm", "ram", "rmvb", "rpm",
                       "flv", "mov", "qt", "nsv", "dpg", "m2ts", "m2t", "mts", "dvr-ms", "k3g", "skm",
                       "evo", "nsr", "amv", "divx", "webm", "wtv", "f4v", "mxf"],
    "FILETYPE_AUDIO": ["wav", "wma", "mpa", "mp2", "m1a", "m2a", "mp3", "ogg", "m4a", "aac", "mka",
                       "ra", "flac", "ape", "mpc", "mod", "ac3", "eac3", "dts", "dtshd", "wv", "tak",
                       "cda", "dsf", "tta", "aiff", "aif", "opus", "amr"]
}