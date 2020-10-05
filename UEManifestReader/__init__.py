# -*- coding: utf-8 -*-
import json
import asyncio
import aiohttp
from .enums import Platform
from .converter import *
from .classes.FManifestData import FManifestData

class UEManifestReader():
    def __init__(self, **kwargs):
        self.loop = kwargs.get('loop', asyncio.get_event_loop())
        self.is_serialized = False
    
    async def download_manifest(self, platform: Platform = Platform.Windows, return_parsed = True):
        if platform == Platform.Windows:
            launcher_asset_url = 'https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/Windows/4fe75bbc5a674f4f9b356b5c90567da5/Fortnite?label=Live'
        elif platform == Platform.Android:
            launcher_asset_url = 'https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/Android/5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds?label=Live'
        elif platform == Platform.iOS:
            launcher_asset_url = 'https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/IOS/5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds?label=Live'
        else:
            raise ValueError(Platform)

        async with aiohttp.ClientSession() as session:
            # Get the EG1 Token to fetch the manifest info
            async with session.post(
                url = 'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token',
                data = {
                    'grant_type': 'client_credentials',
                    'token_token': 'eg1'
                },
                headers = {
                    'Authorization': 'basic MzRhMDJjZjhmNDQxNGUyOWIxNTkyMTg3NmRhMzZmOWE6ZGFhZmJjY2M3Mzc3NDUwMzlkZmZlNTNkOTRmYzc2Y2Y='
                }
            ) as response:
                access_token = (await response.json())['access_token']
            
            async with session.get(
                url = launcher_asset_url,
                headers = {'Authorization': f'bearer {access_token}'}
            ) as response:
                manifest_info = await response.json()
        
            distribution = manifest_info['items']['MANIFEST']['distribution']
            path = manifest_info['items']['MANIFEST']['path']
            signature = manifest_info['items']['MANIFEST']['signature']
            manifest_url = f'{distribution}{path}?{signature}'

            async with session.get(manifest_url) as response:
                manifest = await response.read()
            
        if return_parsed:
            return self.parse_manifest(manifest)

    def return_manifest_as_json(self, manifest) -> dict:
        parsed = {}

        if self.is_serialized:
            return {
                "ManifestVersion": manifest.Meta.FeatureLevelInt,
                "bIsFileData": manifest.Meta.IsFileData,
                "AppID": manifest.Meta.AppID,
                "AppNameString": manifest.Meta.AppName,
                "BuildVersionString": manifest.Meta.BuildVersion,
                "LaunchExeString": manifest.Meta.LaunchExe,
                "LaunchCommand": manifest.Meta.LaunchCommand,
                "PrereqIds": manifest.Meta.PrereqIds,
                "PrereqName": manifest.Meta.PrereqName,
                "PrereqPath": manifest.Meta.PrereqPath,
                "PrereqArgs": manifest.Meta.PrereqArgs,
                "ChunkSubDir": manifest.Meta.ChunkSubDir,
                "FileSubDir": manifest.Meta.FileSubDir,
                "FileManifestList": [
                    {
                        "Filename": fileManifest.Filename,
                        "FileHash": fileManifest.FileHash.hex().upper(),
                        "FileChunkParts": [{
                            "Offset": str(ChunkPart.Offset),
                            "Size": str(ChunkPart.Size),
                            "Guid": ChunkPart.Guid,
                        } for ChunkPart in fileManifest.ChunkParts]
                    }
                    for fileManifest in manifest.FileManifestList.FileManifest],
                "ChunkHashList": {ChunkInfo.Guid: str(ChunkInfo.Hash) for ChunkInfo in manifest.ChunkDataList.ChunkList},
                "DataGroupList": {ChunkInfo.Guid: str(ChunkInfo.GroupNumber)[-2:] for ChunkInfo in manifest.ChunkDataList.ChunkList}
            }
        else:
            manifest['ManifestFileVersion'] = str(int(manifest['ManifestFileVersion']))
            manifest['AppID'] = str(int(manifest['AppID']))

            for File in manifest['FileManifestList']:
                for chunk in File['FileChunkParts']:
                    chunk['Offset'] = ParseIntBlob32(chunk['Offset'])
                    chunk['Size'] = ParseIntBlob32(chunk["Size"])

            for Guid, GroupNumber in manifest['DataGroupList'].items():
                manifest['DataGroupList'][Guid] = str(GroupNumber)[-2:]

            for Guid, Hash in manifest['ChunkHashList'].items():
                manifest['ChunkHashList'][Guid] = ParseIntBlob64(Hash)
        
            return manifest

    def parse_manifest(self, manifest: bytes):
        try:
            manifest = json.loads(manifest)
        except:
            self.is_serialized = True
            manifest = FManifestData(manifest)

        return self.return_manifest_as_json(manifest)