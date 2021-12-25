#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as ET
import os
import re

def parse_arguments():
    parser = argparse.ArgumentParser(
        "Restore Audacity 2.x projects from their .aup and .au files.")
    parser.add_argument('aup_file', metavar="aup-file",
        help="AUP file of the project to be recovered.")
    parser.add_argument('-d', '--data',
        help="Directory containing the project's .au files (usually contained in the _data folder). By default, the .aup file's directory is used.")
    parser.add_argument('-o', '--output',
        help="Output directory of the restored project. Will be created if necessary. By default, the .aup file's directory is used.")
    parser.add_argument('-c', '--copy',
        help="Copy all files into the restored project structure. By default, the projects are restored by moving the files into the necessary direcory structure.",
        action='store_true')
    
    return parser.parse_args()

def project_file_path(file_path):
    if not os.path.isfile(file_path):
        raise ValueError("AUP project file does not exist: {}".format(
            os.path.abspath(file_path))
        )
    return os.path.abspath(file_path)

def data_file_path(file_path_from_args, project_file_path):
    data_file_path = project_file_path if file_path_from_args is None else file_path_from_args
    return os.path.dirname(os.path.abspath(data_file_path))

def get_namespace(tag):
        return re.search('{.*}', tag)[0]

def get_data_dir(root):
    def remove_namespace(tag):
        return tag[len(get_namespace(tag)):]  

    if not remove_namespace(root.tag) == "project":
        raise TypeError("AUP project file does not start with a project tag.")
    if not "projname" in root.attrib:
        raise TypeError("AUP project file does not contain project name.")
    return root.get("projname")

def get_data_files(root):
    namespace = get_namespace(root.tag)
    return [simpleblockfile.get('filename') for simpleblockfile in root.iter('{}simpleblockfile'.format(namespace))]

args = parse_arguments()

project_path = project_file_path(args.aup_file)
data_path = data_file_path(args.data, project_path)
output_path = project_path if args.output is None else os.path.abspath(args.output)

project_tree = ET.parse(args.aup_file)
project_root = project_tree.getroot()

output_data_path = os.path.join(output_path, get_data_dir(project_root))

data_files = get_data_files(project_root)
print(data_files)
