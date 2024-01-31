# # %%
# data science
import pandas as pd
import numpy as np
import stats_arrays as sarrays # for uncertainty distributions
# system
import pathlib
# debugging
import logging
# project configuration
import tomllib

# local imports
import ecopylot.utils as utils

utils.load_project_configuration()


def _get_dataframe_stats(df: pd.DataFrame) -> dict:
        

def generate_stochastic_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds stochastic columns to the dataframe.

    For single values, this would look like:

    1: static value
    2: lognormal distribution
    5: triangular distribution

    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  | scale | shape |
    |-------------|-----------|-----|------------------|-----|-----|------|-------|-------|
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | NaN   | NaN   |
    | 456         | bar       | ... | 5                | 8.4 | 2   | 11.2 | NaN   | NaN   |
    | 789         | baz       | ... | 2                | 2.3 | 0.1 | 5.5  | 0.3   | NaN   |

    if we now choose iterations = 3, we get:
    
    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  | iteration | stochastic |
    |-------------|-----------|-----|------------------|-----|-----|------|-----------|------------|
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | 1         | 0.1        |
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | 2         | 0.1        |
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | 3         | 0.1        |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 | 1         | 9.2        |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 | 2         | 7.8        |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 | 3         | 8.9        |
    | 789         | baz       | ... | 5                | 2.3 | 0.1 | 5.5  | 1         | 2.8        |
    | 789         | baz       | ... | 5                | 2.3 | 0.1 | 5.5  | 2         | 3.2        |
    | 789         | baz       | ... | 5                | 2.3 | 0.1 | 5.5  | 3         | 3.1        |


    ```
    {
        (...)
        "uncertainty_type": 1, # static value (no uncertainty)
        "loc": 0.1,
        "min": NaN,
        "max": NaN,
        (...)
    }
    ```
    For distributions, this would look like:
    ```
    {
        (...)
        "uncertainty_type": 2, # lognormal distribution
        "loc": 8.4,
        "min": 2,
        "max": 11.2,
        (...)
    }
    ```
    """

def generate_parameter_dicts(df: pd.DataFrame) -> pd.DataFrame:
    """
    To a Pandas DataFrame of this form:

    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  | scale | shape |
    |-------------|-----------|-----|------------------|-----|-----|------|-------|-------|
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | NaN   | NaN   |
    | 456         | bar       | ... | 5                | 8.4 | 2   | 11.2 | NaN   | NaN   |
    | 789         | baz       | ... | 2                | 2.3 | 0.1 | 5.5  | 0.3   | NaN   |
    
    adds a column "stochastic_dict" with the following content:

    | UID (index) | parameter | ... | stochastic_dict                                    |
    |-------------|-----------|-----|----------------------------------------------------|
    | 123         | foo       | ... | {"loc": 0.1}                                       |
    | 456         | bar       | ... | {"loc": 8.4, "min": 2, "max": 11.2}                |
    | 789         | baz       | ... | {"loc": 2.3, "min": 0.1, "max": 5.5, "scale": 0.3} |

    Note that the number of distribution-related columns (eg. "scale", "shape") will depend
    on the number of unique uncertainty types in the dataframe.
    For instance, if the dataframe contains only lognormal distributions (type "2"),
    the "scale" and "shape" columns will be not be present in the dataframe. 

    Parameters
    ----------
    df : pd.DataFrame
        A Pandas DataFrame containing the parameter data.

    Returns
    -------
    pd.DataFrame
        The Pandas DataFrame with the added "stochastic_dict" column.

    See Also
    --------
    The full list of possible uncertainty types is available from the `stats_arrays` documentation:
    `stats_arrays uncertainty types <https://stats-arrays.readthedocs.io/en/latest/index.html?highlight=stats_arrays%20distributions#mapping-parameter-array-columns-to-uncertainty-distributions>`_.   
    """

    distributions_columns: list = [
        'loc',
        'scale',
        'shape',
        'min',
        'max',
    ]
    if not set(distributions_columns).issubset(df.columns):
        raise Exception(f"DataFrame does not contain any of the distribution-related columns: {distributions_columns}")

    df['stochastic_dict'] = df[distributions_columns].apply(lambda x: x.dropna().to_dict(), axis=1)

    return df

    