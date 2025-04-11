import sys
import uuid

from base import ScriptBase
from db import DatabaseInitializer


def _latest(conn, website):
    cursor = conn.execute("""
        SELECT id, contents
        FROM website_updates 
        WHERE website = ?
        ORDER BY fetch_time DESC 
        LIMIT 1
    """, (website,))
    row = cursor.fetchone()
    return (row[0], row[1]) if row else (None, None)


class Recorder(ScriptBase, DatabaseInitializer):
    def __init__(self, website, fetch_time):
        super().__init__(website)
        DatabaseInitializer.__init__(self)
        self.fetch_time = fetch_time

    def run(self):
        self.init_db()

        with self.connection() as conn:
            previous_id, previous_content = _latest(conn, self.website)
            new_id = str(uuid.uuid4())
            content = sys.stdin.read()

            conn.execute(
                "INSERT INTO website_updates (id, website, fetch_time, contents, previous_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (new_id, self.website, self.fetch_time, content, previous_id)
            )
            conn.commit()

            if previous_content:
                print(previous_content)


if __name__ == "__main__":
    Recorder(sys.argv[1], sys.argv[2]).main()
