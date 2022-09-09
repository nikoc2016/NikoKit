import os.path as p
import yaml

from NikoKit.NikoStd.NKDataStructure import NKDataStructure


class NKConfig(NKDataStructure):
    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            self.__dict__[attr_name] = kwargs[attr_name]

        super(NKConfig, self).__init__()

    def patch_yaml_config(self, yaml_path, silent_mode=False):
        try:
            with open(p.join(yaml_path), "r") as f:
                config_dict = yaml.load(f, Loader=yaml.FullLoader)
                try:
                    self.update_by_dict(config_dict)
                except Exception as e:
                    print("Cfg::yaml cfg patch error:", e)
        except Exception as e:
            if not silent_mode:
                print("Cfg::can't open yaml cfg:", e)

    def save_yaml_config(self, yaml_path, silent_mode=False):
        try:
            with open(p.join(yaml_path), "w") as f:
                yaml.dump(data=vars(self), stream=f)
        except Exception as e:
            if not silent_mode:
                print("Cfg::save yaml cfg failed:", e)

    def configure_parser(self, parser):
        for key, value in vars(self).items():
            if type(value) == bool:
                parser.add_argument("--%s" % key, action='store_true', help="Default:%s" % value)
                parser.add_argument("--no-%s" % key, dest=key, action='store_false', help="Default:%s" % value)
                parser.set_defaults(**{key: value})
            elif type(value) == int:
                parser.add_argument("--%s" % key, type=int, help=str(value))
            elif type(value) == float:
                parser.add_argument("--%s" % key, type=float, help=str(value))
            elif type(value) == list:
                parser.add_argument("--%s" % key, action='append', help=str(value), type=str)
            else:
                parser.add_argument("--%s" % key, type=str, help=str(value))

    def patch_from_parser(self, parser, custom_arg_list=None):
        if custom_arg_list:
            arg_dict = vars(parser.parse_args(custom_arg_list))
        else:
            arg_dict = vars(parser.parse_args())

        self.update_by_dict(arg_dict)

    def update_by_dict(self, data_dict):
        for key, value in data_dict.items():
            if value:
                self.__dict__[key] = value
