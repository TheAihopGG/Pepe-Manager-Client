import tarfile
import shutil
import os
import rich
import requests
from logging import *
from data.settings import *
from services.config import *
from services.typed_dicts import TypedPackage
from services.package import is_package
from enum import Enum
from urllib.parse import urlparse

__doc__ = """Contains actions' tools and vars"""
config = load_config()

class ActionsList(Enum):
    """Class with actions names"""
    list = 'list'
    update_packages = 'update-packages'
    download = 'download'
    remove = 'remove'
    set = 'set'
    show = 'show'


class Actions:
    """Class with actions functions"""
    @staticmethod
    def list():
        """Shows downloaded packages"""
        rich.print('Packages list:')
        if packages := config['packages']:
            for package in packages:
                rich.print(f'{package['name']}-{package['version']}')

        else:
            rich.print('There is no downloaded packages')

    @staticmethod
    def update_packages():
        """Updates config['packages']"""
        packages: list[TypedPackage] = []
        for package_dir in os.listdir(config['packages_dir_path']):
            if package := is_package(package_dir):
                packages.append(package)

        edit_config('packages', packages)
        rich.print('Packages have updated')
    
    @staticmethod
    def download(
        download_package: TypedPackage,
        packed_package_extension: str = '.tar.gz',
        packages_dir_path = config['packages_dir_path'],
    ):
        """Downloads package from package_url in config['packages_dir_path']"""
        package_dir_name = f'{download_package['name']}{download_package['version']}'

        rich.print(f'Downloading package: {download_package['name']}-{download_package['version']} by @{download_package['author']}')
        rich.print(f'Requesting to {urlparse(download_package['url']).hostname}')
        # download package
        try:
            response = requests.get(download_package['url'])

        except requests.RequestException as error:
            rich.print(error)

        except requests.exceptions.ConnectionError:
            rich.print('Pepe Manager API is offline now')

        else:
            if response.ok:
                with open(f'{packages_dir_path}/{package_dir_name}{packed_package_extension}', 'wb') as packed_package_file:
                    packed_package_file.write(response.content)
                # unpack package
                rich.print(f'Unpacking {download_package['name']}')
                match packed_package_extension:
                    case '.tar.gz':
                        rich.print(f'Detected extension: .tar.gz')
                        packed_package_file = tarfile.open(f'{packages_dir_path}/{package_dir_name}{packed_package_extension}', mode='r:gz')
                        packed_package_file.extractall(packages_dir_path)
                        os.remove(f'{packages_dir_path}/{download_package['name']}{download_package['version']}.tar.gz')
                        rich.print(f'Successfully downloaded {download_package['name']}-{download_package['version']}')
                        # add package to config
                        edit_config('packages', config['packages']+[download_package])
                    
                    case _:
                        rich.print(f'Unsupported package file extension: {packed_package_extension}')

            else:
                rich.print(response.text)

    @staticmethod
    def remove(remove_package: TypedPackage):
        """Removes package in config['packages_dir_path']"""
        # remove package
        rich.print(f'Removing: {remove_package['name']}-{remove_package['version']}')
        for package_dir in os.listdir(config['packages_dir_path']):
            if package := is_package(package_dir, config['packages_dir_path']):
                if package['id'] == remove_package['id']:
                    shutil.rmtree(f'{config['packages_dir_path']}/{package_dir}')

        # remove package from config
        for [index, package] in enumerate(config['packages']):
            if package['id'] == remove_package['id']:
                del config['packages'][index]
                break

        edit_config('packages', config['packages'])
        rich.print(f'Successfully removed {remove_package['name']}-{remove_package['version']}')
    
    @staticmethod
    def set(option: str, value: str):
        """Edits option in config"""
        edit_config(option, value)
    
    @staticmethod
    def show(show_package: TypedPackage):
        """Shows package info"""
        for [key, value] in show_package.items():
            rich.print(f'{key}: {value}')
