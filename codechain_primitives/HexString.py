from rlp import encode
import string
import binascii
import re


class _HexString(bytes):

    def __new__(cls, value, *args, **kwargs):
        if type(value) is str:
            if not cls.check_string(value):
                raise ValueError(f"Expected hexstring but found {value}")
            value = bytes.fromhex(
                value[2:] if value.startswith("0x") else value)

        if hasattr(cls, 'LENGTH') and len(value) > cls.LENGTH:
            raise ValueError(
                f"Expected {cls.LENGTH} byte hexstring for creating {cls.__name__} but found {value}({len(value)})")
        return super().__new__(cls, value, *args, **kwargs)

    @classmethod
    def check_string(cls, value):
        return None != re.match("^(0x)?[0-9a-fA-F]{" + str(cls.LENGTH * 2) + "}$", value)

    @classmethod
    def from_rlp(cls, buffer):
        if not isinstance(buffer, (bytes, bytearray)):
            raise ValueError("Argument should be bytearray")
        data = buffer[1:]
        first = buffer[0]

        if cls is H512:
            length = data[0]
            data = data[1:]
            if first != 0xb8 or len(data) != length:
                raise ValueError("Invalid RLP data")
        else:
            length = first - 0x80
            if len(data) != length:
                raise ValueError("Invalid RLP data")

        return cls(data)

    @classmethod
    def check(cls, param):
        try:
            return True if type(param) is cls else cls.check_string(param)
        except:
            return False

    def to_encoded_object(self):
        return self

    def rlp_bytes(self):
        return encode(self.to_encoded_object())

    def __str__(self):
        return binascii.hexlify(self).decode('ascii')

    def to_json(self):
        return binascii.hexlify(self).decode('ascii')

    @classmethod
    def from_json(cls, string):
        return cls(string)


class H128(_HexString):
    LENGTH = 16
    ZERO = bytes.fromhex("00000000000000000000000000000000")


class H160(_HexString):
    LENGTH = 20
    ZERO = bytes.fromhex("0000000000000000000000000000000000000000")


class H256(_HexString):
    LENGTH = 32
    ZERO = bytes.fromhex(
        "0000000000000000000000000000000000000000000000000000000000000000")


class H512(_HexString):
    LENGTH = 64
    ZERO = bytes.fromhex(
        "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")