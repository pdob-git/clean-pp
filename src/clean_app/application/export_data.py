from clean_app.domain.entities.user import User
from clean_app.infrastructure.exporters.base import DataExporter


class ExportDataUseCase:
    def __init__(self, exporter: DataExporter) -> None:
        self._exporter = exporter

    def execute(self, users: list[User], file_path: str) -> None:
        self._exporter.export(users, file_path)
