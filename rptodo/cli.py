"""This module provides the RP to-do CLI."""

from typing import Optional
import typer
from pathlib import Path
from typing_extensions import Annotated

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
        db_path = database.get_database_path(config.CONFIG_DATA_PATH)
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
        Optional[bool],
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
