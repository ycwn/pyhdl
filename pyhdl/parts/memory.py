

from pyhdl.core import *



@module("EMURAM64K8", [ "N", "N", "B16", "B8" ], [ "B8" ])
def emuram64k8(s, c, a, di, do):

	memory = [ 0 for n in range(1 << 16) ]

	def sim():
		if c.value:   do.value = memory[a.value]
		elif s.value: memory[a.value] = di.value

	def read(addr):
		return memory[addr]

	def write(addr, val):
		memory[addr] = val

	return { 'sim': sim, 'attrs': { 'read': read, 'write': write } }



@module("EMURAM64K16", [ "N", "N", "B16", "B16" ], [ "B16" ])
def emuram64k16(wr, rd, a, di, do):

	memory = [ 0 for n in range(1 << 16) ]

	def sim():
		if rd.value:
			do.value = memory[a.value];

		elif wr.value:
			memory[a.value] = di.value;

	def read(addr):
		return memory[addr]

	def write(addr, val):
		memory[addr] = val

	return { 'sim': sim, 'attrs': { 'read': read, 'write': write } }



@module("EMUROM64K16", [ "N", "N", "B16", "B16" ], [ "B16" ])
def emurom64k16(wr, rd, a, di, do):

	memory = [ 0 for n in range(1 << 16) ]

	def sim():
		if rd.value:
			do.value = memory[a.value]

	def load(data):
		memory[0:len(data)] = data

	return { 'sim': sim, 'attrs': { 'load': load } }



@module("EMUMMIO16", [ "N", "N", "B16", "B16" ], [ "B16" ])
def emummio16(wr, rd, a, di, do):

	rd_f = None
	wr_f = None

	def sim():
		if rd.value and rd_f: do.value = rd_f(a.value)
		if wr.value and wr_f: wr_f(a.value, di.value)

	def set_rd(r):
		nonlocal rd_f
		rd_f = r

	def set_wr(w):
		nonlocal wr_f
		wr_f = w

	return { 'sim': sim, 'attrs': { 'read': set_rd, 'write': set_wr } }


