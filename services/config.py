import json
from services.typed_dicts import TypedConfig
from typing import Any
from os.path import exists
from data.settings import CONFIG_PATH

DEFAULT_CONFIG = {
    "packages_dir_path":None,
    "packages":[]
}


def init_config(config_path: str = CONFIG_PATH):
    if not exists(config_path):
        with open(config_path, 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file)


def load_config(config_path: str = CONFIG_PATH) -> TypedConfig:
    init_config(config_path=config_path)
    return json.load(open(config_path))


def edit_config(key: str, value: Any):
    with open(CONFIG_PATH, 'r') as config_file:
        config: TypedConfig = json.load(config_file)
    config[key] = value
    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config, config_file)
