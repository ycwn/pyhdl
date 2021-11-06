

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("NOT8", [ "B8" ], [ "B8" ])
def not8(a, x):
	return [ not1(aa, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX8", [ "N", "B8", "B8" ], [ "B8" ])
def mux8(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("ADC8", [ "B8", "B8", "N" ], [ "B8", "N" ])
def adc8(a, b, ci, x, co):

	adcs  = []
	carry = ci

	for n in range(7):

		adc   = adc1(a[n], b[n], carry, x[n])
		carry = adc.o

		adcs.append(adc)

	adcs.append(adc1(a[7], b[7], carry, x[7], co))
	return adcs



@module("INC8", [ "B8", "N" ], [ "B8", "N" ])
def inc8(a, ci, x, co):
	return [ adc8(a, mkconst("ZERO", 8, 0), ci, x, co) ]



@module("SUB8", [ "B8", "B8" ], [ "B8" ])
def sub8(a, b, x):

	neg = not8(b)
	adc = adc8(a, neg.x, one, x)

	return [ neg, adc ]



@module("EQZ8", [ "B8" ], [ "N" ])
def eqz8(a, x):

	or0_0 = or1(a[0], a[1])
	or0_1 = or1(a[2], a[3])
	or0_2 = or1(a[4], a[5])
	or0_3 = or1(a[6], a[7])

	or1_0 = or1(or0_0.x, or0_1.x)
	or1_1 = or1(or0_2.x, or0_3.x)

	or2_0 = nor1(or1_0.x, or1_1.x, x)

	return [
		or0_0, or0_1, or0_2, or0_3,
		or1_0, or1_1,
		or2_0
	]



@module("LTZ8", [ "B8" ], [ "N" ])
def ltz8(a, x):
	return [ buf1(a[7], x) ]



@module("LAT8", [ "N", "B8" ], [ "B8" ])
def lat8(s, d, x):
	return [ dff1(s, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("REG8", [ "N", "N", "B8" ], [ "B8" ])
def reg8(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR8", [ "N", "N", "B8", "N" ], [ "B8", "N" ])
def ctr8(s, c, d, ci, x, co):

	inc = inc8(x, ci, bus("", 8), co)
	mux = mux8(s, inc.x, d);
	reg = reg8(one, c, mux.x, x)

	return [ inc, mux, reg ]

