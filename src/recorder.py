import sys

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
    def __init__(self, website, update_id, content):
        super().__init__(website)
        DatabaseInitializer.__init__(self)
        self.update_id = update_id
        self.content = content

    def run(self):
        self.init_db()

        with self.connection() as conn:
            previous_id, previous_content = _latest(conn, self.website)

            conn.execute(
                "INSERT INTO website_updates (id, website, fetch_time, contents, previous_id) "
                "VALUES (?, ?, datetime(), ?, ?)",
                (self.update_id, self.website, self.content, previous_id)
            )
            conn.commit()

            return previous_content


if __name__ == "__main__":
    print(Recorder(sys.argv[1], sys.argv[2], sys.argv[3]).main())
