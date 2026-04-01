import sqlite3


def init_database(db_path: str = "users2.db") -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            loginname TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL
        )
    """)

    sample_users = [
        ("John", "Doe", "jdoe", "john.doe@example.com"),
        ("Jane", "Smith", "jsmith", "jane.smith@example.com"),
        ("Bob", "Johnson", "bjohnson", "bob.johnson@example.com"),
        ("Alice", "Williams", "awilliams", "alice.williams@example.com"),
        ("Charlie", "Brown", "cbrown", "charlie.brown@example.com"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO users (name, surname, loginname, email) VALUES (?, ?, ?, ?)",
        sample_users
    )

    conn.commit()
    conn.close()
    print(f"Database '{db_path}' created with {len(sample_users)} sample users.")


if __name__ == "__main__":
    init_database()