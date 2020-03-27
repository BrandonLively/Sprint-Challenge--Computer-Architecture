#!/usr/bin/env python3

"""Main."""

import sys
import os
from cpu import *

basedir = os.path.abspath(os.getcwd())

filename = "scstretch.ls8"

filepath = os.path.join(basedir, filename)

cpu = CPU()

cpu.load(filepath)
cpu.run()