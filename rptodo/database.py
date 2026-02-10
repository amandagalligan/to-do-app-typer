"""Module provides RP to-do database functionality"""

import configparser
from pathlib import Path

from rptodo import DB_WRITE_ERROR, SUCCESS

# Define default path to database config file if user doesn't provide one
DEFAULT_DB_FILE_PATH = Path(__file__).parent.parent.joinpath(".default_todo.json")


def get_database_path(config_file: Path) -> Path:
    """returns the current path to todo database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)

    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Creates the to-do database and initialize with empty do-to list"""
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
