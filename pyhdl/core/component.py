

import inspect

from .net import *
from .bus import *


class component:

	name    = ""
	inputs  = []
	outputs = []
	subs    = []
	emit    = None
	sim     = None



	def __init__(self, name, inputs, outputs, subs, emit, sim, attrs):

		self.name    = name
		self.inputs  = inputs
		self.outputs = outputs
		self.subs    = subs
		self.emit    = emit
		self.sim     = sim

		for k,v in attrs.items():
			setattr(self, k, v)



	def visit(self, enter, leave):

		if enter:
			enter(self)

		for sub in self.subs:
			sub.visit(enter, leave)

		if leave:
			leave(self)



def module(name, inputs, outputs):

	def generate_component(builder):

		def build_component(*args):

			# Check the arguments and see if we have enough inputs
			if len(args) < len(inputs):
				raise Exception("Module %s used with wrong number of inputs: Expected %d, got %d" % (name, len(inputs), len(args)))

			net_in  = list(args[0:len(inputs)])
			net_out = list(args[len(inputs):])

			# Check and see if we have too many outputs
			# Outputs are optional, so we don't care if some are missing
			if len(net_out) > len(outputs):
				raise Exception("Module %s used with wrong number of outputs: Expected %d at most, got %d" % (name, len(outputs), len(conn_out)))

			# Generate temporary outputs for the missing ones
			for n in range(len(net_out), len(outputs)):
				if   outputs[n]    == "N": net_out.append(net())
				elif outputs[n][0] == "B": net_out.append(bus("", int(outputs[n][1:])))

			# Now call the builder to generate the description,
			# which can either be a list of subcomponents, or
			# a dict containing a function to emit the component,
			# a function to simulate it, a list of subcomponents
			# and a list of optional attributes to set
			net_io  = net_in  + net_out
			net_oi  = net_out + net_in
			desc    = builder(*net_io)
			subs    = []
			emit    = None
			sim     = None
			attrs   = {}

			if isinstance(desc, dict):
				if 'subs'  in desc: subs  = desc['subs']
				if 'emit'  in desc: emit  = desc['emit']
				if 'sim'   in desc: sim   = desc['sim']
				if 'attrs' in desc: attrs = desc['attrs']

			else:
				subs = desc

			iomap = {
				arg: net_io[argn] for argn, arg in enumerate(inspect.signature(builder).parameters)
			}

			# Generate a default emitter if one was not supplied
			if emit == None:
				emit = lambda: "; COMPONENT %s(%s)" % (
						name,
						", ".join([ conn.ident() for conn in net_oi ])
					)
			# Generate the component
			return component(name, net_in, net_out, subs, emit, sim, { **iomap, **attrs })



		def create():

			argv = []

			for argn, argt in zip(inspect.signature(builder).parameters, inputs + outputs):
				if   argt    == "N": argv.append(net(argn))
				elif argt[0] == "B": argv.append(bus(argn.upper(), int(argt[1:])))

			return build_component(*argv)



		setattr(build_component, 'name',    name)
		setattr(build_component, 'args',    list(inspect.signature(builder).parameters))
		setattr(build_component, 'inputs',  inputs)
		setattr(build_component, 'outputs', outputs)
		setattr(build_component, 'create',  create)

		return build_component

	return generate_component

