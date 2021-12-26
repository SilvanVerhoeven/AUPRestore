from .auputils import get_data_folder_name
import argparse
import os
import xml.etree.ElementTree as ET

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


class ProjectPaths:
    def __init__(self, project_file_path, data_dir_path, output_dir_path):
        self.project_file = self.get_project_file_path(project_file_path)
        self.project = os.path.dirname(self.project_file)
        self.data_files = self.get_data_dir_path(data_dir_path)
        self.output = self.project if output_dir_path is None else os.path.abspath(output_dir_path)
        
        project_tree = ET.parse(self.project_file)
        project_root = project_tree.getroot()
        
        self.output_data = os.path.join(self.output, get_data_folder_name(project_root))
    
    @staticmethod
    def get_project_file_path(file_path):
        """Validates and returns absolute path of project file (.aup).

        Parameters
        ----------
        file_path
            Path to project file. May be absolute or relative.

        Raises
        ------
        ValueError
            If there does not exist a file at the given path.
        """

        project_file_path = os.path.abspath(file_path)

        if not os.path.isfile(file_path):
            raise ValueError("AUP project file does not exist: {}".format(
                project_file_path)
            )
            
        return project_file_path
    
    def get_data_dir_path(self, data_dir_path):
        """Validates and returns absolute path to directory containing the project data files.

        Parameters
        ----------
        data_dir_path
            Path to directory containing the project data files. May be absolute, relative or None. If None, the project file directory path is returned.
        
        Raises
        ------
        ValueError
            If `data_dir_path` is not None but does not exist.
        """

        data_file_path = self.project_file if data_dir_path is None else data_dir_path
        data_file_path = os.path.dirname(os.path.abspath(data_file_path))
        if not os.path.exists(data_file_path):
            raise ValueError("Path do data files does not exist: {}".format(
                data_file_path
            ))
        return data_file_path
