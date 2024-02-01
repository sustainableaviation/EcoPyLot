# %%
import timeit
import pandas as pd
import numpy as np
import time

import carculator as carc
import pandas as pd


def caculator_data_import(iterations:int):
    cip = carc.CarInputParameters()
    cip.stochastic(iterations = iterations)
    dcts, array = carc.fill_xarray_from_input_parameters(cip)

def measure_function_time(
    function: callable,
    number: int = 1,
    repeat: int = 1,
    iterations: int = 1000,
) -> pd.DataFrame:
    time_carculator_list: list =  timeit.repeat(
        stmt = f"caculator_data_import({iterations})",
        setup = "from __main__ import caculator_data_import",
        number = number,
        repeat = repeat,
        timer = time.perf_counter,
    )
    time_carculator: float = np.mean(time_carculator_list)
    return time_carculator


df_time = pd.DataFrame({'iterations': [1, 10, 1E2, 1E3, 1E4, 1E5]})

df_time = df_time.apply(lambda row: measure_function_time(calculator_data_import, iterations=row['iterations']), axis=1)
