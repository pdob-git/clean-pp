from dataclasses import dataclass

from clean_app.application.export_data import ExportDataUseCase
from clean_app.application.get_users import GetUsersUseCase
from clean_app.infrastructure.sqlite_repo import SQLiteUserRepository
from clean_app.infrastructure.exporters.csv_exporter import CsvExporter
from clean_app.infrastructure.exporters.excel_exporter import ExcelExporter

from clean_app.application.login import LoginUseCase

@dataclass
class Container:
    get_users: GetUsersUseCase
    export_use_case: ExportDataUseCase
    login_use_case: LoginUseCase


def build_container(db_path: str) -> Container:
    repo = SQLiteUserRepository(db_path)

    get_users = GetUsersUseCase(repo)

    exporters = {
        "csv": CsvExporter(),
        "excel": ExcelExporter(),
    }
    export_use_case = ExportDataUseCase(exporters)

    login_use_case = LoginUseCase()

    return Container(
        get_users=get_users,
        export_use_case=export_use_case,
        login_use_case=login_use_case,
    )