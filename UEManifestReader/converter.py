# -*- coding: utf-8 -*-
def ULongToHexHash(long: int):
    buffer = [None] * 8
    buffer[0] = (long >> 56).to_bytes(28,byteorder='little').hex()[:2]
    buffer[1] = (long >> 48).to_bytes(28,byteorder='little').hex()[:2]
    buffer[2] = (long >> 40).to_bytes(28,byteorder='little').hex()[:2]
    buffer[3] = (long >> 32).to_bytes(28,byteorder='little').hex()[:2]
    buffer[4] = (long >> 24).to_bytes(28,byteorder='little').hex()[:2]
    buffer[5] = (long >> 16).to_bytes(28,byteorder='little').hex()[:2]
    buffer[6] = (long >> 8).to_bytes(28,byteorder='little').hex()[:2]
    buffer[7] = (long).to_bytes(28,byteorder='little').hex()[:2]
    return (''.join(buffer)).upper()

def SwapOrder(data: bytes) -> bytes:
    hex_str = data.hex()
    data = [None] * len(hex_str)
    # TODO: Improve this ^
    if len(hex_str) == 8:
        data[0] = hex_str[6]
        data[1] = hex_str[7]
        data[2] = hex_str[4]
        data[3] = hex_str[5]

        data[4] = hex_str[2]
        data[5] = hex_str[3]
        data[6] = hex_str[0]
        data[7] = hex_str[1]

        return ''.join(data)

def ParseIntBlob32(_hash: str) -> str:
    if (4 < (len(_hash) % 3) or len(_hash) % 3 != 0):
        raise ValueError(f'Failed to convert {_hash} to Blob 32')
    
    numbers = []
    i = 0
    while i < len(_hash):
        numstr = int(_hash[i] + _hash[i+1] + _hash[i+2])
        numbers.append(numstr)
        i += 3

    return int.from_bytes(bytearray(numbers), byteorder='little', signed=False)

def ParseIntBlob64(_hash: str) -> str:
    if (len(_hash) % 3 != 0):
        raise ValueError(f'Failed to convert {_hash} to Blob 64')

    hex_str = ""
    i = 0
    while i < len(_hash):
        num_str = hex(int((str(_hash[i]) + str(_hash[i+1]) + str(_hash[i+2]))))[2:]
        if len(num_str) == 1:
            num_str = f'0{num_str}'
        
        hex_str = num_str + hex_str
        i += 3

    return hex_str