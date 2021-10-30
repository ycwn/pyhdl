

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

		adc   = adc1(a[n], b[n], carry, x[n])
		carry = adc.outputs[1]

		adcs.append(adc)

	adcs.append(adc1(a[31], b[31], carry, x[31], co))
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

	or0_0  = or1(a[ 0], a[ 1])
	or0_1  = or1(a[ 2], a[ 3])
	or0_2  = or1(a[ 4], a[ 5])
	or0_3  = or1(a[ 6], a[ 7])
	or0_4  = or1(a[ 8], a[ 9])
	or0_5  = or1(a[10], a[11])
	or0_6  = or1(a[12], a[13])
	or0_7  = or1(a[14], a[15])
	or0_8  = or1(a[16], a[17])
	or0_9  = or1(a[18], a[19])
	or0_10 = or1(a[20], a[21])
	or0_11 = or1(a[22], a[23])
	or0_12 = or1(a[24], a[25])
	or0_13 = or1(a[26], a[27])
	or0_14 = or1(a[28], a[29])
	or0_15 = or1(a[30], a[31])

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
	return [ buf1(a[31], x) ]



@module("REG32", [ "N", "N", "B32" ], [ "B32" ])
def reg32(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR32", [ "N", "N", "B32" ], [ "B32" ])
def ctr32(s, c, d, x):

	inc = inc32(x)
	mux = mux32(s, inc.outputs[0], d);
	reg = reg32(one, c, mux.outputs[0], x)

	return [ inc, mux, reg ]

