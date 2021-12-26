#! /usr/bin/env python3

from os import read
from shutil import Error
from auprestore.core import restructure_data
from auprestore.utils.argutils import parse_arguments, ProjectPaths
from auprestore.utils.auputils import get_data_files
import xml.etree.ElementTree as ET

def print_progress_bar(counter, total, title='Progress:'):
    length = 60
    progress = round(counter / total * length)
    bar = '{}{}'.format(
        '█' * progress,
        '-' * (length - progress)
    )
    print('{} |{}| {} /{}'.format(
        title,
        bar,
        counter,
        total
    ), end='\r' if counter < total else '\n')

def update_progress_bar(counter, total, filename, action, suffix, title_len=25):
    title = "{} {}{}".format(action, filename, suffix)
    padding_right = ' ' * (title_len - len(title))
    print_progress_bar(counter, total, title + padding_right)

def update_restructure_move_progress(counter, total, filename):
    update_progress_bar(counter, total, filename, "Move", "...")

def update_restructure_copy_progress(counter, total, filename):
    update_progress_bar(counter, total, filename, "Copying", "...")

def file_already_exists(input_file_path, output_file_path):
    print("\n███ This file already exists:")
    print("    {}".format(input_file_path))
    print("at  {}".format(output_file_path))
    print("███ It will be skipped.")
    
    prompt = "    Do you want to continue with the other files of this project? [y/n] "
    while True:
        answer = input(prompt)
        if answer == 'y':
            return
        elif answer == 'n':
            exit()
        else:
            prompt = "Please answer with 'y' (yes) or 'n' (no): "

args = parse_arguments()
paths = ProjectPaths(args.aup_file, args.data, args.output)

project_tree = ET.parse(paths.project_file)
project_root = project_tree.getroot()

data_files = get_data_files(project_root)
restructure_data(data_files, paths.data_files, paths.output_data, update_restructure_move_progress, file_already_exists, args.copy)
update_progress_bar(len(data_files), len(data_files), "", "Restructuring completed", "")
