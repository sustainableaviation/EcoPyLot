# %%
# data science
import pandas as pd
import numpy as np
# import stats_arrays as sa # for uncertainty distributions
# system
import json
import pathlib
# debugging
import logging
# project configuration
import configparser
import tomllib


# load project configuration file
config: dict = tomllib.load(open(pathlib.Path(__file__).parent/"configuration.toml", "rb"))

# %%
def _load_json(json_input: str | pathlib.PurePath) -> dict:
    """
    Unpacks JSON data from a file or a string.

    This method parses JSON data using the json.loads() method for strings
    and the json.load() method for files.
    It returns a dictionary representation of the JSON data, according to the
    `json.JSONDecoder conversion table <https://docs.python.org/3/library/json.html#encoders-and-decoders>`_.

    Parameters
    ----------
    json_input : str or pathlib.PurePath
        A JSON string or a path to a JSON file.

    Returns
    -------
    dict
        A dictionary representation of the JSON data.

    See Also
    --------
    json.load : Loads JSON data from a file.
    json.loads : Loads JSON data from a string.
    """

    if isinstance(json_input, pathlib.PurePath):
        try:
            with open(json_input) as file:
                json_data = json.load(file)
        except json.JSONDecodeError:
            raise TypeError(f"Error decoding JSON from file: {json_input}")
    elif isinstance(json_input, str):
        try:
            json_data = json.loads(json_input)
        except json.JSONDecodeError:
            raise TypeError(f"Error decoding JSON from string: {json_input}")
    else:
        logging.error("Input must be a string or a path to a JSON file.")
        raise TypeError("Input must be a string or a path to a JSON file.")

    logging.info(f"JSON data loaded successfully (#entries: {len(json_data)}, size in memory: {sys.getsizeof(json_data)} bytes)")

    return json_data


def _parse_json(json_data: dict) -> pd.DataFrame:
    """
    Parses JSON data into a Pandas DataFrame.

    This method converts a dictionary representation of JSON data into a
    Pandas DataFrame, expanding JSON objects (=parameter/metadata pairs)
    rows according to the logic:

    JSON input:

    {
        "123": {
            "parameter": "foo",
            "value": 11,
            "loc": 11,
            "min": 5,
            "max": 13,
            "uncertainty": 4,
            "metadata1": ["ε", "β"],
            "metadata2": "μ"
        },
        "456": {
            "parameter": "bar",
            "value": 6,
            "loc": 6,
            "min": None,
            "max": None,
            "uncertainty": 1,
            "metadata1": "β",
            "metadata2": ["μ", "θ"]
        }
    }

    Pandas DataFrame:
    
    | UID | parameter | value | loc | min  | max  | uncertainty | metadata1  | metadata2   | ... |
    |-----|-----------|-------|-----|------|------|-------------|------------|-------------|-----|
    | 123 | foo       | 11    | 11  | 5    | 13   | 4           | ["ε", "β"] | "β"         | ... |
    | 456 | bar       | 6     | 6   | None | None | 1           | "μ"        | ["μ", "θ"]  | ... |


    Parameters
    ----------
    json_data : dict
        A dictionary representation of the JSON data,
        as returned by the _load_json() method.


    Returns
    -------
    pandas.DataFrame
        A Pandas DataFrame containing the parsed JSON data.

    See Also
    --------
    `stats_arrays uncertainty types <https://stats-arrays.readthedocs.io/en/latest/index.html?highlight=stats_arrays%20distributions#mapping-parameter-array-columns-to-uncertainty-distributions>`_.
    """

    if not isinstance(json_data, dict):
        raise ValueError("Parameters/Metadata are not of correct type (expected `dict`, got `{}`)".format(type(parameters)))
    
    
