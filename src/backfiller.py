import json
import logging
import sys

import boto3

from base import ScriptBase
from db import DatabaseInitializer


class Backfiller(ScriptBase, DatabaseInitializer):
    def __init__(self, table_name):
        super().__init__()
        DatabaseInitializer.__init__(self)
        self.table_name = table_name

    def run(self):
        if not self.init_db():
            raise Exception("database already exists and has tables, won't try backfilling it")

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.table_name)
        items = table.scan()['Items']

        with self.connection(backfill=True) as conn:
            for item in items:
                id, previous, fetch_time = item['id'], item.get('previous'), item.get('fetch_time')
                website, uuid = id.split(':')
                previous_uuid = previous.split(':')[1] if previous else None

                content = item.get('contents')
                content = list(content) if isinstance(content, set) else content

                if uuid == "LATEST":
                    continue

                conn.execute(
                    "INSERT INTO website_updates (id, website, fetch_time, contents, previous_id) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (uuid, website, fetch_time, json.dumps(content), previous_uuid)
                )

            conn.commit()

        logging.info(f"Backfilled {len(items)} records from DynamoDB to local DB")


if __name__ == "__main__":
    Backfiller(sys.argv[1]).main()
