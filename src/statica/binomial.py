import click
from tabulate import tabulate
from scipy.stats import binom


def _option_n(name, required=True):
    def decorator(function):
        function = click.option(
            name, "-n", "--n", type=int, required=required, help="Number of trials"
        )(function)

        return function

    return decorator


def _option_p(name, required=True):
    def decorator(function):
        function = click.option(
            name,
            "-p",
            "--p",
            type=click.FloatRange(
                min=0, max=1, min_open=False, max_open=False, clamp=False
            ),
            required=required,
            help="Probability of a single success",
        )(function)

        return function

    return decorator


@click.group()
def binomial():
    pass


@click.command()
@_option_n(name="n")
@_option_p(name="p")
def pmf(n, p):
    probabilities = [[None, None]] * (n + 1)
    for k in range(0, n + 1):
        probabilities[k] = k, binom.pmf(k, n, p).item()
    output = tabulate(
        probabilities, headers=["k", "P(X = k)"], colalign=("right", "left")
    )
    click.echo(output)


binomial.add_command(pmf)
