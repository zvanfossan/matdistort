import os
import shutil
def dirs():
    leaf_dirs = []
    def find_leaf_dirs(current_path):
        is_leaf = True
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            if os.path.isdir(entry_path):
                is_leaf = False
                find_leaf_dirs(entry_path)
        if is_leaf:
            leaf_dirs.append(current_path)
        return leaf_dirs
    return find_leaf_dirs('base_dir')

def copy_file_to_leaf_directories(incar_path, kpoint_path, potcar_path, submitsh_path, base_path='base_dir'):
    """
    Copies a given file to all leaf directories of the directory structure.
    
    Parameters:
        file_path (str): The path of the file to be copied.
        base_path (str): The base directory where the nested directories are created.
    """
    
    for leaf_dir in dirs():
        shutil.copy(incar_path, leaf_dir)
        shutil.copy(kpoint_path, leaf_dir)
        shutil.copy(potcar_path, leaf_dir)
        shutil.copy(submitsh_path, leaf_dir)
    return

def run_calcs(portion):#, current_path='base_dir'):
    """
    Submits calculations

    Parameters:
        portion (str): specify whether all or a subsection of the calculations should be run.
                        Inputs for this can be 'all' if all calculations are to be submitted 
                        or the name of a specific directory

    """
    initital_directory = os.getcwd()
    if portion == 'all':
        for value in dirs():
            os.chdir(value)
            print(os.getcwd())
            #os.system('sbatch submit.sh')
            os.chdir(initital_directory)
            print(os.getcwd())

    else:
        for i, value in enumerate(dirs()):
            value = value[:len(portion)]
            if value == portion:
                os.chdir(dirs()[i])
                print(os.getcwd())
                #os.system('sbatch submit.sh')
                os.chdir(initital_directory)
                print(os.getcwd())
    return

def get_free_energy():
     return

def get_phonon_frequencies():
     return

run_calcs(portion='all')