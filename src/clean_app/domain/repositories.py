from abc import ABC, abstractmethod

from clean_app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass
