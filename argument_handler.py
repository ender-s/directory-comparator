"""Define and parse the arguments expected from users."""


import argparse


class ArgumentHandler:
    """A class for handling user-specified arguments."""

    def __init__(self) -> None:
        """Initialize ArgumentHandler with argument definitions."""
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-o", "--original",
                                 type=str, help="Path of the original directory", required=True)
        self.parser.add_argument("-n", "--new",
                                 type=str,
                                 help="Path of the relatively new directory where any differences"
                                      " from the original directory are to be reported as changes",
                                 required=True)
        self.parser.add_argument("-dhc", "--disable-hash-check",
                                 action="store_true", default=False,
                                 help="Disable comparison based on file content")

    def parse(self) -> argparse.Namespace:
        """Return the parsed arguments.

        :return: Parsed arguments.
        :rtype: argparse.Namespace
        """
        return self.parser.parse_args()
