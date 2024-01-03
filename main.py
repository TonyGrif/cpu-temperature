#!/usr/bin/env python3

"""This is the main module for the cpu-temperature project.
"""

import argparse
import logging
from pathlib import Path

from parse_temps import parse_raw_temps
from src.core import Core


def main():
    """Run the cpu-temperature program."""
    parser = argparse.ArgumentParser(
        prog="CPU Temperatures",
        description="Analyzes CPU temperature changes over time.",
    )

    parser.add_argument("txt_file", type=Path, help="Path to text file.")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable DEBUG console logs."
    )

    args = parser.parse_args()

    if not args.txt_file.is_file() or args.txt_file.suffix != ".txt":
        print("Must supply a real text file")
        return

    if args.debug is True:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug logs activated")

    cores = []

    with open(args.txt_file, "r", encoding="utf-8") as temps:
        # Get number of cores, create structure for each, then go back
        last_line = temps.tell()
        count = len((temps.readline()).split())
        logging.debug("Creating structures for %s cores", count)

        for core_num in range(count):
            cores.append(Core(core_num))

        temps.seek(last_line)

        # Parse data
        for f_temps in parse_raw_temps(temps):
            # Catch new lines at the end
            if not f_temps[1]:
                break

            for count, temp in enumerate(f_temps[1]):
                logging.debug("Adding (%s, %s) to core %s", f_temps[0], temp, count)
                cores[count].add_reading((f_temps[0], temp))

    for core in cores:
        core.write_to_file()

    return


if __name__ == "__main__":
    main()
