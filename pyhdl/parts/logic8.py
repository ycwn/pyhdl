

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

		adc   = adc1(a.nets[n], b.nets[n], carry, x.nets[n])
		carry = adc.outputs[1]

		adcs.append(adc)

	adcs.append(adc1(a.nets[7], b.nets[7], carry, x.nets[7], co))
	return adcs



@module("INC8", [ "B8" ], [ "B8" ])
def inc8(a, x):
	return [ adc8(a, mkconst("ZERO", 8, 0), one, x) ]



@module("SUB8", [ "B8", "B8" ], [ "B8" ])
def sub8(a, b, x):

	neg = not8(b)
	adc = adc8(a, neg.outputs[0], one, x)

	return [ neg, adc ]



@module("EQZ8", [ "B8" ], [ "N" ])
def eqz8(a, x):

	or0_0 = or1(a.nets[ 0], a.nets[ 1])
	or0_1 = or1(a.nets[ 2], a.nets[ 3])
	or0_2 = or1(a.nets[ 4], a.nets[ 5])
	or0_3 = or1(a.nets[ 6], a.nets[ 7])

	or1_0 = or1(or0_0.outputs[0], or0_1.outputs[0])
	or1_1 = or1(or0_2.outputs[0], or0_3.outputs[0])

	or2_0 = nor1(or1_0.outputs[0], or1_1.outputs[0], x)

	return [
		or0_0, or0_1, or0_2, or0_3,
		or1_0, or1_1,
		or2_0
	]



@module("LTZ8", [ "B8" ], [ "N" ])
def ltz8(a, x):
	return [ buf1(a.nets[7], x) ]



@module("REG8", [ "N", "N", "B8" ], [ "B8" ])
def reg8(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR8", [ "N", "N", "B8" ], [ "B8" ])
def ctr8(s, c, d, x):

	inc = inc8(x)
	mux = mux8(s, inc.outputs[0], d);
	reg = reg8(one, c, mux.outputs[0], x)

	return [ inc, mux, reg ]

