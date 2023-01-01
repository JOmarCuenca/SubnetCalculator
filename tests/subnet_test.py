import unittest
from Subnet import subnet
from netclasses.ip import IP, IPClass
from netclasses.ip_subnet import IPSubnetCollection, IPSubnet

IP_ADDRESS = "10.0.0.0"
RESERVED_BITS = 10


class IPClasses_Tests(unittest.TestCase):
    
    def test_correct_init(self):
        ip = IP(IP_ADDRESS)
        self.assertEqual(ip.ipClass, IPClass.A)

        for ipPart in ip.ipParts:
            self.assertEquals(len(ipPart), 8)

    def test_equivalence(self):
        a = IP(IP_ADDRESS)
        b = IP(IP_ADDRESS)

        print(a == b)

        self.assertEqual(a,b)

class IPSubnets_Tests(unittest.TestCase):

    def test_equivalence(self):
        a = IPSubnetCollection(
            segmentIP=IPSubnet(
                IP("10.0.0.0"),
                IP("10.0.0.1"),
                IP("10.63.255.254"),
                IP("10.63.255.255"),
            ),
            subnets=[
                IPSubnet(
                    IP("10.64.0.0"),
                    IP("10.64.0.1"),
                    IP("10.127.255.254"),
                    IP("10.127.255.255"),
                ),
                IPSubnet(
                    IP("10.128.0.0"),
                    IP("10.128.0.1"),
                    IP("10.191.255.254"),
                    IP("10.191.255.255"),
                ),
            ],
            broadcastIP=IPSubnet(
                IP("10.192.0.0"),
                IP("10.192.0.1"),
                IP("10.255.255.254"),
                IP("10.255.255.255"),
            ),
            mask=IP("255.192.0.0")
        )
        b = IPSubnetCollection(
            segmentIP=IPSubnet(
                IP("10.0.0.0"),
                IP("10.0.0.1"),
                IP("10.63.255.254"),
                IP("10.63.255.255"),
            ),
            subnets=[
                IPSubnet(
                    IP("10.64.0.0"),
                    IP("10.64.0.1"),
                    IP("10.127.255.254"),
                    IP("10.127.255.255"),
                ),
                IPSubnet(
                    IP("10.128.0.0"),
                    IP("10.128.0.1"),
                    IP("10.191.255.254"),
                    IP("10.191.255.255"),
                ),
            ],
            broadcastIP=IPSubnet(
                IP("10.192.0.0"),
                IP("10.192.0.1"),
                IP("10.255.255.254"),
                IP("10.255.255.255"),
            ),
            mask=IP("255.192.0.0")
        )

        self.assertEqual(a.segmentIP, b.segmentIP)

class Integration_Test(unittest.TestCase):

    def test_functionality_integrated(self):
        target = IPSubnetCollection(
            segmentIP=IPSubnet(
                IP("10.0.0.0"),
                IP("10.0.0.1"),
                IP("10.63.255.254"),
                IP("10.63.255.255"),
            ),
            subnets=[
                IPSubnet(
                    IP("10.64.0.0"),
                    IP("10.64.0.1"),
                    IP("10.127.255.254"),
                    IP("10.127.255.255"),
                ),
                IPSubnet(
                    IP("10.128.0.0"),
                    IP("10.128.0.1"),
                    IP("10.191.255.254"),
                    IP("10.191.255.255"),
                ),
            ],
            broadcastIP=IPSubnet(
                IP("10.192.0.0"),
                IP("10.192.0.1"),
                IP("10.255.255.254"),
                IP("10.255.255.255"),
            ),
            mask=IP("255.192.0.0")
        )

        result = subnet(IP_ADDRESS, RESERVED_BITS)

        self.assertEqual(target, result)

if __name__ == '__main__':
    unittest.main()