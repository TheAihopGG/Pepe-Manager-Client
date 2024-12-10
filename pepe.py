# -*- encoding: utf-8 -*-
import requests
import json
import rich
from sys import argv
from argparse import ArgumentParser, Namespace
from data.settings import *
from services.config import *
from services.actions import ActionsList, Actions
from services.typed_dicts import TypedAPIResponse
from services.package import *

config = load_config() # config contains such user vars are like packages, packages_dir_path 

__doc__ = """Contains main functions"""

class ProgramArgs(Namespace):
    """Contains possible fields of `parse_args` response"""
    action: str
    package_name: str | None
    package_version: str | None
    option: str | None
    value: str | None


def execute_args(args: ProgramArgs):
    """Invokes an action with necessary parameters"""
    action = args.action
    match action.lower():
        case ActionsList.list.value:
            Actions.update_packages()
            Actions.list()

        case ActionsList.update_packages.value:
            Actions.update_packages()

        case ActionsList.download.value:
            if args.package_name and args.package_version:
                response: TypedAPIResponse = requests.post(f'{API_URL}api/package/?name={args.package_name}&version={args.package_version}')
                if response.ok:
                    Actions.download(json.loads(response.content.decode())['package'])
                else:
                    rich.print(response.content['detail'])
            elif not args.package_name:
                rich.print('--package-name is required')
            elif not args.package_version:
                rich.print('--package-version is required')
        
        case ActionsList.remove.value:
            Actions.update_packages()
            if args.package_name and args.package_version:
                if package_config := get_package_config_by_name_version(args.package_name, args.package_version, config['packages']):
                    Actions.remove(package_config)
                else:
                    rich.print(f'Package not found: name: {args.package_name}, version: {args.package_version}')
            elif not args.package_name:
                rich.print('--package-name is required')
            elif not args.package_version:
                if packages_configs := get_packages(lambda package: package['name'] == args.package_name, config['packages']):
                    for package_config in packages_configs:
                        Actions.remove(package_config)
                else:
                    rich.print(f'Packages not found: name: {args.package_name}')
        
        case ActionsList.set.value:
            if args.option and args.value:
                if args.option in DEFAULT_CONFIG:
                    Actions.set(args.option, args.value)
                else:
                    rich.print(f'Unknown option {args.option}')
            elif not args.option:
                rich.print('--option is required')
            elif not args.value:
                rich.print('--value is required')
        
        case ActionsList.show.value:
            if args.package_name and args.package_version:
                if package_config := get_package_config_by_name_version(args.package_name, args.package_version, config['packages']):
                    Actions.show(package_config)
                else:
                    rich.print(f'Package not found: name: {args.package_name}, version: {args.package_version}')
            elif not args.package_name:
                rich.print('--package-name is required')
            elif not args.package_version:
                if package_config := get_package_config_by_name(args.package_name, config['packages']):
                    Actions.show(package_config)
                else:
                    rich.print(f'Package not found: name: {args.package_name}')

def parse_args() -> ProgramArgs:
    """Parse args with using argparse and return TypedProgramArgs"""
    parser = ArgumentParser(
        prog=f'{PROG_NAME} {PROG_VERSION}',
        description=PROG_DESCRIPTION
    )
    # add arguments
    parser.add_argument('action') # it is like download, list, remove...
    parser.add_argument('--package-name', '-pn') # package name necessary for download, show and remove commands
    parser.add_argument('--package-version', '-pv') # package version is necessary for download, show and remove commands
    parser.add_argument('--option', '-op') # option is necessary for set command
    parser.add_argument('--value', '-v') # value is necessary for set command
    return parser.parse_args()

# init config.json
init_config()
# execute command
execute_args(parse_args())
