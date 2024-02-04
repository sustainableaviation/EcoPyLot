# %%
# performance
import time
import timeit
# data science
import pandas as pd
import numpy as np
# Carculator
import carculator as carc
# EcoPylot
from ecopylot import inputoutput
from ecopylot import statistics


def carculator_data_import(iterations:int):
    cip = carc.CarInputParameters()
    cip.stochastic(iterations = int(iterations)) # force cast to integer
    dcts, array = carc.fill_xarray_from_input_parameters(cip)


def ecopylot_data_import(iterations:int):
    df = inputoutput.load_data_from_json(filep)
    statistics.generate_stochastic_dataframe(df = df, iterations = iterations)


def measure_function_time(
    stmt: str,
    setup: str,
    number: int = 1,
    repeat: int = 1,
) -> pd.DataFrame:
    """
    Measures the time it takes to run a function.

    Some more docstrings...
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

df_time_measured.plot.bar(
    x = "iterations",
    y = "time_carculator",
)