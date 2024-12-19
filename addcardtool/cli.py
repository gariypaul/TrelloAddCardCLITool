import typer
import subprocess
from PyInquirer import prompt, print_json, Separator
from rich import print as rprint
from typing import Optional
from addcardtool import __app_name__, __version__

app = typer.Typer()


def version_callback(value: bool):
    if value:
        rprint(f"{__app_name__} version: {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the applications version then exit application",
        callback=version_callback,
        is_eager=True,
    )
) -> None:
    pass
