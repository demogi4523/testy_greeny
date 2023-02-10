import asyncio

import typer

from script import run

cli = typer.Typer()

@cli.callback(invoke_without_command=True)
def fill_db() -> None:
    asyncio.run(run())


@cli.command()
async def migate() -> None:
    pass


@cli.command()
async def test() -> None:
    pass


if __name__ == "__main__":
    # FIXME: module cli not working
    cli()
