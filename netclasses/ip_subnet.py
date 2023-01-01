from dataclasses import dataclass
from .ip import IP


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


@dataclass(frozen=True, eq=True)
class IPSubnetCollection:
    segmentIP: IPSubnet
    subnets: list[IPSubnet]
    broadcastIP: IPSubnet
    
    mask : IP

    def __str__(self) -> str:
        parts = [
            "The range of the segment (which cannot be used) is:",
            str(self.segmentIP),
            "\n"
            "The range of overall broadcast address (which cannot be used) is:",
            str(self.broadcastIP),
            "",
            f"The subnet mask is -> {self.mask}",
            "",
        ]

        for i, subnet in enumerate(self.subnets):
            parts.extend([
                f"The subnet number -> {i + 1}",
                str(subnet),
                "",
            ])

        return "\n".join(parts).rstrip()

    


if __name__ == '__main__':
    print(IPSubnet(
        IP("10.64.0.0"),
        IP("10.64.0.1"),
        IP("10.127.255.254"),
        IP("10.127.255.255"),
    ))

    subnets = IPSubnetCollection(
        segmentIP=IPSubnet(
            IP("10.0.0.0"),
            IP("10.0.0.1"),
            IP("10.63.255.254"),
            IP("10.63.255.255"),
        ),
        subnets=[
            IPSubnet(
                IP("10.64.0.0"),
                IP("10.64.0.1"),
                IP("10.127.255.254"),
                IP("10.127.255.255"),
            ),
            IPSubnet(
                IP("10.128.0.0"),
                IP("10.128.0.1"),
                IP("10.191.255.254"),
                IP("10.191.255.255"),
            ),
        ],
        broadcastIP=IPSubnet(
            IP("10.192.0.0"),
            IP("10.192.0.1"),
            IP("10.255.255.254"),
            IP("10.255.255.255"),
        ),
        mask=IP("255.192.0.0")
    )

    print(subnets)
