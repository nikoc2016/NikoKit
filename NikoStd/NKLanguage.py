# encoding=utf-8
from NikoKit.NikoStd import NKConst


class NKLanguage:
    def __init__(self):
        self.dictionaries = {
            NKConst.ZH_CN: {
                "UNLOAD": u"未加载",
                "LOADING": u"加载中",
                "UPDATING": u"更新中",
                "CLEARING": u"清理中",
                "LOADED": u"已加载",
                "LOAD_ERROR": u"加载错误",
                "ALL": u"全部",
                "UNGROUPED": u"未分组",
                "valid": u"合法",
                "invalid": u"非法",
                "analysis": u"分析",
                "day": u"日",
                "week": u"周",
                "month": u"月",
                "year": u"年",
                "start": u"开始",
                "end": u"结束",
                "name": u"名字",
                "error": u"错误",
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
                "log": u"记录",
                "logs": u"日志",
                "animate": u"动画",
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
                "window": u"窗口",
                "NQWindowDataLoader": u"数据加载管理器",
                "data": u"数据",
                "pack": u"包",
                "status": u"状态",
                "time": u"时间",
                "task": u"任务",
                "gap": u"间隔",
                "update": u"更新",
                "available": u"可用",
                "operation": u"操作",
                "next_time": u"下次",
                "countdown": u"倒数",
                "selection": u"选择",
                "chosen": u"选中",
                "holiday": u"节假日",
                "project": u"项目",
                "employee": u"员工",
                "statistic": u"统计",
                "immediately": u"立即",
                "preview": u"预览",
                "welcome_back": u"欢迎回来",
                "show": u"显示",
                "detail": u"详情",
                "reason": u"原因",
                "i_understand": u"我知道了",
                "execute": "执行",
                "console": "控制台",
                "file": "文件",
                "send": "发送",
                "ctime": "修改时间",
                "atime": "访问时间",
                "size": "大小",
                "path": "路径"
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
