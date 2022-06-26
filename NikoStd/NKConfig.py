import ast
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
                    yaml_config = self.__class__(**config_dict)
                    self.update(yaml_config)
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
            if isinstance(value, int):
                parser.add_argument(f"--{key}", type=int, help=str(value))
            elif isinstance(value, float):
                parser.add_argument(f"--{key}", type=float, help=str(value))
            elif isinstance(value, bool):
                parser.add_argument(f"--{key}", help='True or False', type=ast.literal_eval)
            elif isinstance(value, list):
                parser.add_argument(f"--{key}", action='append', help=str(value), type=str)
            else:
                parser.add_argument(f"--{key}", type=str, help=str(value))

    def patch_from_parser(self, parser, custom_arg_list=None):
        if custom_arg_list:
            arg_dict = vars(parser.parse_args(custom_arg_list))
        else:
            arg_dict = vars(parser.parse_args())
        for key, value in arg_dict.items():
            if value:
                self.__dict__[key] = value
