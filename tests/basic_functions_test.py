import unittest
from netclasses.ip import IP, IPClass
from netclasses.ip_subnet import IPSubnetCollection, IPSubnet
import common


class IPClasses_Tests(unittest.TestCase):

    def test_correct_init(self):
        ip = IP(common.IP_ADDRESS)
        self.assertEqual(ip.ipClass, IPClass.A)

        for ipPart in ip.ipBinaryParts:
            self.assertEquals(len(ipPart), 8)

    def test_equivalence(self):
        a = IP(common.IP_ADDRESS)
        b = IP(common.IP_ADDRESS)

        self.assertEqual(a, b)


class IPSubnets_Tests(unittest.TestCase):

    def test_equivalence(self):
        a = IPSubnetCollection(
            segmentIP=IPSubnet(
                IP('10.0.0.0'),
                IP('10.0.0.1'),
                IP('10.63.255.254'),
                IP('10.63.255.255'),
            ),
            subnets=[
                IPSubnet(
                    IP('10.64.0.0'),
                    IP('10.64.0.1'),
                    IP('10.127.255.254'),
                    IP('10.127.255.255'),
                ),
                IPSubnet(
                    IP('10.128.0.0'),
                    IP('10.128.0.1'),
                    IP('10.191.255.254'),
                    IP('10.191.255.255'),
                ),
            ],
            broadcastIP=IPSubnet(
                IP('10.192.0.0'),
                IP('10.192.0.1'),
                IP('10.255.255.254'),
                IP('10.255.255.255'),
            ),
            mask=IP('255.192.0.0'),
        )
        b = IPSubnetCollection(
            segmentIP=IPSubnet(
                IP('10.0.0.0'),
                IP('10.0.0.1'),
                IP('10.63.255.254'),
                IP('10.63.255.255'),
            ),
            subnets=[
                IPSubnet(
                    IP('10.64.0.0'),
                    IP('10.64.0.1'),
                    IP('10.127.255.254'),
                    IP('10.127.255.255'),
                ),
                IPSubnet(
                    IP('10.128.0.0'),
                    IP('10.128.0.1'),
                    IP('10.191.255.254'),
                    IP('10.191.255.255'),
                ),
            ],
            broadcastIP=IPSubnet(
                IP('10.192.0.0'),
                IP('10.192.0.1'),
                IP('10.255.255.254'),
                IP('10.255.255.255'),
            ),
            mask=IP('255.192.0.0'),
        )

        self.assertEqual(a.segmentIP, b.segmentIP)


if __name__ == '__main__':
    unittest.main()
