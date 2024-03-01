from matlab_reader import MatlabReader
import h5py
import pytest
import json
import os

@pytest.fixture
def matlab_reader():
    """
    Initalise a instance of MatlabReader class for testing
    """
    mr = MatlabReader(f'{os.getcwd()}{os.sep}data_input{os.sep}workspace.mat')
    return mr


def test_get_mat_file(matlab_reader: MatlabReader): 
    """
    Test the return of the matlab file as HDF5-file

    Args:
        matlab_reader (MatlabReader): MatlabReader Instance for testing
    """    
    file = matlab_reader.get_mat_file()
    assert isinstance(file, h5py.File)


def test_close_current_mat_file(matlab_reader: MatlabReader):
    """
    Test if the Matlab file within the MatlabReader is correctly closed

    Args:
        matlab_reader (MatlabReader): MatlabReader Instance for testing
    """
    value = matlab_reader.close_current_mat_file() 
    assert value == None


def test_get_dictionary_from_struct(matlab_reader: MatlabReader):
    """
    Test if there is a dictionary returned 

    Args:
        matlab_reader (MatlabReader): MatlabReader Instance for testing
    """ 
    value = matlab_reader.get_dictionary_from_struct('FCAData_onC')
    assert isinstance(value, dict)   


def test_if_dict_is_json_serializable(matlab_reader: MatlabReader):
    """
    Test if dictionary returned by matlab_reader using keyword json is
    json serializable

    Args:
        matlab_reader (MatlabReader): MatlabReader Instance for testing
    """ 
    struct_as_dict = matlab_reader.get_dictionary_from_struct('FCAData_onC',
                                                arraytype = 'json')
    try:
        # Attempt to serialize the data to JSON format
        json_data = json.dumps(struct_as_dict)
    except (TypeError, ValueError) as e:
        # Handle serialization errors
        pytest.fail(f"Serialization to JSON failed: {e}")

    # Assertion: Check if serialization was successful
    assert json_data is not None, "Serialization to JSON failed"




# FCAData_onC = mr.get_dictionary_from_struct('FCAData_onC',arraytype='json')
# print(FCAData_onC['tip'])
# print(FCAData_onC['map'])


# with open(f'{os.getcwd()}{os.sep}output{os.sep}FCAData_onC.json','w') as json_file:
#     json.dump(FCAData_onC,json_file)

# mr.update_mat_file(f'{os.getcwd()}{os.sep}data_input{os.sep}workspace.mat')
# print(mr._mat_file)