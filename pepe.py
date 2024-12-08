# -*- encoding: utf-8 -*-
import argparse
from sys import argv
from data.settings import *
from services.config import *
from services.actions import ActionsList, actions
from services.args import ProgramArgs

def execute_args(args: ProgramArgs):
    action = args.action
    match action.lower():
        case ActionsList.LIST:
            actions[ActionsList.LIST]()
        case ActionsList.UPDATE_PACKAGES:
            actions[ActionsList.UPDATE_PACKAGES]()

def main():
    # parse args
    parser = argparse.ArgumentParser(
        prog=f'{PROG_NAME} {PROG_VERSION}',
        description=PROG_DESCRIPTION
    )
    parser.add_argument('action')
    execute_args(parser.parse_args())

init_config()
main()