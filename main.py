"""The main module of the tool.

:raises RuntimeError: If at least one of specified paths is not a directory.
"""


import argparse
import os

from argument_handler import ArgumentHandler
from change_reporter import ChangeReporter
from directory_comparator import DirectoryComparator


def main(args: argparse.Namespace) -> None:
    """Start the comparison and report the results.

    :param args: Parsed arguments specified by the user
    :type args: argparse.Namespace
    :raises RuntimeError: If at least one of specified paths is not a directory.
    """
    original_path = os.path.abspath(args.original)
    new_path = os.path.abspath(args.new)
    disable_hash_check = args.disable_hash_check

    for path in (original_path, new_path):
        if not os.path.isdir(path):
            raise RuntimeError(f"No such directory!: {path}")

    change_map = DirectoryComparator(original_path, new_path, disable_hash_check).compare()
    ChangeReporter.report(change_map)

if __name__ == "__main__":
    main(ArgumentHandler().parse())
