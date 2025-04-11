import logging
import os
import sqlite3

from contextlib import contextmanager
from pathlib import Path


class ConnectionProvider:
    def __init__(self, db_path):
        self.db_path = Path(db_path)

    @contextmanager
    def connection(self, backfill=False):
        conn = sqlite3.connect(
            self.db_path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        try:
            if not backfill:
                conn.execute('PRAGMA foreign_keys = ON')
            yield conn
        finally:
            conn.close()


class DatabaseInitializer(ConnectionProvider):
    def __init__(self):
        data_path_prefix = os.environ.get("DATA_PATH_PREFIX", "./sql")
        self.db_path = Path(f"{data_path_prefix}/updates.db")
        super().__init__(self.db_path)

        self.schema_path = Path("sql/schema.sql")
        self.logger = logging.getLogger(__name__)

    def init_db(self) -> bool:
        """
        Initialize the database if it doesn't exist or if it's empty.
        Creates all tables and indexes defined in the schema file.
        """
        db_exists = self.db_path.exists()

        # Create the database directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with self.connection() as conn:
            cursor = conn.cursor()

            # Check if any tables exist
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)

            tables = cursor.fetchall()

            if not db_exists or not tables:
                self.logger.info(
                    "Initializing database at %s with schema from %s",
                    self.db_path,
                    self.schema_path
                )

                try:
                    with open(self.schema_path, 'r') as f:
                        schema = f.read()
                        conn.executescript(schema)
                    conn.commit()
                    self.logger.info("Database initialization completed successfully")
                except Exception as e:
                    self.logger.error("Failed to initialize database: %s", str(e))
                    raise

                return True

            self.logger.info("Database already exists and contains tables")
            return False
