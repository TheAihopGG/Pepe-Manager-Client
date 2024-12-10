# -*- encoding: utf-8 -*-
import argparse
import requests
import json
import rich
from sys import argv
from data.settings import *
from services.config import *
from services.actions import ActionsList, Actions
from services.args import ProgramArgs
from services.package import TypedPackage, is_downloaded_package

config = load_config()

def execute_args(args: ProgramArgs):
    action = args.action
    match action.lower():
        case ActionsList.list.value:
            Actions.update_packages()
            Actions.list()

        case ActionsList.update_packages.value:
            Actions.update_packages()

        case ActionsList.download.value:
            if args.package_name and args.package_version:
                response = requests.post(f'{API_URL}api/package/?name={args.package_name}&version={args.package_version}')
                if response.ok:
                    package_config: dict[TypedPackage] = json.loads(response.content.decode())['package']
                    Actions.download(package_config=package_config)
                else:
                    rich.print(response.text)
            elif not args.package_name:
                rich.print('You must specify parameter: --package-name')
            elif not args.package_version:
                rich.print('You must specify parameter: --package-version')
        
        case ActionsList.remove.value:
            Actions.update_packages()
            if args.package_name and args.package_version:
                if is_downloaded_package(args.package_name, args.package_version, config):
                    Actions.remove(args.package_name, args.package_version)
                else:
                    rich.print(f'Package not found: name: {args.package_name}, version: {args.package_version}')
            elif not args.package_name:
                rich.print('You must specify parameter: --package-name')
            elif not args.package_version:
                rich.print('You must specify parameter: --package-version')


def main():
    # parse args
    parser = argparse.ArgumentParser(
        prog=f'{PROG_NAME} {PROG_VERSION}',
        description=PROG_DESCRIPTION
    )
    parser.add_argument('action')
    parser.add_argument('--package-name', '-pn')
    parser.add_argument('--package-version', '-pv')

    execute_args(parser.parse_args())

init_config()
main()