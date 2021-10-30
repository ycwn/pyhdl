

from pyhdl.core import *



@module("NAND", [ "N", "N" ], [ "N" ])
def nand1(a, b, x):

	def sim():
		x.value = not (a.value and b.value)

	def emit():
		return "\tNAND %s, %s, %s" % (x.ident(), a.ident(), b.ident())

	return { 'sim': sim, 'emit': emit }



@module("NOT", [ "N" ], [ "N" ])
def not1(a, x):
	return [ nand1(a, a, x) ]



@module("BUF", [ "N" ], [ "N" ])
def buf1(a, x):

	neg0 = not1(a)
	neg1 = not1(neg0.x, x)

	return [ neg0, neg1 ]



@module("AND", [ "N", "N" ], [ "N" ])
def and1(a, b, x):

	xab = nand1(a, b)
	y   = not1(xab.x, x)

	return [ xab, y ]



@module("OR", [ "N", "N" ], [ "N" ])
def or1(a, b, x):

	xa = not1(a)
	xb = not1(b)
	y  = nand1(xa.x, xb.x, x)

	return [ xa, xb, y ]



@module("NOR", [ "N", "N" ], [ "N" ])
def nor1(a, b, x):

	xab = or1(a, b)
	y   = not1(xab.x, x)

	return [ xab, y ]



@module("XOR", [ "N", "N" ], [ "N" ])
def xor1(a, b, x):

	xab = nand1(a,     b)
	xa  = nand1(a,     xab.x)
	xb  = nand1(xab.x, b)
	y   = nand1(xa.x,  xb.x, x)

	return [ xab, xa, xb, y ]



@module("ADD", [ "N", "N" ], [ "N", "N" ])
def add1(a, b, s, c):

	sab = xor1(a, b, s)
	cab = and1(a, b, c)

	return [ sab, cab ]



@module("ADC", [ "N", "N", "N" ], [ "N", "N" ])
def adc1(a, b, c, s, o):

	s0 = add1(a, b)
	s1 = add1(c, s0.s, s)
	ov = or1(s0.c, s1.c, o)

	return [ s0, s1, ov ]



@module("MUX", [ "N", "N", "N" ], [ "N" ])
def mux1(s, d0, d1, x):

	ns  = not1(s)
	s0  = and1(d0, ns.x)
	s1  = and1(d1, s)
	out = or1(s0.x, s1.x, x)

	return [ ns, s0, s1, out ]



@module("DMUX", [ "N", "N" ], [ "N", "N" ])
def dmux1(s, c, x0, x1):

	ns  = not1(s)
	cx0 = and1(c, ns.x, x0)
	cx1 = and1(c, s,    x1)

	return [ ns, cx0, cx1 ]



@module("DFF", [ "N", "N" ], [ "N", "N" ])
def dff1(c, d, q, p):

	b = not1(d)

	sr0_q = nand1(c, d)
	sr0_p = nand1(c, b.x)

	sr1_q = nand1(sr0_q.x, p,       q)
	sr1_p = nand1(q,       sr0_p.x, p)

	return [ b, sr0_p, sr0_q, sr1_p, sr1_q ]



@module("SDFF", [ "N", "N", "N" ], [ "N", "N" ])
def sdff1(s, c, d, q, p):

	cs = nand1(s, c)
	ss = nand1(s, cs.x)
	n0 = not1(ss.x)
	d0 = nand1(d, n0.x)

	q0 = net()
	p0 = net()

	sr0_q = nand1(d0.x, p0, q0)
	sr0_p = nand1(ss.x, q0, p0)

	ck = nand1(c, q0)

	sr1_q = nand1(ck.x, p, q)
	sr1_p = nand1(cs.x, q, p)

	return [ cs, ss, n0, d0, sr0_p, sr0_q, ck, sr1_p, sr1_q ]

