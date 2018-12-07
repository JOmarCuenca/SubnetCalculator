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

#recibe el ip y lo clasifica para poder determinar la mascara por default
def clase(ip):
    tipo=int(ip[0][2:],2)
    if(tipo<0):
        return "La ip ingresada esta mal escrita",-1
    elif(tipo<128):
        return [255,0,0,0],1
    elif(tipo<192):
        return [255,255,0,0],2
    elif(tipo<224):
        return [255,255,255,0],3
    else:
        return "error",-1

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
    print(st)
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

#basado en el numero de bits reservados y la mascara default
#modifica la mascara para volverla la mascara de subred
def subnet(mask,tip,subred):
    rbits=subred-(8*(tip))
    while(rbits>=8):
        mask[tip]=255
        tip+=1
        rbits-=8
    if(rbits!=0):
        sub=0
        for x in range(rbits):
            sub+=2**(7-x)
        mask[tip]=sub
    return rbits

def subred(ip,bits,subred):
    return "none"

#el menu y lo que permite manejar la GUI
def main(ip,bit):
    ipv4=divide(ip)
    if(type(ipv4)==str or bit>32):
        return "Algun dato introducido es erroneo"
    mask,it=clase(ipv4)
    usebits=subnet(mask,it,bit)
    done=True
    while(done):
        print("La mascara de subred es: " + prip(mask))
        subr=input("Que subred buscas? ")
        if(subred==0 or subred>=(2**usebits)-1):
            print("No es accesible esa subred")
        else:
            result=subred(ipv4,usebits,subr)

#me la pelas mamon


add="192.168.1.0"
rbits=29
Bcast="192.168.1.255"
maskreal="255.255.255.0"
ip=divide(add)
print(ip)
prip(ip)
