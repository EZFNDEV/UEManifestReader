# -*- coding: utf-8 -*-
# Credits to: https://github.com/Shiqan/fortnite-replay-reader/blob/master/ray/reader.py
import sys, bitstring
from enum import Enum

class BitTypes(Enum):
    """ See bitstring for more types """
    INT_32 = 'intle:32'
    UINT8 = 'uint:8'
    UINT_32 = 'uintle:32'
    UINT_64 = 'uintle:64'
    BIT = 'bin:1'
    BYTE = 'bytes:1'
        
class ConstBitStreamWrapper(bitstring.ConstBitStream):
    """ Wrapper for the bitstring.ConstBitStream class to provide some convience methods """

    def skip(self, count):
        """ Skip the next count bytes """
        self.bytepos += count
    
    def read_uint8(self):
        """ Read and interpret next 8 bits as an unassigned integer """
        return self.read(BitTypes.UINT8.value)

    def read_uint32(self):
        """ Read and interpret next 32 bits as an unassigned integer """
        return self.read(BitTypes.UINT_32.value)

    def read_int32(self):
        """ Read and interpret next 32 bits as an signed integer """
        return self.read(BitTypes.INT_32.value)

    def read_uint64(self):
        """  Read and interpret next 64 bits as an unassigned integer """
        return self.read(BitTypes.UINT_64.value)

    def read_byte(self):
        """ Read and interpret next bit as an integer """
        return int.from_bytes(self.read(BitTypes.BYTE.value), byteorder='little')

    def read_bytes(self, size):
        """ Read and interpret next bit as an integer """
        return self.read('bytes:'+str(size))

    def read_array(self, f):
        """ Read an array where the first 32 bits indicate the length of the array """
        length = self.read_uint32()
        return [f() for _ in range(length)]

    def read_string(self):
        """ Read and interpret next i bits as a string where i is determined defined by the first 32 bits """
        size = self.read_int32()

        if size == 0:
            return ""

        is_unicode = size < 0

        if is_unicode:
            size *= -2
            return self.read_bytes(size)[:-2].decode('utf-16')

        stream_bytes = self.read_bytes(size)
        string = stream_bytes[:-1]
        if stream_bytes[-1] != 0:
            raise Exception('End of string not zero')

        try:
            return string.decode('utf-8')
        except UnicodeDecodeError:
            return string.decode('latin-1')