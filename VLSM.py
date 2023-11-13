# It is necessary to import from Subnet.py
# otherwise it will not work
from Subnet import transformBitsIntoIPString, binarySum
from classes.netArgs import VLSMArgs
from netclasses.ip import IP, IPSubnet
from netclasses.ip_vlsm import IPVLSMSubnet, IPVLSMSubnetCollection

# similar to the initialization of the subnets
# Divides the original ip into its cocmponents in binary
# in string form and deduces its class


def reverseSort(arr: list):
    return list(reversed(sorted(arr)))


def _calculateMaskSize(size):
    """Calculates the requiered bits in order for the hosts to work."""
    res = 0
    while (True):
        assert (res <= size)
        if (2**res > size):
            return res
        else:
            res += 1


def _broadcastAddressGenerator(quantity: int):
    """Creates the string for the broadcast of that subnet."""
    return '1' * len(quantity)

# creates all the different combinations for the subnets
# IP,hosts,broadcast


def _joinSubnetParts(unmutableBits: str, networkBits: str, subnetIdAddress: str, firstHostAddress: str, lastHostAddress: str, broadcastAddress: str) -> IPSubnet:
    always = unmutableBits+networkBits
    return IPSubnet(
        subnetIP=IP(transformBitsIntoIPString(always+subnetIdAddress)),
        firstHost=IP(transformBitsIntoIPString(always+firstHostAddress)),
        lastHost=IP(transformBitsIntoIPString(always+lastHostAddress)),
        broadcastIP=IP(transformBitsIntoIPString(always+broadcastAddress)),
    )


def generateMaskFromHosts(host) -> IP:
    """Creates the mask for the Subnet using the bits dedicated for the
    hosts."""
    mask = '1' * (32 - host) + '0' * host
    return IP(transformBitsIntoIPString(mask))

# module that makes the actual subnetting


def _generateVLSMSubnet(ip: IP, subnetSize: int) -> tuple[IPVLSMSubnet, IP]:
    binaryAddress = ''.join(ip.ipBinaryParts)
    reservedBits, availableBits = ip.ipClass.reserved_bits, ip.ipClass.available_bits
    hostBits = _calculateMaskSize(subnetSize)

    unmutableIPAddress, networkIPAddress, subnetIPaddress = binaryAddress[:reservedBits], binaryAddress[
        reservedBits: reservedBits + (
            availableBits - hostBits
        )
    ], binaryAddress[reservedBits + (availableBits - hostBits):]

    fhost = binarySum(subnetIPaddress, 1)
    broadcast = _broadcastAddressGenerator(subnetIPaddress)
    lhost = binarySum(broadcast, -1)
    subnet = _joinSubnetParts(
        unmutableIPAddress, networkIPAddress, subnetIPaddress, fhost, lhost, broadcast,
    )
    nextIPToUse = binarySum((unmutableIPAddress+networkIPAddress+broadcast), 1)
    result = IPVLSMSubnet.fromSubnet(
        subnet, subnetSize, 32 - hostBits, generateMaskFromHosts(hostBits), )
    return result, IP(transformBitsIntoIPString(nextIPToUse))

# Mastermind for the code
# Recieves the parameters and then creates the dictionary
# where everything is saved for later exportation


def vlsmSubnetGenerator(ipString: str, targetSubnets: list[int]) -> IPVLSMSubnetCollection:

    targetSubnets = reverseSort(targetSubnets)

    ipAddress, originalIPAddress = IP(ipString), IP(ipString)

    subnets = []

    for targetSubnetSize in targetSubnets:
        subnet, ipAddress = _generateVLSMSubnet(ipAddress, targetSubnetSize)
        subnets.append(subnet)

    return IPVLSMSubnetCollection(
        originalIPAddress,
        subnets,
    )


if __name__ == '__main__':

    args = VLSMArgs.parseArgs()

    result = vlsmSubnetGenerator(args.ipAddress, args.subnets)

    if (args.filename):
        with open(args.filename, 'w') as f:
            f.write(str(result))
    else:
        print(result)
