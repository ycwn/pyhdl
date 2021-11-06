

import pyhdl.core as core
import pyhdl.parts.logic16 as logic

from ..common import *



test_component(logic.not16(core.bus("A", 16)),
	[
		[ 0 ], [ 1 ], [ 65534 ], [ 65535 ],
	],
	[
		[ 65535 ], [ 65534 ], [ 1 ], [ 0 ]
	]
)



test_component(logic.mux16(core.net(), core.bus("A", 16), core.bus("B", 16)),
	[
		[ False, 420, 69 ], [ True, 420, 69 ]
	],
	[
		[ 420 ], [ 69 ]
	]
)



test_component(logic.adc16(core.bus("A", 16), core.bus("B", 16), core.net()),
	[
		[ 10,    15, False ],
		[ 65535, 0,  False ],
		[ 65534, 0,  True  ],
		[ 65535, 0,  True  ]
	],
	[
		[ 25,    False ],
		[ 65535, False ],
		[ 65535, False ],
		[ 0,     True  ]
	]
)



test_component(logic.inc16(core.bus("A", 16), core.net()),
	[
		[ 0, True ], [ 1, True ], [ 65534, True ], [ 65535, True ],
	],
	[
		[ 1 ], [ 2 ], [ 65535 ], [ 0 ]
	]
)



test_component(logic.sub16(core.bus("A", 16), core.bus("B", 16)),
	[
		[ 0,     0      ],
		[ 1,     0      ],
		[ 1,     1      ],
		[ 1,     2      ],
		[ 1,     3      ],
		[ 2,     2      ],
		[ 4,     2      ],
		[ 32768, 32768  ],
		[ 32768, 32770  ]
	],
	[
		[ 0     ],
		[ 1     ],
		[ 0     ],
		[ 65535 ],
		[ 65534 ],
		[ 0     ],
		[ 2     ],
		[ 0     ],
		[ 65534 ]
	]
)



test_component(logic.eqz16(core.bus("A", 16)),
	[
		[ 0       ],
		[ 1 <<  0 ], [ 1 <<  1 ], [ 1 <<  2 ], [ 1 <<  3 ],
		[ 1 <<  4 ], [ 1 <<  5 ], [ 1 <<  6 ], [ 1 <<  7 ],
		[ 1 <<  8 ], [ 1 <<  9 ], [ 1 << 10 ], [ 1 << 11 ],
		[ 1 << 12 ], [ 1 << 13 ], [ 1 << 14 ], [ 1 << 15 ]
	],
	[
		[ True  ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ]
	]
)



test_component(logic.ltz16(core.bus("A", 16)),
	[
		[ 0       ],
		[ 1 <<  0 ], [ 1 <<  1 ], [ 1 <<  2 ], [ 1 <<  3 ],
		[ 1 <<  4 ], [ 1 <<  5 ], [ 1 <<  6 ], [ 1 <<  7 ],
		[ 1 <<  8 ], [ 1 <<  9 ], [ 1 << 10 ], [ 1 << 11 ],
		[ 1 << 12 ], [ 1 << 13 ], [ 1 << 14 ], [ 1 << 15 ]
	],
	[
		[ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ True  ]
	]
)



test_component(logic.reg16(core.net(), core.net(), core.bus("A", 16)),
	[
		[ True,  False, 0   ],
		[ True,  False, 42  ],
		[ False, True,  0   ],
		[ False, False, 1   ],
		[ False, True,  2   ],
		[ True,  False, 69  ],
		[ True,  True,  420 ],
		[ False, True,  0   ]
	],
	[
		[ 0  ],
		[ 0  ],
		[ 42 ],
		[ 42 ],
		[ 42 ],
		[ 42 ],
		[ 69 ],
		[ 69 ]
	]
)



test_component(logic.ctr16(core.net(), core.net(), core.bus("A", 16), core.net()),
	[
		[ True,  False, 42,  True ],
		[ True,  True,  69,  True ],
		[ False, False, 0,   True ],
		[ False, True,  1,   True ],
		[ False, False, 2,   True ],
		[ False, True,  69,  True ],
		[ True,  False, 420, True ],
		[ True,  True,  0,   True ]
	],
	[
		[   0 ],
		[  42 ],
		[  42 ],
		[  43 ],
		[  43 ],
		[  44 ],
		[  44 ],
		[ 420 ]
	]
)

