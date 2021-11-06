

import pyhdl.core as core
import pyhdl.parts.memory as memory

from ..common import *



test_component(memory.emuram64k8(core.net(), core.net(), core.bus("A", 16), core.bus("DI", 8)),
	[
		[ True,  False, 0,     123 ],
		[ True,  False, 1,     42  ],
		[ True,  False, 65534, 69  ],
		[ True,  False, 65535, 55  ],
		[ False, True,  0,     0   ],
		[ False, True,  1,     1   ],
		[ False, True,  65534, 2   ],
		[ False, True,  65535, 3   ]

	],
	[
		[ 0   ],
		[ 0   ],
		[ 0   ],
		[ 0   ],
		[ 123 ],
		[ 42  ],
		[ 69  ],
		[ 55  ]
	]
)



test_component(memory.emuram64k16(core.net(), core.net(), core.bus("A", 16), core.bus("DI", 16)),
	[
		[ True,  False, 0,     123 ],
		[ True,  False, 1,     42  ],
		[ True,  False, 65534, 69  ],
		[ True,  False, 65535, 420 ],
		[ False, True,  0,     0   ],
		[ False, True,  1,     1   ],
		[ False, True,  65534, 2   ],
		[ False, True,  65535, 3   ]

	],
	[
		[ 0   ],
		[ 0   ],
		[ 0   ],
		[ 0   ],
		[ 123 ],
		[ 42  ],
		[ 69  ],
		[ 420 ]
	]
)



DATA = [
	[ 0, 0, 0 ],
	[ 1, 0, 0 ],
	[ 1, 0, 0 ],
	[ 0, 1, 0 ],
	[ 1, 0, 0 ],
	[ 0, 1, 0 ],
	[ 0, 1, 0 ],
	[ 1, 1, 0 ]
]

test_component(memory.rom(DATA, core.bus("R", 8), core.bus("D", 3)),
	[
		[ 0x00 ],
		[ 0x01 ],
		[ 0x02 ],
		[ 0x04 ],
		[ 0x08 ],
		[ 0x10 ],
		[ 0x20 ],
		[ 0x40 ],
		[ 0x80 ]
	],
	[
		[ 0x00 ],
		[ 0x00 ],
		[ 0x01 ],
		[ 0x01 ],
		[ 0x02 ],
		[ 0x01 ],
		[ 0x02 ],
		[ 0x02 ],
		[ 0x03 ]
	]
)

