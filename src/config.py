from enum import Enum
import sys


class WebsiteFetcher(Enum):
    SIMPLE = 1
    SELENIUM = 2

class Website:
    STULTS = "STULTS"
    TERHUNE = "TERHUNE"


SUPPORTED_WEBSITES = {
    Website.TERHUNE: {
        "url": "https://www.terhuneorchards.com/pick-your-own-schedule/",
        "fetcher": WebsiteFetcher.SIMPLE,
    },
    Website.STULTS: {
        "url": "https://stultsfarm.com/",
        "fetcher": WebsiteFetcher.SELENIUM,
    }
}


if __name__ == "__main__":
    print(SUPPORTED_WEBSITES[sys.argv[1]])
