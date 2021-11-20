

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("NOT8", [ "B8" ], [ "B8" ])
def not8(a, x):
	return [ not1(aa, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("AND8", [ "B8", "B8" ], [ "B8" ])
def and8(a, b, x):
	return [ and1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("AND8S", [ "B8", "N" ], [ "B8" ])
def and8s(a, b, x):
	return [ and1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("OR8", [ "B8", "B8" ], [ "B8" ])
def or8(a, b, x):
	return [ or1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR8", [ "B8", "B8" ], [ "B8" ])
def xor8(a, b, x):
	return [ xor1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR8S", [ "B8", "N" ], [ "B8" ])
def xor8s(a, b, x):
	return [ xor1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX8", [ "N", "B8", "B8" ], [ "B8" ])
def mux8(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("DMUX8", [ "N", "B8" ], [ "B8", "B8" ])
def dmux8(s, x, d0, d1):
	return [ dmux1(s, xx, dd0, dd1) for xx, dd0, dd1 in zip(x.nets, d0.nets, d1.nets) ]



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



@module("SUB8", [ "B8", "B8", "N" ], [ "B8", "N" ])
def sub8(a, b, bi, x, bo):

	neg = not8(b)
	cbi = not1(bi)
	adc = adc8(a, neg.x, cbi.x, x)
	bco = not1(adc.co, bo)

	return [ neg, cbi, adc, bco ]



@module("DEC8", [ "B8", "N" ], [ "B8", "N" ])
def dec8(a, ci, x, co):
	return [ sub8(a, mkconst("ZERO", 8, 0), ci, x, co) ]



@module("SHL8", [ "B8", "N" ], [ "B8", "N" ])
def shl8(a, ci, x, co):
	return [
		buf1(
			a[n-1] if n > 0       else ci,
			x[n]   if n < x.width else co
		) for n in range(0, 9)
	]



@module("SHR8", [ "N", "N" ], [ "N", "N" ])
def shr8(a, ci, x, co):
	return [
		buf1(
			a[n]   if n < a.width else ci,
			x[n-1] if n > 0       else co
		) for n in range(0, 9)
	]



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



@module("LATCH8", [ "N", "B8" ], [ "B8" ])
def latch8(s, d, x):
	return [ dff1(s, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("REG8", [ "N", "N", "B8" ], [ "B8" ])
def reg8(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR8", [ "N", "N", "B8", "N" ], [ "B8", "N" ])
def ctr8(s, c, d, ci, x, co):

	inc = inc8(x, ci, bus(8), co)
	mux = mux8(s, inc.x, d);
	reg = reg8(one, c, mux.x, x)

	return [ inc, mux, reg ]

