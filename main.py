#!/usr/bin/env python3

import yaml
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file',
                    help='The file to use to store config and data.',
                    default='data.yml')
args=parser.parse_args()

def print_module_tree(module_list, prestring):
    """Prints a tree of modules from module_list.
    prestring will be put at the start of each message,
    and 2 spaces will be appended for each added layer"""
    for module in module_list:
        print(f'{prestring}Module {module["module"]} with percentage {module["weighting"]}')
        if 'modules' in module:
            print_module_tree(module["modules"], prestring+"  ")

def check_module_tree(module_list):
    """Checks the module tree inside module_list.
    Will check that the total percentage is 100,
    and will throw an error otherwise"""
    total_percent = 0
    for module in module_list:
        total_percent += module["weighting"]
        if 'modules' in module:
            if check_module_tree(module["modules"]) == False:
                print(f"Config File Invalid \n{module['module']}'s submodules do not sum to 100%", file=sys.stderr)
                sys.exit()
    if total_percent != 100:
        # The percentages do not add up to 100, we should throw an error
        return False

def calc_percentage(module_list):
    """Calculates the weighted average percentage inside module_list,
    assuming anything without a percent is 0"""
    weightedPercents=[]
    percentages=[]
    weightings=[]
    for module in module_list:
        if 'modules' in module:
            # we need to recursively compute it
            percent = calc_percentage(module['modules'])
        elif 'percent' in module:
            percent=module["percent"]
        else:
            # This module currently has no percent,
            # so we don't want to append to the list
            continue
        weighting=module["weighting"]
        percentages.append(percent)
        weightings.append(weighting)
        weightedPercents.append(percent*weighting/100)
    return sum(weightedPercents)/len(weightedPercents)


def check_config_file(config):
    """Checks whether the config file is valid"""
    if check_module_tree(config["modules"]) == False:
        print(f"Config File Invalid \nRoot tree's percent does not sum to 100", file=sys.stderr)
        sys.exit()


def open_config_file():
    """Open and check the config file is valid.
    Returns a dictionary containing the config"""
    with open(args.file,"r") as config_file:
        # Load the config file
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print("Config File Invalid, YAML processor returns:")
            print(exc,file=sys.stderr)
            sys.exit()
    check_config_file(config)
    return config


config = open_config_file()

print(calc_percentage(config["modules"]))
