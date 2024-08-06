import os
import shutil

def create_nested_directories(list_of_lists, base_path='base_dir'):
    """
    Creates a nested directory structure based on a list of lists.
    
    Parameters:
        list_of_lists (list of lists): The input list where each sublist defines the depth and number of directories.
        base_path (str): The base directory where the nested directories will be created.
    """
    def create_dirs(current_path, sublists):
        if not sublists:
            return
        current_level = sublists[0]
        for value in current_level:
            dir_name = str(value).replace('-', 'n')
            new_dir_path = os.path.join(current_path, dir_name)
            os.makedirs(new_dir_path, exist_ok=True)
            create_dirs(new_dir_path, sublists[1:])

    # Create the base directory if it does not exist
    os.makedirs(base_path, exist_ok=True)
    print(f"Base directory '{base_path}' created successfully")
    
    create_dirs(base_path, list_of_lists)


def copy_file_to_leaf_directories(incar_path, kpoint_path, potcar_path, submitsh_path, base_path='base_dir'):
    """
    Copies a given file to all leaf directories of the directory structure.
    
    Parameters:
        file_path (str): The path of the file to be copied.
        base_path (str): The base directory where the nested directories are created.
    """
    def find_leaf_dirs(current_path):
        is_leaf = True
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                is_leaf = False
                find_leaf_dirs(entry_path)
        if is_leaf:
            leaf_dirs.append(current_path)

    leaf_dirs = []
    find_leaf_dirs(base_path)
    
    for leaf_dir in leaf_dirs:
        shutil.copy(incar_path, leaf_dir)
        shutil.copy(kpoint_path, leaf_dir)
        shutil.copy(potcar_path, leaf_dir)
        shutil.copy(submitsh_path, leaf_dir)


# Example usage
list_of_lists = [
    [-1, 2, 3],  # This will create 3 directories at the first level
    [4, 5],     # This will create 2 directories inside each first level directory
    [6]         # This will create 1 directory inside each second level directory
]

#create_nested_directories(list_of_lists)
copy_file_to_leaf_directories('./test', base_path='base_dir')