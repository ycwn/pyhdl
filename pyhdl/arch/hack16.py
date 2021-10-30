

from pyhdl.core import *

from pyhdl.parts.logic   import *
from pyhdl.parts.logic4  import *
from pyhdl.parts.logic16 import *
from pyhdl.parts.memory  import *
from pyhdl.parts.clock   import *



@module("UNALU16", [ "N", "N", "B16" ], [ "B16" ])
def unalu16(z, n, x, y):

	zr0 = not1(z)
	zr1 = and16s(x, zr0.outputs[0])
	neg = xor16s(zr1.outputs[0], n, y)

	return [ zr0, zr1, neg ]



@module("ALU16", [ "N", "N", "N", "N", "N", "N", "B16", "B16" ], [ "B16" ])
def alu16(zx, nx, zy, ny, f, no, x, y, z):

	xx = unalu16(zx, nx, x)
	yy = unalu16(zy, ny, y)

	op_and = and16(xx.outputs[0], yy.outputs[0])
	op_add = adc16(xx.outputs[0], yy.outputs[0], zero)

	op = mux16(f, op_and.outputs[0], op_add.outputs[0])
	zz = xor16s(op.outputs[0], no, z)

	return [ xx, yy, op_and, op_add, op, zz ]



@module("CMP16", [ "N", "N", "N", "B16" ], [ "N" ])
def cmp16(lt, eq, gt, x, c):

	ltz = ltz16(x)
	eqz = eqz16(x)

	leqz = or1(ltz.outputs[0], eqz.outputs[0])
	gtz  = not1(leqz.outputs[0])

	clt = and1(ltz.outputs[0], lt)
	ceq = and1(eqz.outputs[0], eq)
	cgt = and1(gtz.outputs[0], gt)

	c0 = or1(clt.outputs[0], ceq.outputs[0])
	c1 = or1(c0.outputs[0],  cgt.outputs[0], c)

	return [ ltz, eqz, leqz, gtz, clt, ceq, cgt, c0, c1 ]



@module("INDEC16", [ "B16" ], [ "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "B16" ])
def indec16(x, ci, sm, zx, nx, zy, ny, f, no, a, d, da, lt, eq, gt, w):

	m_i = ltz16(x, ci)
	m_d = not1(m_i.outputs[0])

	iw = and16s(x, m_i.outputs[0])

	o_sm = buf1(iw.outputs[0][12], sm)
	o_zx = buf1(iw.outputs[0][11], zx)
	o_nx = buf1(iw.outputs[0][10], nx)
	o_zy = buf1(iw.outputs[0][ 9], zy)
	o_ny = buf1(iw.outputs[0][ 8], ny)
	o_f  = buf1(iw.outputs[0][ 7], f)
	o_no = buf1(iw.outputs[0][ 6], no)

	o_a  = or1( iw.outputs[0][5], m_d.outputs[0], a)
	o_d  = buf1(iw.outputs[0][4], d)
	o_da = buf1(iw.outputs[0][3], da)

	o_lt = buf1(iw.outputs[0][2], lt)
	o_eq = buf1(iw.outputs[0][1], eq)
	o_gt = buf1(iw.outputs[0][0], gt)

	o_w = and16s(x, m_d.outputs[0], w)

	return [ m_i, m_d, iw, o_sm, o_zx, o_nx, o_zy, o_ny, o_f, o_no, o_a, o_d, o_da, o_lt, o_eq, o_gt, o_w ]



@module("CPU16", [ "N", "B16", "B16" ], [ "N", "N", "B16", "B16", "B16" ])
def cpu16(c, iw, di, wr, rd, pc, a, do):

	alu_x = bus("X", 16)
	alu_y = bus("Y", 16)

	indec = indec16(iw)

	bwr = and1(indec.outputs[10], c, wr)
	brd = buf1(c, rd)

	alu = alu16(
		indec.outputs[2], indec.outputs[3], # zx, nx
		indec.outputs[4], indec.outputs[5], # zy, ny
		indec.outputs[6], indec.outputs[7], # f,  no
		alu_x, alu_y)

	mem_wr = mux16(indec.outputs[0], indec.outputs[14], alu.outputs[0], do)

	reg_a = reg16(indec.outputs[8], c, do, a)
	reg_d = reg16(indec.outputs[9], c, do, alu_x)

	mem_rd = mux16(indec.outputs[1], a, di, alu_y)

	jcmp = cmp16(indec.outputs[11], indec.outputs[12], indec.outputs[13], alu.outputs[0])
	pctr = ctr16(jcmp.outputs[0], c, a, pc)

	return [ indec, bwr, brd, alu, mem_wr, reg_a, reg_d, mem_rd, jcmp, pctr ]



@module("HACK16", [], [])
def hack16():

	wr = net("WR")
	rd = net("RD")

	i  = bus("I",  16)
	pc = bus("P",  16)
	a  = bus("A",  16)
	di = bus("DI", 16)
	do = bus("DO", 16)

	clk = clock()

	cpu = cpu16(clk.outputs[0], i, di, wr, rd, pc, a, do)
	sel = sel4(a[12], a[13], a[14], a[15])
	io  = buf1(sel.outputs[15])
	mem = not1(sel.outputs[15])

	mem_wr = and1(wr, mem.outputs[0])
	mem_rd = and1(rd, mem.outputs[0])

	io_wr = and1(wr, io.outputs[0])
	io_rd = and1(rd, io.outputs[0])

	ram  = ram64k16(mem_wr.outputs[0], mem_rd.outputs[0], a, do, di)
	rom  = rom64k16(zero, clk.outputs[0], pc, i, i)
	mmio = mmio16(io_wr.outputs[0], io_rd.outputs[0], a, do, di)

	return {
		'subs':[
			clk, cpu, sel, io, mem, mem_wr, mem_rd, io_wr, io_rd, ram, rom, mmio
		],
		'attrs': {
			'clk':  clk,
			'rom':  rom,
			'ram':  ram,
			'mmio': mmio
		}
	}


