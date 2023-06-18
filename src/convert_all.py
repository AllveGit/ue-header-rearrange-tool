# Copyright Allve, Inc. All Rights Reserved.

import configparser
import os

from util import util_path
from logic import header_include_rearrange

def check_config_valid(config_source_path, config_uproject_path):
    return len(config_source_path) > 0 and len(config_uproject_path) > 0

def get_cpp_h_files_recursive(search_path):
    file_paths = []
    for filename in os.listdir(search_path):
        file_path = util_path.convert_absoulte_path(search_path, filename)
        if os.path.isdir(file_path):
            for subfile_path in get_cpp_h_files_recursive(file_path):
                file_paths.append(subfile_path)
            continue
        if util_path.check_file_type_cpp(filename) or util_path.check_file_type_header(filename):
            file_paths.append(file_path)
    return file_paths

# Parsing execute option from arguments
# argument 1 - target sourcecode path
def process_convert_all():
    # Parsing config
    config = configparser.ConfigParser()
    config.read(util_path.get_config_path())
    config_source_path = config['ProjectSetting']['SourcePath']
    config_uproject_path = config['ProjectSetting']['UProjectPath']

    if check_config_valid(config_source_path, config_uproject_path) == False:
        print("Config setting invalid!")

    # Converting
    convert_file_paths = get_cpp_h_files_recursive(config_source_path)
    for convert_file_path in convert_file_paths: 
        header_include_rearrange.process(convert_file_path, config_source_path, config_uproject_path)

process_convert_all()