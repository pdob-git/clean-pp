import pandas as pd

from clean_app.domain.entities.user import User
from clean_app.domain.exporters import DataExporter


class ExcelExporter(DataExporter):
    @property
    def extension(self) -> str:
        return ".xlsx"

    def export(self, users: list[User], file_path: str) -> None:
        data = {
            "id": [u.id for u in users],
            "name": [u.name for u in users],
            "surname": [u.surname for u in users],
            "loginname": [u.loginname for u in users],
            "email": [u.email for u in users],
        }
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False, engine="openpyxl")
