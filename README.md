# read_in_matlab_via_python

## Matlab Reader Class

The Matlab Reader class is a Python class designed to read HDF5 files created with MATLAB. 
The class provides various methods to extract data from the HDF5 file and structure it into a Python dictionary.

### Usage

To use the class, you first need to create an instance of the class and specify the path to the MATLAB HDF5 file:

# Python example:
reader = MatlabReader('path/to/file.mat')

Methods:

The class provides the following methods:

    change_mat_file(path_to_matlab_file): Updates the currently opened MATLAB HDF5 file by first closing the current file and then opening the new file.

    get_data_from_reference(ref, parent_group, arraytype='numpy'): Extracts data from a reference in the HDF5 file and structures it into a Python dictionary.

    get_dictionary_from_struct(keyword, arraytype='numpy'): Extracts the data from the structure with the specified keyword in the HDF5 file and structures it into a Python dictionary.

    convert_integer_array_to_string(data): Converts a NumPy array of integers into a string.

    print_dict_structure(d, indent=0): Prints the structure of the given dictionary with the specified indentation depth.

    close_current_mat_file(): Closes the currently opened MATLAB HDF5 file and releases the reference.


Dependencies:

The class uses the following Python libraries:

    NumPy
    h5py

Make sure these libraries are installed in your Python environment before using the class.


Example:
Here is a simple example of how the class can be used:


import numpy as np
from matlab_reader import MatlabReader

# Path to the MATLAB HDF5 file
file_path = 'path/to/file.mat'

# Create an instance of the Matlab Reader class
reader = MatlabReader(file_path)

# Extract data from the structure 'structure_keyword'
data_dict = reader.get_dictionary_from_struct('structure_keyword')

# Print the structure of the resulting dictionary
reader.print_dict_structure(data_dict)

# Close the opened HDF5 file
reader.close_current_mat_file()

Another example for using the Matlab Reader Class within another Python program is given in test_matlab_reader.py.