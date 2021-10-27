

import pyhdl.core as core



def test_component(what, inputs, outputs):

	print("Component: %s" % what.name)
	print("%s\t|%s" % (
		"".join([ "\t"  + chr(x + 65) for x in range(len(inputs[0])) ]),
		"".join([ "\tX" + str(x)      for x in range(len(outputs[0])) ])))
	print("%s|%s" % ("--------" * (len(inputs[0]) + 1), "--------" * (len(outputs[0]) + 1)))

	for n in range(len(inputs)):

		out = core.util.simulate(what, inputs[n])
		ok  = all([ x == y for x,y in zip(out, outputs[n])])

		print("%s\t|%s\t[ %s ]" % (
			"".join([ "\t" + str(int(x)) for x in inputs[n] ]),
			"".join([ "\t" + str(int(x)) for x in out ]),
			"\033[1;32m OK \033[0m" if ok else "\033[1;31mFAIL\033[0m"
			))

	print()

