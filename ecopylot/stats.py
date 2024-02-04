# # %%
# data science
import pandas as pd
import numpy as np
import stats_arrays as sarrays # for uncertainty distributions
# system
import pathlib
# debugging
import logging

# local imports
# import ecopylot.utils as utils

# utils.load_project_configuration()


def get_stats(df: pd.DataFrame) -> dict:
    """
    Get basic statistics for a dataframe.

    The function returns a dictionary with the following statistics:
    
    """
    pass
        

def _add_distribution_dict_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column with the distribution parameters as a dictionary.

    The function takes a dataframe of the form:

    +-------------+-----------+-----+------------------+-----+-----+------+-------+-------+
    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  | scale | shape |
    +=============+===========+=====+==================+=====+=====+======+=======+=======+
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | NaN   | NaN   |
    +-------------+-----------+-----+------------------+-----+-----+------+-------+-------+
    | 456         | bar       | ... | 5                | 8.4 | 2   | 11.2 | NaN   | NaN   |
    +-------------+-----------+-----+------------------+-----+-----+------+-------+-------+
    
    and adds a column ``parameter_value_distribution_dict`` to return a dataframe of the form:

    +-------------+-----------+-----+----------------------------------------------------+
    | UID (index) | parameter | ... | parameter_value_distribution_dict                  |
    +=============+===========+=====+====================================================+
    | 123         | foo       | ... | {"loc": 0.1}                                       |
    +-------------+-----------+-----+----------------------------------------------------+
    | 456         | bar       | ... | {"loc": 8.4, "min": 2, "max": 11.2}                |
    +-------------+-----------+-----+----------------------------------------------------+

    Parameters
    ----------
    df : pd.DataFrame
        A Pandas DataFrame containing the parameter data.

    Returns
    -------
    pd.DataFrame
        The Pandas DataFrame with the added ``parameter_value_distribution_dict`` column.


    Notes 
    -----
    Note that the number of distribution-related columns (eg. ``scale``, ``shape``) will depend
    on the number of unique uncertainty types in the dataframe.
    For instance, if the dataframe contains only lognormal distributions (type ``2``),
    the ``scale`` and ``shape`` columns will be not be present in the dataframe.     
    
    See Also
    --------
    The full list of possible uncertainty types is available from the `stats_arrays` documentation:
    `stats_arrays uncertainty types <https://stats-arrays.readthedocs.io/en/latest/index.html?highlight=stats_arrays%20distributions#mapping-parameter-array-columns-to-uncertainty-distributions>`_.   
    """

    distributions_columns_all: list = [
        'loc',
        'scale',
        'shape',
        'minimum',
        'maximum',
    ]
    distribution_columns_present: list = list(set(distributions_columns_all).intersection(df.columns))

    if not any(col in df.columns for col in distributions_columns_all):
        raise Exception(f"DataFrame does not contain any of the distribution-related columns: {distributions_columns}")

    df['parameter_value_distribution_dict'] = df[distribution_columns_present].apply(lambda x: x.dropna().to_dict(), axis=1)

    return df


def _sample_parameters_from_distrivution(df: pd.DataFrame, iterations: int) -> pd.DataFrame:
    """
    Adds a stochastic column to the dataframe.

    The function takes a dataframe of the form
    (provided by `_add_distribution_dict_column`):

    +-------------+-----------+-----+----------------------------------------------------------------------+
    | UID (index) | parameter | ... | parameter_value_distribution_dict                                    |
    +-------------+-----------+-----+----------------------------------------------------------------------+
    | 123         | foo       | ... | {"loc": 0.1, "uncertainty_type": 1}                                  |
    +-------------+-----------+-----+----------------------------------------------------------------------+
    | 456         | bar       | ... | {"loc": 8.4, "minimum": 2, "maximum": 11.2, "uncertainty_type": 5}   |
    +-------------+-----------+-----+----------------------------------------------------------------------+


    and, depending on the variable ``iterations``, adds a column ``stochastic``.
    For ``iterations=3``, the function returns a dataframe of the form:

    +-------------+-----------+-----+----------------------------------------------------+
    | UID (index) | parameter | ... | parameter_value_stochastic                         |
    +=============+===========+=====+====================================================+
    | 123         | foo       | ... | [0.1, 0.1, 0.1]                                    |
    +-------------+-----------+-----+----------------------------------------------------+
    | 456         | bar       | ... | [6.52059172, 5.89316567, 8.15385019]               |
    +-------------+-----------+-----+----------------------------------------------------+
    """

    if 'parameter_value_distribution_dict' not in df.columns:
        raise ValueError("DataFrame does not have 'parameter_value_distribution_dict' column")

    list_of_dicts: list = list(df['parameter_value_distribution_dict'])

    parameters: np.ndarray = sarrays.UncertaintyBase.from_dicts(*list_of_dicts)
    
    montecarlogen: sarrays.MCRandomNumberGenerator = sarrays.MCRandomNumberGenerator(parameters)

    parameters_stochastic: np.ndarray = montecarlogen.generate(int(iterations))

    df['parameter_value_stochastic'] =  list(parameters_stochastic)

    return df


def generate_stochastic_dataframe(df: pd.DataFrame, iterations: int) -> pd.DataFrame:
    """
    Adds a stochastic column to the dataframe.

    The function takes a dataframe of the form:

    +-------------+-----------+-----+------------------+-----+-----+------+-------+-------+
    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  | scale | shape |
    +=============+===========+=====+==================+=====+=====+======+=======+=======+
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | NaN   | NaN   |
    +-------------+-----------+-----+------------------+-----+-----+------+-------+-------+
    | 456         | bar       | ... | 5                | 8.4 | 2   | 11.2 | NaN   | NaN   |
    +-------------+-----------+-----+------------------+-----+-----+------+-------+-------+

    and, depending on the variable ``iterations``, adds a column ``stochastic``.
    For ``iterations=3``, the function returns a dataframe of the form:

    +-------------+-----------+-----+----------------------------------------------------+
    | UID (index) | parameter | ... | parameter_value_stochastic                         |
    +=============+===========+=====+====================================================+
    | 123         | foo       | ... | [0.1, 0.1, 0.1]                                    |
    +-------------+-----------+-----+----------------------------------------------------+
    | 456         | bar       | ... | [6.52059172, 5.89316567, 8.15385019]               |
    +-------------+-----------+-----+----------------------------------------------------+

    Parameters
    ----------
    df : pd.DataFrame
        A Pandas DataFrame containing the parameter data.

    iterations : int
        The number of iterations to generate.

    """
    
    df = _add_distribution_dict_column(df)
    df = _sample_parameters_from_distrivution(df, iterations)

    return df