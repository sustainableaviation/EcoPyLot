# %%
# data science
import pandas as pd
# system
import json
import pathlib
# debugging
import logging

# local imports
import ecopylot.utils as utils


def _load_json(json_input: str | pathlib.PurePath) -> dict:
    """
    Unpacks JSON data from a file or a string.

    The function parses JSON data using the json.loads() method for strings
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

    The function converts a dictionary representation of JSON data into a
    Pandas DataFrame, expanding JSON objects (=`parameter`/`metadata` pairs)
    into rows. The JSON data is expected to be of the form:

    .. code-block:: json

        {
            "123": {
                "parameter": "foo",
                "value": 11,
                "loc": 11,
                "minimum": 5,
                "maximum": 13,
                "uncertainty": 4,
                "metadata1": ["alpha", "beta"],
                "metadata2": "gamma"
            },
            "456": {
                "parameter": "bar",
                "value": 6,
                "loc": 6,
                "minimum": null,
                "maximum": null,
                "uncertainty": 1,
                "metadata1": "beta",
                "metadata2": ["gamma", "delta"]
            }
        }

    The function will return a DataFrame of the form:
    
    +--------------+-----------+-------+-----+------+------+-------------+-------------------+---------------------+-----+
    | UID (=index) | parameter | value | loc | min  | max  | uncertainty | metadata1         | metadata2           | ... |
    +==============+===========+=======+=====+======+======+=============+===================+=====================+=====+
    | 123          | foo       | 11    | 11  | 5    | 13   | 4           | ["alpha", "beta"] | "gamma"             | ... |
    +--------------+-----------+-------+-----+------+------+-------------+-------------------+---------------------+-----+
    | 456          | bar       | 6     | 6   | None | None | 1           | "beta"            | ["gamma", "delta"]  | ... |
    +--------------+-----------+-------+-----+------+------+-------------+-------------------+---------------------+-----+

    Parameters
    ----------
    json_data : dict
        A dictionary representation of the JSON data,
        as returned by the _load_json() method.


    Returns
    -------
    pandas.DataFrame
        A Pandas DataFrame containing the parsed JSON data.
    """

    if not isinstance(json_data, dict):
        raise ValueError("Parameters/Metadata are not of correct type (expected `dict`, got `{}`)".format(type(parameters)))
    
    df = pd.DataFrame.from_dict(json_data, orient="index")
    df = df.rename_axis('UID')

    logging.info(f"JSON data parsed to pd.DataFrame successfully (#entries: {len(df)}, size in memory: {sys.getsizeof(df)} bytes)")

    return df


def load_data_from_json(json_input: str | pathlib.PurePath) -> pd.DataFrame:
    """
    Loads data from a JSON file or string into a DataFrame.

    The function converts a string or file containing JSON data into a
    Pandas DataFrame, expanding JSON objects (=`parameter`/`metadata` pairs)
    into rows. The JSON data is expected to be of the form:

    .. code-block:: json

        {
            "123": {
                "parameter": "foo",
                "value": 11,
                "loc": 11,
                "minimum": 5,
                "maximum": 13,
                "uncertainty": 4,
                "metadata1": ["alpha", "beta"],
                "metadata2": "gamma"
            },
            "456": {
                "parameter": "bar",
                "value": 6,
                "loc": 6,
                "minimum": null,
                "maximum": null,
                "uncertainty": 1,
                "metadata1": "beta",
                "metadata2": ["gamma", "delta"]
            }
        }

    The function will return a DataFrame of the form:
    
    +--------------+-----------+-------+-----+------+------+-------------+-------------------+---------------------+-----+
    | UID (=index) | parameter | value | loc | min  | max  | uncertainty | metadata1         | metadata2           | ... |
    +==============+===========+=======+=====+======+======+=============+===================+=====================+=====+
    | 123          | foo       | 11    | 11  | 5    | 13   | 4           | ["alpha", "beta"] | "gamma"             | ... |
    +--------------+-----------+-------+-----+------+------+-------------+-------------------+---------------------+-----+
    | 456          | bar       | 6     | 6   | None | None | 1           | "beta"            | ["gamma", "delta"]  | ... |
    +--------------+-----------+-------+-----+------+------+-------------+-------------------+---------------------+-----+

    Parameters
    ----------
    json_input : str or pathlib.PurePath
        A JSON string or a path to a JSON file.

    Returns
    -------
    pandas.DataFrame
        A Pandas DataFrame containing the parsed JSON data.

    See Also
    --------
    _load_json : Unpacks JSON data from a file or a string.
    _parse_json : Parses JSON data into a Pandas DataFrame.
    """

    json_data = _load_json(json_input)
    df = _parse_json(json_data)

    return df