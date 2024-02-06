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

| index | 2001 | 2001 | 2002 | 2002 | ... |
|-------|------|------|------|------|-----|
| 1     | low  | high | low  | high | ... |
| 2     | 1    | 2    | 7    | 8    | ... |
| 3     | NaN  | NaN  | 12   | 13   | ... |

| index | 1    | 2    | 3    | 4    | ... |
|-------|------|------|------|------|-----|
| 1     | 2001 | 2001 | 2002 | 2002 | ... |
| 2     | low  | high | low  | high | ... |
| 3     | 1    | 2    | 7    | 8    | ... |
| 4     | NaN  | NaN  | 12   | 13   | ... |

|       | 2001        | 2002        | ... |
| index | low  | high | low  | high | ... |
|-------|------|------|------|------|-----|
| 1     | 1    | 2    | 7    | 8    | ... |
| 2     | NaN  | NaN  | 12   | 13   | ... |



to:

| index | year | low | high | ... |
|-------|------|-----|------|-----|
| 1     | 2001 | 1   | 2    | ... |
| 2     | 2002 | 7   | 8    | ... |
| 3     | 2002 | 12  | 13   | ... |
"""