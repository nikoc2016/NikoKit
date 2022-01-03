# encoding=utf-8
from NikoKit.NikoStd import NKConst

LANGUAGE_CHOSEN = NKConst.ZH_CN
LANGUAGE_TABLE = {
    NKConst.ZH_CN: {
        "hello": u"你好"
    }
}


def tran(lang_key):
    try:
        return LANGUAGE_TABLE[LANGUAGE_CHOSEN][lang_key]
    except:
        return lang_key
