#!/usr/bin/env python3


import argparse
import importlib
import sys



def pwarn(msg):
	sys.stderr.write("vlogc: ")
	sys.stderr.write(msg)
	sys.stderr.write("\n")
	sys.stderr.flush()



def perror(msg):
	pwarn(msg)
	sys.exit(1)



def passert(cond, msg):
	if not cond: perror(msg)



def parse_command_line():

	argp = argparse.ArgumentParser(description="Verilog Transpiler")
	argp.add_argument('-o',  '--output',                       type=str, help='Set output file')
	argp.add_argument('-I',  '--include', action='append',     type=str, help='Append to include search path')
	argp.add_argument('-v',  '--verbose', action='store_true',           help='Preserve the source as comments')
	argp.add_argument('modules', nargs=argparse.REMAINDER)

	argv = argp.parse_args()

	if not argv.output:  argv.output  = 'a.out.v'
	if not argv.include: argv.include = []

	return argv



def process_module(instance, verbose):

	inputs  = [ net for i in instance.inputs  for net in i.netnames() ]
	outputs = [ net for o in instance.outputs for net in o.netnames() ]
	nets    = []
	gates   = []


	def vlog_emit(part):

		nonlocal nets
		nonlocal gates

		if part.name == 'NAND':

			gate = [ 'nand' ]

			for ios in part.outputs + part.inputs:
				for net in ios.netnames():
					gate.append(net)
					if net not in nets and net not in outputs and net not in inputs:
						nets.append(net)

			gates.append(gate)

		else:
			gates.append([ '// ' + part.emit() ])


	outputs = "output " + ", ".join(outputs) if len(instance.outputs) > 0 else ""
	inputs  = "input "  + ", ".join(inputs)  if len(instance.inputs)  > 0 else ""
	sep     = ", " if len(outputs) > 0 and len(inputs) > 0 else ""

	instance.visit(vlog_emit, None)

	yield "module %s(%s%s%s);" % (instance.name, outputs, sep, inputs)
	yield ""

	for n in nets:
		yield "\twire %s;" % n

	yield ""

	index = 0

	for gate in gates:
		if gate[0] == 'nand':
			yield "\t%s g%d(%s);" % (gate[0], index, ", ".join(gate[1:]))
			index += 1

		elif verbose:
			yield gate[0]

	yield ""
	yield "endmodule"



def gather_modules(module_names):

	modules = []

	for module_name in module_names:

		if not '.' in module_name:
			perror("Invalid module name '%s'" % module_name)

		dot     = module_name.rindex('.')
		libname = module_name[:dot]
		modname = module_name[dot+1:]

		try:    lib = importlib.import_module(libname)
		except: perror("Unable to import '%s'" % libname)

		try:    mod = getattr(lib, modname)
		except: perror("There is no module '%s' in '%s'" % (modname, libname))

		try:    modules.append(mod.create())
		except: perror("Failed to create an instance of '%s'" % module_name)

	return modules



def compile_modules(modules, output, verbose):

	with open(output if output != '-' else "/dev/stdout", 'w') as vlog:

		for module in modules:

			vlog.write("\n")
			vlog.write("\n")

			for line in process_module(module, verbose):
				vlog.write(line)
				vlog.write("\n")

			vlog.write("\n")
			vlog.write("\n")



argv      = parse_command_line()
sys.path += argv.include


modules = gather_modules(argv.modules)
compile_modules(modules, argv.output, argv.verbose)

