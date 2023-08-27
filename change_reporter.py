"""Report the changes detected by DirectoryComparator"""


from typing import Dict


class ChangeReporter:
    """A class for reporting changes."""

    @staticmethod
    def report(change_map: Dict[str, str]) -> None:
        """Report the changes found in the given dictionary

        :param change_map: a dict containing relative paths along with their change notes
        :type change_map: Dict[str, str]
        """
        if len(change_map) == 0:
            print("No change has been found!")
            return

        print("Changes:")
        for key, value in change_map.items():
            if value == "-":
                print ("[-] " + key)
            elif value == "+":
                print ("[+] " + key)
            else:
                print (key + ": " + value)
