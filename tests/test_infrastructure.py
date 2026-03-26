import os
import tempfile

import pytest

from clean_app.domain.entities.user import User
from clean_app.infrastructure.exporters import CsvExporter, ExcelExporter
from clean_app.infrastructure.sqlite_repo import SQLiteUserRepository


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    import sqlite3
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE users ("
        "id INTEGER PRIMARY KEY, "
        "name TEXT, "
        "surname TEXT, "
        "loginname TEXT UNIQUE, "
        "email TEXT)"
    )
    conn.commit()
    conn.close()
    yield path
    os.unlink(path)


@pytest.fixture
def sample_users():
    return [
        User(1, "John", "Doe", "jdoe", "john@example.com"),
        User(2, "Jane", "Smith", "jsmith", "jane@example.com"),
    ]


class TestUserEntity:
    def test_user_creation(self):
        user = User(1, "John", "Doe", "jdoe", "john@example.com")
        assert user.id == 1
        assert user.name == "John"
        assert user.surname == "Doe"
        assert user.loginname == "jdoe"
        assert user.email == "john@example.com"


class TestSQLiteUserRepository:
    def test_get_all_empty(self, temp_db):
        repo = SQLiteUserRepository(temp_db)
        users = repo.get_all()
        assert users == []

    def test_get_all_with_data(self, temp_db):
        import sqlite3
        conn = sqlite3.connect(temp_db)
        conn.execute("INSERT INTO users VALUES (1, 'John', 'Doe', 'jdoe', 'john@example.com')")
        conn.commit()
        conn.close()

        repo = SQLiteUserRepository(temp_db)
        users = repo.get_all()

        assert len(users) == 1
        assert users[0].name == "John"

    def test_get_by_id_found(self, temp_db):
        import sqlite3
        conn = sqlite3.connect(temp_db)
        conn.execute("INSERT INTO users VALUES (1, 'John', 'Doe', 'jdoe', 'john@example.com')")
        conn.commit()
        conn.close()

        repo = SQLiteUserRepository(temp_db)
        user = repo.get_by_id(1)

        assert user is not None
        assert user.name == "John"

    def test_get_by_id_not_found(self, temp_db):
        repo = SQLiteUserRepository(temp_db)
        user = repo.get_by_id(999)
        assert user is None


class TestCsvExporter:
    def test_export_creates_file(self, temp_db, sample_users):
        import tempfile
        output_path = tempfile.mktemp(suffix=".csv")

        exporter = CsvExporter()
        exporter.export(sample_users, output_path)

        assert os.path.exists(output_path)
        with open(output_path) as f:
            content = f.read()
            assert "John" in content
            assert "Jane" in content

        os.unlink(output_path)


class TestExcelExporter:
    def test_export_creates_file(self, temp_db, sample_users):
        import tempfile
        output_path = tempfile.mktemp(suffix=".xlsx")

        exporter = ExcelExporter()
        exporter.export(sample_users, output_path)

        assert os.path.exists(output_path)
        os.unlink(output_path)
