from dataclasses import dataclass
from .ip import IP, IPSubnet

@dataclass(frozen=True, eq=True)
class IPVLSMSubnet(IPSubnet):
    hosts : int
    decimalMask : int
    mask : IP

    def fromSubnet(subnet : IPSubnet, hosts : int, decimalMask : int, mask : IP):
        return IPVLSMSubnet(
            subnet.subnetIP,
            subnet.firstHost,
            subnet.lastHost,
            subnet.broadcastIP,
            hosts,
            decimalMask,
            mask,
        )

    def __str__(self) -> str:

        parts = [
            f'The available hosts in this subnet are {self.hosts}' ,
            super().__str__(),
            f'The Subnet mask in decimal form is: {self.decimalMask}',
            f'The Subnet mask is -> {self.mask}',
        ]

        return '\n'.join(parts)

@dataclass(frozen=True, eq=True)
class IPVLSMSubnetCollection:
    originalIP : IP
    subnets : list[IPVLSMSubnet]

    def __str__(self) -> str:

        parts = [
            f'The next subnets are for ip: {self.originalIP}',
            '',
        ]

        for i, subnet in enumerate(self.subnets):
            parts.extend([
                f'Subnet #{i + 1}',
                str(subnet),
                '',
            ])

        return '\n'.join(parts).rstrip()
