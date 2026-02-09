import typer

app = typer.Typer()


@app.command()
def greet(name: str, age: int = 20):
    typer.echo(f"Hellow {name}, you are {age} years old ")


if __name__ == "__main__":
    app()
