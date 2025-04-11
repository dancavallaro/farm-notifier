import json
import logging
import sys

import boto3

from base import ScriptBase


def send_email(website, update):
    ses = boto3.client("sesv2")
    resp = ses.send_email(
        FromEmailAddress="Produce Updates <produce@dancavallaro.com>", # TODO: constant/config/envvar; change domain/name?
        Destination={
            "ToAddresses": ["dan.t.cavallaro+produce@gmail.com"], # TODO: constant/config/envvar
        },
        Content={
            "Template": {
                "TemplateName": "WebsiteUpdateEmailTemplate-Prod", # TODO: should be from envvar
                "TemplateData": json.dumps({
                    "website": website,
                    "update": update
                }),
            }
        }
    )
    logging.info(f"Successfully sent email with {resp['MessageId']=}")


class DiffNotifier(ScriptBase):
    def __init__(self, website, previous_update, latest_update):
        super().__init__(website)
        self.previous_update = previous_update
        self.latest_update = latest_update

    def run(self):
        previous = json.loads(self.previous_update)
        latest = json.loads(self.latest_update)
        update = {"latest": latest}

        if type(previous) is list and type(latest) is list:
            previous_items = set(previous)
            latest_items = set(latest)
            update["added"] = list(latest_items - previous_items)
            update["removed"] = list(previous_items - latest_items)
        elif type(previous) is str and type(latest) is str:
            pass
        else:
            raise Exception("PREVIOUS and LATEST must be both strings, or both lists")

        logging.info(f"Sending email for latest update for {self.website=}: {update}")
        send_email(self.website, update) # TODO: send email if config was provided


def main():
    website, previous_update, latest_update = sys.argv[1:]
    DiffNotifier(website, previous_update, latest_update).main()

if __name__ == "__main__":
    main()
