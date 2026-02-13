"""Module provides RP to-do config functionality"""

import configparser
from pathlib import Path

from rptodo import (
    DB_WRITE_ERROR,
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
)

# Go two parent directories up to project root directory
CONFIG_DATA_PATH = Path(__file__).parent.parent
CONFIG_FILE_PATH = CONFIG_DATA_PATH / "config.ini"


# Define private helper function to try and create the config directory path
# Then try to create the config file config.ini within this path
# This function returns a type annotated "int" operation response code
def _init_config_file() -> int:
    try:
        CONFIG_DATA_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR

    return SUCCESS


# Another private helper function to create and initialise the database
# This will creates a dictionary with string value db_path
# representing path to JSON file and write this to config.ini
def _create_database(db_path: str) -> int:
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}

    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR

    return SUCCESS


def init_app(db_path: str) -> int:
    """Initializes the application config file"""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    database_code = _create_database(db_path)
    if database_code != SUCCESS:
        return database_code

    return SUCCESS
