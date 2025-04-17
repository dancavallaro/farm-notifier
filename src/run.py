#!/usr/bin/env python3
import io
import json
import logging
import os
import sys
import uuid

import boto3

from base import ScriptBase
from fetcher import Fetcher
from parser import Parser
from recorder import Recorder
from differ import Differ


FROM_ADDRESS = "Farm Updates <farm-notifier@cavnet.cloud>"
TO_ADDRESSES = ["dan.t.cavallaro+produce@gmail.com"]

MINIO_S3_ARGS = {
    "endpoint_url": os.getenv("S3_ENDPOINT_URL"),
    "aws_access_key_id": os.getenv("S3_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("S3_SECRET_ACCESS_KEY"),
}


class Runner(ScriptBase):
    def __init__(self, website):
        super().__init__(website)

    def run(self):
        update_id = str(uuid.uuid4())
        logging.info(f"Processing today's update for {self.website} ({update_id=})")

        # Retrieve website source
        html_source = Fetcher(self.website).run()

        # Store the source in S3
        source_bucket_name = os.getenv("SOURCE_BUCKET_NAME")
        if source_bucket_name is not None:
            key = f"{self.website}/{update_id}"
            logging.info(f"Writing page source to {key=} in {source_bucket_name=}")

            source_bucket = boto3.resource("s3", **MINIO_S3_ARGS).Bucket(source_bucket_name)
            source_bucket.put_object(Key=key, Body=html_source)

        # Parse the source to find today's update
        latest = Parser(self.website, io.StringIO(html_source)).run()

        # Store update in DB and get the previous update
        previous = Recorder(self.website, update_id, latest).run()

        # Diff latest and previous updates
        diffed = Differ(previous, latest).run()

        # Send summary email
        email_template_name = os.getenv("EMAIL_TEMPLATE_NAME")
        if email_template_name is not None:
            logging.info(f"Sending email for latest update for {self.website=}: {diffed}")
            send_email(email_template_name, self.website, diffed)
        else :
            logging.info(f"Latest update for {self.website=}: {diffed}")


def send_email(email_template_name, website, update):
    ses = boto3.client("sesv2")
    resp = ses.send_email(
        FromEmailAddress=FROM_ADDRESS,
        Destination={
            "ToAddresses": TO_ADDRESSES,
        },
        Content={
            "Template": {
                "TemplateName": email_template_name,
                "TemplateData": json.dumps({
                    "website": website,
                    "update": update
                }),
            }
        }
    )
    logging.info(f"Successfully sent email with {resp['MessageId']=}")

def main():
    Runner(sys.argv[1]).main()

if __name__ == "__main__":
    main()
