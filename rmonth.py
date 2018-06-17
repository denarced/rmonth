#!/usr/bin/env python3

import argparse
import json
import os
import time


def read_config(cli_args):
    filen = "rmonth.json"
    paths = [
        cli_args.config,
        filen,
        os.path.join(os.path.expanduser("~"), ".rmonth", filen)
    ]
    for each in paths:
        # Actually only cli_args.config can be None but like this code is
        # simpler.
        if each is not None:
            if os.path.exists(each):
                with open(each) as f:
                    return json.load(f)


def walk(dirs, prune_dirs):
    walked = set()
    for each in dirs:
        for root, dirs, files in os.walk(each["path"]):
            # Don't walk the same directory twice
            fullpath = os.path.abspath(root)
            if fullpath in walked:
                continue
            else:
                walked.add(fullpath)

            for each_file in files:
                yield os.path.join(root, each_file)
            if not each["recursive"]:
                break
            if len(prune_dirs) > 0:
                for removed in prune_dirs & set(dirs):
                    dirs.remove(removed)


def is_old_enough(epoch_secs, path):
    day_secs = 60 * 60 * 24
    secs_old = int(epoch_secs) - int(os.path.getmtime(path))
    days_old = secs_old // day_secs
    return days_old != 0 and days_old % 30 == 0


def main():
    parser = argparse.ArgumentParser(description="Do the deed")
    parser.add_argument("-c", "--config")
    parsed = parser.parse_args()
    config = read_config(parsed)

    epoch_secs = time.time()
    prune_dirs = set(config["config"]["prune_dirs"])
    dirs = (each for each in config["dirs"])
    files = (each for each in walk(dirs, prune_dirs))
    old_files = (each for each in files if is_old_enough(epoch_secs, each))
    for each in old_files:
        print(each)

if __name__ == "__main__":
    main()
