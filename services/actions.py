import os
import rich
import json
import functools
from typing import Callable
from logging import *
from data.settings import *
from services.config import *

config = load_config()

def debug_invoke_deco(func: Callable[..., None], **kwargs):
    """Prints function name"""
    @functools.wraps(func)
    def wrapper():
        rich.print(f'invoked: {func.__name__}')
        return func(**kwargs)
    return wrapper


class ActionsList:
    """Class with all actions"""
    LIST = 'list'


class Actions:
    """Class with actions functions"""
    @staticmethod
    @reload_config_deco
    @debug_invoke_deco
    def list():
        rich.print_json(str(config['packages']))

actions: dict[str, Callable[..., None]] = {
    ActionsList.LIST: Actions.list
}
