"""Module provides the RP to-do model controller."""

from typing import Any, NamedTuple
from pathlib import Path
from rptodo.database import DatabaseHandler
from rptodo import DB_READ_ERROR

# The todo data data model will be represented as follows:
# to = {
#   "Description": Text,
#   "Priority": Interger,
#   "Done": Boolean
#  }


class CurrentToDo(NamedTuple):
    """Python subclass of NamedTuple that holds todo dictionary and error code.
    This acts like a container where we couple the status report with each attempt to add item to the todo list
    """

    todo: dict[str, Any]
    error: int


# Class composition where we make the DatabaseHandler class part of the
# ToDoer class or has relationship with this class.
class ToDoer:
    """Utility class for interacting with the database"""

    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: list[str], priority: int = 2) -> CurrentToDo:
        """Add a new to-do to the database."""
        # As it'll be received as a list we need to join. In addition we can check if it ends with . and if
        # not append a . to end.
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        # Read all the items in the file , append a new to-do item
        # write the new updated list back into the file
        # Items returned will be instance of CurrenttoDo containing list of to-do if any and error
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentToDo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        # Return the container which holds the todo list and the error code
        return CurrentToDo(todo, write.error)
