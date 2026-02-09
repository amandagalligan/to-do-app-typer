"""This module provides the RP to-do CLI."""

from typing import Optional
import typer
from typing_extensions import Annotated

from rptodo import ERRORS, __app_name__, __version__

app = typer.Typer()

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
