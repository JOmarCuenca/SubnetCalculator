# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 00:03:09 2018
@author: Jesus Omar Cuenca Espino
"""
#receives the ip in form of a string so it can be divided and proccessed accordingly
def divide(ip):
    ipf=[0,0,0,0]
    s=""
    i=0
    for x in ip:
        if(x=='.'):
            if(int(s)<256):
                num=bin(int(s))[2:]
                while(len(num)<8):
                    num='0'+num
                ipf[i]=num
                s=""
                i+=1
            else:
                return "La ip ingresada esta mal escrita"
        else:
            s+=x
    if(int(s)>=256):
        return "La ip ingresada esta mal escrita"
    num=bin(int(s))[2:]
    while(len(num)<8):
        num='0'+num
    ipf[3]=num
    for x in ipf:
        if(type(x)!=str):
            return "error"
    return ipf

#receives the ip generated from divide and then clasifies so it can find the mask by default
def clase(ip):
    tipo=int(ip[0],2)
    if(tipo<0):
        return -1
    elif(tipo<128):
        return 1
    elif(tipo<192):
        return 2
    elif(tipo<224):
        return 3
    else:
        return -1

#checks the subnet mask so there are no contradictions
def comp(cl,smask):
    for x in range(cl):
        if(smask[x]!=255):
            return True
    return False

#function to calculate the subnet mask
def final_mask(cl,use):
    if(use>30 or use<9):
        return "error"
    msk=[0,0,0,0]
    pos=0
    while(use>8):
        msk[pos]=255
        pos+=1
        use-=8
    if(comp(cl,msk)):
        return "error"
    count=7
    final=0
    while(use>0):
        final+=2**count
        count-=1
        use-=1
    msk[pos]=final
    return msk

#Prints the mask
def pmask(mask):
    st=""
    for x in range(4):
        st+=str(mask[x])
        if(x<3):
            st+='.'
    return st

#merges the functions above in a single process meant to only be used once
def init(ipi,m):
    ip=divide(ipi)
    claseip=clase(ip)
    usebits=m-claseip*8
    if(usebits<1):
        return ipi,claseip,m,"error"
    else:
        mask=final_mask(claseip,m)
        return ip,claseip,mask,usebits

#Makes easier the proccess of conversion into the ipv4 address
def transform_bits(string):
    if(len(string)<32):
        return "error"
    else:
        cont=0
        res=""
        while(cont<32):
            if(cont in [8,16,24]):
                res+='.'
            res+=string[cont]
            cont+=1
        return res

#Converts a large string into an ordered string in the form of an ipv4 address
def transform_bits2(string):
    close=transform_bits(string)
    st=""
    res=""
    for x in close:
        if(x=='.'):
            st=int(st,2)
            res+=str(st)+'.'
            st=""
        else:
            st+=x
    res+=str(int(st,2))
    return res

#checks if the input string is a candidate to be a broadcast address
def broadcast(string):
    for x in string:
        if(x=='0'):
            return True
    return False

#Makes possible the iteraton over the subnets
def binarySum(subnet,quantity):
    long=len(subnet)
    num=int(subnet,2)
    num+=quantity
    res=bin(int(num))[2:]
    while(len(res)<long):
        res='0'+res
    return res

#makes the union between the different parts of the ip
def union(un,net,host):
    return transform_bits2(un+net+host)

#function that exports the dictionary introduced as parameter
#into a .txt in the working directory in a readable format
def export(dict,mask):
    writer=open("Subnets.txt","w")

    writer.write("\n")
    string="The range of the segment (which cannot be used) is:"
    writer.write(string+"\n" )
    arr=dict[0]
    string="Sub_ip= "+arr[0]+", Hosts= "+arr[1]+"-"+arr[2]+" Broadcast= "+arr[3]
    writer.write(string+"\n" )
    writer.write("\n")
    string="The range of overall broadcast address (which cannot be used) is:"
    writer.write(string+"\n" )
    arr=dict[len(dict)-1]
    string="Sub_ip= "+arr[0]+" Hosts= "+arr[1]+"-"+arr[2]+" Broadcast= "+arr[3]
    writer.write(string+"\n" )
    writer.write("\n")

    string="The subnet mask is = "+pmask(mask)
    writer.write(string+"\n" )
    writer.write("\n")

    for x in range(1,len(dict)-1):
        string="The subnet number "+str(x)
        writer.write(string+"\n" )
        arr=dict[x]
        string="Sub_ip= "+arr[0]+" \tHosts= "+arr[1]+"-"+arr[2]+" \tBroadcast= "+arr[3]
        writer.write(string+"\n" )
        writer.write("\n")


    writer.close()

#This is the main and most important function because it uses the other functions
#to be able to give you what you are asking for, all the subnets in a dictionary
#that will be given to you, but also exported to .txt
def subnet(ipi,ubits):
    ip,cl,mask,bits=init(ipi,ubits)
    if(bits=="error" or type(ip)==str):
        return "error"
    origin=""
    for x in ip:
        origin+=x
    unmut=""
    bits_no_usables=cl*8
    for x in range(bits_no_usables):
        unmut+=origin[x]

    subnet_init=bits_no_usables+1
    bits_subnet=""
    for x in range(subnet_init,subnet_init+bits):
        bits_subnet+='0'

    bits_usable_zeros=""
    broad=""
    for x in range(len(bits_subnet+unmut),len(origin)):
        broad+='1'
        bits_usable_zeros+='0'
    bits_usable_last=binarySum(broad,-1)
    first=binarySum(bits_usable_zeros,1)

    dictionary={}
    condition=broadcast(bits_subnet)
    while(condition):
        condition=broadcast(bits_subnet)
        component=["","","",""]
        #ip of the network
        component[0]=union(unmut,bits_subnet,bits_usable_zeros)

        #first host
        component[1]=union(unmut,bits_subnet,first)

        #last host
        component[2]=union(unmut,bits_subnet,bits_usable_last)

        #broadcast
        component[3]=union(unmut,bits_subnet,broad)

        dictionary[len(dictionary)]=component
        bits_subnet=binarySum(bits_subnet,1)
    #export(dictionary,mask)
    return dictionary


#The menu
def main():
    ip=input("What will the ip to subnet be? ")
    try:
        bit=int(input("How many bits shall be reserved for the subnets? "))
        final=subnet(ip,bit)
    except ValueError:
        final="error"
    if(final=="error"):
        print("There has been an error with the parameters you introduced")
        print("Please introduce them again\n")
        main()
    else:
        print("DONE!")
        cont=True
        while(cont):
            valid=True
            ans=input("What subnet are you looking for? ")
            if(ans=="end"):
                cont=False
                break
            else:
                try:
                    ans=int(ans)
                except ValueError:
                    print("That's not a valid number, try again. (type 'end' to finish)")
                    valid=False
            if(cont and valid):
                if(ans==0 or ans==len(final)-1):
                    print("Remember that you cannot use this range of ip's")
                    arr=final[ans]
                    string="Sub_ip= "+arr[0]+" \nHosts= "+arr[1]+"-"+arr[2]+" \nBroadcast= "+arr[3]
                    print(string)
                elif(ans>0 and ans<len(final)-1):
                    arr=final[ans]
                    string="Sub_ip= "+arr[0]+" \nHosts= "+arr[1]+"-"+arr[2]+" \nBroadcast= "+arr[3]
                    print(string)
                else:
                    print("That number of subnet does not exist in my records")
                print("\n")
#May the Force be with you
