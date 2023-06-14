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

# Header include rearrange functions
def search_header(header_path, search_path):
    result = False
    filenames = os.listdir(search_path)
    for filename in filenames:
        full_filepath = search_path + '/' + filename
        if header_path in full_filepath:
            result = True
            break
        elif os.path.isdir(full_filepath) and result == False:
            if search_header(header_path, full_filepath):
                result = True
                break

    return result

def get_module_from_header(header_path, source_path, module_names):
    if 'generated.h' in header_path:
        return 'Gen'
    else:
        for module_name in module_names:
            full_module_path = source_path + '/' + module_name
            if (search_header(header_path, full_module_path)):
                return module_name

    return 'UE'

# Parsing source code to header rearrange
is_collect_start = False
is_commenting = False

include_headers = dict()

f = open('E:/Programming/Projects/Unreal/AreaOfOperations/Project/Source/AOGame/Character/Actor/AOCharacter.h', 'r', encoding='utf-8')

file_lines = f.readlines()
for line in file_lines:
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
            header_path = header_path.replace('"', '')
            
            header_module_name = get_module_from_header(header_path, config_source_path, config_module_names)
            if header_module_name in include_headers:
                include_headers[header_module_name].append(line)
            else:
                include_headers[header_module_name] = [line]
        else:
            is_collect_start = False
            print('Collect End')
    elif '#pragma once' in line:
        is_collect_start = True
        print('Collect Start')
        
f.close()

# sorting order


# rewriting
is_replacing = False
f = open('E:/Programming/Projects/Unreal/AreaOfOperations/Project/Source/AOGame/Character/Actor/AOCharacter.h', 'w', encoding='utf-8')
for line in file_lines:
    if is_replacing is False:
        f.write(line)

    if '#pragma once' in line:
        is_replacing = True
    elif 'generated.h' in line:
        is_replacing = False
        for include_module_name in include_headers:
            f.write('\n')
            f.write('//' + include_module_name + '\n')
            for include_header_line in include_headers[include_module_name]:
                f.write(include_header_line) 
f.close()