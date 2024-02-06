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