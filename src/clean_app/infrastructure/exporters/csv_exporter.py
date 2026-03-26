import csv

from clean_app.domain.entities.user import User
from clean_app.infrastructure.exporters.base import DataExporter


class CsvExporter(DataExporter):
    @property
    def extension(self) -> str:
        return ".csv"

    def export(self, users: list[User], file_path: str) -> None:
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "surname", "loginname", "email"])
            for user in users:
                writer.writerow([
                    user.id,
                    user.name,
                    user.surname,
                    user.loginname,
                    user.email
                ])
