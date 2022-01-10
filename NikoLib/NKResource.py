import os
import os.path as p

from NikoKit.NikoLib.NKFileSystem import get_base64_from_file, scout

NK_RES_CODE = "NKRes = %s"


def pack_dir_to_res(res_dir, res_lib_path, ext_list=None):
    if p.isdir(res_dir) and os.listdir(res_dir):

        pack_targets = {}
        for root, dirs, files in os.walk(res_dir):
            for file in files:
                if ext_list and p.splitext(file)[1] not in ext_list:
                    continue

                if file in pack_targets.keys():
                    raise Exception("Duplicate file:" + file)
                else:
                    pack_targets[file] = p.join(root, file)

        base64_file_dict = {}

        for pack_file_name, pack_file_path in pack_targets.items():
            base64_file_dict[pack_file_name] = get_base64_from_file(pack_file_path)

        try:
            scout(res_lib_path)
            os.remove(res_lib_path)
        except:
            pass

        with open(res_lib_path, "w") as f:
            f.write(NK_RES_CODE % str(base64_file_dict))
