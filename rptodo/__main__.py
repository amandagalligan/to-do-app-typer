"""RP To-Do entry point script."""

# rptodo/__main__.py
from rptodo import __app_name__, cli


# Define the main entry point for the rptodo command-line application
# It calls the app object, which is a typer.Typer instance
# defined inside the cli.py module
def main():
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
