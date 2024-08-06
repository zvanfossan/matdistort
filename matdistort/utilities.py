import os
import shutil

def find_leaf_dirs(current_path, leaf_dirs):
        is_leaf = True
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                is_leaf = False
                find_leaf_dirs(entry_path)
        if is_leaf:
            leaf_dirs.append(current_path)

def copy_file_to_leaf_directories(incar_path, kpoint_path, potcar_path, submitsh_path, base_path='base_dir'):
    """
    Copies a given file to all leaf directories of the directory structure.
    
    Parameters:
        file_path (str): The path of the file to be copied.
        base_path (str): The base directory where the nested directories are created.
    """

    leaf_dirs = []
    find_leaf_dirs(base_path, leaf_dirs)
    
    for leaf_dir in leaf_dirs:
        shutil.copy(incar_path, leaf_dir)
        shutil.copy(kpoint_path, leaf_dir)
        shutil.copy(potcar_path, leaf_dir)
        shutil.copy(submitsh_path, leaf_dir)
    return

def run_calcs(portion, base_path='base_dir'):
    """
    Submits calculations

    Parameters:
        portion (str): specify whether all or a subsection of the calculations should be run.

    """
    leaf_dirs = []
    find_leaf_dirs(base_path, leaf_dirs)
    portion
    return



# Example usage
list_of_lists = [
    [-1, 2, 3],  # This will create 3 directories at the first level
    [4, 5],     # This will create 2 directories inside each first level directory
    [6]         # This will create 1 directory inside each second level directory
]

#create_nested_directories(list_of_lists)
copy_file_to_leaf_directories('./test', base_path='base_dir')