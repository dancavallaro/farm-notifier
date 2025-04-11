import json
import logging
import sys

from bs4 import BeautifulSoup

from base import ScriptBase
from config import Website


def stults_parser(soup):
    produce_list = None

    for ul in soup.find_all("ul"):
        div = ul.find_parent("div", class_="wpb_wrapper")
        if div:
            produce_list = ul
            break

    produce = [item.string.replace("-", "").strip() for item in produce_list.find_all("li")]
    produce.sort()

    return produce


def terhune_parser(soup):
    updates = soup.find_all('p', class_='blurbColor')

    if len(updates) != 1:
        raise Exception(f"Oops! Expected 1 update, found {len(updates)}.")

    update_text = updates[0].get_text().strip()

    return update_text


class Parser(ScriptBase):
    def __init__(self, website):
        super().__init__(website)

    def run(self):
        logging.info(f"Parsing snapshot of website {self.website}")

        if self.website == Website.STULTS:
            parser = stults_parser
        elif self.website == Website.TERHUNE:
            parser = terhune_parser
        else:
            raise Exception(f"Invalid website '{self.website}'")

        page_source = sys.stdin.read()
        soup = BeautifulSoup(page_source, "html.parser")

        print(json.dumps(parser(soup)))


if __name__ == "__main__":
    Parser(sys.argv[1]).main()
