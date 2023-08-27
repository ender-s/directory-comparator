"""Compare two directories in terms of differences between them.

Differences include file/directory additions/removals,
file content changes, and type changes.
"""


import hashlib
import os
from typing import Dict, Set


class DirectoryComparator:
    """A class that consists of required methods to perform comparison of directories."""

    def __init__(self, original_path: str, new_path: str, disable_hash_check: bool) -> None:
        """Initializes DirectoryComparator with required attributes.

        :param original_path: Path of the original directory.
        :type original_path: str
        :param new_path: Path of the relatively new directory where any differences from
                         the original directory are to be reported as changes.
        :type new_path: str
        :param disable_hash_check: A boolean flag specifying whether or not comparison
                                   based on file contents is disabled.
        :type disable_hash_check: bool
        """
        self._original_path = original_path
        self._new_path = new_path
        self._disable_hash_check = disable_hash_check

    def _analyze_changes(self, original_path_root: str, original_paths: Set[str],
                         new_path_root: str, new_paths: Set[str]) -> Dict[str, str]:
        """Analyze and detect the changes made in the new path.

        :param original_path_root: Path of the original directory.
        :type original_path_root: str
        :param original_paths: A set containing paths of subfiles and subdirectories under
                               original_path_root.
        :type original_paths: Set[str]
        :param new_path_root: Path of the relatively new directory where any differences from
                              the original directory are to be reported as changes.
        :type new_path_root: str
        :param new_paths: A set containing paths of subfiles and subdirectories under
                          new_path_root.
        :type new_paths: Set[str]
        :return: A dict whose keys are paths in the new directory subject to any change
                 and values are change notes.
        :rtype: Dict[str, str]
        """
        change_map = {}

        for i in original_paths:
            if not i in new_paths:
                change_map[i] = "-"
            else:
                original_file_path = os.path.join(original_path_root, i)
                new_file_path = os.path.join(new_path_root, i)
                if self._is_hashable(original_file_path) and self._is_hashable(new_file_path):
                    if not self._disable_hash_check:
                        original_file_hash = self._calculate_hash(original_file_path)
                        new_file_hash = self._calculate_hash(new_file_path)
                        if original_file_hash != new_file_hash:
                            change_map[i] = "different hash"

                elif not self._are_types_same(original_file_path, new_file_path):
                    change_map[i] = "different type"

        for i in new_paths:
            if not i in original_paths:
                change_map[i] = "+"

        return change_map

    def _is_hashable(self, path: str) -> bool:
        """Return whether or not the given path refers to a hashable file.

        :param path: The path to be checked if it is hashable.
        :type path: str
        :return: True if the file is hashable. False otherwise.
        :rtype: bool
        """
        return not os.path.isdir(path) and not os.path.islink(path) and os.path.isfile(path)

    def _are_types_same(self, path1: str, path2: str) -> bool:
        """Check if given two paths refer to the same type of file.

        :param path1, path2: Paths for type equality check
        :type path1, path2: str
        :return: True if given paths refer to the same type of file. False otherwise.
        :rtype: bool
        """
        if os.path.isdir(path1) and os.path.isdir(path2):
            return True

        if os.path.isfile(path1) and os.path.isfile(path2):
            return True

        if os.path.islink(path1) and os.path.islink(path2):
            return True

        return False

    def _calculate_hash(self, path: str, block_size: int = 8192) -> str:
        """Calculate SHA-256 hash of the file at given path.

        :param path: Path of the file whose hash is to be calculated.
        :type path: str
        :param block_size: The size of a block for reading the file in blocks, defaults to 8192.
        :type block_size: int, optional
        :return: SHA-256 hash of the file.
        :rtype: str
        """
        sha256: hashlib._Hash = hashlib.sha256()
        with open(path, "rb") as file:
            while True:
                r = file.read(block_size)
                if not r:
                    break
                else:
                    sha256.update(r)

        return sha256.hexdigest()

    def scan_directory(self, path: str) -> Set[str]:
        """
        Return a set consisting of paths of all
        subfiles and subdirectories found in the given path.

        :param path: path of the directory whose subfiles and
                     subdirectories are to be recorded in a set.
        :type path: str
        :return: a set containing the paths of subfiles and
                 subdirectories found under the given path.
        :rtype: Set[str]
        """
        paths: Set[str] = set()
        self._scan_directory(paths, os.path.abspath(path), "")
        return paths

    def _scan_directory(self, paths: Set[str], root: str, path: str) -> None:
        """
        Recursively traverse all subdirectories in the given path and
        collect paths of all subdirectories and subfiles under the given path
        in the given set.

        :param paths: a set to store the relative paths
        :type paths: Set[str]
        :param root: the root path specified by the user
        :type root: str
        :param path: the relative path to scan
        :type path: str
        """
        paths.add(path)
        current_path: str = os.path.join(root, path)
        try:
            for i in os.scandir(current_path):
                relative_path: str = os.path.join(path, os.path.split(i)[1])
                if not os.path.isdir(i):
                    paths.add(relative_path)
                else:
                    self._scan_directory(paths, root, relative_path)
        except PermissionError as error:
            print(str(error))

    def compare(self) -> Dict[str, str]:
        """Manage the comparison process and return the results.

        :return: Results of the change analysis.
        :rtype: Dict[str, str]
        """
        print("Scanning directories...")
        original_paths: Set[str] = self.scan_directory(self._original_path)
        new_paths: Set[str] = self.scan_directory(self._new_path)

        print("Analyzing changes...")
        return self._analyze_changes(self._original_path, original_paths,
                                     self._new_path, new_paths)
