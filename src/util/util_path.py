# Copyright Allve, Inc. All Rights Reserved.

import os

def convert_absoulte_path(directory_path, filename):
    return directory_path + '/' + filename

def get_current_work_directory_path():
    return os.getcwd()
    
def get_config_path():
    return get_current_work_directory_path() + '/' + '../config.ini'

def get_extension_from_file(filename):
    name, extension = os.path.splitext(filename)
    return extension

def get_directory_names_from_path(path):
    directory_names=[]
    for filename in os.listdir(path):
        absoulte_path = convert_absoulte_path(path, filename)
        # check file type is directory
        if os.path.isdir(absoulte_path):
            directory_names.append(filename)
    return directory_names

def check_file_type_cpp(filename):
    return '.cpp' in get_extension_from_file(filename)

def check_file_type_header(filename):
    return '.h' in get_extension_from_file(filename)