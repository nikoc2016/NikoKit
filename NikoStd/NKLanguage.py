# encoding=utf-8
from NikoKit.NikoStd import NKConst


class NKLanguage:
    def __init__(self):
        self.dictionaries = {
            NKConst.ZH_CN: {
                "UNLOAD": "未加载",
                "LOADING": "加载中",
                "UPDATING": "更新中",
                "CLEARING": "清理中",
                "LOADED": "已加载",
                "LOAD_ERROR": "加载错误",
                "test": u"测试",
                "hello": u"你好",
                "and": u"和",
                "or": u"或",
                "correct": u"正确",
                "incorrect": u"不正确",
                "account": u"账户",
                "username": u"用户名",
                "password": u"密码",
                "remember": u"记住",
                "auto": u"自动",
                "login": u"登录",
                "animation": u"动画",
                "asset": u"资产",
                "texture": u"贴图",
                "fx": u"特效",
                "art": u"美术",
                "assemble": u"组装",
                "import": u"导入",
                "export": u"导出",
                "light": u"灯光",
                "render": u"渲染",
                "kpi": u"绩效",
                "panel": u"面板",
                "load": "加载",
                "download": u"下载",
                "clear": u"清空",
                "all": u"全部",
                "apply": u"应用",
                "setting": u"设置",
                "NQWindowDataLoader": u"数据加载管理器",
                "data": "数据",
                "pack": "包",
                "status": "状态",
                "time": "时间",
                "gap": "间隔",
                "update": "更新",
                "available": "可用",
                "operation": "操作",
                "next_time": "下次",
                "countdown": "倒数",
            }
        }
        self.chosen_language = NKConst.ZH_CN

    def patch(self, language, patch_pack):
        self.dictionaries[language].update(patch_pack)

    def tran(self, lang_key):
        try:
            return self.dictionaries[self.chosen_language][lang_key]
        except:
            return lang_key + " "
