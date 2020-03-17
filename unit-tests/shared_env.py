#!/usr/bin/env python3

"""
shared environment unit-test.
"""

###
### SETUP PATHS
###

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCLUDE_DIR = os.path.join(BASE_DIR, '..', 'include')
LIB_DIR = os.path.join(BASE_DIR, '..', 'lib')
sys.path.append(INCLUDE_DIR)
sys.path.append(LIB_DIR)

################################################################################
################################################################################
################################################################################

from optimathsat import * # pylint: disable=unused-wildcard-import,wildcard-import

# NOTE: the instance of shared environment
#       must ALWAYS be deleted BEFORE the
#       instance of environment it originates
#       from.

#
## Test Shared SMT Environment
#

E1 = msat_create_env()
if MSAT_ERROR_ENV(E1):
    raise Exception("Invalid Environment Pointer")

E2 = msat_create_shared_env(None, E1)
if MSAT_ERROR_ENV(E2):
    raise Exception("Invalid Environment Pointer")

msat_destroy_env(E2)
msat_destroy_env(E1)

#
## Test Shared OMT Environment
#

OE1 = msat_create_opt_env()
if MSAT_ERROR_ENV(OE1):
    raise Exception("Invalid Environment Pointer")

OE2 = msat_create_shared_opt_env(None, OE1)
if MSAT_ERROR_ENV(OE2):
    raise Exception("Invalid Environment Pointer")

msat_destroy_env(OE2)
msat_destroy_env(OE1)
