

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



@module("XOR16S", [ "B16", "N" ], [ "B16" ])
def xor16s(a, b, x):
	return [ xor1(aa, b, xx) for aa, xx in zip(a.nets, x.nets) ]



@module("MUX16", [ "N", "B16", "B16" ], [ "B16" ])
def mux16(s, d0, d1, x):
	return [ mux1(s, dd0, dd1, xx) for dd0, dd1, xx in zip(d0.nets, d1.nets, x.nets) ]



@module("ADC16", [ "B16", "B16", "N" ], [ "B16", "N" ])
def adc16(a, b, ci, x, co):

	adcs  = []
	carry = ci

	for n in range(15):

		adc   = adc1(a.nets[n], b.nets[n], carry, x.nets[n])
		carry = adc.outputs[1]

		adcs.append(adc)

	adcs.append(adc1(a.nets[15], b.nets[15], carry, x.nets[15], co))
	return adcs



@module("INC16", [ "B16" ], [ "B16" ])
def inc16(a, x):
	return [ adc16(a, mkconst("ZERO", 16, 0), one, x) ]



@module("SUB16", [ "B16", "B16" ], [ "B16" ])
def sub16(a, b, x):

	neg = not16(b)
	adc = adc16(a, neg.outputs[0], one, x)

	return [ neg, adc ]



@module("EQZ16", [ "B16" ], [ "N" ])
def eqz16(a, x):

	or0_0 = or1(a.nets[ 0], a.nets[ 1])
	or0_1 = or1(a.nets[ 2], a.nets[ 3])
	or0_2 = or1(a.nets[ 4], a.nets[ 5])
	or0_3 = or1(a.nets[ 6], a.nets[ 7])
	or0_4 = or1(a.nets[ 8], a.nets[ 9])
	or0_5 = or1(a.nets[10], a.nets[11])
	or0_6 = or1(a.nets[12], a.nets[13])
	or0_7 = or1(a.nets[14], a.nets[15])

	or1_0 = or1(or0_0.outputs[0], or0_1.outputs[0])
	or1_1 = or1(or0_2.outputs[0], or0_3.outputs[0])
	or1_2 = or1(or0_4.outputs[0], or0_5.outputs[0])
	or1_3 = or1(or0_6.outputs[0], or0_7.outputs[0])

	or2_0 = or1(or1_0.outputs[0], or1_1.outputs[0])
	or2_1 = or1(or1_2.outputs[0], or1_3.outputs[0])

	or3_0 = nor1(or2_0.outputs[0], or2_1.outputs[0], x)

	return [
		or0_0, or0_1, or0_2, or0_3, or0_4, or0_5, or0_6, or0_7,
		or1_0, or1_1, or1_2, or1_3,
		or2_0, or2_1,
		or3_0
	]



@module("LTZ16", [ "B16" ], [ "N" ])
def ltz16(a, x):
	return [ buf1(a.nets[15], x) ]



@module("REG16", [ "N", "N", "B16" ], [ "B16" ])
def reg16(s, c, d, x):
	return [ sdff1(s, c, dd, xx) for dd, xx in zip(d.nets, x.nets) ]



@module("CTR16", [ "N", "N", "B16" ], [ "B16" ])
def ctr16(s, c, d, x):

	inc = inc16(x)
	mux = mux16(s, inc.outputs[0], d);
	reg = reg16(one, c, mux.outputs[0], x)

	return [ inc, mux, reg ]

