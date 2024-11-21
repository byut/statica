import click

from .binomial import *


# CLI entry point
@click.group()
def app():
    pass


app.add_command(binomial)

if __name__ == "__main__":
    app()
