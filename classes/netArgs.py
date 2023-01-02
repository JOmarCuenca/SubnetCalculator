from dataclasses import dataclass
from argparse import ArgumentParser

class NetArgs:

    def parseArgs():
        raise NotImplementedError()


@dataclass(frozen=True)
class SubnetArgs(NetArgs):
    ipAddress: str
    reservedBits: int
    filename: str | None

    def parseArgs():
        parser = ArgumentParser(
            prog='Subnet Calculator',
            description='This program calculates subnets from an ip V4, using reserved bits',
            epilog='May the force be with you',
        )

        parser.add_argument("ipAddress", type=str,
                            help="IP V4 address to subnet",)
        parser.add_argument("reservedBits", type=int,
                            help="Bits to be used by the subnets",)
        parser.add_argument("-o", type=str, nargs='?',
                            help="If you wanna export the result send as a param the filename to export", dest="filename")

        args = parser.parse_args()

        return SubnetArgs(args.ipAddress, args.reservedBits, filename=args.filename)

@dataclass(frozen=True)
class VLSMArgs(NetArgs):
    ipAddress: str
    subnets: list[int]
    filename: str | None

    def parseArgs():
        parser = ArgumentParser(
            prog='Subnet Calculator',
            description='This program calculates subnets from an ip V4, using reserved bits',
            epilog='May the force be with you',
        )

        parser.add_argument("ipAddress", type=str,
                            help="IP V4 address to subnet",)
        parser.add_argument("subnets", type=list[int],
                            help="Subnets to be calculated",)
        parser.add_argument("-o", type=str, nargs='?',
                            help="If you wanna export the result send as a param the filename to export", dest="filename")

        args = parser.parse_args()

        return VLSMArgs(args.ipAddress, args.subnets, filename=args.filename)
