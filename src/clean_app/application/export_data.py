from clean_app.domain.entities.user import User
from clean_app.domain.exporters import DataExporter


class ExportDataUseCase:
    def __init__(self, exporters: dict[str, DataExporter]) -> None:
        self._exporters = exporters

    def execute(self, users: list[User], file_path: str, format_type: str) -> None:
        exporter = self._exporters.get(format_type.lower())
        if exporter is None:
            supported = ", ".join(self._exporters.keys())
            raise ValueError(f"Unsupported format: {format_type}. Supported: {supported}")
        exporter.export(users, file_path)
