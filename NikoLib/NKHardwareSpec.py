import math
import subprocess

import wmi

from NikoKit.NikoStd import NKConst


class NKHardwareSpec:
    def __init__(self):
        self.snapshot = wmi.WMI()

    def get_cpus(self):
        cpu_data = []
        cpus = self.snapshot.Win32_Processor()
        for cpu in cpus:
            cpu_data.append(
                {
                    "cpu_name": cpu.Name,
                    "cpu_serial": cpu.ProcessorId,
                    "cpu_core": cpu.NumberOfCores
                }
            )
        return cpu_data

    def get_ram(self):
        ram_in_GB = 0
        for i in self.snapshot.Win32_ComputerSystem():
            ram_in_GB += math.ceil(float(i.TotalPhysicalMemory) / (1024 ** 3))
        return ram_in_GB

    def get_mboard(self):
        mainboard = []
        for board_id in self.snapshot.Win32_BaseBoard():
            mboard_info = {
                "mboard_id": board_id.SerialNumber,
                "mboard_name": board_id.Product,
                "mboard_mfr": board_id.Manufacturer,
            }

            # If mboard_id is " " or "To be filled by O.E.M."， OVERRIDE
            if " " in str(mboard_info["mboard_id"]):
                output = subprocess.check_output('wmic csproduct get uuid')
                try:
                    output = output.decode()
                except:
                    pass
                try:
                    output = output.decode(NKConst.SYS_CHARSET)
                except:
                    pass
                mboard_info["mboard_id"] = output.split('\n')[1].strip()

            mainboard.append(mboard_info)
        return mainboard

    def get_hdrive(self):
        hdrive = []
        for hdrive_obj in self.snapshot.Win32_DiskDrive():
            try:
                hdrive.append({
                    "hdrive_id": hdrive_obj.SerialNumber.strip(),
                    "hdrive_name": hdrive_obj.Caption,
                    "hdrive_size_in_GB": int(int(hdrive_obj.Size) // (1000 ** 3)),
                })
            except:
                print("NKMachineSpec::Skip Device(%s, %s, %s)" % (str(hdrive_obj.SerialNumber.strip()),
                                                                  str(hdrive_obj.Caption),
                                                                  str(hdrive_obj.Size)))
        return hdrive

    def get_vcard(self):
        try:
            return self.snapshot.Win32_VideoController()[0].Caption
        except:
            pass
        return None

    def get_mac(self):
        mac_addr = None
        not_match_keywords = ["WAN Miniport", "VMware", "Bluetooth"]

        for record in self.snapshot.WIN32_NetworkAdapter():
            # For each Network Adapter
            if record.MACAddress:
                # Check if correct Network Adapter
                match = True
                for keyword in not_match_keywords:
                    try:
                        if keyword.lower() in str(record.Caption).lower():
                            match = False
                            break
                    except:
                        match = False
                # Found Mac
                if match:
                    mac_addr = str(record.MACAddress).replace(":", ".").lower()
        return mac_addr

    def get_snapshot(self):
        return {
            "cpus": self.get_cpus(),
            "mboards": self.get_mboard(),
            "hdrives": self.get_hdrive(),
            "vcard": self.get_vcard(),
            "ram": self.get_ram(),
            'mac': self.get_mac()
        }
