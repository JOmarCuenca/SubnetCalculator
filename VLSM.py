# It is necessary to import from Subnet.py
# otherwise it will not work
from Subnet import transform_bits_into_ip_string, binary_sum
from classes.netArgs import VLSMArgs
from netclasses.ip import IP, IPSubnet
from netclasses.ip_vlsm import IPVLSMSubnet, IPVLSMSubnetCollection

# similar to the initialization of the subnets
# Divides the original ip into its cocmponents in binary
# in string form and deduces its class


def _calculate_mask_size(size):
    """Calculates the requiered bits in order for the hosts to work."""
    res = 0
    while (True):
        assert (res <= size)
        if (2**res > size):
            return res
        else:
            res += 1


def _broadcast_address_generator(quantity: str):
    """Creates the string for the broadcast of that subnet."""
    return '1' * len(quantity)

# creates all the different combinations for the subnets
# IP,hosts,broadcast


def _join_subnet_parts(unmutableBits: str, networkBits: str, subnetIdAddress: str, firstHostAddress: str, lastHostAddress: str, broadcastAddress: str) -> IPSubnet:
    always = unmutableBits+networkBits
    return IPSubnet(
        subnetIP=IP(transform_bits_into_ip_string(always+subnetIdAddress)),
        firstHost=IP(transform_bits_into_ip_string(always+firstHostAddress)),
        lastHost=IP(transform_bits_into_ip_string(always+lastHostAddress)),
        broadcastIP=IP(transform_bits_into_ip_string(always+broadcastAddress)),
    )


def generate_mask_from_hosts(host) -> IP:
    """Creates the mask for the Subnet using the bits dedicated for the
    hosts."""
    mask = '1' * (32 - host) + '0' * host
    return IP(transform_bits_into_ip_string(mask))

# module that makes the actual subnetting


def _generate_vlsm_subnet(ip: IP, subnetSize: int) -> tuple[IPVLSMSubnet, IP]:
    binaryAddress = ''.join(ip.ipBinaryParts)
    reservedBits, availableBits = ip.ipClass.reserved_bits, ip.ipClass.available_bits
    hostBits = _calculate_mask_size(subnetSize)

    unmutableIPAddress, networkIPAddress, subnetIPaddress = binaryAddress[:reservedBits], binaryAddress[
        reservedBits: reservedBits + (
            availableBits - hostBits
        )
    ], binaryAddress[reservedBits + (availableBits - hostBits):]

    fhost = binary_sum(subnetIPaddress, 1)
    broadcast = _broadcast_address_generator(subnetIPaddress)
    lhost = binary_sum(broadcast, -1)
    subnet = _join_subnet_parts(
        unmutableIPAddress, networkIPAddress, subnetIPaddress, fhost, lhost, broadcast,
    )
    nextIPToUse = binary_sum((unmutableIPAddress+networkIPAddress+broadcast), 1)
    result = IPVLSMSubnet.from_subnet(
        subnet, subnetSize, 32 - hostBits, generate_mask_from_hosts(hostBits), )
    return result, IP(transform_bits_into_ip_string(nextIPToUse))

# Mastermind for the code
# Recieves the parameters and then creates the dictionary
# where everything is saved for later exportation


def vlsm_subnet_generator(ipString: str, targetSubnets: list[int]) -> IPVLSMSubnetCollection:

    ipAddress, originalIPAddress = IP(ipString), IP(ipString)

    subnets = []

    for targetSubnetSize in reversed(sorted(targetSubnets)):
        subnet, ipAddress = _generate_vlsm_subnet(ipAddress, targetSubnetSize)
        subnets.append(subnet)

    return IPVLSMSubnetCollection(
        originalIPAddress,
        subnets,
    )


if __name__ == '__main__':

    args = VLSMArgs.parse_args()

    result = vlsm_subnet_generator(args.ipAddress, args.subnets)

    if (args.filename):
        with open(args.filename, 'w') as f:
            f.write(str(result))
    else:
        print(result)
