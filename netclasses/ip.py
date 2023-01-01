from .ip_class import IPClass

class IP:
    def __init__(self, ipString : str):
        self.ipString = ipString
        self.ipParts = IP.divide(self.ipString)
        self.ipClass = IPClass.category(int(self.ipParts[0], 2))

    def _intToBinStr(value : int) -> str:
        s = bin(value)[2:]
        return s.rjust(8, "0")

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
            ipf.append(IP._intToBinStr(intVal))

        return ipf