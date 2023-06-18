# Copyright Allve, Inc. All Rights Reserved.

import configparser
import sys

from util import util_path
from logic import header_include_rearrange

def check_argument_valid(args_converttarget_path):
    return len(args_converttarget_path) > 0

def check_config_valid(config_source_path, config_uproject_path):
    return len(config_source_path) > 0 and len(config_uproject_path) > 0

# Parsing execute option from arguments
# argument 1 - target sourcecode path
def process_convert():
    args_converttarget_path = ''
    if len(sys.argv) >= 2:
        args_converttarget_path = sys.argv[1]

    if check_argument_valid(args_converttarget_path) == False:
        print("Execute argument invalid!")
        return

    # Parsing config
    config = configparser.ConfigParser()
    config.read(util_path.get_config_path())
    config_source_path = config['ProjectSetting']['SourcePath']
    config_uproject_path = config['ProjectSetting']['UProjectPath']

    if check_config_valid(config_source_path, config_uproject_path) == False:
        print("Config setting invalid!")

    # Converting
    header_include_rearrange.process(args_converttarget_path, config_source_path, config_uproject_path)

process_convert()