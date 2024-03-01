import numpy as np
import h5py 


class MatlabReader:
    """
    A class for reading in mat-files encoded in -v7.3 format using h5py.
    """
    def __init__(self, path_to_matlab_file: str):
        """
        Initialize the MatlabReader based on a Matlab file read in
        as h5py-file.

        Parameters:
            path_to_matlab_file (str): The path to the Matlab file.
        """
        self._mat_file = h5py.File(path_to_matlab_file)


    def get_mat_file(self) -> h5py.File:
        """
        Get the currently open mat file in HDF5 format.

        Returns:
            h5py.File: The HDF5 file.
        """
        return self._mat_file

    def close_current_mat_file(self) -> None:
        """
        Closes the currently open mat file.
        """
        if hasattr(self, '_mat_file') and self._mat_file is not None:
            self._mat_file.close()
            self._mat_file = None
            print("Current MATLAB file closed and reference released.")


    def change_mat_file(self, path_to_matlab_file: str) -> None:
        """
        Changes the currently open mat file.

        Parameters:
            path_to_matlab_file (str): The path to the new Matlab file.
        """
        self.close_current_mat_file()
        self._mat_file = h5py.File(path_to_matlab_file)
        print('New MATLAB file in HDF5 format read.')
        


    def get_data_from_reference(self, ref: str, parent_group: h5py.Group,
                                 arraytype: str = 'numpy') -> dict:
        """
        Get data from a referenced object within a parent group.

        Parameters:
            ref (str): The reference string.
            parent_group (h5py.Group): The parent group.
            arraytype (str, optional): The type of array to return 
                                       ('numpy' or 'json').

        Returns:
            dict: A dictionary containing the retrieved data.
        """
        referenced_object = parent_group[ref]
        data_dictionary = {}

        
        if isinstance(referenced_object, h5py.Dataset):
            
            array_of_possible_references = referenced_object[:]

            if np.ndim(array_of_possible_references) == 2:
                data = []  
                for possible_ref in array_of_possible_references:

                    for individual_possible_ref in possible_ref:
                        if isinstance(individual_possible_ref,h5py.Reference):
                            data.append(self._mat_file[individual_possible_ref])
                        else:
                            data.append(individual_possible_ref)
            else:
                data = referenced_object[:]
            

            data = np.array(data)
            if data.dtype=='uint16':
                data = self.convert_integer_array_to_string(data)

            if arraytype == 'json':
                if isinstance(data, np.ndarray):
                    data = data.tolist()
            
            data_dictionary.update({ref : data})
            
            return data_dictionary       
        
        elif isinstance(referenced_object, h5py.Group):
            
            # print(f'{ref} is a group. Contents:')
            subdict = {}
            subkeys = list(referenced_object.keys())
            for subkey in subkeys:
                # print(f'- {subkey}')
                
                subdict.update(
                    self.get_data_from_reference(subkey, 
                                                 referenced_object,arraytype)
                    )
            
            data_dictionary.update({ref:subdict})

            return data_dictionary 
        

    def print_dict_structure(self, d: dict, indent: int = 0) -> None:
        """
        Print the structure of a dictionary.

        Parameters:
            d (dict): The dictionary to print.
            indent (int): The indentation level.
        """
        
        for key, value in d.items():
            print('|  ' * indent + f'{str(key)} : {type(value)}')
            if isinstance(value, dict):
                self.print_dict_structure(value, indent + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.print_dict_structure(item, indent + 1)



    def get_dictionary_from_struct(self, keyword: str,
                                    arraytype: str = 'numpy') -> dict:
        """
        Get a dictionary from a struct in the HDF5 file.

        Parameters:
            keyword (str): The keyword for the struct.
            arraytype (str, optional): The type of array to return ('numpy' or 'json').

        Returns:
            dict: A dictionary generated from the struct with lists in arraytype format
        """
        mat_struct = self._mat_file[keyword]
        dictfromstruct = {}
        for key in list(mat_struct.keys()):
            dictfromstruct.update(
                self.get_data_from_reference(key, mat_struct, arraytype)
                )

        return dictfromstruct


    def convert_integer_array_to_string(self, data) -> str:
        """
        Convert an array of integers to a string.

        Parameters:
            data (numpy.ndarray): The array of integers.

        Returns:
            str: The resulting string.
        """
        charList = [chr(integer) for integer in data]
        return ''.join(charList)




