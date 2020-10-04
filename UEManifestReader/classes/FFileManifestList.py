# -*- coding: utf-8 -*-
from typing import List
from UEManifestReader.enums import *
from UEManifestReader.converter import *
from UEManifestReader.classes.FChunkDataList import FChunkDataList
from UEManifestReader.classes.stream_reader import ConstBitStreamWrapper

# A data structure describing the part of a chunk used to construct a file
class FChunkPart():
   def __init__(self, Guid: str, Offset: int, Size: int):
       # The GUID of the chunk containing this part.
       self.Guid = Guid
       # The offset of the first byte into the chunk.
       self.Offset = Offset
       # The size of this part.
       self.Size = Size

class FFileManifest():
    def __init__(self):
        # The build relative filename.
        self.Filename = None
        # Whether this is a symlink to another file.
        self.SymlinkTarget = None
        # The file SHA1.
        self.FileHash = None
        # The flags for this file.
        self.FileMetaFlags = None
        # The install tags for this file.
        self.InstallTags = None
        # The list of chunk parts to stitch.
        self.ChunkParts = []
        # The size of this file.
        self.FileSize = None

class FFileManifestList():
    def __init__(self, reader: ConstBitStreamWrapper):
        StartPos = reader.bytepos
        DataSize = reader.read_uint32()
        DataVersion = reader.read_uint8()

        ElementCount = reader.read_int32()
        self.FileManifest = [FFileManifest() for _ in range(ElementCount)]

        # Serialise the ManifestMetaVersion::Original version variables.
        if (DataVersion >= EFileManifestListVersion.Original.value):
            for idx, _ in enumerate(self.FileManifest):
                self.FileManifest[idx].Filename = reader.read_string()

            for idx, _ in enumerate(self.FileManifest):
                self.FileManifest[idx].SymlinkTarget = reader.read_string()

            for idx, _ in enumerate(self.FileManifest):
                self.FileManifest[idx].FileHash = reader.read_bytes(20)

            for idx, _ in enumerate(self.FileManifest):
                self.FileManifest[idx].FileMetaFlags = reader.read_uint8()

            for idx, _ in enumerate(self.FileManifest):
                self.FileManifest[idx].InstallTags = reader.read_array(reader.read_string)
            
            for idx, _ in enumerate(self.FileManifest):
                self.FileManifest[idx].ChunkParts = self.ReadChunkParts(reader)

        # We must always make sure to seek the archive to the correct end location.
        reader.bytepos = StartPos + DataSize

    def ReadChunkParts(self, reader: ConstBitStreamWrapper) -> List[FChunkPart]:
        ChunkCount = reader.read_int32()
        FChunkParts = []
        for _ in range(ChunkCount):
            reader.skip(4)
            FChunkParts.append(
                FChunkPart(
                    Guid = self.ReadFChunkPartGuid(reader),
                    Offset = reader.read_int32(),
                    Size = reader.read_int32()
                )
            )
        return FChunkParts

    def ReadFChunkPartGuid(self, reader: ConstBitStreamWrapper) -> str:
        hex_str = ''
        hex_str += SwapOrder(reader.read_bytes(4))
        hex_str += SwapOrder(reader.read_bytes(4))
        hex_str += SwapOrder(reader.read_bytes(4))
        hex_str += SwapOrder(reader.read_bytes(4))
        return hex_str.upper()