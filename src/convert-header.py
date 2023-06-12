# Copyright Allve, Inc. All Rights Reserved.

import configparser
import os
import sys

# Utility functions
def get_current_work_directory_path():
    return os.getcwd()
    
def get_config_path():
    return get_current_work_directory_path() + '/config.ini'

# Parsing execute option from arguments
option_code_path = ''
if len(sys.argv) >= 2:
    option_code_path = sys.argv[1]

# Parsing config related to header rearrange
config = configparser.ConfigParser()
config.read(get_config_path())
config_source_path = config['ProjectSetting']['SourcePath']

config_module_names = []
for file_name in os.listdir(config_source_path):
    absoulte_path = os.path.join(config_source_path, file_name)
    if os.path.isdir(absoulte_path):
        config_module_names.append(file_name)

# Parsing source code to header rearrange
is_collect_start = False
is_commenting = False

f = open('E:/Programming/Projects/Unreal/AreaOfOperations/Project/Source/AOGame/Character/Component/AOCharacterMovementComponent.h', 'r', encoding='utf-8')
for line in f.readlines():
    if is_collect_start:
        nospace_line = line.replace(" ", "")
        if nospace_line == '\n' or '//' in line:
            continue

        if '/*' in line:
            is_commenting = True

        if is_commenting:
            if '*/' in line:
                is_commenting = False
            continue

        if '#include' in line:
            header_path = line.strip('#include ')
            header_path = header_path.replace('\n', '')
            print(header_path)
        else:
            is_collect_start = False
            print('Collect End')
    elif '#pragma once' in line:
        is_collect_start = True
        print('Collect Start')
        

# Test
print(config_source_path)
print(config_module_names)