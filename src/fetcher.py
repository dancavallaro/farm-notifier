import logging
import os
import sys
import urllib.request
import uuid

import boto3

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from base import ScriptBase
from config import WebsiteFetcher


def fetch_page_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("window-size=2560x1440")
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    options.add_argument("--remote-debugging-port=9222")

    ua = UserAgent()
    options.add_argument(f"user-agent={ua.chrome}")

    options.binary_location = "/opt/chrome/chrome-linux/chrome"
    service = Service(executable_path="/opt/chromedriver/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    return driver.page_source


def fetch_page_simple(url):
    request = urllib.request.Request(url, headers={
        # Terhune randomly started responding with 403 Forbidden, but this seems to work.
        "User-Agent": "curl/8.3.0"
    })
    with urllib.request.urlopen(request) as response:
        return response.read()


class Fetcher(ScriptBase):
    def __init__(self, website):
        super().__init__(website)

    def run(self):
        logging.info(f"Fetching website {self.website}")

        fetcher_name = self.config["fetcher"]

        if fetcher_name == WebsiteFetcher.SIMPLE:
            fetcher = fetch_page_simple
        elif fetcher_name == WebsiteFetcher.SELENIUM:
            fetcher = fetch_page_selenium
        else:
            raise Exception(f"Invalid fetcher '{fetcher_name}'")

        page_source = fetcher(self.config["url"])

        source_bucket_name = os.getenv("SOURCE_BUCKET_NAME")
        if source_bucket_name is not None:
            source_bucket = boto3.resource("s3").Bucket(source_bucket_name)

            upload_id = str(uuid.uuid4())
            key = f"{self.website}/{upload_id}"
            logging.info(f"Writing page source to {key=} in {source_bucket_name=}")
            source_bucket.put_object(Key=key, Body=page_source)

        print(page_source)


if __name__ == "__main__":
    Fetcher(sys.argv[1]).main()
