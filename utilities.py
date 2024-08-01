import os

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
            print(f"Directory '{new_dir_path}' created successfully")
            create_dirs(new_dir_path, sublists[1:])

    # Create the base directory if it does not exist
    os.makedirs(base_path, exist_ok=True)
    print(f"Base directory '{base_path}' created successfully")
    
    create_dirs(base_path, list_of_lists)

def create_poscars(parent_structure):
    """
    Walk through created directory and 
    
    """
    return


# Example usage
list_of_lists = [
    [-1, 2, 3],  # This will create 3 directories at the first level
    [4, 5],     # This will create 2 directories inside each first level directory
    [6]         # This will create 1 directory inside each second level directory
]

create_nested_directories(list_of_lists)