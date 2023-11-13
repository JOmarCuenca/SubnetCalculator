from random import shuffle, seed

seed(42)

IP_ADDRESS = '10.0.0.0'
RESERVED_BITS = 10

VLSM_IP_ADDRESS = '192.168.254.0'
SUBNETS_SIZES = [95, 70, 50, 20, 2, 2]

shuffle(SUBNETS_SIZES)
