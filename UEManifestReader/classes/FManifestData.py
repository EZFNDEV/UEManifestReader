# -*- coding: utf-8 -*-
import zlib
from UEManifestReader.enums import *
from UEManifestReader.classes.FCustomFields import FCustomFields
from UEManifestReader.classes.FManifestMeta import FManifestMeta
from UEManifestReader.classes.FChunkDataList import FChunkDataList
from UEManifestReader.classes.FManifestHeader import FManifestHeader
from UEManifestReader.classes.stream_reader import ConstBitStreamWrapper
from UEManifestReader.classes.FFileManifestList import FFileManifestList

# FManifestData - The public interface to load/saving manifest files.
class FManifestData():
    def __init__(self, data: bytes):
        self.reader = ConstBitStreamWrapper(data)
        self.start()

    def start(self):
        StartPos = self.reader.bytepos

        # Read the Manifest Header
        self.Header = FManifestHeader(self.reader)

        # If we are loading an old format, defer to the old code!
        if (self.Header.Version.value < EFeatureLevel.StoredAsBinaryData.value):
            FullDataSize = GetFullDataSize(Header)
            FullData = reader.read_bytes(FullDataSize)
            self.reader.bytepos = StartPos

            temp = FManifestData(self.reader.read_bytes(FullDataSize))
            self.Meta = temp.Meta
            self.ChunkDataList = temp.ChunkDataList
            self.FileManifestList = temp.FileManifestList
            self.CustomFields = temp.CustomFields
            return
        else:
            # Compression format selection - we only have one right now.
            # Fill the array with loaded data.
            # DataSizeCompressed always equals the size of the data following the header.
            if self.Header.StoredAs == EManifestStorageFlags.Compressed.value:
                Decompressed = zlib.decompress(self.reader.read_bytes(self.Header.DataSizeCompressed))
                ManifestRawData = ConstBitStreamWrapper(Decompressed)
            elif self.Header.StoredAs == EManifestStorageFlags.Encrypted.value:
                raise Exception('Encrypted Manifests are not supported yet')
        
        # Read the Manifest Meta
        self.Meta = FManifestMeta(ManifestRawData)
        # Read the Manifest Chunk List
        self.ChunkDataList = FChunkDataList(ManifestRawData)
        # Read the Manifest File List
        self.FileManifestList = FFileManifestList(ManifestRawData)
        # Read the Custom Fields
        self.CustomFields = FCustomFields(ManifestRawData)

    def GetFullDataSize(self) -> int:
        bIsCompressed = self.Header.StoredAs == EManifestStorageFlags.Compressed
        return self.Header.HeaderSize + (bIsCompressed if Header.DataSizeCompressed else Header.DataSizeUncompressed)