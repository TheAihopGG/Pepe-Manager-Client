import json
from services.config import TypedConfig
from typing import TypedDict
from os.path import exists

class TypedPackage(TypedDict):
    id: int
    name: str
    author: str
    version: str
    url: str

def is_package(package_dir: str, config: TypedConfig) -> (None | TypedPackage):
    package_config_path = f'{config['packages_dir_path']}/{package_dir}/config.json'
    if exists(package_config_path):
        package_config: TypedPackage = json.load(open(package_config_path))
        if set(package_config.keys()) == set(TypedPackage.__mutable_keys__):
            return package_config
    else:
        return None