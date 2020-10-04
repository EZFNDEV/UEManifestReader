 # UEManifestReader

[![Current pypi version](https://img.shields.io/pypi/v/UEManifestReader.svg)](https://pypi.org/project/UEManifestReader/)

# Basic usage
```py
import json
import UEManifestReader
from UEManifestReader.enums import Platform

Reader = UEManifestReader.UEManifestReader()

async def downloader():
    manifest = await Reader.download_manifest(Platform.Android)
    open('android_manifest.json', 'w+').write(json.dumps(manifest, indent=2))

Reader.loop.run_until_complete(downloader())
```
# Need help?
If you need more help feel free to join this [discord server](https://discord.gg/jht3aM2).
