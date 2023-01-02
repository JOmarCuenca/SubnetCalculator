import unittest
from Subnet import subnet
from netclasses.ip import IP
from netclasses.ip_subnet import IPSubnetCollection, IPSubnet
import common

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

        result = subnet(common.IP_ADDRESS, common.RESERVED_BITS)

        self.assertEqual(target, result)

if __name__ == '__main__':
    unittest.main()