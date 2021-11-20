

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("NOT16", [ "B16" ], [ "B16" ])
def not16(a, x):
	return [ not1(aa, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("AND16", [ "B16", "B16" ], [ "B16" ])
def and16(a, b, x):
	return [ and1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("AND16S", [ "B16", "N" ], [ "B16" ])
def and16s(a, b, x):
	return [ and1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("OR16", [ "B16", "B16" ], [ "B16" ])
def or16(a, b, x):
	return [ or1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR16", [ "B16", "B16" ], [ "B16" ])
def xor16(a, b, x):
	return [ xor1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR16S", [ "B16", "N" ], [ "B16" ])
def xor16s(a, b, x):
	return [ xor1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX16", [ "N", "B16", "B16" ], [ "B16" ])
def mux16(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("DMUX16", [ "N", "B16" ], [ "B16", "B16" ])
def dmux16(s, x, d0, d1):
	return [ dmux1(s, xx, dd0, dd1) for xx, dd0, dd1 in zip(x.nets, d0.nets, d1.nets) ]



@module("ADC16", [ "B16", "B16", "N" ], [ "B16", "N" ])
def adc16(a, b, ci, x, co):

	adcs  = []
	carry = ci

	for n in range(15):

		adc   = adc1(a[n], b[n], carry, x[n])
		carry = adc.o

		adcs.append(adc)

	adcs.append(adc1(a[15], b[15], carry, x[15], co))
	return adcs



@module("INC16", [ "B16", "N" ], [ "B16", "N" ])
def inc16(a, ci, x, co):
	return [ adc16(a, mkconst("ZERO", 16, 0), ci, x, co) ]



@module("SUB16", [ "B16", "B16", "N" ], [ "B16", "N" ])
def sub16(a, b, bi, x, bo):

	neg = not16(b)
	cbi = not1(bi)
	adc = adc16(a, neg.x, cbi.x, x)
	bco = not1(adc.co, bo)

	return [ neg, cbi, adc, bco ]



@module("DEC16", [ "B16", "N" ], [ "B16", "N" ])
def dec16(a, ci, x, co):
	return [ sub16(a, mkconst("ZERO", 16, 0), ci, x, co) ]



@module("IDC16", [ "B16", "N", "N" ], [ "B16", "N" ])
def idc16(a, ud, ci, x, co):

	cbi = xor1(ci, ud)
	adc = adc16(a, bus.repl(ud, 16), cbi.x, x)
	bco = xor1(adc.co, ud, co)

	return [ cbi, adc, bco ]



@module("SHL16", [ "B16", "N" ], [ "B16", "N" ])
def shl16(a, ci, x, co):
	return [
		buf1(
			a[n-1] if n > 0       else ci,
			x[n]   if n < x.width else co
		) for n in range(0, 17)
	]



@module("SHR16", [ "N", "N" ], [ "N", "N" ])
def shr16(a, ci, x, co):
	return [
		buf1(
			a[n]   if n < a.width else ci,
			x[n-1] if n > 0       else co
		) for n in range(0, 17)
	]



@module("EQZ16", [ "B16" ], [ "N" ])
def eqz16(a, x):

	or0_0 = or1(a[ 0], a[ 1])
	or0_1 = or1(a[ 2], a[ 3])
	or0_2 = or1(a[ 4], a[ 5])
	or0_3 = or1(a[ 6], a[ 7])
	or0_4 = or1(a[ 8], a[ 9])
	or0_5 = or1(a[10], a[11])
	or0_6 = or1(a[12], a[13])
	or0_7 = or1(a[14], a[15])

	or1_0 = or1(or0_0.x, or0_1.x)
	or1_1 = or1(or0_2.x, or0_3.x)
	or1_2 = or1(or0_4.x, or0_5.x)
	or1_3 = or1(or0_6.x, or0_7.x)

	or2_0 = or1(or1_0.x, or1_1.x)
	or2_1 = or1(or1_2.x, or1_3.x)

	or3_0 = nor1(or2_0.x, or2_1.x, x)

	return [
		or0_0, or0_1, or0_2, or0_3, or0_4, or0_5, or0_6, or0_7,
		or1_0, or1_1, or1_2, or1_3,
		or2_0, or2_1,
		or3_0
	]



@module("LTZ16", [ "B16" ], [ "N" ])
def ltz16(a, x):
	return [ buf1(a[15], x) ]



@module("LATCH16", [ "N", "B16" ], [ "B16" ])
def latch16(s, d, x):
	return [ dff1(s, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("REG16", [ "N", "N", "B16" ], [ "B16" ])
def reg16(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR16", [ "N", "N", "B16", "N" ], [ "B16", "N" ])
def ctr16(s, c, d, ci, x, co):

	inc = inc16(x, ci, bus(16), co)
	mux = mux16(s, inc.x, d);
	reg = reg16(one, c, mux.x, x)

	return [ inc, mux, reg ]

