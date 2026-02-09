import typer

app = typer.Typer()


@app.command()
def greet(name: str, age: int = 20):
    typer.echo(f"Hellow {name}, you are {age} years old ")


@app.command()
def goodbye(name: str):
    typer.echo(f"Goodbye, {name}")


if __name__ == "__main__":
    app()

"""
python main.py --help    
                                                                                                                            
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                 
                                                                                                                            
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                  │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.           │
│ --help                        Show this message and exit.                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ greet                                                                                                                    │
│ goodbye                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

python main.py goodbye joe
Goodbye, joe
"""
