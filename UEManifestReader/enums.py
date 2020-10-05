# -*- coding: utf-8 -*-
from enum import Enum

class Platform(Enum):
    Windows = 0,
    Android = 1,
    iOS = 2,

# Enum which describes the FManifestMeta data version.
class EManifestMetaVersion(Enum):
    Original = 0
    SerialisesBuildId = 1
    # Always after the latest version, signifies the latest version plus 1 to allow initialization simplicity.
    LatestPlusOne = 2
    Latest = LatestPlusOne - 1

ManifestHeaderVersionSizes = [
    # EFeatureLevel::Original is 37B (32b Magic, 32b HeaderSize, 32b DataSizeUncompressed, 32b DataSizeCompressed, 160b SHA1, 8b StoredAs)
    # This remained the same all up to including EFeatureLevel::StoresPrerequisiteIds.
    37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37,
    # EFeatureLevel::StoredAsBinaryData is 41B, (296b Original, 32b Version).
    # This remained the same all up to including EFeatureLevel::UsesBuildTimeGeneratedBuildId.
    41, 41, 41, 41, 41
]

# An enum type to describe supported features of a certain manifest.

class EFeatureLevel(Enum):
    # The original version.
	Original = 0

    # Support for custom fields.
	CustomFields = 1
    # Started storing the version number.
	StartStoringVersion = 2
	# Made after data files where renamed to include the hash value, these chunks now go to ChunksV2.
	DataFileRenames = 3
	# Manifest stores whether build was constructed with chunk or file data.
	StoresIfChunkOrFileData = 4
	# Manifest stores group number for each chunk/file data for reference so that external readers don't need to know how to calculate them.
	StoresDataGroupNumbers = 5
	# Added support for chunk compression, these chunks now go to ChunksV3. NB: Not File Data Compression yet.
	ChunkCompressionSupport = 6
	# Manifest stores product prerequisites info.
	StoresPrerequisitesInfo = 7
	# Manifest stores chunk download sizes.
	StoresChunkFileSizes = 8
	# Manifest can optionally be stored using UObject serialization and compressed.
	StoredAsCompressedUClass = 9
	# These two features were removed and never used.
	UNUSED_0 = 10
	UNUSED_1 = 11
	# Manifest stores chunk data SHA1 hash to use in place of data compare, for faster generation.
	StoresChunkDataShaHashes = 12
	# Manifest stores Prerequisite Ids.
	StoresPrerequisiteIds = 13
	# The first minimal binary format was added. UObject classes will no longer be saved out when binary selected.
	StoredAsBinaryData = 14
	# Temporary level where manifest can reference chunks with dynamic window size, but did not serialize them. Chunks from here onwards are stored in ChunksV4.
	VariableSizeChunksWithoutWindowSizeChunkInfo = 15
	# Manifest can reference chunks with dynamic window size, and also serializes them.
	VariableSizeChunks = 16
	# Manifest uses a build id generated from its metadata.
	UsesRuntimeGeneratedBuildId = 17
	# Manifest uses a build id generated unique at build time, and stored in manifest.
	UsesBuildTimeGeneratedBuildId = 18

	# !! Always after the latest version entry, signifies the latest version plus 1 to allow the following Latest alias.
	LatestPlusOne = 19
	# An alias for the actual latest version value.
	Latest = LatestPlusOne - 1
	# An alias to provide the latest version of a manifest supported by file data (nochunks).
	LatestNoChunks = StoresChunkFileSizes
	# An alias to provide the latest version of a manifest supported by a json serialized format.
	LatestJson = StoresPrerequisiteIds
	# An alias to provide the first available version of optimised delta manifest saving.
	FirstOptimisedDelta = UsesRuntimeGeneratedBuildId

	# More aliases, but this time for values that have been renamed
	StoresUniqueBuildId = UsesRuntimeGeneratedBuildId

	# JSON manifests were stored with a version of 255 during a certain CL range due to a bug.
	# We will treat this as being StoresChunkFileSizes in code.
	BrokenJsonVersion = 255
	# This is for UObject default, so that we always serialize it.

	Invalid = -1

# A flags enum for manifest headers which specify storage types.
class EManifestStorageFlags(Enum):
    # Stored as raw data.
    Null       = 0,
    # Flag for compressed data.
    Compressed = 1
    # Flag for encrypted. If also compressed, decrypt first. Encryption will ruin compressibility.
    Encrypted  = 1 << 1



# Enum which describes the FChunkDataList data version.
class EChunkDataListVersion(Enum):
    Original = 0
    # Always after the latest version, signifies the latest version plus 1 to allow initialization simplicity.
    LatestPlusOne = 1
    Latest = LatestPlusOne - 1

# Enum which describes the FFileManifestList data version.
class EFileManifestListVersion(Enum):
    Original = 0
    # Always after the latest version, signifies the latest version plus 1 to allow initialization simplicity.
    LatestPlusOne = 1
    Latest = LatestPlusOne - 1

# Enum which describes the FChunkDataList data version.
class EChunkDataListVersion(Enum):
    Original = 0
    # Always after the latest version, signifies the latest version plus 1 to allow initialization simplicity.
    LatestPlusOne = 1
    Latest = LatestPlusOne - 1