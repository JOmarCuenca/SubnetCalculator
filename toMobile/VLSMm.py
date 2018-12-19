#It is necessary to import from Subnet.py
#otherwise it will not work
from Subnetm import divide,clase,transform_bits2,binarySum

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

#similar to the initialization of the subnets
#Divides the original ip into its cocmponents in binary
#in string form and deduces its class
def convert(ipi):
    origin=divide(ipi)
    clas=clase(origin)
    res=""
    for x in origin:
        res+=x
    return res,clas

#Calculates the requiered bits in order for the hosts to work
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

#Creates the string for the broadcast of that subnet
def broad(quantity):
    res=""
    for x in range(len(quantity)):
        res+='1'
    return res

#creates all the different combinations for the subnets
#IP,hosts,broadcast
def permut(noTouch,net,id,first,last,broad):
    always=noTouch+net
    ip=transform_bits2(always+id)
    fhost=transform_bits2(always+first)
    lhost=transform_bits2(always+last)
    broadcast=transform_bits2(always+broad)
    return [ip,fhost,lhost,broadcast]

#creates the mask for the Subnet using the bits dedicated for the hosts
def mask(host):
    mask=""
    for x in range(32-host):
        mask+='1'
    for x in range(host):
        mask+='0'
    return transform_bits2(mask)

#module that makes the actual subnetting
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
    result.append(mask(hostBit))
    result.append(netBits)
    return result,next

#exports everything into a .txt for later analysis
def export(dictionary):
    writer=open("VLSM.txt","w")

    writer.write('\n')
    arr=dictionary[1]
    writer.write("The next subnets are for the ip: "+arr[0]+"\n\n")

    for x in range(1,len(dictionary)+1):
        string="The subnet number "+str(x)+":"
        writer.write(string+"\n")
        arr=dictionary[x]
        string="The available hosts in this subnet are:\t"+str(arr[6])
        writer.write(string+"\n")
        string="Sub_ip= "+arr[0]+" \tHosts= "+arr[1]+" - "+arr[2]+" \tBroadcast= "+arr[3]
        writer.write(string+"\n" )
        string="The Subnet mask in decimal form is: "+str(arr[5])+"\t, the subnet mask is: "+arr[4]
        writer.write(string+"\n\n")


    writer.close()

#Mastermind for the code
#Recieves the parameters and then creates the dictionary
#where everything is saved for later exportation
def vlsm(ipi,dump):
    num=[]
    sub=[]
    i=0
    for x in dump:
        if(not(x in sub)):
            sub.append(x)
            num.append(0)
    for x in sub:
        for y in dump:
            if(x==y):
                num[i]+=1
        i+=1
    if(len(sub)!=len(num)):
        print("Error")
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
            result.append(sub[x])
            dict[cont]=result
            cont+=1
    #export(dict)
    print("\n")
    for x in dict:
        arr=dict[x]
        print("The subnet number "+str(x)+":\n")
        print("The available hosts in this subnet are:\n"+str(arr[6])+"\n")
        print("Sub_ip= "+arr[0]+" \nHosts= "+arr[1]+" - "+arr[2]+" \nBroadcast= "+arr[3]+"\n")
        print("The Subnet mask in decimal form is: "+str(arr[5])+"\n, the subnet mask is: "+arr[4]+"\n\n")

def inip():
    done=False
    while(not(done)):
        ip=input("What will the ip be? = ")
        if(type(divide(ip))!=str):
            done=True
        else:
            print("There is a problem with the ip you just gave me, try again\n")
    return ip

def multIn(string,arr):
    num=""
    times=""
    change=False
    for x in string:
        if(x!='x' and x!='*'):
            if(change):
                times+=x
            else:
                num+=x
        else:
            change=True
    num=int(num)
    times=int(times)
    for x in range(times):
        arr.append(num)

def inHost():
    sub=[]
    done=False
    while(not(done)):
        accept=True
        try:
            i=input("How many hosts? (type 'go' to run the algorithm) ")
            if(i=="go"):
                done=True
            elif('x' in i or '*' in i):
                multIn(i,sub)
                accept=False
            else:
                i=int(i)
        except ValueError:
            print("There has been an error with the number you introduced, try again\n")
            accept=False
        if(accept and not(done)):
            sub.append(i)
    return sub

def mainV():
    ip=inip()
    sub=inHost()
    vlsm(ip,sub)
