"""This module provides the RP to-do CLI."""

from pathlib import Path
from typing import Annotated

import typer

from rptodo import ERRORS, __app_name__, __version__, config, database, rptodo

app = typer.Typer()


@app.command()
def init(
    db_path: Annotated[
        str,
        typer.Option(
            "--db-path",
            "-db",
            prompt="The to-do database location?",
        ),
    ] = str(database.DEFAULT_DB_FILE_PATH),
) -> None:
    """Initializes the to-do datbase"""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do database is {db_path}", fg=typer.colors.GREEN)


# Access the ToDoer class from our cli application with this helper function
# This function will instanciate an instace of the rptodo.ToDoer
def get_todoer() -> rptodo.ToDoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'config file not found. Please run "rptodo init', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists():
        return rptodo.ToDoer(db_path)
    else:
        typer.secho('Database not found. Please run "rptodo init', fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command()
def add(
    description: Annotated[
        list[str], typer.Argument(..., help="The to-do item description")
    ],
    priority: Annotated[
        int,
        typer.Option(
            "---priority", "-p", min=1, max=3, help="The to-do item priority value"
        ),
    ] = 2,
) -> None:
    """Add new to-do to the database"""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding the error code failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f""" to-do: "{todo['Description']} was added"""
            f""" with priority: "{priority}""",
            fg=typer.colors.GREEN,
        )


@app.command(name="list")
def list_all() -> None:
    """List all to-do"""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho("There are no to-do items in the database", fg=typer.colors.RED)
        raise typer.Exit()
    typer.secho("\nTo-Do list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = " ".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    # Loops through each todo item in todo_list. enumerate(..., 1)
    # assigns a sequential number to id, starting from 1.
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done = todo.values()

        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 2) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 1) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )

        typer.secho("-" * len(headers) + "", fg=typer.colors.BLUE)


@app.command(name="complete")
def set_done(
    todo_id: Annotated[int, typer.Argument(..., help="The to-do ID to update")],
) -> None:
    """Complete to-do by setting is done using to-do ID"""
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(
            f'Completing to-do #"{todo_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f""" to-do #{todo_id} "{todo["Description"]}" completed!""",
            fg=typer.colors.GREEN,
        )


# typer.echo(...): If the flag was used, it prints the application's
# name and version to the terminal (e.g., "rptodo v 0.1.0").
# In short, this is the function that makes a --version option work.
def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v {__version__}")
        raise typer.Exit()


# @app.callback()  defines a “root-level” function for the CLI app:
# Lets you define global CLI parameters (options/arguments) that apply
# before all subcommands
@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            "-v",
            help="Shows the application version",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """The main entry point for the to-do application"""
    return
