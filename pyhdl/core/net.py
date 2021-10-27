

net_tmp_name  = "tmp"
net_tmp_index = 0


class net:

	name  = None
	index = 0

	_value = False



	def __init__(self, name=None, index=0):

		if name:
			self.name  = name
			self.index = index

		else:
			global net_tmp_name
			global net_tmp_index

			self.name  = net_tmp_name
			self.index = net_tmp_index

			net_tmp_index += 1



	@property
	def value(self):    return self._value



	@value.setter
	def value(self, v): self._value = bool(v)



	def ident(self):
		return "%s%d" % (self.name, self.index)

