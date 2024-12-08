import rich
import json
import functools
from typing import TypedDict, Callable
from os.path import exists
from data.settings import CONFIG_PATH

DEFAULT_CONFIG = {
    "packages_dir_path":None,
    "packages":[]
}

class TypedConfig(TypedDict):
    packages_dir_path: str
    packages: list[dict]

def create_config(config_path: str = CONFIG_PATH):
    if not exists(config_path):
        with open(config_path, 'w') as config_file:
            json.dump(config_file, DEFAULT_CONFIG)

def load_config(config_path: str = CONFIG_PATH) -> TypedConfig:
    create_config(config_path=config_path)
    return json.load(open(config_path))

def reload_config_deco(func: Callable[..., None], **kwargs):
    """Reload config in global var `config`"""
    rich.print(f'invoked: {reload_config_deco.__name__}')
    @functools.wraps(func)
    def wrapper():
        global config
        config = load_config()
        return func(**kwargs)
    return wrapper

def reload_config():
    """Reload config in global var `config`"""
    global config
    config = load_config()
    rich.print(f'invoked: {__name__}')

config = load_config()
