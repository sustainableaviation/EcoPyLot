# %%
import pandas as pd
import numpy as np

#project
import inout
import utils

import pathlib
from pathlib import Path

import logging

config: dict = utils.load_project_configuration()

dict_dist_mapping = config['uncertainty_distributions_mapping']

mypath = Path("/Users/michaelweinold/github/EcoPyLot/dev/other/Input data_bus.xlsx")

# %%

def _load_excel(excel_input: pathlib.PurePath) -> pd.DataFrame:
    """
    Loads data from an Excel `xls` or `xlsx` file into a DataFrame.

    Parameters
    ----------
    excel_input : pathlib.PurePath
        The path to the Excel file.
    
    Returns
    -------
    pd.DataFrame
        The DataFrame containing the data from the Excel file.
    
    Raises
    ------
    TypeError
        If the input is not a `pathlib.PurePath` to an Excel file.
    """

    if isinstance(excel_input, pathlib.PurePath):
        pass
    else:
        raise TypeError("Input must be a pathlib.PurePath to an Excel file.")

    df = pd.read_excel(
        io = excel_input,
        header = None,
        engine = 'openpyxl',
        na_values = ['None', 'none', 'N/A', 'n/a', 'NA', 'na', 'NaN', 'nan', '', ' '],
        keep_default_na = True,
        na_filter = True,
        decimal = '.',
    )

    logging.info(f"Excel data loaded successfully (#rows: {df.shape[0]}, #columns: {df.shape[1]}, size in memory: {sys.getsizeof(df)} bytes)")

    return df


def _columns_string_to_list(df: pd.DataFrame, list_string_cols: list) -> pd.DataFrame:
    """
    Converts the content of columns containing string enumerations to lists.

    The function converts the content of columns containing string enumerations of the form:

    `alpha, beta`
    
    into lists of the form:

    `["alpha", "beta"]`

    If the column contains a single value, the function will convert it into a list with a single element.
    If the data type of the column is not a string, the function will leave it unchanged.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
    
    list_string_cols : list
        The list of column names containing string enumerations.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the content of the columns containing string enumerations converted to lists.
    """
    for col in list_string_cols:
        df[col] = df[col].apply(
            lambda x:
            [item.strip() for item in x.split(',')]
            if isinstance(x, str) else x
        )

    logging.info(f"Columns {list_string_cols} converted to lists.")

    return df


def _uncertainty_distribution_string_to_code(
        df: pd.DataFrame,
        uncertainty_col: str,
        uncertainty_dict: dict
    ) -> pd.DataFrame:
    """
    Converts the string description of uncertainty distributions to `stats_arrays` integer codes.

    The function converts the string description of uncertainty distributions
    in a dataframe column `uncertainty_col` of the form:

    | uncertainty_col | ... |
    |-----------------|-----|
    | triangular      | ... |
    | normal          | ... |

    into `stats_arrays` integer codes in a new column `uncertainty` of the form:

    | uncertainty_col | uncertainty | ... |
    |-----------------|-------------|-----|
    | triangular      | 5           | ... |
    | normal          | 3           | ... |

    The dictionary `uncertainty_dict` is expected to contain
    the mapping between the string description of
    the uncertainty distributions and the `stats_arrays` integer codes.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.

    uncertainty_col : str
        The name of the column containing the string description of the uncertainty distributions.

    uncertainty_dict : dict
        The dictionary containing the mapping between the string description of the uncertainty distributions and the `stats_arrays` integer codes.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the string description of the uncertainty distributions converted to `stats_arrays` integer codes.

    See Also
    --------
    ``stats_arrays` list of uncertainty distributions <https://stats-arrays.readthedocs.io/en/latest/#mapping-parameter-array-columns-to-uncertainty-distributions>`__

    """
    df['uncertainty'] = df[uncertainty_col].replace(uncertainty_dict)

    logging.info(f"Column {uncertainty_col} converted to `stats_arrays` integer codes.")

    return df


