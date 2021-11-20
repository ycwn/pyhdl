

from pyhdl.core        import *
from pyhdl.parts.logic import *



@module("NOT4", [ "B4" ], [ "B4" ])
def not4(a, x):
	return [ not1(aa, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("AND4", [ "B4", "B4" ], [ "B4" ])
def and4(a, b, x):
	return [ and1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("AND4S", [ "B4", "N" ], [ "B4" ])
def and4s(a, b, x):
	return [ and1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("OR4", [ "B4", "B4" ], [ "B4" ])
def or4(a, b, x):
	return [ or1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR4", [ "B4", "B4" ], [ "B4" ])
def xor4(a, b, x):
	return [ xor1(aa, bb, xx) for aa, bb, xx in zip(a.nets, b.nets, x.nets) ]



@module("XOR4S", [ "B4", "N" ], [ "B4" ])
def xor4s(a, b, x):
	return [ xor1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX4", [ "N", "B4", "B4" ], [ "B4" ])
def mux4(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("DMUX4", [ "N", "B4" ], [ "B4", "B4" ])
def dmux4(s, x, d0, d1):
	return [ dmux1(s, xx, dd0, dd1) for xx, dd0, dd1 in zip(x.nets, d0.nets, d1.nets) ]



@module("ADC4", [ "B4", "B4", "N" ], [ "B4", "N" ])
def adc4(a, b, ci, x, co):

	adcs  = []
	carry = ci

	for n in range(3):

		adc   = adc1(a[n], b[n], carry, x[n])
		carry = adc.o

		adcs.append(adc)

	adcs.append(adc1(a[3], b[3], carry, x[3], co))
	return adcs



@module("INC4", [ "B4", "N" ], [ "B4", "N" ])
def inc4(a, ci, x, co):
	return [ adc4(a, mkconst("ZERO", 4, 0), ci, x, co) ]



@module("SUB4", [ "B4", "B4", "N" ], [ "B4", "N" ])
def sub4(a, b, bi, x, bo):

	neg = not4(b)
	cbi = not1(bi)
	adc = adc4(a, neg.x, cbi.x, x)
	bco = not1(adc.co, bo)

	return [ neg, cbi, adc, bco ]



@module("DEC4", [ "B4", "N" ], [ "B4", "N" ])
def dec4(a, ci, x, co):
	return [ sub4(a, mkconst("ZERO", 4, 0), ci, x, co) ]



@module("SHL4", [ "B4", "N" ], [ "B4", "N" ])
def shl4(a, ci, x, co):
	return [
		buf1(
			a[n-1] if n > 0       else ci,
			x[n]   if n < x.width else co
		) for n in range(0, 5)
	]



@module("SHR4", [ "N", "N" ], [ "N", "N" ])
def shr4(a, ci, x, co):
	return [
		buf1(
			a[n]   if n < a.width else ci,
			x[n-1] if n > 0       else co
		) for n in range(0, 5)
	]



@module("EQZ4", [ "B4" ], [ "N" ])
def eqz4(a, x):

	or0_0 = or1(a[0], a[1])
	or0_1 = or1(a[2], a[3])

	or1_0 = nor1(or0_0.x, or0_1.x, x)

	return [
		or0_0, or0_1,
		or1_0
	]



@module("LTZ4", [ "B4" ], [ "N" ])
def ltz4(a, x):
	return [ buf1(a[3], x) ]



@module("LATCH4", [ "N", "B4" ], [ "B4" ])
def latch4(s, d, x):
	return [ dff1(s, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("REG4", [ "N", "N", "B4" ], [ "B4" ])
def reg4(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR4", [ "N", "N", "B4", "N" ], [ "B4", "N" ])
def ctr4(s, c, d, ci, x, co):

	inc = inc4(x, ci, bus("", 4), co)
	mux = mux4(s, inc.x, d);
	reg = reg4(one, c, mux.x, x)

	return [ inc, mux, reg ]



@module("SEL4", [ "N", "N", "N", "N" ], [ "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N" ])
def sel4(x0, x1, x2, x3, y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15):

	n0 = not1(x0)
	n1 = not1(x1)
	n2 = not1(x2)
	n3 = not1(x3)

	g_n0_n1 = and1(n0.x, n1.x)
	g_n2_n3 = and1(n2.x, n3.x)
	g_x0_n1 = and1(x0,   n1.x)
	g_n0_x1 = and1(n0.x, x1)
	g_x0_x1 = and1(x0,   x1)
	g_x2_n3 = and1(x2,   n3.x)
	g_n2_x3 = and1(n2.x, x3)
	g_x2_x3 = and1(x2,   x3)

	g_y00 = and1(g_n0_n1.x, g_n2_n3.x, y0)
	g_y01 = and1(g_x0_n1.x, g_n2_n3.x, y1)
	g_y02 = and1(g_n0_x1.x, g_n2_n3.x, y2)
	g_y03 = and1(g_x0_x1.x, g_n2_n3.x, y3)
	g_y04 = and1(g_n0_n1.x, g_x2_n3.x, y4)
	g_y05 = and1(g_x0_n1.x, g_x2_n3.x, y5)
	g_y06 = and1(g_n0_x1.x, g_x2_n3.x, y6)
	g_y07 = and1(g_x0_x1.x, g_x2_n3.x, y7)
	g_y08 = and1(g_n0_n1.x, g_n2_x3.x, y8)
	g_y09 = and1(g_x0_n1.x, g_n2_x3.x, y9)
	g_y10 = and1(g_n0_x1.x, g_n2_x3.x, y10)
	g_y11 = and1(g_x0_x1.x, g_n2_x3.x, y11)
	g_y12 = and1(g_n0_n1.x, g_x2_x3.x, y12)
	g_y13 = and1(g_x0_n1.x, g_x2_x3.x, y13)
	g_y14 = and1(g_n0_x1.x, g_x2_x3.x, y14)
	g_y15 = and1(g_x0_x1.x, g_x2_x3.x, y15)

	return [
		n0, n1, n2, n3,

		g_n0_n1, g_n2_n3, g_x0_n1, g_n0_x1,
		g_x0_x1, g_x2_n3, g_n2_x3, g_x2_x3,

		g_y00, g_y01, g_y02, g_y03, g_y04, g_y05, g_y06, g_y07,
		g_y08, g_y09, g_y10, g_y11, g_y12, g_y13, g_y14, g_y15
	]

