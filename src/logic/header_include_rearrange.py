# Copyright Allve, Inc. All Rights Reserved.

import os

from util import util_path

# Header include rearrange functions
def check_exist_header_recursive(header_path, check_path):
    result = False
    for filename in os.listdir(check_path):
        if result == True:
            break
        file_path = util_path.convert_absoulte_path(check_path, filename)
        if header_path in file_path:
            result = True
        elif os.path.isdir(file_path):
            result = check_exist_header_recursive(header_path, file_path)
    return result

def check_headerinclude_startpart(line):
    return '/' in line and 'header' in line and 'include' in line and 'start' in line 

def check_headerinclude_endpart(line):
    return '/' in line and 'header' in line and 'include' in line and 'end' in line 

def get_defined_modulenames(config_source_path):
    return util_path.get_directory_names_from_path(config_source_path)

def get_modulename_header_belongs(header_path, config_source_path, modulenames):
    if 'generated.h' in header_path:
        return 'Gen'
    
    for modulename in modulenames:
        absoulte_module_path = util_path.convert_absoulte_path(config_source_path, modulename)
        if check_exist_header_recursive(header_path, absoulte_module_path):
            return modulename

    return 'UE'

def create_headerincludelines_dict(origin_filelines, config_source_path, modulenames):
    headerincludelines_dict = dict()

    is_headerinclude_part = False
    for fileline in origin_filelines:
        check_fileline = fileline.lower()
        if check_headerinclude_startpart(check_fileline):
            is_headerinclude_part = True
        elif check_headerinclude_endpart(check_fileline):
            is_headerinclude_part = False
            break

        if is_headerinclude_part == False:
            continue

        if '#include' in fileline:
            header_path = fileline.strip('#include ')
            header_path = header_path.replace('\n', '')
            header_path = header_path.replace('"', '')
            
            header_modulename = get_modulename_header_belongs(header_path, config_source_path, modulenames)
            if header_modulename in headerincludelines_dict:
                headerincludelines_dict[header_modulename].append(fileline)
            else:
                headerincludelines_dict[header_modulename] = [fileline]

    return headerincludelines_dict

def get_module_orders(config_uproject_path, modulenames):
    # First order module is unrealengine
    module_orders = ["UE"]

    f = open(config_uproject_path, 'r', encoding='utf-8')
    is_moduleconfig_part = False
    module_depth = 0
    for fileline in f.readlines():
        if "Modules" in fileline:
            is_moduleconfig_part = True
        if is_moduleconfig_part == False:
            continue

        if '[' in fileline:
            module_depth += 1
        if ']' in fileline:
            module_depth -= 1
        if module_depth <= 0:
            break

        if "Name" in fileline:
            for modulename in modulenames:
                if modulename in fileline:
                    module_orders.append(modulename)
                    break

    # Last order module is generate
    module_orders.append("Gen")
    f.close()

    return module_orders

# logic
def process(target_convert_path, config_source_path, config_uproject_path):
    defined_modulenames = get_defined_modulenames(config_source_path)

    module_orders = get_module_orders(config_uproject_path, defined_modulenames)

    rf = open(target_convert_path, 'r', encoding='utf-8')
    origin_filelines = rf.readlines()
    rf.close()

    headerincludelines_dict = create_headerincludelines_dict(origin_filelines, config_source_path, defined_modulenames)
    for header_modulename in headerincludelines_dict:
        headerincludelines_dict[header_modulename].sort()

    is_converting_part = False
    wf = open(target_convert_path, 'w', encoding='utf-8')
    for fileline in origin_filelines:
        if is_converting_part == False:
            wf.write(fileline)

        check_fileline = fileline.lower()
        if check_headerinclude_startpart(check_fileline):
            is_converting_part = True
        if check_headerinclude_endpart(check_fileline):
            is_converting_part = False
            for modulename in module_orders:
                if not modulename in headerincludelines_dict:
                    continue
                wf.write('\n')
                wf.write('//' + modulename + '\n')
                for headerincludeline in headerincludelines_dict[modulename]:
                    wf.write(headerincludeline) 
            wf.write('\n')
            wf.write(fileline)
    wf.close()