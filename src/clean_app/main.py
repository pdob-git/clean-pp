import click

from clean_app.application.export_data import ExportDataUseCase
from clean_app.application.get_users import GetUsersUseCase
from clean_app.infrastructure.exporters.csv_exporter import CsvExporter
from clean_app.infrastructure.exporters.excel_exporter import ExcelExporter
from clean_app.infrastructure.sqlite_repo import SQLiteUserRepository
from clean_app.presentation.cli.commands import cli


def build_cli() -> click.Group:
    repo = SQLiteUserRepository("users.db")

    get_users = GetUsersUseCase(repo)

    exporters = {
        "csv": CsvExporter(),
        "excel": ExcelExporter(),
    }
    export_use_case = ExportDataUseCase(exporters)

    cli.obj = {  # type: ignore[attr-defined]
        "get_users": get_users,
        "export_use_case": export_use_case,
    }
    return cli


def main() -> None:
    app = build_cli()
    app()


if __name__ == "__main__":
    main()
