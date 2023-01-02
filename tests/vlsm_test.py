import unittest
from VLSM import vlsm
from netclasses.ip import IP
from netclasses.ip_vlsm import IPVLSMSubnet, IPVLSMSubnetCollection
from tests.common import VLSM_IP_ADDRESS, SUBNETS_SIZES


class Integration_Test(unittest.TestCase):

    def test_functionality_integrated(self):
        target = IPVLSMSubnetCollection(
            IP(VLSM_IP_ADDRESS),
            [
                IPVLSMSubnet(
                    IP("192.168.254.0"),
                    IP("192.168.254.1"),
                    IP("192.168.254.126"),
                    IP("192.168.254.127"),
                    95,
                    25,
                    IP("255.255.255.128"),
                ),
                IPVLSMSubnet(
                    IP("192.168.254.128"),
                    IP("192.168.254.129"),
                    IP("192.168.254.254"),
                    IP("192.168.254.255"),
                    70,
                    25,
                    IP("255.255.255.128"),
                ),
                IPVLSMSubnet(
                    IP("192.168.255.0"),
                    IP("192.168.255.1"),
                    IP("192.168.255.62"),
                    IP("192.168.255.63"),
                    50,
                    26,
                    IP("255.255.255.192"),
                ),
                IPVLSMSubnet(
                    IP("192.168.255.64"),
                    IP("192.168.255.65"),
                    IP("192.168.255.94"),
                    IP("192.168.255.95"),
                    20,
                    27,
                    IP("255.255.255.224"),
                ),
                IPVLSMSubnet(
                    IP("192.168.255.96"),
                    IP("192.168.255.97"),
                    IP("192.168.255.98"),
                    IP("192.168.255.99"),
                    2,
                    30,
                    IP("255.255.255.252"),
                ),
                IPVLSMSubnet(
                    IP("192.168.255.100"),
                    IP("192.168.255.101"),
                    IP("192.168.255.102"),
                    IP("192.168.255.103"),
                    2,
                    30,
                    IP("255.255.255.252"),
                ),
            ]
        )

        print(SUBNETS_SIZES)

        result = vlsm(VLSM_IP_ADDRESS, SUBNETS_SIZES)

        self.assertEqual(target, result)


if __name__ == '__main__':
    unittest.main()
