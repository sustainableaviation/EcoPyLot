# data science
import pandas as pd
import json
# system
import pathlib
# debugging
import logging


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
    Pandas DataFrame, expanding lists into multiple rows and including other
    attributes in each row.

    Parameters
    ----------
    json_data : dict
        A dictionary representation of the JSON data, as returned by the
        _load_json() method.

    Returns
    -------
    pandas.DataFrame
        A Pandas DataFrame containing the parsed JSON data.
    """
