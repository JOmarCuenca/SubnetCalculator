from enum import IntEnum


class IPClass(IntEnum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5

    @property
    def reserved_bits(self) -> int:
        return self.value * 8

    @property
    def available_bits(self) -> int:
        return 32 - self.reserved_bits

    @staticmethod
    def category(binaryNum: int):
        assert (binaryNum > 0 and binaryNum < 256)

        if (binaryNum < 128):
            return IPClass.A
        elif (binaryNum < 192):
            return IPClass.B
        elif (binaryNum < 224):
            return IPClass.C
        elif binaryNum < 240:
            return IPClass.D
        else:
            return IPClass.E
