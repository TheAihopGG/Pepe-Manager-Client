import json
from services.config import TypedConfig
from services.typed_dicts import TypedPackage
from os.path import exists

def is_package(
    package_dir: str,
    config: TypedConfig
) -> (None | TypedPackage):
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
    return package_name in (package_config['name'] for package_config in config['packages']) and package_version in (package_config['version'] for package_config in config['packages']) if config['packages'] else False
