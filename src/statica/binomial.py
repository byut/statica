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


@click.command()
@_option_n(name="n")
@_option_p(name="p")
@click.option("operator", "--lt", flag_value="lt")
@click.option("operator", "--gt", flag_value="gt")
@click.option("operator", "--leq", flag_value="leq", default=True)
@click.option("operator", "--geq", flag_value="geq")
def cdf(n, p, operator):
    def leq(k, n, p):
        return binom.cdf(k, n, p)

    def lt(k, n, p):
        return leq(k - 1, n, p)

    def gt(k, n, p):
        return 1 - leq(k, n, p)

    def geq(k, n, p):
        return 1 - lt(k, n, p)

    probabilities = [[None, None]] * (n + 1)
    function = None
    signature = None

    match operator:
        case "lt":
            function = lt
            signature = "P(X < k)"
        case "gt":
            function = gt
            signature = "P(X > k)"
        case "leq":
            function = leq
            signature = "P(X <= k)"
        case "geq":
            function = geq
            signature = "P(X >= k)"

    for k in range(0, n + 1):
        probabilities[k] = k, function(k, n, p).item()

    output = tabulate(
        probabilities, headers=["k", signature], colalign=("right", "left")
    )
    click.echo(output)


binomial.add_command(pmf)
binomial.add_command(cdf)
