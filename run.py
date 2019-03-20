#!/usr/bin/env python3

"""
Runs all unit-tests.
"""

import glob
import os
import subprocess

###
###
###

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MATCHES = glob.glob(os.path.join(BASE_DIR, "unit-tests", "*.py"))

for test in MATCHES:
    file_name = os.path.basename(test)
    print_str = "\t" + "#" * 32 + "\n" \
                "\t### {:^24s} ###\n" + \
                "\t" + "#" * 32 + "\n"
    print(print_str.format(file_name))
    subprocess.check_call([test])
    print("\n")
