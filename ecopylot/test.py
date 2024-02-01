import timeit
import importing
import stats

from pathlib import Path

filep = Path('/Users/michaelweinold/github/carculator/carculator/data/default_parameters.json')

df = importing.load_data_from_json(filep)

stats.generate_stochastic_dataframe(df=df, iterations=1000)