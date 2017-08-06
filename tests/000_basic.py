#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
"""
000_basic.py - basic tests for GPXViewer
"""

import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import utils

# that kinda summarizes the current situation ...
EMBARRASSING = True


class TestsGPXViewer(unittest.TestCase):
    """ Tests go here.
    """
    def testBasics(self):
        """
        """
        self.assertTrue(EMBARRASSING)

    def testDegConversion(self):
        """Make sure conversion from degree to radian works
        """
        pi = 3.14159
        self.assertAlmostEqual(utils.deg2rad(180), pi, places=4)
