import json

import requests
from requests.adapters import HTTPAdapter


class NKOpenHM:
    def __init__(self, json_url="http://localhost:8085/data.json", silent_mode=False):
        self.silent_mode = silent_mode
        self.json_url = json_url

    def get_json(self):
        return requests.get(self.json_url, timeout=1).json()

    @classmethod
    def _add_package(cls, packages, current_node):
        if "Children" in current_node.keys():
            packages.append(current_node)
            for child_node in current_node["Children"]:
                cls._add_package(packages, child_node)

    def extract_cpus(self, ohm_packs):
        cpu_packs = []
        for pack in ohm_packs:
            try:
                if (pack["Children"][0]["Text"] == "Clocks" and
                        pack["Children"][1]["Text"] == "Temperatures" and
                        pack["Children"][2]["Text"] == "Load" and
                        pack["Children"][3]["Text"] == "Powers"):
                    cpu_packs.append({
                        "name": pack['Text'],
                        "temp": pack['Children'][1]["Children"][-1]["Value"],
                        "load": pack['Children'][2]["Children"][0]["Value"],
                        "power": pack['Children'][3]["Children"][0]["Value"],
                    })
            except:
                pass
        return cpu_packs

    def extract_gpus(self, ohm_packs):
        gpu_packs = []
        for pack in ohm_packs:
            try:
                if (pack["Children"][0]["Text"] == "Clocks" and
                        pack["Children"][1]["Text"] == "Temperatures" and
                        pack["Children"][2]["Text"] == "Load" and
                        pack["Children"][3]["Text"] == "Fans"):
                    gpu_packs.append({
                        "name": pack['Text'],
                        "temp": pack['Children'][1]["Children"][0]["Value"],
                        "load": pack['Children'][2]["Children"][0]["Value"],
                        "fans": pack['Children'][3]["Children"][0]["Value"],
                        "power": pack['Children'][5]["Children"][0]["Value"],
                    })
            except:
                pass
        return gpu_packs

    def get_snapshot(self):
        ohm_json = self.get_json()
        ohm_packs = []
        self._add_package(ohm_packs, ohm_json)

        return {
            "cpus": self.extract_cpus(ohm_packs),
            "gpus": self.extract_gpus(ohm_packs)
        }

# if __name__ == '__main__':
#     a = NKOpenHM("http://localhost:8085/data.json")
#     print(a.get_snapshot())
