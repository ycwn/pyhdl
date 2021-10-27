

import pyhdl.core as core
import pyhdl.arch.hack16 as h16

from ..common import *



test_component(h16.unalu16(core.net(), core.net(), core.bus("A", 16)),
	[
		[ False,  False, 0     ],
		[ False,  True,  0     ],
		[ True,   False, 0     ],
		[ True,   True,  0     ],
		[ False,  False, 27    ],
		[ False,  True,  27    ],
		[ True,   False, 27    ],
		[ True,   True,  27    ],
		[ False,  False, 65535 ],
		[ False,  True,  65535 ]
	],
	[
		[ 0     ],
		[ 65535 ],
		[ 0     ],
		[ 65535 ],
		[ 27    ],
		[ 65508 ],
		[ 0     ],
		[ 65535 ],
		[ 65535 ],
		[ 0     ]
	]
)



test_component(h16.alu16(core.net(), core.net(), core.net(), core.net(), core.net(), core.net(), core.bus("X", 16), core.bus("Y", 16)),
	[
		[ True,  False, True,  False, False, False, 27, 65532 ],
		[ True,  True,  True,  True,  True,  True,  27, 65532 ],
		[ True,  True,  True,  False, True,  False, 27, 65532 ],
		[ False, False, True,  True,  False, False, 27, 65532 ],
		[ True,  True,  False, False, False, False, 27, 65532 ],
		[ False, False, True , True,  False, True,  27, 65520 ],
		[ True,  True,  False, False, False, True,  27, 65520 ],
		[ False, False, True,  True,  True,  True,  27, 65532 ],
		[ True,  True,  False, False, True,  True,  27, 65532 ],
		[ False, True,  True,  True,  True,  True,  27, 65532 ]
	],
	[
		[ 0     ],
		[ 1     ],
		[ 65535 ],
		[ 27    ],
		[ 65532 ],
		[ 65508 ],
		[ 15    ],
		[ 65509 ],
		[ 4     ],
		[ 28    ]
	]
)



test_component(h16.cmp16(core.net(), core.net(), core.net(), core.bus("A", 16)),
	[
		[ False, False, False, 0     ],
		[ False, False, False, 1     ],
		[ False, False, False, 2     ],
		[ False, False, False, 65535 ],
		[ True,  True,  True,  0     ],
		[ True,  True,  True,  1     ],
		[ True,  True,  True,  2     ],
		[ True,  True,  True,  65535 ],
		[ False, False, True,  0     ],
		[ False, False, True,  1     ]
	],
	[
		[ False ],
		[ False ],
		[ False ],
		[ False ],
		[ True  ],
		[ True  ],
		[ True  ],
		[ True  ],
		[ False ],
		[ True  ]
	]
)



test_component(h16.indec16(core.bus("A", 16)),
	[
		[ 61408 ],
		[ 57368 ],
		[ 64550 ],
		[ 1234  ]
	],
	[
		[ True,  False, True,  True,  True,  True,  True,  True,  True,  False, False, False, False, False, 0    ],
		[ True,  False, False, False, False, False, False, False, False, True,  True,  False, False, False, 0    ],
		[ True,  True,  True,  True,  False, False, False, False, True,  False, False, True,  True,  False, 0    ],
		[ False, False, False, False, False, False, False, False, True,  False, False, False, False, False, 1234 ]
	]
)

