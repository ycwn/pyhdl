#!/usr/bin/env python3


import argparse
import sys


SRC_A   = 0x0000
SRC_PTR = 0x1000

DST_NOP = 0x0000
DST_A   = 0x0020
DST_D   = 0x0010
DST_PTR = 0x0008

OP_LABEL   = -1
OP_COMMENT = -2
OP_EQU     = -3
OP_ORG     = -4

OP_LDA  = 0x0000	#            LDA xxxx
OP_LDZ  = 0x8A00	#     0      LDZ A, D, @A
OP_LDO  = 0x8FC0	#     1      LDO A, D, @A
OP_LDN  = 0x8F00	#    -1      LDN A, D, @A
OP_STD  = 0x8300	#     D      STD A, D, @A
OP_STA  = 0x8C00	#     A      STA A, D, @A
OP_NOTD = 0x8340	#    ~D      NOTD A, D, @A
OP_NOTA = 0x8C40	#    ~A      NOTA A, D, @A
OP_NEGD = 0x83C0	#    -D      NEGD A, D, @A
OP_NEGA = 0x8CC0	#    -A      NEGA A, D, @A
OP_DECD = 0x8380	#    D-1     DECD A, D, @A
OP_INCD = 0x87C0	#    D+1     INCD A, D, @A
OP_DECA = 0x8C80	#    A-1     DECA A, D, @A
OP_INCA = 0x8DC0	#    A+1     INCA A, D, @A
OP_AND  = 0x8000	#    D&A     AND  A, D, @A
OP_ADD  = 0x8080	#    D+A     ADD  A, D, @A
OP_SUBA = 0x81C0	#    A-D     SUBA A, D, @A
OP_SUBD = 0x84C0	#    D-A     SUBD A, D, @A
OP_OR   = 0x8540	#    D|A     OR   A, D, @A

COND_NONE = 0x0000
COND_G    = 0x0001
COND_Z    = 0x0002
COND_GZ   = 0x0003
COND_L    = 0x0004
COND_NZ   = 0x0005
COND_LZ   = 0x0006
COND_JMP  = 0x0007

MASK_OP  = 0x8000
MASK_OPC = 0x8FC0
MASK_SRC = 0x1000
MASK_PFX = 0x0007


# List of conditional prefixes
COND_PREFIX = {
	'JG':  COND_G,
	'JZ':  COND_Z,  'JE':  COND_Z,
	'JGZ': COND_GZ, 'JGE': COND_GZ,
	'JL':  COND_L,
	'JNZ': COND_NZ, 'JNE': COND_NZ,
	'JLZ': COND_LZ, 'JLE': COND_LZ,
	'JMP': COND_JMP
}

# List on non-addressable opcodes
OP_NONADDR = {
	'LDZ':  OP_LDZ,  'LDO':  OP_LDO,  'LDN':  OP_LDN,  'STD':  OP_STD,
	'NOTD': OP_NOTD, 'NEGD': OP_NEGD, 'DECD': OP_DECD, 'INCD': OP_INCD
}

# List of addressable opcodes
OP_ADDR = {
	'STA':  OP_STA,  'NOTA': OP_NOTA, 'NEGA': OP_NEGA, 'DECA': OP_DECA,
	'INCA': OP_INCA, 'AND':  OP_AND,  'ADD':  OP_ADD,  'SUBA': OP_SUBA,
	'SUBD': OP_SUBD, 'OR':   OP_OR
}



def pwarn(msg):
	sys.stderr.write("hackasm: ")
	sys.stderr.write(msg)
	sys.stderr.write("\n")
	sys.stderr.flush()



def perror(msg):
	pwarn(msg)
	sys.exit(1)



def passert(cond, msg):
	if not cond: perror(msg)



def parse_command_line():

	argp = argparse.ArgumentParser(description="HACK16 Assembler")
	argp.add_argument('-o',  '--output',      type=str,            help='Set output file')
	argp.add_argument('-d',  '--disassemble', action='store_true', help='Disassemble the source')
	argp.add_argument('-v',  '--verbose',     action='store_true', help='Preserve the source as comments')
	argp.add_argument('source')

	argv = argp.parse_args()

	if not argv.output:
		if argv.source != '-':
			extension   = ".asm" if argv.disassemble else ".bin"
			argv.output = (argv.source[:argv.source.rindex('.')] if '.' in argv.source else argv.source) + extension

		else:
			argv.output = "-"

	return argv



