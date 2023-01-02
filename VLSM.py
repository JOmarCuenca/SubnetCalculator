# It is necessary to import from Subnet.py
# otherwise it will not work
from Subnet import divide, clase, _transformBitsIntoIPString, binarySum

# bubbleSort inverted


def sort(arr, pos):
    long = len(arr)
    while long > 1:
        for x in range(long):
            y = x+1
            if (y < long):
                if (arr[x] < arr[y]):
                    temp = arr[x]
                    arr[x] = arr[y]
                    arr[y] = temp
                    temp = pos[x]
                    pos[x] = pos[y]
                    pos[y] = temp
        long -= 1

# similar to the initialization of the subnets
# Divides the original ip into its cocmponents in binary
# in string form and deduces its class


def convert(ipi):
    origin = divide(ipi)
    clas = clase(origin)
    res = ""
    for x in origin:
        res += x
    return res, clas

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
    ip = _transformBitsIntoIPString(always+id)
    fhost = _transformBitsIntoIPString(always+first)
    lhost = _transformBitsIntoIPString(always+last)
    broadcast = _transformBitsIntoIPString(always+broad)
    return [ip, fhost, lhost, broadcast]

# creates the mask for the Subnet using the bits dedicated for the hosts


def mask(host):
    mask = ""
    for x in range(32-host):
        mask += '1'
    for x in range(host):
        mask += '0'
    return _transformBitsIntoIPString(mask)

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

# exports everything into a .txt for later analysis


def export(dictionary):
    writer = open("VLSM.txt", "w")

    writer.write('\n')
    arr = dictionary[1]
    writer.write("The next subnets are for the ip: "+arr[0]+"\n\n")

    for x in range(1, len(dictionary)+1):
        string = "The subnet number "+str(x)+":"
        writer.write(string+"\n")
        arr = dictionary[x]
        string = "The available hosts in this subnet are:\t"+str(arr[6])
        writer.write(string+"\n")
        string = "Sub_ip= "+arr[0]+" \tHosts= " + \
            arr[1]+" - "+arr[2]+" \tBroadcast= "+arr[3]
        writer.write(string+"\n")
        string = "The Subnet mask in decimal form is: " + \
            str(arr[5])+"\t, the subnet mask is: "+arr[4]
        writer.write(string+"\n\n")

    writer.close()

# Mastermind for the code
# Recieves the parameters and then creates the dictionary
# where everything is saved for later exportation


def vlsm(ipi, dump):
    num = []
    sub = []
    i = 0
    for x in dump:
        if (not (x in sub)):
            sub.append(x)
            num.append(0)
    for x in sub:
        for y in dump:
            if (x == y):
                num[i] += 1
        i += 1
    if (len(sub) != len(num)):
        print("Error")
        return "Error"
    origin, cl = convert(ipi)
    sort(sub, num)
    unmutBits = 8*cl
    usebits = 32-unmutBits
    dict = {}
    cont = 1
    for x in range(len(sub)):
        for y in range(num[x]):
            result, origin = root(origin, usebits, unmutBits, sub[x])
            result.append(sub[x])
            dict[cont] = result
            cont += 1
    export(dict)
    print("Done!")
    return ("Done!")


# default ip for VLSM
# just change the parameters to subnet other ip
ip = "192.168.254.0"
sub = [95, 70, 50, 20, 2, 2]
# num=[1,1,1,1,2]
vlsm(ip, sub)
