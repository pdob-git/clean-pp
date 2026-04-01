import click
from clean_app.container import build_container, Container


@click.group()
@click.option("--db-path", default="users.db", help="Path to SQLite database")
@click.pass_context
def cli(ctx: click.Context, db_path: str) -> None:
    ctx.obj = build_container(db_path)


@cli.command()
@click.pass_context
def get_users(ctx: click.Context) -> None:
    container: Container = ctx.obj
    use_case = container.get_users
    users = use_case.execute()

    if not users:
        click.echo("No users found.")
        return

    click.echo(f"Found {len(users)} users:")
    for user in users:
        click.echo(
            f"  {user.id}: {user.name} {user.surname} "
            f"({user.loginname}) - {user.email}"
        )

@cli.command()
@click.pass_context
@click.option("--host", prompt=True)
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def login(ctx: click.Context, host: str, user: str, password: str) -> None:
    container: Container = ctx.obj
    container.login_use_case.execute(host, user, password)

@cli.command()
@click.pass_context
@click.option(
    "--format",
    "export_format",
    default="csv",
    type=click.Choice(["csv", "excel"]),
)
@click.option("--output", required=True)
def export(ctx: click.Context, export_format: str, output: str) -> None:
    container: Container = ctx.obj

    users = container.get_users.execute()

    if not users:
        click.echo("No users to export.")
        return

    container.export_use_case.execute(users, output, export_format)

    click.echo(f"Exported {len(users)} users to {output}")