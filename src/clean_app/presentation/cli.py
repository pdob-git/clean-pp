import click

from clean_app.application.get_users import GetUsersUseCase
from clean_app.infrastructure.exporters import get_exporter
from clean_app.infrastructure.sqlite_repo import SQLiteUserRepository


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--host", prompt=True, help="Database host")
@click.option("--user", prompt=True, help="Database user")
@click.option("--password", prompt=True, hide_input=True, help="Database password")
@click.option("--db-path", default="users.db", help="Path to SQLite database")
def login(host: str, user: str, password: str, db_path: str) -> None:
    click.echo(f"Credentials stored for user: {user}")
    click.echo(f"Database path: {db_path}")


@cli.command()
@click.option("--db-path", default="users.db", help="Path to SQLite database")
def get_users(db_path: str) -> None:
    repo = SQLiteUserRepository(db_path)
    use_case = GetUsersUseCase(repo)
    users = use_case.execute()

    if not users:
        click.echo("No users found.")
        return

    click.echo(f"Found {len(users)} users:")
    for user in users:
        click.echo(f"  {user.id}: {user.name} {user.surname} ({user.loginname}) - {user.email}")


@cli.command()
@click.option("--db-path", default="users.db", help="Path to SQLite database")
@click.option(
    "--format",
    "export_format",
    default="csv",
    type=click.Choice(["csv", "excel"]),
    help="Export format"
)
@click.option("--output", required=True, help="Output file path")
def export(db_path: str, export_format: str, output: str) -> None:
    repo = SQLiteUserRepository(db_path)
    get_use_case = GetUsersUseCase(repo)
    users = get_use_case.execute()

    if not users:
        click.echo("No users to export.")
        return

    exporter = get_exporter(export_format)

    from clean_app.application.export_data import ExportDataUseCase
    export_use_case = ExportDataUseCase(exporter)
    export_use_case.execute(users, output)

    click.echo(f"Exported {len(users)} users to {output}")


if __name__ == "__main__":
    cli()
