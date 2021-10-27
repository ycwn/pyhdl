#!/usr/bin/env python3


import sys
import argparse
import os

sys.path.insert(0, os.getcwd())

from pyhdl.core        import *
from pyhdl.arch.hack16 import *



def pwarn(msg):
	sys.stderr.write("hacksim: ")
	sys.stderr.write(msg)
	sys.stderr.write("\n")
	sys.stderr.flush()



def perror(msg):
	pwarn(msg)
	sys.exit(1)



def passert(cond, msg):
	if not cond: perror(msg)



def parse_command_line():

	argp = argparse.ArgumentParser(description="HACK16 Simulator")
	argp.add_argument('-c',  '--cycles',  type=int, help='Max cycles to run')
	argp.add_argument('rom')

	argv = argp.parse_args()

	if not argv.cycles:
		argv.cycles = 0

	return argv



def parse_rom(rom):

	opcodes = []

	with open(rom if rom != '-' else "/dev/stdin", 'r') as code:
		for lineno, line in enumerate(code):

			if ';' in line:
				line = line[:line.index(';')]

			line = line.strip()

			if line != "":
				try:
					opcodes.append(int(line, 0))

				except:
					passert(False,
						"%s:%d: Invalid opcode '%s'" %
						(rom, lineno + 1, line)
					)

	return opcodes



argv = parse_command_line()
rom  = parse_rom(argv.rom)

hack = hack16()

hack.rom.load(rom)
hack.mmio.write(lambda a, d: sys.stdout.write(chr(d & 255)))

if argv.cycles > 0:

	for n in range(argv.cycles):
		simulate(hack, [])

else:
	while True:
		simulate(hack, [])

