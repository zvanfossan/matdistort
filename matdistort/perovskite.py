import os
import numpy as np
from pymatgen.core.structure import Structure

def create_directories_with_poscars(parent_structure, param_dict):
    """
    Walk through the directory tree and distort the parent structure based on the values of the directories.
    Distortions by irreducible representations are defined using the same notation as Isodistort as provided 
    by the Isotropy Software Suit. Normal strains should be provided in decimal form and shear strains should
    be defined using the basic definition of shear strain.

    Parameters:
        parent_structure (file path to parent structure POSCAR): The parent structure to be distorted
        param_dict (dict): A dictionary in which the keys are named according to irreps and the values
                            that are either floats or lists of floats. Key names should can be any of
                            the following expressions (gm1, gm3_a0, gm3_0a, gm5_a00, gm5_0a0, gm5_00a,
                                                        oct_rot_x, oct_rot_y, oct_rot_z, exx, eyy, ezz,
                                                        exy, exz, eyz)
    """
    
    def get_values_from_dict(param_dict):
        values_list = []
        for value in param_dict.values():
            values_list.append(value)
        return values_list

    def get_keys_from_dict(param_dict):
        keys_list = []
        for key in param_dict.keys():
            keys_list.append(key)
        return keys_list

    def convert_values_to_list(input_list):
        i = 0
        while i < len(input_list):
            if isinstance(input_list[i], (int, float)):
                if input_list[i] == 0:
                    input_list.pop(i)
                else:
                    input_list[i] = [input_list[i]]
                    i += 1
            else:
                i += 1
        return input_list
    

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
            for value in sublists:
                if value == 0:
                    continue
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

    def copy_file_to_leaf_directories(file_path, base_path='base_dir'):
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
        keys = get_keys_from_dict(param_dict)
        print("Number of calculations setup:", len(leaf_dirs))
        for i, leaf_dir in enumerate(leaf_dirs):

            normalized_path = os.path.normpath(leaf_dir)
            directories = normalized_path.split(os.sep)
            directories.pop(0)
            for i, value in enumerate(directories):
                if 'n' in value:
                    directories[i] = value.replace('n', '-')
            float_list = [float(item) for item in directories]

            lattice = struct.lattice.matrix
            gm1_strain = 0
            gm3_a0_strain = 0
            gm3_0a_strain = 0
            gm5_a00_strain = 0
            gm5_0a0_strain = 0
            gm5_00a_strain = 0
            oct_rot_x = 0
            oct_rot_y = 0
            oct_rot_z = 0
            exx = 0
            eyy = 0
            ezz = 0
            exy = 0
            exz = 0
            eyz = 0

            if keys[i] == 'gm1':
                gm1_strain = float_list[i]*np.sqrt(3)/3

            if keys[i] == 'gm3_a0':
                gm3_a0_strain = float_list[i]*np.sqrt(6)/3

            if keys[i] == 'gm3_0a':
                gm3_0a_strain = float_list[i]*np.sqrt(2)/2

            if keys[i] == 'gm5_a00':
                gm5_a00_strain = float_list[i]*np.sqrt(2)/2

            if keys[i] == 'gm5_0a0':
                gm5_0a0_strain = float_list[i]*np.sqrt(2)/2

            if keys[i] == 'gm5_00a':
                gm5_00a_strain = float_list[i]*np.sqrt(2)/2

            if keys[i] == 'oct_rot_x':
                'x-rot'

            if keys[i] == 'oct_rot_y':
                'y-rot'

            if keys[i] == 'oct_rot_z':
                'z-rot'

            if keys[i] == 'exx':
                exx = float_list[i]

            if keys[i] == 'eyy':
                eyy = float_list[i]

            if keys[i] == 'ezz':
                ezz = float_list[i]

            if keys[i] == 'exy':
                exy = float_list[i]*np.sqrt(2)/2

            if keys[i] == 'exz':
                exz = float_list[i]*np.sqrt(2)/2

            if keys[i] == 'eyz':
                eyz = float_list[i]*np.sqrt(2)/2

            uniaxial_strains = np.zeros((3,3))
            shear_strains = np.zeros((3,3))

            uniaxial_strains = np.array([[gm1_strain - 0.5*gm3_a0_strain + gm3_0a_strain + exx, 0, 0],
                                         [0, gm1_strain - 0.5*gm3_a0_strain - gm3_0a_strain + eyy, 0],
                                         [0, 0, gm1_strain + gm3_a0_strain + ezz]])
            
            shear_strains = np.array([[0, (gm5_a00_strain + exy)*lattice[1,1], (gm5_0a0_strain + exz)*lattice[2,2]],
                                      [(gm5_a00_strain + exy)*lattice[0,0], 0, (gm5_00a_strain + eyz)*lattice[2,2]],
                                      [(gm5_0a0_strain + exz)*lattice[0,0], (gm5_00a_strain + eyz)*lattice[2,2], 0]])

            updated_lattice = np.transpose(uniaxial_strains.dot(np.transpose(lattice)) + shear_strains + np.transpose(lattice))
            new_structure = Structure(updated_lattice, struct.species, struct.frac_coords)
            new_structure.to(fmt='poscar', filename = os.path.join(leaf_dir,'POSCAR'))
    
    list_of_params = get_values_from_dict(param_dict)
    list_of_lists = convert_values_to_list(list_of_params)
    struct = Structure.from_file(parent_structure)

    create_nested_directories(list_of_lists)
    copy_file_to_leaf_directories(parent_structure)

    return