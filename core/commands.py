import click


@click.command()
@click.option('--test', prompt='', help='help')
def cli(**kwargs):
    print(kwargs)
