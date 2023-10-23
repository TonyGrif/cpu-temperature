#!/usr/bin/env python3

"""This is the main module for the cpu-temperature project.
"""

import argparse
from pathlib import Path


from parse_temps import parse_raw_temps
from src.piecewise import piecewise_linear_interpolation


def main():
    """Run the cpu-temperature program."""
    parser = argparse.ArgumentParser(
        prog="cpu-temperature",
        description="Analyzes CPU temperature changes over time",
    )

    parser.add_argument("txt_file", type=Path, help="Path to text file")

    args = parser.parse_args()

    if not args.txt_file.is_file() or args.txt_file.suffix != ".txt":
        print("Must supply a real text file")
        return

    # TODO: restructure
    times = []
    core0 = []
    core1 = []
    core2 = []
    core3 = []
    cores = []

    with open(args.txt_file, "r") as temps:
        # Output as one strucutre for now
        for f_temps in parse_raw_temps(temps):
            times.append(f_temps[0])
            core0.append(f_temps[1][0])
            core1.append(f_temps[1][1])
            core2.append(f_temps[1][2])
            core3.append(f_temps[1][3])

    cores.append(core0)
    cores.append(core1)
    cores.append(core2)
    cores.append(core3)

    for x in range(4):
        print(f"Core {x} \n============")
        for count, time in enumerate(times):
            if count + 1 > len(times) - 1:
                break
            # TODO: way too verbose a f-string
            print(
                f"{time} <= x <= {times[count+1]}; y= {piecewise_linear_interpolation(time, times[count+1], cores[x][count], cores[x][count+1])}; interpolation\n"
            )

    return


if __name__ == "__main__":
    main()
