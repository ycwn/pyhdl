

from .net import *
from .bus import *


zero = net("CONST", 0)
one  = net("CONST", 1)

zero.value = False
one.value  = True



def mkconst(name, bits, val):

	b = bus(name, bits)

	for n in range(bits):
		b.nets[n] = one if val & (1 << n) else zero

	return b



def simulate(m, inputs):

	for n in range(len(inputs)):
		m.inputs[n].value = inputs[n]

	def s(mm):
		if mm.sim:
			mm.sim()

	m.visit(None, s)

	return [ x.value for x in m.outputs ]



def watch(n, c):

	csim = c.sim

	def sim():
		print("%s [%s]:" % (n, c.name))
		print("\tIN:")
		for i in c.inputs: print("\t\t%s = %x (%d)" % (i.ident(), i.value, i.value))
		print("\tOUT:")
		for i in c.outputs: print("\t\t%s = %x (%d)" % (i.ident(), i.value, i.value))
		if csim:
			csim()

	c.sim = sim
	return c


