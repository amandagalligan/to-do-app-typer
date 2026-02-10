"""Module provides RP to-do database functionality"""

import configparser
from pathlib import Path
import json
from typing import Any, NamedTuple

from rptodo import DB_WRITE_ERROR, DB_READ_ERROR, SUCCESS, JSON_ERROR


class DBResponse(NamedTuple):
    """Datacontainer to send and receive data from database"""

    todo_list: list[
        dict[str, Any]
    ]  # represent list of todos to write and hold values you read from database
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        """
        Try to read the todo items from datbase/json file.
        if it fails return empty list and the ERROR
        If it succeeds return the list to caller
        """
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: list[dict[str, Any]]) -> DBResponse:
        """
        Try to write todo items to database/json file
        This method takes a list of to-do's of type list[dict[str, Any]]
        """
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
                return DBResponse(todo_list, SUCCESS)
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)


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
