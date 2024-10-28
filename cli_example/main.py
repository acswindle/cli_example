import typer
import rich
from typing import Annotated
from functools import wraps
from time import sleep
from rich.progress import track
from rich.table import Table
from rich.console import Console

app = typer.Typer()

admin = {"username": "admin", "password": "password"}
active_users = ["jack", "jill", "jane", "john", "jamey"]

USERLIST_TYPE = Annotated[list[str], typer.Argument(help="List of users")]
VERBOSE_TYPE = Annotated[bool, typer.Option(help="Show vebose output")]
USERNAME_TYPE = Annotated[str, typer.Option(help="Your username", envvar="USERNAME")]
PASSWORD_TYPE = Annotated[
    str,
    typer.Option(help="Your password", prompt=True, hide_input=True, envvar="PASSWORD"),
]


def requires_credentials(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs["username"] != admin["username"]:
            rich.print("[bold red]:locked_with_key:Invalid Credentials[/bold red]")
            exit(1)
        if kwargs["password"] != admin["password"]:
            rich.print("[bold red]:locked_with_key:Invalid Credentials[/bold red]")
            exit(1)
        return func(*args, **kwargs)

    return wrapper


@app.command()
@requires_credentials
def add_users(
    users: USERLIST_TYPE,
    password: PASSWORD_TYPE,
    verbose: VERBOSE_TYPE = False,
    username: USERNAME_TYPE = "admin",
):
    """Add users to active user database"""
    for user in users:
        if verbose:
            print(f"User {user} added")
    print("Completed adding users")


@app.command()
@requires_credentials
def delete_users(
    users: USERLIST_TYPE,
    password: PASSWORD_TYPE,
    verbose: VERBOSE_TYPE = False,
    username: USERNAME_TYPE = "admin",
):
    """Delete users from active user database"""
    for user in users:
        if user not in active_users:
            rich.print(
                f"[bold yellow]:warning:Could not delete {user}. Not in active user database[/bold yellow]"
            )
        else:
            rich.print(f"[green]:white_check_mark:User {user} deleted[/green]")


@app.command()
def list_users(
    verbose: VERBOSE_TYPE = False,
):
    table = Table(title="Active Users")
    table.add_column("Username", justify="center", style="magenta")
    for user in track(active_users, description="Loading Users..."):
        sleep(1)
        table.add_row(user)
        if verbose:
            rich.print(f"User {user}")
    rich.print("Done loading users")
    console = Console()
    console.print(table)


if __name__ == "__main__":
    app()
