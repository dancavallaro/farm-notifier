import logging
import sys
import urllib.request

from fake_useragent import UserAgent
from retry import retry
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from base import ScriptBase
from config import WebsiteFetcher


class FetchError(Exception):
    pass


@retry(FetchError, tries=3, delay=2, backoff=2)
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
    source = driver.page_source

    # Every once in a while the Stults fetcher gets a response that looks like
    # '<html><head></head><body></body></html>'. I haven't figured out why, but
    # it always seems to work fine on a second try.
    if len(source) < 1000:
        logging.error(f"Website source is smaller than expected: {source}")
        raise FetchError("website source is truncated, try again")

    return source


def fetch_page_simple(url):
    request = urllib.request.Request(url, headers={
        # Terhune randomly started responding with 403 Forbidden, but this seems to work.
        "User-Agent": "curl/8.3.0"
    })
    with urllib.request.urlopen(request) as response:
        return str(response.read())


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

        return fetcher(self.config["url"])


if __name__ == "__main__":
    print(Fetcher(sys.argv[1]).main())
