# -*- encoding: utf-8 -*-
import requests
import json
import rich
from os.path import exists
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
    package_id: int | None
    option: str | None
    value: str | None


def execute_args(args: ProgramArgs):
    """Invokes an action with necessary parameters"""
    action = args.action
    match action.lower():
        case ActionsList.list.value:
            if exists(config['packages_dir_path']):
                Actions.update_packages()
                Actions.list()

            else:
                rich.print(f'Option `packages_dir_path`: path does not exists')

        case ActionsList.update_packages.value:
            Actions.update_packages()

        case ActionsList.download.value:
            if args.package_name and args.package_version and exists(config['packages_dir_path']):
                Actions.update_packages()
                if not get_package_config_by_name_version(args.package_name, args.package_version, config['packages']):
                    response: TypedAPIResponse = requests.get(f'{API_URL}api/package/?name={args.package_name}&version={args.package_version}')
                    if response.ok:
                        Actions.download(json.loads(response.content.decode())['package'])
                
                    else:
                        rich.print(f'Package not found')
                        
                else:
                    rich.print(f'Package is downloaded')
            
            elif args.package_id and exists(config['packages_dir_path']):
                Actions.update_packages()
                if not get_package(lambda p: str(p['id']) == args.package_id, config['packages']) and exists(config['packages_dir_path']):
                    response: TypedAPIResponse = requests.get(f'{API_URL}api/package_by_field/?field=id&value={args.package_id}')
                    if response.ok:
                        Actions.download(json.loads(response.content.decode())['package'])
                
                    else:
                        rich.print(f'Package not found')
                
                else:
                    rich.print(f'Package is downloaded')
            
            elif not exists(config['packages_dir_path']):
                rich.print(f'Option `packages_dir_path`: path does not exists')

            elif not args.package_name:
                rich.print('--package-name is required')
            
            elif not args.package_version:
                rich.print('--package-version is required')
        
        case ActionsList.remove.value:
            if args.package_name and args.package_version and exists(config['packages_dir_path']):
                Actions.update_packages()
                package = get_package_config_by_name_version(args.package_name, args.package_version, config['packages'])
                
                if package:
                    Actions.remove(package)

                else:
                    rich.print(f'Package not found')
            
            elif args.package_id and exists(config['packages_dir_path']):
                Actions.update_packages()
                package = get_package(lambda p: str(p['id']) == args.package_id, config['packages'])
                
                if package:
                    Actions.remove(package)

                else:
                    rich.print(f'Package not found')

            elif args.package_name and exists(config['packages_dir_path']):
                Actions.update_packages()
                if packages_configs := get_packages(lambda package: package['name'] == args.package_name, config['packages']):
                    for package in packages_configs:
                        Actions.remove(package)

                else:
                    rich.print(f'Packages not found: name: {args.package_name}')
            
            elif not exists(config['packages_dir_path']):
                rich.print(f'Option `packages_dir_path`: path does not exists')
            
            elif not args.package_name:
                rich.print('--package-name is required')
        
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
            if args.package_name and args.package_version and exists(config['packages_dir_path']):
                package = get_package_config_by_name_version(args.package_name, args.package_version, config['packages']) 
                
                if package:
                    Actions.show(package)

                else:
                    rich.print('Package not found')
            
            elif args.package_id and exists(config['packages_dir_path']):
                package = get_package(lambda p: str(p['id']) == args.package_id, config['packages']) 

                if package:
                    Actions.show(package)

                else:
                    rich.print('Package not found')
            
            elif args.package_name and exists(config['packages_dir_path']):
                if packages := get_packages(lambda p: p['name'] == args.package_name):
                    for package in packages:
                        Actions.show(package)
                    
                else:
                    rich.print('Package not found')
                
            elif not exists(config['packages_dir_path']):
                rich.print(f'Option `packages_dir_path`: path does not exists')

            elif not args.package_name:
                rich.print('--package-name is required')


def parse_args() -> ProgramArgs:
    """Parse args with using argparse and return TypedProgramArgs"""
    parser = ArgumentParser(
        prog=f'<action> [options]',
        description=PROG_DESCRIPTION
    )
    # add arguments
    parser.add_argument('action')
    parser.add_argument('--package-name', '-pn')
    parser.add_argument('--package-version', '-pv')
    parser.add_argument('--package-id', '-pi')
    parser.add_argument('--option', '-op')
    parser.add_argument('--value', '-v')
    return parser.parse_args()

# init config.json
init_config()
# execute command
execute_args(parse_args())
