import os
from scipy.io import loadmat
import numpy as np

def get_path(filename):
    """Find filename in ./data/ directory and return its path

    Args:
        filename (str): file we're looking for in ./data/ directory.

    Returns:
        str: absolute path to file "filename" in ./data/ dir.

    """

    here_dir = os.path.dirname(os.path.realpath('__file__'))
    file_dir = os.path.join(here_dir, 'data', filename)
    return(file_dir)

def get_connectivity_matrices(filepath):
    """Read connectivity matrices from .mat file.

    Args:
        filepath (str): full path to .mat file containing connectivity matrices.

    Returns:
        arr: Array of connectivity matrices, one per patient.

    """

    from pathlib import Path
    my_file = Path(filepath)

    if my_file.is_file():
        healthy_14    = loadmat(my_file)['S'] #load data for all 14 patients
        conn_matrices = np.transpose(healthy_14)
        return(conn_matrices)

    else:
        print(my_file)
        raise(FileNotFoundError('Is path to file correct??'))