def assembler_parse_source(source, verbose):

	opcodes = []

	with open(source if source != '-' else "/dev/stdin", 'r') as asm:
		for lineno, line in enumerate(asm):

			if verbose:
				opcodes.append([ OP_COMMENT, line.strip() ])

			if ';' in line:
				line = line[:line.index(';')]

			if ':' in line:
				sep = line.index(':')
				opcodes.append([ OP_LABEL, line[:sep].strip() ])
				line = line[sep+1:]

			line = line.strip()

			if line == "":
				continue


			space   = line.index(' ') if ' ' in line else len(line)
			pfxname = ""
			prefix  = COND_NONE
			opcode  = line[:space].upper()
			line    = line[space+1:].strip()
			args    = []
			src_reg = SRC_A
			dst_reg = DST_NOP


			if opcode in COND_PREFIX:
				space   = line.index(' ') if ' ' in line else len(line)
				pfxname = opcode
				prefix  = COND_PREFIX[opcode]
				opcode  = line[:space].upper()
				line    = line[space+1:].strip()

			if opcode == "":
				passert(prefix == COND_JMP,
					"%s:%d: Conditional prefix %s can't be used on its own" %
					(source, lineno + 1, pfxname)
				)
				opcode = "LDZ"


			if opcode[-1] == '@':
				opcode  = opcode[:-1]
				src_reg = SRC_PTR


			if line != "":
				args = [ x.strip() for x in line.split(',') ]


			if opcode == "LDA":

				passert(prefix == COND_NONE,
					"%s:%d: Conditional prefix %s can't be used with LDA opcode" %
					(source, lineno + 1, pfxname)
				)
				passert(len(args) == 1,
					"%s:%d: LDA requires exactly one argument" %
					(source, lineno + 1)
				)

				val = args[0]

				if "'" in val:
					passert(len(val) == 3 and val[0] == "'" and val[-1] == "'",
						"%s:%d: Invalid literal (%s)" %
						(source, lineno + 1, val)
					)
					val = ord(val[1])

				else:
					try:
						val = int(val, 0)
						passert(val >= 0 and val < 32768,
							"%s:%d: Integer literal (%d) out of range 0-32768" %
							(source, lineno + 1, val)
						)
					except:
						pass

				opcodes.append([ OP_LDA, val ])


			elif opcode == "DB":

				passert(prefix == COND_NONE,
					"%s:%d: Conditional prefix %s can't be used with DB opcode" %
					(source, lineno + 1, pfxname)
				)
				passert(len(args) >= 1,
					"%s:%d: DB expects at least one argument" %
					(source, lineno + 1)
				)

				for arg in args:

					if "'" in arg:
						passert(len(arg) == 3 and arg[0] == "'" and arg[-1] == "'",
							"%s:%d: Invalid literal (%s)" %
							(source, lineno + 1, arg)
						)
						opcodes.append([ ord(arg[1]), 0 ])

					elif '"' in arg:
						passert(len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"',
							"%s:%d: Invalid string (%s)" %
							(source, lineno + 1, arg)
						)
						for ch in bytes(arg[1:-1], 'utf-8'):
							opcodes.append([ ch, 0 ])

					else:
						try:
							val = int(arg, 0)
							passert(val >= 0 and val < 256,
								"%s:%d: Integer literal (%s) out of range 0-255" %
								(source, lineno + 1, arg)
							)
							opcodes.append([ val, 0 ])
						except:
							passert(False,
								"%s:%d: Invalid integer literal (%s)" %
								(source, lineno + 1, arg)
							)


			elif opcode == "DW":

				passert(prefix == COND_NONE,
					"%s:%d: Conditional prefix %s can't be used with DW opcode" %
					(source, lineno + 1, pfxname)
				)
				passert(len(args) >= 1,
					"%s:%d: DW expects at least one argument" %
					(source, lineno + 1)
				)

				for arg in args:

					if "'" in arg:
						passert(len(arg) >= 3 and len(arg) < 5 and arg[0] == "'" and arg[-1] == "'",
							"%s:%d: Invalid literal (%s)" %
							(source, lineno + 1, arg)
						)
						opcodes.append([
							sum([ (1 << (8*n)) * ord(x)
								for n, x in enumerate(arg[1:-1])
							]), 0
						])

					elif '"' in arg:
						passert(len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"',
							"%s:%d: Invalid string (%s)" %
							(source, lineno + 1, arg)
						)
						for ch in bytes(arg[1:-1], 'utf-16')[2:]:
							opcodes.append([ ch, 0 ])

					else:
						try:
							val = int(arg, 0)
							passert(val >= 0 and val < 65536,
								"%s:%d: Integer literal (%s) out of range 0-65535" %
								(source, lineno + 1, arg)
							)
							opcodes.append([ val, 0 ])
						except:
							passert(False,
								"%s:%d: Invalid integer literal (%s)" %
								(source, lineno + 1, arg)
							)

			else:
				op = 0

				if opcode in OP_NONADDR:
					passert(src_reg == SRC_A,
						"%s:%d: %s can't be used in dereference mode" %
						(source, lineno + 1, arg)
					)
					op = OP_NONADDR[opcode]

				elif opcode in OP_ADDR:
					op = OP_ADDR[opcode]

				else:
					passert(False,
						"%s:%d: Invalid opcode '%s'" %
						(source, lineno + 1, opcode)
					)


				for arg in args:
					if   arg == 'A'  or arg == 'a':  dst_reg = dst_reg | DST_A
					elif arg == 'D'  or arg == 'd':  dst_reg = dst_reg | DST_D
					elif arg == '@A' or arg == '@a': dst_reg = dst_reg | DST_PTR
					else:
						passert(False,
							"%s:%d: Invalid destination '%s'" %
							(source, lineno + 1, arg)
						)


				opcodes.append([ op, prefix | src_reg | dst_reg ])

	return opcodes



