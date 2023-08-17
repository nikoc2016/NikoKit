# encoding=utf-8
from NikoKit.NikoStd import NKConst


class NKLanguage:
    def __init__(self):
        self.dictionaries = {
            NKConst.ZH_CN: {
                "backup": u"备份",
                "UNLOAD": u"未加载",
                "LOADING": u"加载中",
                "UPDATING": u"更新中",
                "CLEARING": u"清理中",
                "LOADED": u"已加载",
                "LOAD_ERROR": u"加载错误",
                "ALL": u"全部",
                "UNGROUPED": u"未分组",
                "advance_setting": u"高级设置",
                "copy": u"复制",
                "paste": u"粘贴",
                "compare": u"对比",
                "valid": u"合法",
                "invalid": u"非法",
                "analysis": u"分析",
                "enable": u"启用",
                "disable": u"禁用",
                "disabled": u"已禁用",
                "browse": u"浏览",
                "day": u"日",
                "week": u"周",
                "month": u"月",
                "year": u"年",
                "hour": u"小时",
                "minute": u"分钟",
                "second": u"秒",
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
                "drag_and_drop": u"拖拽并放置在此处",
                "drag_and_drop_file": u"拖拽文件并放置在此处",
                "drag_and_drop_dir": u"拖拽文件夹并放置在此处",
                "drag_and_drop_file_or_dir": u"拖拽(文件/文件夹)并放置在此处",
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
                "switch": u"切换",
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
                "launch": u"启动",
                "reason": u"原因",
                "i_understand": u"我知道了",
                "execute": "执行",
                "generate": "生成",
                "console": "控制台",
                "file": "文件",
                "send": "发送",
                "ctime": "修改时间",
                "atime": "访问时间",
                "size": "大小",
                "path": "路径",
                "submit": "提交",
                "run": "运行",
                "stop": "停止",
                "restart": "重启",
                "channel": "频道",
                "quit": "退出",
                "select": "选择",
                "select_all": "全选",
                "select_inverse": "反选",
                "select_none": "不选",
                "confirm": "确定",
                "refresh": "刷新",
                "frequency": "频率",
                "tool": "工具",
                "module": "模块",
                "search": "搜索",
                "seat": "座位",
                "number": "数字",
                "succeed": "成功",
                "fail": "失败",
                "result": "结果",
                "save_settings": "保存设置",
                "remove_invalid_urls": "删除无效路径",
                "compress": "压缩",
                "7z_compress_src": "压缩文件夹",
                "7z_out_dir": "输出文件夹",
                "7z_out_filename": "输出文件名",
                "7z_compress_level": "压缩等级(L)",
                "7z_dictionary_size": "字典大小(D)",
                "7z_word_size": "单词大小(W)",
                "7z_solid_block_size": "固实数据大小",
                "7z_cpu_threads": "CPU线程数(最多%i)",
                "7z_memory_usage": "允许使用的系统内存",
                "7z_split_to_volumes_mb": "分卷大小(MB)",
                "7z_remove_src": "操作完成后删除源文件",
            }
        }
        self.chosen_language = NKConst.ZH_CN

    def patch(self, language, patch_pack):
        self.dictionaries[language].update(patch_pack)

    def tran(self, *args):
        result = ""
        for arg in args:
            try:
                result += self.dictionaries[self.chosen_language][arg]
            except:
                result += arg + " "
        return result
