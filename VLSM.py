# It is necessary to import from Subnet.py
# otherwise it will not work
from Subnet import transformBitsIntoIPString, binarySum
from netclasses.ip import IP

# similar to the initialization of the subnets
# Divides the original ip into its cocmponents in binary
# in string form and deduces its class

# Calculates the requiered bits in order for the hosts to work


def calculateSize(size, use):
    done = False
    res = 0
    while (not (done)):
        if (res > size):
            return "Error; Not enough space to subnet"
        if (2**res > size):
            done = True
        else:
            res += 1
    return res

# Creates the string for the broadcast of that subnet


def broad(quantity):
    res = ""
    for x in range(len(quantity)):
        res += '1'
    return res

# creates all the different combinations for the subnets
# IP,hosts,broadcast


def permut(noTouch, net, id, first, last, broad):
    always = noTouch+net
    ip = transformBitsIntoIPString(always+id)
    fhost = transformBitsIntoIPString(always+first)
    lhost = transformBitsIntoIPString(always+last)
    broadcast = transformBitsIntoIPString(always+broad)
    return [ip, fhost, lhost, broadcast]

# creates the mask for the Subnet using the bits dedicated for the hosts


def mask(host):
    mask = ""
    for x in range(32-host):
        mask += '1'
    for x in range(host):
        mask += '0'
    return transformBitsIntoIPString(mask)

# module that makes the actual subnetting


def root(ip, bits, unmut, large):
    unmutable = ip[:unmut]
    hostBit = calculateSize(large, bits)
    netBits = 32-hostBit
    network = ip[unmut:netBits]
    ipnet = ip[netBits:]
    fhost = binarySum(ipnet, 1)
    broadcast = broad(ipnet)
    lhost = binarySum(broadcast, -1)
    result = permut(unmutable, network, ipnet, fhost, lhost, broadcast)
    next = binarySum((unmutable+network+broadcast), 1)
    result.append(mask(hostBit))
    result.append(netBits)
    return result, next

# Mastermind for the code
# Recieves the parameters and then creates the dictionary
# where everything is saved for later exportation


def vlsm(ipString : str, targetSubnets : list[int]):
    
    subnets = {}

    for subnet in targetSubnets:
        if subnet in subnets:
            subnets[subnet] += 1
        else:
            subnets[subnet] = 1

    ipAddress = IP(ipString)
    
    sort(sub, num)
    unmutBits = ipAddress.ipClass.reservedBits()
    usebits = 32-unmutBits
    dict = {}
    cont = 1
    for x in range(len(sub)):
        for y in range(num[x]):
            result, origin = root(origin, usebits, unmutBits, sub[x])
            result.append(sub[x])
            dict[cont] = result
            cont += 1
    
    


if __name__ == '__main__':
    # default ip for VLSM
    # just change the parameters to subnet other ip
    ip = "192.168.254.0"
    sub = [95, 70, 50, 20, 2, 2]

    sub = list(reversed(sorted(sub)))

    # # num=[1,1,1,1,2]
    vlsm(ip, sub)

    
