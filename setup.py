from setuptools import setup, find_packages

setup(
    name = 'UEManifestReader',
    version = '0.0.1',
    description = 'Read and parse Unreal Engine Manifests',
    url = 'https://github.com/LupusLeaks/UEManifestReader',
    author_email = 'admin@ezfn.dev',
    packages = find_packages(),
    license='MIT',
    install_requires = ['aiohttp', 'bitstring']
)