import os
import shutil

def restructure_data(filenames, input_path, output_path, callback_progress, callback_file_exists, copy=False):
    """Restore an Audacity project by recreating the original project structure.
    
    Parameters
    ----------
    filenames
        Set of data file (.au) names which should be restructured.
    input_path
        Path to directory which contains all the data files at the top level.
    output_path
        Path to directory in which the restructured project should be contained (this directory is going to include the .aup project file and the directory with the .au data files).
    """
    for index, filename in enumerate(filenames):
        file_path = os.path.join(input_path, filename)
        file_output_path = os.path.join(
            output_path,
            "e{}".format(filename[1:3]),
            "d{}".format(filename[3:5])
        )
        callback_progress(index, len(filenames), filename)
        if not os.path.exists(file_output_path):
            os.makedirs(file_output_path)
        if copy:
            try:
                shutil.copy2(file_path, file_output_path)
            except shutil.Error:
                callback_file_exists(file_path, file_output_path)
        else:
            try:
                shutil.move(file_path, file_output_path)
            except shutil.Error:
                callback_file_exists(file_path, file_output_path)

