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