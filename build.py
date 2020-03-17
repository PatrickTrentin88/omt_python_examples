#!/usr/bin/env python3

"""
Builds OptiMathSAT Python API with SWIG 3.0.
"""

import glob
import os
import subprocess
from shutil import copyfile

###
### Locate OptiMathSAT
###

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MATCHES = glob.glob(os.path.join(BASE_DIR, "optimathsat", "optimathsat-*", "python"))

if not MATCHES:
    print("Download and unpack the latest distributable version " +
          "of OptiMathSAT in the 'optimathsat' directory.")
    quit(1)

###
### Build OptiMathSAT Python LIB
###

BUILD_PATH = os.path.abspath(MATCHES[0])
subprocess.check_call(['python3', "setup.py", "build"], cwd=BUILD_PATH)

###
### Copy Python LIB Files
###

SRC_MATHSAT_LIB = os.path.join(BUILD_PATH, "optimathsat.py")
SRC_MATHSAT_SO = glob.glob(os.path.join(BUILD_PATH, "build", "lib.*", "*.so"))[0]

DST_MATHSAT_LIB = os.path.join(BASE_DIR, "include", "optimathsat.py")
DST_MATHSAT_SO = os.path.join(BASE_DIR, "lib", "_optimathsat.so")

copyfile(SRC_MATHSAT_LIB, DST_MATHSAT_LIB)
copyfile(SRC_MATHSAT_SO, DST_MATHSAT_SO)
