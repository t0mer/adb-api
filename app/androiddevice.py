from adb_shell.adb_device import AdbDeviceTcp


class AndriodDevice(object):
    id: int
    port: int
    name: str
    ip: str
    device: AdbDeviceTcp

    def __init__(self, id: int, port: int, name: str, ip: str, device: AdbDeviceTcp):
        self.id = id
        self.port = port
        self.name = name
        self.ip = ip
        self.device = device


