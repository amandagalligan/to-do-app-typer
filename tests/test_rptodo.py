"""Unit tests for the rptodo CLI application."""

from typer.testing import CliRunner

from rptodo import __app_name__, __version__
from rptodo.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v {__version__}" in result.stdout