def assembler_patch_labels(codes):

	labels  = {}
	opcodes = []

	addr = 0

	for op, arg in codes:
		if op == OP_LABEL:
			passert(not arg in labels, "Label '%s' already defined" % arg)
			labels[arg] = addr

		elif op == OP_COMMENT: pass
		elif op == OP_EQU:     pass
		elif op == OP_ORG:     pass

		else:
			addr += 1

	for op, arg in codes:
		if op == OP_LABEL:
			continue

		if op == OP_LDA and isinstance(arg, str):
			passert(arg in labels, "Undefined label '%s'" % arg)
			arg = labels[arg]

		opcodes.append([ op, arg ])

	return opcodes



def assembler_generate(output, opcodes):

	with open(output if output != '-' else "/dev/stdout", 'w') as rom:
		for op, arg in opcodes:

			if   op == OP_LABEL: pass
			elif op == OP_EQU:   pass
			elif op == OP_ORG:   pass

			elif op == OP_COMMENT:
				rom.write("%s%s\n" % ("; " if len(arg) > 0 and arg[0] != ';' else "", arg))

			else:
				rom.write("\t0x%04x\n" % (op | arg))



def assembler_compile(src, out, verbose):

	opcodes = assembler_parse_source(src, verbose)
	opcodes = assembler_patch_labels(opcodes)

	assembler_generate(out, opcodes)



def disassembler_parse(source, verbose):

	opcodes = []

	with open(source if source != '-' else "/dev/stdin", 'r') as rom:
		for lineno, line in enumerate(rom):

			if verbose:
				opcodes.append([ OP_COMMENT, line.strip() ])

			if ';' in line:
				line = line[:line.index(';')]

			line = line.strip()

			if line != "":
				try:
					opcodes.append([ int(line, 0), 0 ])

				except:
					passert(False,
						"%s:%d: Invalid opcode '%s'" %
						(source, lineno + 1, line)
					)

	return opcodes



def disassembler_generate(output, opcodes):

	with open(output if output != '-' else "/dev/stdout", 'w') as asm:
		for op, arg in opcodes:

			if op == OP_COMMENT:
				asm.write("%s%s\n" % ("; " if len(arg) > 0 and arg[0] != ';' else "", arg))
				continue

			prefix = ""
			opcode = ""
			srcptr = False
			args   = []

			if op & MASK_OP:

				for pfx, num in COND_PREFIX.items():
					if num == op & MASK_PFX:
						prefix = pfx

				for opc, num in { **OP_ADDR, **OP_NONADDR }.items():
					if num == op & MASK_OPC:
						opcode = opc

				if op & MASK_SRC: srcptr = True
				if op & DST_A:    args.append("A")
				if op & DST_D:    args.append("D")
				if op & DST_PTR:  args.append("@A")

			else:
				opcode = "LDA"
				args   = [ "0x%04x" % op ]

			if opcode == "":
				prefix = ""
				opcode = "DW"
				srcptr = False
				args   = [ "0x%04x" % op ]

			if prefix == "JMP" and opcode == "LDZ" and len(args) == 0:
				opcode = ""


			asm.write("\t%s%s%s%s%s%s\n" % (
				prefix,
				" " if prefix else "",
				opcode,
				"^" if srcptr else "",
				" " if len(args) > 0 else "",
				", ".join(args))
			)



def disassembler_decompile(src, out, verbose):
	opcodes = disassembler_parse(src, verbose)
	disassembler_generate(out, opcodes)



argv = parse_command_line()

if argv.disassemble:
	disassembler_decompile(argv.source, argv.output, argv.verbose)

else:
	assembler_compile(argv.source, argv.output, argv.verbose)

