import click


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
@click.pass_context
@click.option("--db-path", default="users.db", help="Path to SQLite database")
def get_users(ctx: click.Context, db_path: str) -> None:
    use_case = ctx.obj["get_users"]
    users = use_case.execute()

    if not users:
        click.echo("No users found.")
        return

    click.echo(f"Found {len(users)} users:")
    for user in users:
        click.echo(f"  {user.id}: {user.name} {user.surname} ({user.loginname}) - {user.email}")


@cli.command()
@click.pass_context
@click.option("--db-path", default="users.db", help="Path to SQLite database")
@click.option(
    "--format",
    "export_format",
    default="csv",
    type=click.Choice(["csv", "excel"]),
    help="Export format",
)
@click.option("--output", required=True, help="Output file path")
def export(ctx: click.Context, db_path: str, export_format: str, output: str) -> None:
    get_use_case = ctx.obj["get_users"]
    users = get_use_case.execute()

    if not users:
        click.echo("No users to export.")
        return

    export_use_case = ctx.obj["export_use_case"]
    export_use_case.execute(users, output, export_format)

    click.echo(f"Exported {len(users)} users to {output}")
