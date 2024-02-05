# %%
# performance
import time
import timeit
# io
import sys
import pathlib
from pathlib import Path
# data science
import pandas as pd
import numpy as np
# Carculator
import carculator as carc
# EcoPylot
ecopylot_root: pathlib.PosixPath =  Path(__file__).resolve().parents[2]
sys.path.append(str(ecopylot_root / 'ecopylot'))
import inout
import stats


def carculator_data_import(iterations:int) -> None:
    """
    Runs the Carculator data import and statistics functions.
    """
    cip = carc.CarInputParameters()
    cip.stochastic(iterations = int(iterations)) # force cast to integer to avoid errors
    dcts, array = carc.fill_xarray_from_input_parameters(cip)


def ecopylot_data_import(iterations:int) -> None:
    """
    Runs the EcoPylot data import and statistics functions.
    """
    filep = Path('/Users/michaelweinold/github/carculator/carculator/data/default_parameters.json')
    df = inout.load_data_from_json(filep)
    stats.generate_stochastic_dataframe(df = df, iterations = iterations)


def measure_function_time(
    stmt: str,
    setup: str,
    number: int = 1,
    repeat: int = 1,
) -> pd.DataFrame:
    """
    Measures the time it takes to run a function.

    See Also
    --------
    The Python ` `timeit.repeat` <https://docs.python.org/3/library/timeit.html#timeit.repeat>`_.
    """
    time_carculator_list: list =  timeit.repeat(
        stmt = stmt,
        setup = setup,
        number = number,
        repeat = repeat,
        timer = time.perf_counter,
    )
    time_carculator: float = np.mean(time_carculator_list)
    return time_carculator


df_time_measured = pd.DataFrame(
    data = {
        "iterations": [1E0, 1E1, 1E2, 1E3, 1E4], # carculator will crash above 1E4 iterations
    }
)
df_time_measured['iterations'] = df_time_measured['iterations'].astype(int)

df_time_measured['time_carculator'] = df_time_measured.apply(
    lambda x: measure_function_time(
        stmt = f"carculator_data_import({x['iterations']})",
        setup = "from __main__ import carculator_data_import",
        number = 1, 
        repeat = 1,
    ),
    axis = 1
)
df_time_measured['time_ecopylot'] = df_time_measured.apply(
    lambda x: measure_function_time(
        stmt = f"ecopylot_data_import({x['iterations']})",
        setup = "from __main__ import ecopylot_data_import",
        number = 1, 
        repeat = 1,
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

ax.set_ylabel('Runtime [s]\n MBP(Apple M1 Max, 2021)')
ax.set_xlabel('Iterations')

ax.set_xticks([i for i in range(len(df_time_measured))])
ax.set_xticklabels(list(df_time_measured['iterations']))

ax.set_title('Data Load from JSON')

ax.bar(
    x = [i-0.2 for i in range(0, len(df_time_measured))],
    height = df_time_measured['time_carculator'],
    width = 0.5,
    color = 'orange',
    label = 'Carculator'
)
ax.bar(
    x = [i+0.2 for i in range(0, len(df_time_measured))],
    height = df_time_measured['time_ecopylot'],
    width = 0.5,
    color = 'blue',
    label = 'EcoPylot'
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