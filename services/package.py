import json
from services.config import TypedConfig
from services.typed_dicts import TypedPackage
from os.path import exists

__doc__ = """Contains packages' tools"""

def is_package(
    package_dir: str,
    config: TypedConfig
) -> (None | TypedPackage):
    """Checks package's config for necessary values"""
    package_config_path = f'{config['packages_dir_path']}/{package_dir}/config.json'
    if exists(package_config_path):
        package_config: TypedPackage = json.load(open(package_config_path))
        if set(package_config.keys()) == set(TypedPackage.__mutable_keys__):
            return package_config
    else:
        return None


def is_downloaded_package(
    package_name: str,
    package_version: str,
    config: TypedConfig
) -> bool:
    return (package_name in (package_config['name'] if package_config else None for package_config in config['packages']) and package_version in (package_config['version'] for package_config in config['packages'])) if config['packages'] else False


def get_package_config_by_name_version(
    package_name: str,
    package_version: str,
    config: TypedConfig
) -> TypedPackage:
    for package_config in config['packages']:
        if package_config['name'] == package_name and package_config['version'] == package_version:
            return package_config
