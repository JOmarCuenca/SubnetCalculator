from dataclasses import dataclass
from .ip_class import IPClass

class IP:
    def __init__(self, ipString : str):
        self.ipString = ipString
        self.ipParts = IP.divide(self.ipString)
        self.ipClass = IPClass.category(int(self.ipParts[0], 2))

    def __str__(self) -> str:
        return self.ipString

    def __eq__(self, __o: object) -> bool:
        return __o.ipString == self.ipString

    def intToBinStr(value : int, long = 8) -> str:
        s = bin(value)[2:]
        return s.rjust(long, "0")

    def divide(ip : str) -> list[str]:
        """
        Receives the IP in string form and transforms it into the binary parts
        and returns them in a list.
        """
        ipf = []
        ipParts = ip.split('.')

        assert(len(ipParts) == 4)

        for part in ipParts:
            intVal = int(part)
            assert(intVal < 256)
            ipf.append(IP.intToBinStr(intVal))

        return ipf

@dataclass(frozen=True, eq=True)
class IPSubnet:
    subnetIP: IP
    firstHost: IP
    lastHost:  IP
    broadcastIP: IP

    def __str__(self) -> str:
        parts = [
            f"Subnet_IP = {self.subnetIP}",
            f"Hosts = {self.firstHost} - {self.lastHost}",
            f"Broadcast = {self.broadcastIP}",
        ]

        return " | ".join(parts)