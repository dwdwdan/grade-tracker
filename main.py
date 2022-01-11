#!/usr/bin/env python3

import yaml
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',
                    help='The file to use to store config and data.',
                    default='data.yml')

parser.add_argument('--ignore-unmarked',
                    help='If enabled, gradeTracker will not assume that unmarked modules are 0.',
                    dest='ignore_unmarked',
                    default=None,
                    action='store_true')

parser.add_argument('--use-unmarked',
                    help='If enabled, gradeTracker will assume that unmarked modules are 0.',
                    dest='ignore_unmarked',
                    default=None,
                    action='store_false')

parser.add_argument('command',
                    help='Command to run',
                    nargs='?',
                    choices=['print-marks', 'print-modules'])


def print_module_tree(module_list, prestring):
    """Prints a tree of modules from module_list.
    prestring will be put at the start of each message,
    and 2 spaces will be appended for each added layer"""
    for module in module_list:
        print(f'{prestring}Module {module["module"]} with percentage {module["weighting"]}')
        if 'modules' in module:
            # This means there are submodules, so we should recurse into them
            print_module_tree(module["modules"], prestring+"  ")

def check_module_tree(module_list):
    """Checks the module tree inside module_list.
    Will check that the total percentage is 100,
    and will throw an error otherwise"""
    total_weighting = 0
    for module in module_list:
        total_weighting += module["weighting"]
        if 'modules' in module:
            if check_module_tree(module["modules"]) == False:
                print(f"Config File Invalid \n{module['module']}'s submodules do not sum to 100%", file=sys.stderr)
                sys.exit()
    if total_weighting != 100:
        # The percentages do not add up to 100, we should throw an error
        return False


def calc_percentage(module_list, module_name, prestring):
    """Calculates the weighted average percentage inside module_list,
    respecting, ignore_unmarked
    It will also compute print_strings in case we want to print later"""

    # First we want to generate lists of all of the percentages and weightings on this level
    percentages=[]
    weightings=[]
    # This an array of strings ready for later printing
    global print_strings
    if 'print_strings' not in globals():
        print_strings=[]

    for module in module_list:
        if 'modules' in module:
            # we need to recursively compute it
            percent = calc_percentage(module['modules'], module['module'], prestring+"  ")
        elif 'percent' in module:
            # We are at the bottom of the tree, this is as small as we get
            percent=module["percent"]
            print_strings.append(f"{prestring+'  '}{module['module']}: {percent}")
        else:
            # This module currently has no percent,
            # so we don't want to append to the list
            continue
        weighting=module["weighting"]
        percentages.append(percent)
        weightings.append(weighting)

    # If we want to ignore unmarked, we need to adjust the weightings so that this happens
    if args.ignore_unmarked:
        # We don't want to assume 0, so we need to recompute weightings
        # We do this by finding a scale factor to scale them by so the total weighting is 100
        total_weighting=sum(weightings)
        scale_factor=100/total_weighting
        # Now we update weightings to be scaled by the scale factor
        for idx,weighting in enumerate(weightings):
            weightings[idx]=scale_factor*weighting

    # Now we can compute a list of weighted percentages
    weightedPercentages=[]
    for idx,percent in enumerate(percentages):
        weightedPercentages.append(percent*weightings[idx]/100)

    # and then compute the average
    avg=sum(weightedPercentages)/len(weightedPercentages)
    print_strings.append(f'{prestring}{module_name}: {avg}')
    return avg





def check_config_file(config):
    """Checks whether the config file is valid"""
    # This essentially wraps check_module_tree to additionally check the outer layer
    if check_module_tree(config["modules"]) == False:
        print(f"Config File Invalid \nRoot tree's percent does not sum to 100", file=sys.stderr)
        sys.exit()


def open_config_file():
    """Open and check the config file is valid.
    Returns a dictionary containing the config"""

    # I want to parse the arguments here so I can set the default values from
    # the config file before running anything else
    global args
    args=parser.parse_args()

    with open(args.file,"r") as config_file:
        # Load the config file
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print("Config File Invalid, YAML processor returns:")
            print(exc,file=sys.stderr)
            sys.exit()
    check_config_file(config)
    if args.ignore_unmarked==None:
        if "ignore_unmarked" in config:
            args.ignore_unmarked=config["ignore_unmarked"]
        else:
            args.ignore_unmarked=true
    return config


config = open_config_file()

calc_percentage(config["modules"],'Overall','')

if args.command=='print-marks':
    # print_strings give us the right strings but upside down, so we reverse
    # them and then print them
    print_strings.reverse()
    for string in print_strings:
        print(string)
elif args.command=='print-modules':
    print_module_tree(config["modules"],"")
