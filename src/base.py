import logging

from abc import ABC, abstractmethod

from config import SUPPORTED_WEBSITES


class ScriptBase(ABC):
    def __init__(self, website=None):
        if website is not None:
            self.website = website
            self.config = SUPPORTED_WEBSITES[website]

    @abstractmethod
    def run(self):
        pass

    def main(self):
        logging.basicConfig(
            level=logging.INFO, style="{", datefmt="%Y-%m-%d %H:%M",
            format="{asctime} [{levelname}] {message}")

        self.run()
