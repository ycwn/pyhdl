

from .net import *


class bus:

	nets = []
	name = ""



	def __init__(self, name, width):
		self.name = name
		self.nets = [ net(name, bit) for bit in range(width) ]



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

