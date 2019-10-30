import sqlite3


class UseDatabase:
    def __init__(self, config: str) -> None:
        self.config = config

    def __enter__(self) -> 'cursor':
        self.conn = sqlite3.connect(self.config)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
