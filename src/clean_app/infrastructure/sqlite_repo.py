import sqlite3

from clean_app.domain.entities.user import User
from clean_app.domain.repositories import UserRepository


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def get_all(self) -> list[User]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, surname, loginname, email FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [
            User(id=row[0], name=row[1], surname=row[2], loginname=row[3], email=row[4])
            for row in rows
        ]

    def get_by_id(self, user_id: int) -> User | None:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, surname, loginname, email FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return User(id=row[0], name=row[1], surname=row[2], loginname=row[3], email=row[4])
