import os

def get_files_info(working_directory, directory=''):
    working_dir_abs = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_directory = os.path.commonpath([working_dir_abs, target_directory]) == working_dir_abs
    if not valid_target_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if directory not in target_directory:
        return f'Error: "{directory}" is not a directory'

    file_info = str
    for item in target_directory:
        file_info += str(item)







