

from .net import *


class bus:

	nets = []
	name = None



	def __init__(self, width, **kwargs):
		self.name = kwargs['name'] if 'name' in kwargs else ""
		self.nets = [ net(self.name, bit) for bit in range(width) ]



	def __getitem__(self, n):

		subnets = self.nets[n]

		if isinstance(subnets, list):
			subbus = bus(0) if self.name is None else bus(0, name=self.name)
			subbus.nets = subnets
			return subbus

		else:
			return subnets



	def bundle(*args, **kwargs):

		b = bus(0, **kwargs)

		def collect(argv):
			for arg in argv:
				if   isinstance(arg, net): b.nets.append(arg)
				elif isinstance(arg, bus): b.nets += arg.nets
				else:
					argw = []
					try:    argw = list(arg)
					except: pass

					if len(argw) == 0:
						raise Exception("Can't add a %s to a bus" % type(arg))

					collect(argw)

		collect(args)
		return b



	def repl(wire, width, **kwargs):
		return bus.bundle([ wire ] * width, **kwargs)



	@property
	def width(self):
		return len(self.nets)



	@property
	def value(self):
		val = 0
		for k, net in enumerate(self.nets):
			if net.value:
				val += 1 << k
		return val



	@value.setter
	def value(self, val):
		for k, net in enumerate(self.nets):
			net.value = val & (1 << k) != 0



	def ident(self):
		return "%s%d:%d" % (self.name, 0, len(self.nets) - 1)



	def netnames(self):
		return [ net.ident() for net in self.nets ]

