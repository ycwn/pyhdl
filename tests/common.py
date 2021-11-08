

import pyhdl.core as core


test_results = []



def test_component(instance, inputs, outputs):

	print()
	print("Component: %s" % instance.name)
	print("\t%s\t|\t%s" % (
		"\t".join([ x.ident() for x in instance.inputs ]),
		"\t".join([ x.ident() for x in instance.outputs ])))
	print("%s|%s" % ("--------" * (len(inputs[0]) + 1), "--------" * (len(outputs[0]) + 1)))

	fail    = 0
	success = 0

	for n in range(len(inputs)):

		out = core.util.simulate(instance, inputs[n])
		ok  = all([ x == y for x,y in zip(out, outputs[n])])

		if ok: success += 1
		else:  fail += 1

		print("%s\t|%s\t[ %s ]" % (
			"".join([ "\t" + str(int(x)) for x in inputs[n] ]),
			"".join([ "\t" + str(int(x)) for x in out ]),
			"\033[1;32m OK \033[0m" if ok else "\033[1;31mFAIL\033[0m"
			))

	test_results.append([ instance.name, success, fail ])




def test_report():

	print()
	print()
	print("      Component      Success      Fail")
	print("  ----------------------------------------")

	total_s = 0
	total_f = 0
	failed  = []

	for n, s, f in test_results:

		total_s += s
		total_f += f

		print("      %-11s    %4d        %4d" % (n, s, f))

		if f > 0:
			failed.append(n)

	print()
	print("Components tested: %d" % len(test_results))
	print("Successful cases:  %d" % total_s)
	print("Failed cases:      %d" % total_f)

	if len(failed) > 0:
		print("Components failed:")
		for n in failed:
			print("\t%s" % n)

	print()
	print()

