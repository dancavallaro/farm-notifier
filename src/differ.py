import json
import sys

from base import ScriptBase


class Differ(ScriptBase):
    def __init__(self, previous_update, latest_update):
        super().__init__()
        self.previous_update = previous_update
        self.latest_update = latest_update

    def run(self):
        previous = json.loads(self.previous_update) if self.previous_update is not None else None
        latest = json.loads(self.latest_update)
        update = {"latest": latest}

        if type(latest) is list and (type(previous) is list or previous is None):
            previous_items = set(previous) if previous is not None else set()
            latest_items = set(latest)
            update["added"] = list(latest_items - previous_items)
            update["removed"] = list(previous_items - latest_items)
        elif type(latest) is str and (type(previous) is str or previous is None):
            # Don't actually need to do anything in this case, but maybe one day I'll
            # do a fancy diff of these string updates or something.
            pass
        else:
            raise Exception("PREVIOUS and LATEST must be both strings, or both lists")

        return update


def main():
    previous_update, latest_update = sys.argv[1:]
    print(Differ(previous_update, latest_update).main())

if __name__ == "__main__":
    main()
