import click

from src.dwetl.cli.oracle_to_hudi import oracle_to_hudi


@click.group()
@click.version_option(version='2.3.1')
@click.pass_context
def cli(ctx):
    pass

# export
cli.add_command(oracle_to_hudi, "oracle_to_hudi")