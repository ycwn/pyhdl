

from pyhdl.core import *



@module("RAM64K8", [ "N", "N", "B16", "B8" ], [ "B8" ])
def ram64k8(s, c, a, di, do):

	rambank = [ 0 for n in range(1 << 16) ]

	def sim():
		if c.value:   do.value = rambank[a.value]
		elif s.value: rambank[a.value] = di.value

	def read(addr):
		return rambank[addr]

	def write(addr, val):
		rambank[addr] = val

	return { 'sim': sim, 'attrs': { 'read': read, 'write': write } }



@module("RAM64K16", [ "N", "N", "B16", "B16" ], [ "B16" ])
def ram64k16(wr, rd, a, di, do):

	rambank = [ 0 for n in range(1 << 16) ]

	def sim():
		if rd.value:
			do.value = rambank[a.value];

		elif wr.value:
			rambank[a.value] = di.value;

	def read(addr):
		return rambank[addr]

	def write(addr, val):
		rambank[addr] = val

	return { 'sim': sim, 'attrs': { 'read': read, 'write': write } }



@module("ROM64K16", [ "N", "N", "B16", "B16" ], [ "B16" ])
def rom64k16(wr, rd, a, di, do):

	rambank = [ 0 for n in range(1 << 16) ]

	def sim():
		if rd.value: do.value = rambank[a.value]

	def load(data):
		rambank[0:len(data)] = data

	return { 'sim': sim, 'attrs': { 'load': load } }



@module("MMIO16", [ "N", "N", "B16", "B16" ], [ "B16" ])
def mmio16(wr, rd, a, di, do):

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


