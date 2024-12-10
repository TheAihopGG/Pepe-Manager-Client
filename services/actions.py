import tarfile
import shutil
import os
import rich
import requests
from urllib.parse import urlparse
from logging import *
from data.settings import *
from services.config import *
from services.typed_dicts import TypedPackage
from services.package import is_package

config = load_config()

class ActionsList:
    """Class with all actions"""
    LIST = 'list'
    UPDATE_PACKAGES = 'update-packages'
    DOWNLOAD = 'download'
    REMOVE = 'remove'


class Actions:
    """Class with actions functions"""
    @staticmethod
    def list():
        """Shows downloaded packages"""
        global config
        config = load_config()
        rich.print('Packages list:')
        if packages := config['packages']:
            for package in packages:
                rich.print(f'{package['name']}-{package['version']}')
        else:
            rich.print('There is no downloaded packages')

    @staticmethod
    def update_packages():
        """Updates config['packages']"""
        global config
        config = load_config()
        edit_config('packages', [is_package(package_dir, config) for package_dir in os.listdir(config['packages_dir_path'])])
        rich.print('Packages have updated')
    
    @staticmethod
    def download(
        *,
        package_config: TypedPackage,
        package_extension: str = '.tar.gz',
        packages_dir_path = config['packages_dir_path'],
    ):
        """Downloads package from package_url in config['packages_dir_path']"""
        package_dir_name = f'{package_config['name']}{package_config['version']}'

        rich.print(f'Downloading package: {package_config['name']}{package_config['version']} by @{package_config['author']}')
        rich.print(f'Requesting to {urlparse(package_config['url']).hostname}')
        
        try:
            response = requests.get(package_config['url'])
        except requests.RequestException as error:
            rich.print(error)
        except requests.exceptions.ConnectionError:
            rich.print('Pepe Manager API is offline now')
        else:
            if response.ok:
                with open(f'{packages_dir_path}/{package_dir_name}{package_extension}', 'wb') as packed_package_file:
                    packed_package_file.write(response.content)
                # unpack package
                rich.print(f'Unpacking {package_config['name']}')
                match package_extension:
                    case '.tar.gz':
                        rich.print(f'Detected extension: .tar.gz')
                        packed_package_file = tarfile.open(f'{packages_dir_path}/{package_dir_name}{package_extension}', mode='r:gz')
                        packed_package_file.extractall(packages_dir_path)
                        os.remove(f'{packages_dir_path}/{package_config['name']}{package_config['version']}.tar.gz')
                        rich.print(f'Successfully downloaded {package_config['name']}{package_config['version']}')
                        edit_config('packages', config['packages']+[package_config])
                    case _:
                        rich.print(f'Unsupported package file extension: {package_extension}')
            else:
                rich.print(response.text)

    @staticmethod
    def remove(package_name: str, package_version: str):
        """Removes package in config['packages_dir_path']"""
        # remove package
        rich.print(f'Removing: {package_name}{package_version}')
        for package_dir in os.listdir(config['packages_dir_path']):
            package_config: TypedPackage = is_package(package_dir, config)
            if package_config['name'] == package_name and package_config['version'] == package_version:
                shutil.rmtree(f'{config['packages_dir_path']}/{package_dir}')
        # remove package from config
        for [index, package] in enumerate(config['packages']):
            if package['name'] == package_name and package['version'] == package_version:
                del config['packages'][index]
        edit_config('packages', [None if package['name'] == package_name and package['version'] else package for package in config['packages']])
        
        rich.print(f'Successfully removed {package_name}-{package_version}')
