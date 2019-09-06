"""
Contains a class to read, modify, and write config files for sextractor
History:
    Created 2019-09-05
        Varun Iyer <varun_iyer@ucsb.edu>
Classes:
    Sextractor(path) -- read and write sextractor configuration files
"""
from shlex import shlex

 
class Sextractor(dict):
    """
    Read, write, and modify sextractor config files.
    Emulates a dict, so you can read and write config values using dict keys
    Methods:
        __init__ -- create a config.Sextractor object with a path to a conf file
    """
    def __init__(self, path):
        super().__init__()
        self.path = path
        with open(self.path, "r") as conf:
            lines = conf.readlines() 
            for line in lines:
                lexer = shlex(line)
                lexer.whitespace_split = True
                key = lexer.get_token()
                value = conf.readline().strip()
                if not (key and value):
                    continue
                self[key] = value

    def write(self, path=""):
        if path == "":
            path = self.path
        with open(path, "w") as conf:
            for key, value in self.items():
                print("{}\t{}".format(key, value), file=conf)
