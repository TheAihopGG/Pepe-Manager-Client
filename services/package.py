import json
from typing import Callable, Generator
from services.config import TypedConfig, load_config
from services.typed_dicts import TypedPackage
from os.path import exists

__doc__ = """Contains packages' tools"""
config = load_config()

def is_package(
    package_path: str,
    packages_dir_path: str = config['packages_dir_path']
) -> (None | TypedPackage):
    """Checks package's config for necessary values"""
    package_config_path = f'{packages_dir_path}/{package_path}/config.json'
    if exists(package_config_path):
        package_config: TypedPackage = json.load(open(package_config_path))
        if set(package_config.keys()) == set(TypedPackage.__mutable_keys__):
            return package_config
    else:
        return None

def get_package(
    check: Callable[[TypedPackage], bool],
    packages: list[TypedPackage] = config['packages']
) -> (TypedPackage | None):
    """Returns package"""
    for package in packages:
        if check(package):
            return package
    return None


def get_packages(
    check: Callable[[TypedPackage], bool],
    packages: list[TypedPackage] = config['packages']
) -> Generator[TypedPackage, str, None]:
    for package in packages:
        if package and check(package):
            yield package


def get_package_config_by_name_version(
    package_name: str,
    package_version: str,
    packages: list[TypedPackage] = config['packages']
) -> TypedPackage:
    return get_package(
        lambda package: package['name'] == package_name and package['version'] == package_version,
        packages,
    )


def get_package_config_by_name(
    package_name: str,
    packages: list[TypedPackage] = config['packages']
) -> TypedPackage:
    return get_package(
        lambda package: package['name'] == package_name,
        packages,
    )
