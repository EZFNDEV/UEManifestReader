# -*- coding: utf-8 -*-
# from hashlib import sha1
from UEManifestReader.enums import *
from UEManifestReader.classes.stream_reader import ConstBitStreamWrapper

# FManifestMeta - The data implementation for a build meta data.
class FManifestMeta():
    def __init__(self, reader: ConstBitStreamWrapper):
        # Serialise the data header type values.
        StartPos = reader.bytepos

        DataSize = reader.read_uint32()
        DataVersion = reader.read_uint8()

        # Serialise the ManifestMetaVersion::Original version variables.
        if (DataVersion >= EManifestMetaVersion.Original.value):
            self.FeatureLevelInt = reader.read_uint32()
            # Whether this is a legacy 'nochunks' build.
            self.IsFileData = reader.read_byte() == 1
            # The app id provided at generation.
            self.AppID = reader.read_uint32()
            # The app name string provided at generation.
            self.AppName = reader.read_string()
            # The build version string provided at generation.
            self.BuildVersion = reader.read_string()
            # The file in this manifest designated the application executable of the build.
            self.LaunchExe = reader.read_string()
            # The command line required when launching the application executable.
            self.LaunchCommand = reader.read_string()
            # The set of prerequisite ids for dependencies that this build's prerequisite installer will apply.
            self.PrereqIds = reader.read_array(reader.read_string)
            # A display string for the prerequisite provided at generation.
            self.PrereqName = reader.read_string()
            # The file in this manifest designated the launch executable of the prerequisite installer.
            self.PrereqPath = reader.read_string()
            # The command line required when launching the prerequisite installer.
            self.PrereqArgs = reader.read_string()

        # Serialise the BuildId.
        if (DataVersion >= EManifestMetaVersion.SerialisesBuildId.value):
            self.BuildId = reader.read_string()
        # Otherwise, initialise with backwards compatible default when loading.
        else:
            self.BuildId = 'Not added yet' # self.GetBackwardsCompatibleBuildId()
        
        # Chunk Sub Dir
        if (self.FeatureLevelInt < EFeatureLevel.DataFileRenames.value):
            self.ChunkSubDir = 'Chunks'
        elif (self.FeatureLevelInt < EFeatureLevel.ChunkCompressionSupport.value):
            self.ChunkSubDir = 'ChunksV2'
        elif (self.FeatureLevelInt < EFeatureLevel.VariableSizeChunksWithoutWindowSizeChunkInfo.value):
            self.ChunkSubDir = 'ChunksV3'
        else:
            self.ChunkSubDir = 'ChunksV4'

        # File Sub Dir
        if (self.FeatureLevelInt < EFeatureLevel.DataFileRenames.value):
            self.FileSubDir = 'Files'
        elif (self.FeatureLevelInt < EFeatureLevel.StoresChunkDataShaHashes.value):
            self.FileSubDir = 'FilesV2'
        else:
            self.FileSubDir = 'FilesV3'
        
        # We must always make sure to seek the archive to the correct end location.
        reader.bytepos = StartPos + DataSize

    def GetBackwardsCompatibleBuildId(self) -> str:
        # Sha.Update((const uint8*)&ManifestMeta.AppID, sizeof(ManifestMeta.AppID));
        # // For platform agnostic result, we must use UTF8. TCHAR can be 16b, or 32b etc.
        # FTCHARToUTF8 UTF8AppName(*ManifestMeta.AppName);
        # FTCHARToUTF8 UTF8BuildVersion(*ManifestMeta.BuildVersion);
        # FTCHARToUTF8 UTF8LaunchExe(*ManifestMeta.LaunchExe);
        # FTCHARToUTF8 UTF8LaunchCommand(*ManifestMeta.LaunchCommand);
        # Sha.Update((const uint8*)UTF8AppName.Get(), sizeof(ANSICHAR) * UTF8AppName.Length());
        # Sha.Update((const uint8*)UTF8BuildVersion.Get(), sizeof(ANSICHAR) * UTF8BuildVersion.Length());
        # Sha.Update((const uint8*)UTF8LaunchExe.Get(), sizeof(ANSICHAR) * UTF8LaunchExe.Length());
        # Sha.Update((const uint8*)UTF8LaunchCommand.Get(), sizeof(ANSICHAR) * UTF8LaunchCommand.Length());
        # Sha.Final();
        # Sha.GetHash(Hash.Hash);
        pass