from typing import TypedDict
from os.path import exists
from data.settings import CONFIG_PATH
from json import dump

DEFAULT_CONFIG = {
    "packages_dir_path":None
}

class TypedConfig(TypedDict):
    packages_dir_path: str

def create_config(config_path: str = CONFIG_PATH):
    if not exists(config_path):
        with open(config_path, 'w') as config_file:
            dump(config_file, DEFAULT_CONFIG)

__all__: tuple = (
    DEFAULT_CONFIG,
    TypedConfig,
    create_config
)
