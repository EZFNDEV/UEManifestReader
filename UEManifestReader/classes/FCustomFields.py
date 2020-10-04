# -*- coding: utf-8 -*-
from UEManifestReader.enums import *
from UEManifestReader.classes.stream_reader import ConstBitStreamWrapper

class FCustomFields():
    def __init__(self, reader: ConstBitStreamWrapper):
        StartPos = reader.bytepos
        DataSize = reader.read_uint32()
        DataVersion = reader.read_uint8()

        ElementCount = reader.read_int32()
        self.CustomFields = {}

        # Serialise the ManifestMetaVersion::Original version variables.
        if (DataVersion >= EChunkDataListVersion.Original.value):
            for _ in range(ElementCount):
                self.CustomFields[reader.read_string()] = None
            
            for key in self.CustomFields.keys():
                self.CustomFields[key] = reader.read_string()

        # We must always make sure to seek the archive to the correct end location.
        reader.bytepos = StartPos + DataSize