import os
import rich
import json
import functools
from os.path import exists
from typing import Callable
from logging import *
from data.settings import *
from services.config import *
from services.package import TypedPackage, is_package

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
    UPDATE_PACKAGES = 'update-packages'


class Actions:
    """Class with actions functions"""
    @staticmethod
    @debug_invoke_deco
    def list():
        """Shows downloaded packages"""
        global config
        config = load_config()
        rich.print('Packages list:')
        if packages := config['packages']:
            for package in packages:
                rich.print(package['name'], package['version'])
        else:
            rich.print('There is no downloaded packages')

    @staticmethod
    @debug_invoke_deco
    def update_packages():
        """Updates config['packages']"""
        global config
        config = load_config()
        edit_config('packages', [is_package(package_dir, config) for package_dir in os.listdir(config['packages_dir_path'])])

actions: dict[str, Callable[..., None]] = {
    ActionsList.LIST: Actions.list,
    ActionsList.UPDATE_PACKAGES: Actions.update_packages
}
