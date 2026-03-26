from abc import ABC, abstractmethod

from clean_app.domain.entities.user import User


class DataExporter(ABC):
    @abstractmethod
    def export(self, users: list[User], file_path: str) -> None:
        pass

    @property
    @abstractmethod
    def extension(self) -> str:
        pass
