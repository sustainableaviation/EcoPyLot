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
        

array = sarrays.UncertaintyBase.from_dicts(*[self.data[key] for key in keys])
        rng = sarrays.MCRandomNumberGenerator(array)

def generate_stochastic_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds stochastic columns to the dataframe.

    For single values, this would look like:

    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  |
    |-------------|-----------|-----|------------------|-----|-----|------|
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 |

    if we now choose iterations = 3, we get:
    
    | UID (index) | parameter | ... | uncertainty_type | loc | min | max  | iteration | stochastic |
    |-------------|-----------|-----|------------------|-----|-----|------|-----------|------------|
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | 1         | 0.1        |
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | 2         | 0.1        |
    | 123         | foo       | ... | 1                | 0.1 | NaN | NaN  | 3         | 0.1        |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 | 1         | 9.2        |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 | 2         | 7.8        |
    | 456         | bar       | ... | 2                | 8.4 | 2   | 11.2 | 3         | 8.9        |


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