def _stack_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Stacks the DataFrame to make it long-form.

    The function takes a table of the form:

    |       | parameter | 2001               | 2002               | ... |
    |       |           | loc  | low  | high | loc  | low  | high | ... |
    |-------|-----------|------|------|------|------|------|------|-----|
    | 0     | foo       | 1.5  | 1    | 2    | 8    | 7    | 8.5  | ... |
    | 1     | bar       | NaN  | NaN  | Nan  | 14   | 12   | 17   | ... |

    and transforms it into a table of the form:

    |       | parameter | year | loc | low | high | ... |
    |-------|-----------|------|-----|-----|------|-----|
    | 0     | foo       | 2001 | 1.5 | 1   | 2    | ... |
    | 1     | foo       | 2002 | 8   | 7   | 8.5  | ... |
    | 2     | bar       | 2002 | 14  | 12  | 17   | ... |

    See Also
    --------
    `Stack Overflow question <https://stackoverflow.com/a/77945979>`__
    `Pandas User Guide - Reshaping <https://pandas.pydata.org/docs/user_guide/reshaping.html#stack-and-unstack>`__

    Notes
    -----
    `Since Pandas 2.1.0 <https://pandas.pydata.org/docs/whatsnew/v2.1.0.html#new-implementation-of-dataframe-stack>`, the `stack` function by default
    "persists all values from the input", meaning that
    we would get a column with `NaN` values like so:

    | 2001               | 2002               | ... |
    | loc  | low  | high | loc  | low  | high | ... |
    |------|------|------|------|------|------|-----|
    | 1.5  | 1    | 2    | 8    | 7    | 8.5  | ... |
    | NaN  | NaN  | Nan  | 14   | 12   | 17   | ... |

    | year | loc | low | high | ... |
    |------|-----|-----|------|-----|
    | 2001 | 1.5 | 1   | 2    | ... |
    | 2001 | NaN | NaN | NaN  | ... |
    | 2002 | 8   | 7   | 8.5  | ... |
    | 2002 | 14  | 12  | 17   | ... |

    We therefore need to remove this row using the `dropna` function.
    """

    # move all string columns to the index
    # this is to make sure the stack function works only on 'year' columns

    list_cols: list = list(df.columns.get_level_values(0))
    list_string_cols: list = [item for item in list_cols if isinstance(item, str)]
    df = df.set_index(keys = list_string_cols)

    df = df.stack(
        level = 0, # stack 'year' columns
        future_stack=True # https://pandas.pydata.org/docs/whatsnew/v2.1.0.html#new-implementation-of-dataframe-stack
    )

    df = df.dropna(
        axis = 0,
        how = 'all'
    )

    # move the string columns back from the index
    # and reset the index

    df = df.reset_index(drop = False)

    logging.info(f"DataFrame stacked to long-form.")

    return df


def _set_dataframe_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sets the indices of the DataFrame.

    The function takes a table of the form:

    |       | 0         | 1    | 2    | 3    | 4    | ... |
    |-------|-----------|------|------|------|------|-----|
    | 0     | parameter | 2001 | 2001 | 2002 | 2002 | ... |
    | 1     |           | low  | high | low  | high | ... |
    | 2     | foo       | 1    | 2    | 7    | 8    | ... |
    | 3     | bar       | NaN  | NaN  | 12   | 13   | ... |

    and transforms it into a table of the form:

    | year                | 2001        | 2002        | ... |
    | uncertainty_metrics | low  | high | low  | high | ... |
    |---------------------|------|------|------|------|-----|
    | 0                   | 1    | 2    | 7    | 8    | ... |
    | 1                   | NaN  | NaN  | 12   | 13   | ... |

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.

    Returns
    -------
    pd.DataFrame
        The DataFrame with the indices set.
    """

    index = pd.MultiIndex.from_arrays(
        arrays = [
            df.iloc[0, 0:],
            df.iloc[1, 0:]
        ],
        names = (
            'year',
            'uncertainty_metrics'
        )
    )

    df = df.iloc[2:].set_axis(index, axis=1)
    df = df.reset_index(drop = True)

    logging.info(f"DataFrame indices set to {df.index.names}.")

    return df


def load_data_from_excel(
        excel_input: pathlib.PurePath,
        uncertainty_col: str,
        uncertainty_dict: dict,
        list_string_cols: list
    ) -> pd.DataFrame:
    """
    Loads data from an Excel `xls` or `xlsx` file into a DataFrame.

    The function converts an Excel file containing data into a
    Pandas DataFrame, doing XYZ XXXXXXXXXXX.
    The Excel sheet is expected to be of the form (compare also this XXXXX example file):
    
    | index | A         | B              | C                  | D    | E    | F    | G    | H    | I    | ... |
    |-------|-----------|----------------|--------------------|------|------|------|------|------|------|-----|
    | 1     | parameter | classification | uncertainty distr. | 2001 | 2001 | 2001 | 2002 | 2002 | 2002 | ... |
    | 2     |           |                |                    | loc  | low  | high | loc  | low  | high | ... |
    | 3     | foo       | alpha, beta    | triangular         | 1.5  | 1    | 2    | 8    | 7    | 8.5  | ... |
    | 4     | bar       | gamma, delta   | triangular         |      |      |      | 14   | 12   | 17   | ... |

    The function will return a DataFrame of the form:

    | index | parameter | year | classification     | uncertainty code | loc | low | high | ... |
    |-------|-----------|------|--------------------|------------------|-----|-----|------|-----|
    | 0     | foo       | 2001 | ["alpha", "beta"]  | 5                | 1.5 | 1   | 2    | ... |
    | 1     | foo       | 2002 | ["alpha", "beta"]  | 5                | 8   | 7   | 8.5  | ... |
    | 2     | bar       | 2002 | ["gamma", "delta"] | 5                | 14  | 12  | 17   | ... |

    Instead of `loc`, `low`, `high`, other statistical measures can be provided for each year.
    Compare the `stats_arrays` table for more details:
    https://stats-arrays.readthedocs.io/en/latest/index.html#mapping-parameter-array-columns-to-uncertainty-distributions

    Parameters
    ----------
    excel_input : pathlib.PurePath
        The path to the Excel file.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame containing the parsed Excel data.

    Raises
    ------
    TypeError
        If the input is not a `pathlib.PurePath` to an Excel file.
    """

    if isinstance(excel_input, pathlib.PurePath):
        pass
    else:
        raise TypeError("Input must be a pathlib.PurePath to a JSON file.")

    df = _load_excel(excel_input)
    df = _set_dataframe_indices(df)
    df = _uncertainty_distribution_string_to_code(
            df = df,
            uncertainty_col = uncertainty_col,
            uncertainty_dict = uncertainty_dict
    )   
    df = _columns_string_to_list(
            df = df,
            list_string_cols = list_string_cols
    )
    df = _stack_dataframe(df)

    return df


# %%
data = {
    0: ['parameter', '', 'foo', 'bar'],
    1: ['classification', '', 'alpha, beta', 'gamma, delta'],
    2: [2001, 'low', 1, np.nan],
    3: [2001, 'high', 2, np.nan],
    4: [2002, 'low', 7, 12],
    5: [2002, 'high', 8, 13],
}

df = pd.DataFrame(data)