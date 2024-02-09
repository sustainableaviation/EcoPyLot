# %%
import pandas as pd
import numpy as np

#project
import inout
import utils

config: dict = utils.load_project_configuration()

# %%

def myfunc(x):
    return str([item.strip() for item in x.split(',')])


df = pd.read_excel(
    io = '/Users/michaelweinold/github/EcoPyLot/dev/other/Input data_bus.xlsx',
    header=None,
    engine = 'openpyxl',
    na_values = ['None', 'none', 'N/A', 'n/a', 'NA', 'na', 'NaN', 'nan', '', ' '],
    keep_default_na = True,
    na_filter = True,
    decimal = '.',
    #converters = {'powertrain': myfunc}
)

# %%
list_filter = ['heat pump CoP, cooling', 'cooling energy consumption', 'battery cooling unit']
dff = df[df['parameter'].isin(list_filter)]

df['new'] = df['powertrain'].apply(lambda x: [item for item in x.split(',')] if isinstance(x, str) else x)
df['new1'] = df['uncertainty distribution'].replace(config['uncertainty_distributions_mapping'])
# %%

# to do: years to 

"""
How do I transform the following dataframe:

| index | 0         | 1    | 2    | 3    | 4    | ... |
|-------|-----------|------|------|------|------|-----|
| 0     | parameter | 2001 | 2001 | 2002 | 2002 | ... |
| 1     |           | low  | high | low  | high | ... |
| 2     | foo       | 1    | 2    | 7    | 8    | ... |
| 3     | bar       | NaN  | NaN  | 12   | 13   | ... |


to:

| index | parameter | year | low | high | ... |
|-------|-----------|------|-----|------|-----|
| 0     | foo       | 2001 | 1   | 2    | ... |
| 1     | foo       | 2002 | 7   | 8    | ... |
| 2     | bar       | 2002 | 12  | 13   | ... |
"""

"""
| index | 1    | 2    | 3    | 4    | ... |
|-------|------|------|------|------|-----|
| 0     | 2001 | 2001 | 2002 | 2002 | ... |
| 1     | low  | high | low  | high | ... |
| 2     | 1    | 2    | 7    | 8    | ... |
| 3     | NaN  | NaN  | 12   | 13   | ... |

|       | 2001        | 2002        | ... |
| index | low  | high | low  | high | ... |
|-------|------|------|------|------|-----|
| 0     | 1    | 2    | 7    | 8    | ... |
| 1     | NaN  | NaN  | 12   | 13   | ... |
"""

dfyears = df[[col for col in df.columns.unique() if isinstance(df.iloc[0][col], int)]]

multiindex = pd.MultiIndex.from_product(
    [
        list(dfyears.iloc[0].unique()),
        list(dfyears.iloc[1].unique())
    ]
)

dfyears.columns = multiindex
dfyears = dfyears.drop([0, 1])

# %%

data = {
    0: ['parameter', '', 'foo', 'bar'],
    1: [2001, 'low', 1, np.nan],
    2: [2001, 'high', 2, np.nan],
    3: [2002, 'low', 7, 12],
    4: [2002, 'high', 8, 13],
}

df = pd.DataFrame(data)

idx = pd.MultiIndex.from_arrays([df.iloc[0, 1:], df.iloc[1, 1:]],
                                names=('year', None))

out = df.iloc[2:].set_index(0).set_axis(idx, axis=1).rename_axis('parameter').stack(0).reset_index()

# https://stackoverflow.com/a/77945979/7331016

def load_data_from_excel(excel_input: pathlib.PurePath) -> pd.DataFrame:
    """
    Loads data from an Excel `xls` or `xlsx` file into a DataFrame.

    The function converts an Excel file containing data into a
    Pandas DataFrame, doing XYZ XXXXXXXXXXX.
    The Excel sheet is expected to be of the form (compare also this example file):
    
    | index | A         | B              | C                  | D    | E    | F    | G    | H    | I    | ... |
    |-------|-----------|----------------|--------------------|------|------|------|------|------|------|-----|
    | 1     | parameter | classification | uncertainty distr. | 2001 | 2021 | 2001 | 2002 | 2002 | 2002 | ... |
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

    """
# %%
