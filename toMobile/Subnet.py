from VLSMm import mainV
from Subnetm import main

print("I am ready to Subnet")
done=False
while(not(done)):
    done=True
    i=input("Do you want Subnet or VLSM? (s/v) ")
    if(i=="s"):
        main()
    elif(i=="v"):
        mainV()
    elif(i=="end"):
        done=True
    else:
        done=False
        print("I didn't understand, again please\n")
print("Goodbye")
