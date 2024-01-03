"""This module contains the CPU core class.
"""

from pathlib import Path
from typing import Tuple

import numpy as np

from src.equations import least_squares_transpose as lst
from src.equations import piecewise_linear_interpolation as pli


class Core:
    """Class containing data on a CPU core.

    Attributes:
        core_num (int): The CPU core number.
        readings (list): List of tuples of CPU readings.
    """

    def __init__(self, c_num: int) -> None:
        """Constructor for the Core class

        Parameters:
            c_num (int): The CPU core number.
            readings (list): List of tuples containing readings.
        """
        self.core_num = c_num
        self.readings = []

    @property
    def core_num(self) -> int:
        """Get the core number of this Core.

        Returns:
            num (int): The core number.
        """
        return self._core_num

    @core_num.setter
    def core_num(self, num: int) -> None:
        """Set the core number of this Core.

        Parameters:
            num (int): The core number.

        Raises:
            AttributeError: If negative number is passed.
        """
        if num < 0:
            raise AttributeError("Negative core number is not allowed")
        self._core_num = num

    def add_reading(self, point: Tuple) -> None:
        """Add a new reading to the reading list.

        Parameters:
            point (tuple): Tuple containing (time, temperature) readings.
        """
        self.readings.append(point)

    def _to_numpy_arrays(self) -> Tuple:
        """Convert the reading points to x and y matricies.

        Returns:
            x_matrix (tuple[0]): The X matrix.
            y_matrix (tuple[1]): The Y matrix.
        """
        x_points = []
        y_points = []

        for points in self.readings:
            x_points.append([1, points[0]])
            y_points.append([points[1]])

        return np.array(x_points), np.array(y_points)

    def __str__(self) -> str:
        """Return the string representation of this object.

        Returns:
            string (str): String representation
        """
        string = ""

        for count, _ in enumerate(self.readings):
            if count + 1 > len(self.readings) - 1:
                break

            # TODO: Too many variables
            start_time = self.readings[count][0]
            end_time = self.readings[count + 1][0]
            start_temp = self.readings[count][1]
            end_temp = self.readings[count + 1][1]
            y_int, slope = pli(start_time, end_time, start_temp, end_temp)

            string += (
                f"{start_time: <6} <= x <= {end_time: >6}; "
                + f"y = {y_int:.4f} + {slope:.4f}; interpolation\n"
            )

        x_matrix, y_matrix = self._to_numpy_arrays()
        start_time = self.readings[0][0]
        end_time = self.readings[len(self.readings) - 1][0]
        y_int, slope = lst(x_matrix, y_matrix)

        string += (
            f"{start_time: <6} <= x <= {end_time: >6}; "
            + f"y = {y_int:.4f} + {slope:.4f}; least-squares\n"
        )

        return string

    def write_to_file(self, directory: str = "reports") -> None:
        """Write a core's calculations to file.

        Parameters:
            directory (str): The output directory, defaults to reports/
        """
        try:
            Path.mkdir(Path(directory), parents=True)
        except FileExistsError:
            pass

        with open(
            f"{directory}/core-{self.core_num}.txt", "w", encoding="UTF-8"
        ) as file:
            file.write(str(self))
