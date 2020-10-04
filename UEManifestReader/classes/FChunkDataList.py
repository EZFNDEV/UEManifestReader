# -*- coding: utf-8 -*-
from UEManifestReader.enums import *
from UEManifestReader.converter import *
from UEManifestReader.classes.stream_reader import ConstBitStreamWrapper

class FChunkInfo():
   def __init__(self):
       # The GUID for this data.
        self.Guid = None
        # The FRollingHash hashed value for this chunk data.
        self.Hash = None
        # The FSHA hashed value for this chunk data.
        self.ShaHash = None
        # The group number this chunk divides into.
        self.GroupNumber = None
        # The window size for this chunk
        self.WindowSize = 1048576
        # The file download size for this chunk.
        self.FileSize = None

class FChunkDataList():
    def __init__(self, reader: ConstBitStreamWrapper):
        StartPos = reader.bytepos
        DataSize = reader.read_uint32()
        DataVersion = reader.read_uint8()

        ElementCount = reader.read_int32()
        self.ChunkList = [FChunkInfo() for _ in range(ElementCount)]
        # For a struct list type of data, we serialise every variable as it's own flat list.
        # This makes it very simple to handle or skip, extra variables added to the struct later.

        # Serialise the ManifestMetaVersion::Original version variables.
        if (DataVersion >= EChunkDataListVersion.Original.value):
            for idx, _ in enumerate(self.ChunkList):
                self.ChunkList[idx].Guid = self.ReadFChunkInfoGuid(reader)

            for idx, _ in enumerate(self.ChunkList):
                self.ChunkList[idx].Hash = ULongToHexHash(reader.read_uint64())

            for idx, _ in enumerate(self.ChunkList):
                self.ChunkList[idx].ShaHash = reader.read_bytes(20)

            for idx, _ in enumerate(self.ChunkList):
                self.ChunkList[idx].GroupNumber = int(reader.read_uint8())

            for idx, _ in enumerate(self.ChunkList):
                self.ChunkList[idx].WindowSize = reader.read_int32()

            for idx, _ in enumerate(self.ChunkList):
                self.ChunkList[idx].FileSize = int(reader.read_uint8())

        # We must always make sure to seek the archive to the correct end location.
        reader.bytepos = StartPos + DataSize

    def ReadFChunkInfoGuid(self, reader: ConstBitStreamWrapper) -> str:
        hex_str = ''
        hex_str += SwapOrder(reader.read_bytes(4))
        hex_str += SwapOrder(reader.read_bytes(4))
        hex_str += SwapOrder(reader.read_bytes(4))
        hex_str += SwapOrder(reader.read_bytes(4))
        return hex_str.upper()