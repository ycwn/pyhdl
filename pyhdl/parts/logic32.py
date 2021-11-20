

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("NOT32", [ "B32" ], [ "B32" ])
def not32(a, x):
	return [ not1(aa, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("AND32", [ "B32", "B32" ], [ "B32" ])
def and32(a, b, x):
	return [ and1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("AND32S", [ "B32", "N" ], [ "B32" ])
def and32s(a, b, x):
	return [ and1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("OR32", [ "B32", "B32" ], [ "B32" ])
def or32(a, b, x):
	return [ or1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR32", [ "B32", "B32" ], [ "B32" ])
def xor32(a, b, x):
	return [ xor1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR32S", [ "B32", "N" ], [ "B32" ])
def xor32s(a, b, x):
	return [ xor1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX32", [ "N", "B32", "B32" ], [ "B32" ])
def mux32(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("DMUX32", [ "N", "B32" ], [ "B32", "B32" ])
def dmux32(s, x, d0, d1):
	return [ dmux1(s, xx, dd0, dd1) for xx, dd0, dd1 in zip(x.nets, d0.nets, d1.nets) ]



@module("ADC32", [ "B32", "B32", "N" ], [ "B32", "N" ])
def adc32(a, b, ci, x, co):

	adcs  = []
	carry = ci

	for n in range(31):

		adc   = adc1(a[n], b[n], carry, x[n])
		carry = adc.o

		adcs.append(adc)

	adcs.append(adc1(a[31], b[31], carry, x[31], co))
	return adcs



@module("INC32", [ "B32", "N" ], [ "B32", "N" ])
def inc32(a, ci, x, co):
	return [ adc32(a, mkconst("ZERO", 32, 0), ci, x, co) ]



@module("SUB32", [ "B32", "B32", "N" ], [ "B32", "N" ])
def sub32(a, b, bi, x, bo):

	neg = not32(b)
	cbi = not1(bi)
	adc = adc32(a, neg.x, cbi.x, x)
	bco = not1(adc.co, bo)

	return [ neg, cbi, adc, bco ]



@module("DEC32", [ "B32", "N" ], [ "B32", "N" ])
def dec32(a, ci, x, co):
	return [ sub32(a, mkconst("ZERO", 32, 0), ci, x, co) ]



@module("SHL32", [ "B32", "N" ], [ "B32", "N" ])
def shl32(a, ci, x, co):
	return [
		buf1(
			a[n-1] if n > 0       else ci,
			x[n]   if n < x.width else co
		) for n in range(0, 33)
	]



@module("SHR32", [ "N", "N" ], [ "N", "N" ])
def shr32(a, ci, x, co):
	return [
		buf1(
			a[n]   if n < a.width else ci,
			x[n-1] if n > 0       else co
		) for n in range(0, 33)
	]



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

	or1_0 = or1(or0_0.x,  or0_1.x)
	or1_1 = or1(or0_2.x,  or0_3.x)
	or1_2 = or1(or0_4.x,  or0_5.x)
	or1_3 = or1(or0_6.x,  or0_7.x)
	or1_4 = or1(or0_8.x,  or0_9.x)
	or1_5 = or1(or0_10.x, or0_11.x)
	or1_6 = or1(or0_12.x, or0_13.x)
	or1_7 = or1(or0_14.x, or0_15.x)

	or2_0 = or1(or1_0.x, or1_1.x)
	or2_1 = or1(or1_2.x, or1_3.x)
	or2_2 = or1(or1_4.x, or1_5.x)
	or2_3 = or1(or1_6.x, or1_7.x)

	or3_0 = or1(or2_0.x, or2_1.x)
	or3_1 = or1(or2_2.x, or2_3.x)

	or4_0 = nor1(or3_0.x, or3_1.x, x)

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



@module("LATCH32", [ "N", "B32" ], [ "B32" ])
def latch32(s, d, x):
	return [ dff1(s, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("REG32", [ "N", "N", "B32" ], [ "B32" ])
def reg32(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR32", [ "N", "N", "B32", "N" ], [ "B32", "N" ])
def ctr32(s, c, d, ci, x, co):

	inc = inc32(x, ci, bus("", 32), co)
	mux = mux32(s, inc.x, d);
	reg = reg32(one, c, mux.x, x)

	return [ inc, mux, reg ]

