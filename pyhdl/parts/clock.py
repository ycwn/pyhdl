

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("CLOCK", [], [ "N" ])
def clock(c):
	return [ not1(c, c) ]

