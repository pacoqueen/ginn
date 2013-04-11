#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *  # @UnusedWildImport
import ginn  # @UnusedImport

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"

