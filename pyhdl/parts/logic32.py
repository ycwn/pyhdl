

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("NOT32", [ "B32" ], [ "B32" ])
def not32(a, x):
	return [ not1(aa, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX32", [ "N", "B32", "B32" ], [ "B32" ])
def mux32(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("ADC32", [ "B32", "B32", "N" ], [ "B32", "N" ])
def adc32(a, b, ci, x, co):

	adcs  = []
	carry = ci

	for n in range(31):

		adc   = adc1(a.nets[n], b.nets[n], carry, x.nets[n])
		carry = adc.outputs[1]

		adcs.append(adc)

	adcs.append(adc1(a.nets[31], b.nets[31], carry, x.nets[31], co))
	return adcs



@module("INC32", [ "B32" ], [ "B32" ])
def inc32(a, x):
	return [ adc32(a, mkconst("ZERO", 32, 0), one, x) ]



@module("SUB32", [ "B32", "B32" ], [ "B32" ])
def sub32(a, b, x):

	neg = not32(b)
	adc = adc32(a, neg.outputs[0], one, x)

	return [ neg, adc ]



@module("EQZ32", [ "B32" ], [ "N" ])
def eqz32(a, x):

	or0_0  = or1(a.nets[ 0], a.nets[ 1])
	or0_1  = or1(a.nets[ 2], a.nets[ 3])
	or0_2  = or1(a.nets[ 4], a.nets[ 5])
	or0_3  = or1(a.nets[ 6], a.nets[ 7])
	or0_4  = or1(a.nets[ 8], a.nets[ 9])
	or0_5  = or1(a.nets[10], a.nets[11])
	or0_6  = or1(a.nets[12], a.nets[13])
	or0_7  = or1(a.nets[14], a.nets[15])
	or0_8  = or1(a.nets[16], a.nets[17])
	or0_9  = or1(a.nets[18], a.nets[19])
	or0_10 = or1(a.nets[20], a.nets[21])
	or0_11 = or1(a.nets[22], a.nets[23])
	or0_12 = or1(a.nets[24], a.nets[25])
	or0_13 = or1(a.nets[26], a.nets[27])
	or0_14 = or1(a.nets[28], a.nets[29])
	or0_15 = or1(a.nets[30], a.nets[31])

	or1_0 = or1(or0_0.outputs[0],  or0_1.outputs[0])
	or1_1 = or1(or0_2.outputs[0],  or0_3.outputs[0])
	or1_2 = or1(or0_4.outputs[0],  or0_5.outputs[0])
	or1_3 = or1(or0_6.outputs[0],  or0_7.outputs[0])
	or1_4 = or1(or0_8.outputs[0],  or0_9.outputs[0])
	or1_5 = or1(or0_10.outputs[0], or0_11.outputs[0])
	or1_6 = or1(or0_12.outputs[0], or0_13.outputs[0])
	or1_7 = or1(or0_14.outputs[0], or0_15.outputs[0])

	or2_0 = or1(or1_0.outputs[0], or1_1.outputs[0])
	or2_1 = or1(or1_2.outputs[0], or1_3.outputs[0])
	or2_2 = or1(or1_4.outputs[0], or1_5.outputs[0])
	or2_3 = or1(or1_6.outputs[0], or1_7.outputs[0])

	or3_0 = or1(or2_0.outputs[0], or2_1.outputs[0])
	or3_1 = or1(or2_2.outputs[0], or2_3.outputs[0])

	or4_0 = nor1(or3_0.outputs[0], or3_1.outputs[0], x)

	return [
		or0_0, or0_1, or0_2,  or0_3,  or0_4,  or0_5,  or0_6,  or0_7,
		or0_8, or0_9, or0_10, or0_11, or0_12, or0_13, or0_14, or0_15,
		or1_0, or1_1, or1_2,  or1_3,  or1_4,  or1_5,  or1_6,  or1_7,
		or2_0, or2_1, or2_2,  or2_3,
		or3_0, or3_1,
		or4_0
	]



@module("LTZ32", [ "B32" ], [ "N" ])
def ltz32(a, x):
	return [ buf1(a.nets[31], x) ]



@module("REG32", [ "N", "N", "B32" ], [ "B32" ])
def reg32(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR32", [ "N", "N", "B32" ], [ "B32" ])
def ctr32(s, c, d, x):

	inc = inc32(x)
	mux = mux32(s, inc.outputs[0], d);
	reg = reg32(one, c, mux.outputs[0], x)

	return [ inc, mux, reg ]

