import json
import pandas as pd
    
class JSONToDataFrameConverter:
    """
    A class to convert JSON data into a Pandas DataFrame.

    This class takes JSON input, either as a raw string or a path to a JSON file,
    and converts it into a Pandas DataFrame. The JSON structure is expected to 
    contain nested data, with one of the fields as a list that needs to be expanded
    into multiple rows in the DataFrame. Each key in the JSON object is considered a 
    unique identifier (UID) for the rows.

    Methods
    -------
    _load_json(json_input):
        Loads JSON data from a file or a string.

    create_dataframe():
        Processes the JSON data and converts it into a Pandas DataFrame, expanding
        lists into multiple rows and including other attributes in each row.

    Parameters
    ----------
    json_input : str
        A JSON string or a path to a JSON file containing the data to be converted.

    Attributes
    ----------
    json_data : dict
        The JSON data loaded into a Python dictionary.
    """

    def __init__(self, json_input):
        """
        Initializes the JSONToDataFrameConverter with JSON input.

        Parameters
        ----------
        json_input : str
            A JSON string or a path to a JSON file to be loaded.
        """
        self.json_data = self._load_json(json_input)

    def _load_json(self, json_input):
        """
        Loads JSON data from a file or a string.

        This method parses the JSON data and converts it into a Python dictionary.

        Parameters
        ----------
        json_input : str
            A JSON string or a path to a JSON file.

        Returns
        -------
        dict
            A dictionary representation of the JSON data.

        Raises
        ------
        FileNotFoundError
            If the json_input is a file path and the file does not exist.
        json.JSONDecodeError
            If the json_input is not a valid JSON string.
        """
        if json_input.endswith('.json'):
            with open(json_input) as file:
                data = json.load(file)
        else:
            data = json.loads(json_input)
        return data

    def create_dataframe(self):
        """
        Creates and returns a Pandas DataFrame from the loaded JSON data.

        This method processes the JSON data, expanding lists into multiple rows
        and incorporating other attributes in each row. The resulting DataFrame
        has one row for each item in the 'sizes' list of the JSON data, with other
        properties duplicated across these rows.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the processed data from the JSON input.
        """
        frames = []
        for uid, values in self.json_data.items():
            for size in values['sizes']:
                row = values.copy()
                row['sizes'] = size
                row['UID'] = uid
                frames.append(row)

        df = pd.DataFrame(frames)
        return df
