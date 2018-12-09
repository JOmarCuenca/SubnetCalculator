# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 00:03:09 2018
@author: Jesus Omar Cuenca Espino
"""
#recibe el ip en forma de string para que lo pueda dividir y procesar acordemente
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
    return ipf

#recibe el ip generado por divide y lo clasifica para poder determinar la mascara por default
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

#comprobante que la mascara de subnet no tenga contradicciones
def comp(cl,smask):
    for x in range(cl):
        if(smask[x]!=255):
            return True
    return False

#funcion para calcular la mascara de subred
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

#junta los procesos de arriba en uno en automatico
#y calcula los bits utiles para esas subredes
def init(ipi,m):
    ip=divide(ipi)
    claseip=clase(ip)
    usebits=m-claseip*8
    if(usebits<1):
        return ipi,m,"error"
    else:
        mask=final_mask(claseip,m)
        return ip,claseip,mask,usebits

#metodo que acomoda una lista que tenga forma de direccion ip y lo imprime unicamente
def prip(ip):
    if(type(ip)!=list):
        return -1
    st=""
    i=0
    for x in ip:
        st+=str(int(x,2))
        if(i<3):
            st+='.'
        i+=1
    #print(st)
    return st

#acomoda una lista que contenga la mascara para que pueda ser leida
#tiene que ser una funcion distinta debido a que la ip lo estoy manejando como binario y la mascara como int
def pmask(mask):
    st=""
    for x in range(4):
        st+=str(mask[x])
        if(x<3):
            st+='.'
    return st

#acomoda los bits que se encuentran en un string largo en una forma similar a la mascara final en forma de bit
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



#basado en el numero de bits reservados y la mascara default
#modifica la mascara para volverla la mascara de subred
def subnet(ip,cl,bits):
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
        bits_subnet+=origin[x]
    print(transform_bits(origin))
    print(unmut)
    print(bits_subnet)
    print(origin)

#el menu y lo que permite manejar la GUI
def main(ipi,bit):
    ip,cl,mask,use=init(ipi,bit)
    if(use=="error"):
        print("hubo un error con los bits de subred, favor de revisarlo")
    elif(use==0):
        print("There is no space for subnets, would you like to change the subnet length? (y/n) ")
    else:
        subnet(ip,cl,use)


#me la pelas mamon


add="192.168.1.0"
#add=input("Cual es la ip? ")
rbits=29
Bcast="192.168.1.255"
main(add,rbits)
