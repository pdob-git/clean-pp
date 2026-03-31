from clean_app.application.export_data import ExportDataUseCase
from clean_app.application.get_users import GetUsersUseCase
from clean_app.domain.entities.user import User
from clean_app.domain.repositories import UserRepository


class MockUserRepository(UserRepository):
    def __init__(self, users: list[User]):
        self._users = users

    def get_all(self) -> list[User]:
        return self._users

    def get_by_id(self, user_id: int) -> User | None:
        for user in self._users:
            if user.id == user_id:
                return user
        return None


class TestGetUsersUseCase:
    def test_execute_returns_all_users(self):
        users = [
            User(1, "John", "Doe", "jdoe", "john@example.com"),
            User(2, "Jane", "Smith", "jsmith", "jane@example.com"),
        ]
        repo = MockUserRepository(users)
        use_case = GetUsersUseCase(repo)

        result = use_case.execute()

        assert len(result) == 2
        assert result[0].name == "John"

    def test_execute_returns_empty_list(self):
        repo = MockUserRepository([])
        use_case = GetUsersUseCase(repo)

        result = use_case.execute()

        assert result == []

    def test_execute_by_id_found(self):
        users = [User(1, "John", "Doe", "jdoe", "john@example.com")]
        repo = MockUserRepository(users)
        use_case = GetUsersUseCase(repo)

        result = use_case.execute_by_id(1)

        assert result is not None
        assert result.name == "John"

    def test_execute_by_id_not_found(self):
        users = [User(1, "John", "Doe", "jdoe", "john@example.com")]
        repo = MockUserRepository(users)
        use_case = GetUsersUseCase(repo)

        result = use_case.execute_by_id(999)

        assert result is None


class MockExporter:
    def __init__(self):
        self.exported_data = None

    def export(self, users, file_path):
        self.exported_data = (users, file_path)

    @property
    def extension(self):
        return ".mock"


class TestExportDataUseCase:
    def test_execute_calls_exporter(self):
        users = [
            User(1, "John", "Doe", "jdoe", "john@example.com"),
        ]
        exporter = MockExporter()
        use_case = ExportDataUseCase({"csv": exporter})

        use_case.execute(users, "output.csv", "csv")

        assert exporter.exported_data is not None
        assert len(exporter.exported_data[0]) == 1
        assert exporter.exported_data[1] == "output.csv"
