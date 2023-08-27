# directory-comparator
A command-line tool written in Python that compares two directories in terms of file additions/removals and content differences.

# Usage
To see usage of the tool, run the following command:
```bash
$ python3 main.py --help
```
Output:
```bash
usage: main.py [-h] -o ORIGINAL -n NEW [-dhc]

optional arguments:
  -h, --help            show this help message and exit
  -o ORIGINAL, --original ORIGINAL
                        Path of the original directory
  -n NEW, --new NEW     Path of the relatively new directory where any differences from the original directory are to be reported as changes
  -dhc, --disable-hash-check
                        Disable comparison based on file content
```

# Record of a Sample Run
[![asciicast](https://asciinema.org/a/Z7KhIssgW71Lcz8qryU0jdiX1.svg)](https://asciinema.org/a/Z7KhIssgW71Lcz8qryU0jdiX1)