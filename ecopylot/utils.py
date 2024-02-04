# project configuration
import tomllib
import pathlib


def load_project_configuration() -> dict:
    """
    Loads the project configuration file.

    This method loads the project configuration file,
    which is located at the root level of the project.
    It returns a dictionary representation of the configuration file.

    Raises
    ------
    FileNotFoundError: If the configuration file is not found.
    ValueError: If the configuration file is malformatted.
    """
    
    path_config_file: pathlib.Path = pathlib.Path(__file__).parent / "configuration.toml"
    
    if not path_config_file.exists():
        raise FileNotFoundError(f"Configuration file '{path_config_file}' not found.")
    try:
        config_file = tomllib.load(open(path_config_file, "rb"))
    except tomllib.TOMLDecodeError as exception:
        raise ValueError(f"Malformatted configuration file: {exception}")

    return config_file