# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 00:03:09 2018
@author: Jesus Omar Cuenca Espino
"""

from netclasses.ip import IP
from netclasses.ip_subnet import IPSubnet, IPSubnetCollection

def _maskIsValid(currentMask: list[int]):
    """Checks the subnet mask so there are no contradictions."""
    return all([val == 255 for val in currentMask])

def _generateMask(maskBitsToUse: int) -> IP:
    """Calculates the subnet mask."""

    assert (9 <= maskBitsToUse <= 30)

    reservedBits = maskBitsToUse // 8

    msk = [255] * reservedBits

    assert (_maskIsValid(msk))

    maskBitsToUse = maskBitsToUse % 8

    count = 7
    final = 0
    while (maskBitsToUse > 0):
        final += 2**count
        count -= 1
        maskBitsToUse -= 1

    msk.append(final)

    while (len(msk) < 4):
        msk.append(0)

    return IP('.'.join([str(c) for c in msk]))

# merges the functions above in a single process meant to only be used once


def init(ipi, m):
    ip = IP(ipi)
    claseip = ip.ipClass
    usebits = m-ip.ipClass.reserved_bits
    assert (usebits > 0)
    mask = _generateMask(m)
    return ip.ipBinaryParts, claseip.value, mask, usebits


def _separateIPSectionBinary(string) -> str:
    """Separates a string of binary characters using '.' into chunks of 8 sized
    length.

    This to correctly separate each ip section.
    """
    assert (len(string) == 32)
    n = 8
    return '.'.join([
        string[i:i+n]
        for i in range(0, 32, 8)
    ])


def transformBitsIntoIPString(string) -> str:
    """Separate the binary string into 4 ip sections and returns them in
    decimal integers."""
    binarySeparatedIPAddress = _separateIPSectionBinary(string)

    ipSectionsDecimal = [
        str(int(section, 2))
        for section in binarySeparatedIPAddress.split('.')
    ]

    return '.'.join(ipSectionsDecimal)


# checks if the input string is a candidate to be a broadcast address
def isNotBroadcast(value : str): return '0' in value

# Makes possible the iteraton over the subnets


def binarySum(subnet : str, quantity : int):
    """Adds `quantity` to the `subnet` value and returns the value in binary
    form."""
    assert(subnet)
    long = len(subnet)
    num = int(subnet, 2)
    num += quantity
    res = IP.intToBinStr(int(num), long)
    return res

# This is the main and most important function because it uses the other functions
# to be able to give you what you are asking for, all the subnets in a dictionary
# that will be given to you, but also exported to .txt


def subnetGenerator(ipi, ubits):
    ip, cl, mask, bits = init(ipi, ubits)
    if (bits == 'error'):
        return bits
    origin = ''
    for x in ip:
        origin += x
    unmut = ''
    bits_no_usables = cl*8
    for x in range(bits_no_usables):
        unmut += origin[x]

    subnet_init = bits_no_usables+1
    bits_subnet = ''
    for x in range(subnet_init, subnet_init+bits):
        bits_subnet += '0'

    bits_usable_zeros = ''
    broad = ''
    for x in range(len(bits_subnet+unmut), len(origin)):
        broad += '1'
        bits_usable_zeros += '0'
    bits_usable_last = binarySum(broad, -1)
    first = binarySum(bits_usable_zeros, 1)

    dictionary = []
    targetSubnetReached = isNotBroadcast(bits_subnet)

    while targetSubnetReached:
        targetSubnetReached = isNotBroadcast(bits_subnet)

        dictionary.append(
            IPSubnet(
                # ip of the network
                IP(transformBitsIntoIPString(unmut + bits_subnet + bits_usable_zeros)),
                # first host
                IP(transformBitsIntoIPString(unmut + bits_subnet + first)),
                # last host
                IP(transformBitsIntoIPString(unmut + bits_subnet + bits_usable_last)),
                # broadcast
                IP(transformBitsIntoIPString(unmut + bits_subnet + broad)),
            ),
        )

        bits_subnet = binarySum(bits_subnet, 1)

    return IPSubnetCollection(
        segmentIP=dictionary[0],
        subnets=dictionary[1: -1],
        broadcastIP=dictionary[-1],
        mask=mask,
    )


if __name__ == '__main__':
    from classes.netArgs import SubnetArgs

    args = SubnetArgs.parseArgs()
    result = subnetGenerator(args.ipAddress, args.reservedBits)

    if(args.filename):
        with open(args.filename, 'w') as f:
            f.write(str(result))
    else:
        print(result)


# May the Force be with you
