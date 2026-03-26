from clean_app.domain.entities.user import User
from clean_app.domain.repositories import UserRepository


class GetUsersUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self) -> list[User]:
        return self._repository.get_all()

    def execute_by_id(self, user_id: int) -> User | None:
        return self._repository.get_by_id(user_id)
