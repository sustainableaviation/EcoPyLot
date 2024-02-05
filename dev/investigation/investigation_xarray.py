# %%
# data science
import xarray as xr
import pandas as pd
import numpy as np
# io
import sys
import pathlib
from pathlib import Path

"""
| value | parameter | year | size | propulsion |
|-------|-----------|------|------|------------|
| 12.4  | eta       | 2020 | 100  | A-B-C-D    |
| 7.5   | gamma     | 2021 | 220  | A-E-X-D    |
"""

df_size = 10000

def create_sample_dataframe(
    df_size: int,
    num_propulsion_classifications: int
) -> pd.DataFrame:
    """
    Create a sample DataFrame with random data.

    Given the size (=number of rows) of the DataFrame
    and the number of propulsion classifications, the function
    creates a DataFrame with random data of the form:

    | parameter | value | year | size | propulsion1 | propulsion2 | propulsion3 | propulsion4 |
    |-----------|-------|------|------|-------------|-------------|-------------|-------------|
    | eta       | 12.4  | 2020 | 100  | A           | B           | C           | D           |
    | gamma     | 7.5   | 2021 | 220  | A           | E           | X           | D           |

    The purpose of this dataframe is to test the memory footprint
    of the corresponding xarray.DataArray that can be created from it,
    using either the `df.to_xarray()` method
    or the `xr.Dataset.from_dataframe(df, sparse = True)` method.
    """
    df_size
    data = {
        "value": np.random.uniform(low = 0.0, high = 5.0, size = df_size),
        "parameter": np.random.randint(low = 0, high = 1000, size = df_size),
        "year": np.random.randint(low = 2000, high = 2050, size = df_size),
        "size": np.random.randint(low = 50, high = 350, size = df_size),
    }
    for i in range(1, int(num_propulsion_classifications) + 1):
        data[f"propulsion{i}"] = np.random.randint(low = 1, high = 30, size = df_size)

    df = pd.DataFrame(data)
    columns_for_index = list(df.columns)
    columns_for_index.remove("value")
    df.set_index(
        columns_for_index,
        inplace = True
    )
    return df


def measure_memory_xarray(df_size: int, num_propulsion_classifications: int) -> int:
    df = create_sample_dataframe(
        df_size = df_size,
        num_propulsion_classifications = num_propulsion_classifications
    )
    sarray: xr.DataArray = df.to_xarray()
    size_megabytes_sarray: int = sarray.nbytes * 1E-6
    return size_megabytes_sarray


def measure_memory_sparse_xarray(df_size: int, num_propulsion_classifications: int) -> int:
    df = create_sample_dataframe(
        df_size = df_size,
        num_propulsion_classifications = num_propulsion_classifications
    )
    sarray: xr.Dataset = xr.Dataset.from_dataframe(
        df,
        sparse = True
    )
    size_megabytes_sarray: int = sarray.nbytes * 1E-6
    return size_megabytes_sarray


def measure_memory_df(df_size: int, num_propulsion_classifications: int) -> int:
    df = create_sample_dataframe(
        df_size = df_size,
        num_propulsion_classifications = num_propulsion_classifications
    )
    size_megabytes_df: int = sys.getsizeof(df) * 1E-6
    return size_megabytes_df


df_memory_measured = pd.DataFrame(
    data = {
        "classifications": [1, 2], # Python kernel will crash above 2 (already 2GB memory!)
    }
)

df_memory_measured['memory_xarray'] = df_memory_measured.apply(
    lambda x: measure_memory_xarray(
        df_size = df_size,
        num_propulsion_classifications = x['classifications']
    ),
    axis = 1
)
df_memory_measured['memory_xarray_sparse'] = df_memory_measured.apply(
    lambda x: measure_memory_sparse_xarray(
        df_size = df_size,
        num_propulsion_classifications = x['classifications']
    ),
    axis = 1
)
df_memory_measured['memory_df'] = df_memory_measured.apply(
    lambda x: measure_memory_df(
        df_size = df_size,
        num_propulsion_classifications = x['classifications']
    ),
    axis = 1
)


# %%
import matplotlib.pyplot as plt
cm = 1/2.54 # for inches-cm conversion

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(9*cm, 6*cm), # A4=(210x297)mm,
)

ax.set_yscale('log')

ax.set_ylabel('Memory [MB])')
ax.set_xlabel('Propulsion Classifications')

ax.set_xticks([i for i in range(len(df_memory_measured))])
ax.set_xticklabels(list(df_memory_measured['classifications']))

ax.set_title('xr.DataArray/pd.DataFrame Memory Use')

ax.bar(
    x = [i-0.2 for i in range(0, len(df_memory_measured))],
    height = df_memory_measured['memory_xarray'],
    width = 0.4,
    color = 'red',
    label = 'DataArray'
)
ax.bar(
    x = [i for i in range(0, len(df_memory_measured))],
    height = df_memory_measured['memory_xarray_sparse'],
    width = 0.4,
    color = 'orange',
    label = 'DataArray (sparse)'
)
ax.bar(
    x = [i+0.2 for i in range(0, len(df_memory_measured))],
    height = df_memory_measured['memory_df'],
    width = 0.4,
    color = 'blue',
    label = 'DataFrame'
)

ax.legend()

file_path: pathlib.PosixPath = Path(__file__).resolve()
figure_name: str = str(file_path.stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)