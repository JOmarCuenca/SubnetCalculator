#It is necessary to import from Subnet.py
#otherwise it will not work
from Subnet import divide,clase,transform_bits2,binarySum

#bubbleSort inverted
def sort(arr,pos):
    long=len(arr)
    while long>1:
        for x in range(long):
            y=x+1
            if(y<long):
                if(arr[x]<arr[y]):
                     temp=arr[x]
                     arr[x]=arr[y]
                     arr[y]=temp
                     temp=pos[x]
                     pos[x]=pos[y]
                     pos[y]=temp
        long-=1


def convert(ipi):
    origin=divide(ipi)
    clas=clase(origin)
    res=""
    for x in origin:
        res+=x
    return res,clas

def calculateSize(size,use):
    done=False
    res=0
    while(not(done)):
        if(res>size):
            return "Error; Not enough space to subnet"
        if(2**res>size):
            done=True
        else:
            res+=1
    return res

def broad(quantity):
    res=""
    for x in range(len(quantity)):
        res+='1'
    return res

def permut(noTouch,net,id,first,last,broad):
    always=noTouch+net
    ip=transform_bits2(always+id)
    fhost=transform_bits2(always+first)
    lhost=transform_bits2(always+last)
    broadcast=transform_bits2(always+broad)
    mask=""
    return [ip,fhost,lhost,broadcast,mask]


def root(ip,bits,unmut,large):
    unmutable=ip[:unmut]
    hostBit=calculateSize(large,bits)
    netBits=32-hostBit
    network=ip[unmut:netBits]
    ipnet=ip[netBits:]
    fhost=binarySum(ipnet,1)
    broadcast=broad(ipnet)
    lhost=binarySum(broadcast,-1)
    result=permut(unmutable,network,ipnet,fhost,lhost,broadcast)
    next=binarySum((unmutable+network+broadcast),1)
    return result,next


def vlsm(ipi,sub,num):
    if(len(sub)!=len(num)):
        return "Error"
    origin,cl=convert(ipi)
    sort(sub,num)
    unmutBits=8*cl
    usebits=32-unmutBits
    dict={}
    cont=1
    for x in range(len(sub)):
        for y in range(num[x]):
            result,origin=root(origin,usebits,unmutBits,sub[x])
            dict[cont]=result
            cont+=1
    for x in dict:
        print(dict[x])








ip="10.0.0.0"
sub=[50,1000,400,2]
num=[4,1,8,5]
vlsm(ip,sub,num)
