# -*- coding: utf-8 -*-
from UEManifestReader.enums import *
from UEManifestReader.classes.stream_reader import ConstBitStreamWrapper

# The manifest header magic codeword, for quick checking that the opened file is probably a manifest file.
MANIFEST_HEADER_MAGIC = 0x44BEC00C

class FManifestHeader():
    def __init__(self, reader: ConstBitStreamWrapper, StartPos: int = 0):
        self.Magic = reader.read_uint32()
        # The size of this header.
        self.HeaderSize = reader.read_uint32()
        # The size of this data uncompressed.
        self.DataSizeUncompressed = reader.read_uint32()
        # The size of this data compressed.
        self.DataSizeCompressed = reader.read_uint32()
        # The SHA1 hash for the manifest data that follows.
        self.SHAHash = reader.read_bytes(20)
        # How the chunk data is stored.
        self.StoredAs = reader.read_uint8()

        bSuccess = self.Magic == MANIFEST_HEADER_MAGIC
        ExpectedSerializedBytes = ManifestHeaderVersionSizes[EFeatureLevel.Original.value]

        # After the Original with no specific version serialized, the header size increased and we had a version to load.
        if (bSuccess and self.HeaderSize > ManifestHeaderVersionSizes[EFeatureLevel.Original.value]):
            # The version of this header and manifest data format, driven by the feature level.
            Version = reader.read_int32()
            self.Version = ([e for e in EFeatureLevel.__members__.values() if e.value == Version])[0]
            ExpectedSerializedBytes = ManifestHeaderVersionSizes[self.Version.value]
        elif (bSuccess):
            # Otherwise, this header was at the version for a UObject class before this code refactor.
            self.Version = EFeatureLevel.StoredAsCompressedUClass

        # Make sure the expected number of bytes were serialized. In practice this will catch errors where type
		# serialization operators changed their format and that will need investigating.
        bSuccess = bSuccess and (reader.bytepos - StartPos) == ExpectedSerializedBytes
        if (bSuccess):
            # Make sure the archive now points to data location.
            reader.bytepos = StartPos + self.HeaderSize
        else:
            # If we had a serialization error when loading, raise an error
            raise Exception('Failed to read the Manifest Header')