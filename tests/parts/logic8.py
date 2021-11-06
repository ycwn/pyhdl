

import pyhdl.core as core
import pyhdl.parts.logic8 as logic

from ..common import *



test_component(logic.not8(core.bus("A", 8)),
	[
		[ 0 ], [ 1 ], [ 254 ], [ 255 ],
	],
	[
		[ 255 ], [ 254 ], [ 1 ], [ 0 ]
	]
)



test_component(logic.mux8(core.net(), core.bus("A", 8), core.bus("B", 8)),
	[
		[ False, 42, 69 ], [ True, 42, 69 ]
	],
	[
		[ 42 ], [ 69 ]
	]
)



test_component(logic.adc8(core.bus("A", 8), core.bus("B", 8), core.net()),
	[
		[ 10,  15, False ],
		[ 255, 0,  False ],
		[ 254, 0,  True  ],
		[ 255, 0,  True  ]
	],
	[
		[ 25,  False ],
		[ 255, False ],
		[ 255, False ],
		[ 0,   True  ]
	]
)



test_component(logic.inc8(core.bus("A", 8), core.net("C")),
	[
		[ 0, True ], [ 1, True ], [ 254, True ], [ 255, True ],
	],
	[
		[ 1 ], [ 2 ], [ 255 ], [ 0 ]
	]
)



test_component(logic.sub8(core.bus("A", 8), core.bus("B", 8)),
	[
		[ 0,   0   ],
		[ 1,   0   ],
		[ 1,   1   ],
		[ 1,   2   ],
		[ 1,   3   ],
		[ 2,   2   ],
		[ 4,   2   ],
		[ 128, 128 ],
		[ 128, 130 ]
	],
	[
		[ 0   ],
		[ 1   ],
		[ 0   ],
		[ 255 ],
		[ 254 ],
		[ 0   ],
		[ 2   ],
		[ 0   ],
		[ 254 ]
	]
)



test_component(logic.eqz8(core.bus("A", 8)),
	[
		[ 0      ],
		[ 1 << 0 ], [ 1 << 1 ], [ 1 << 2 ], [ 1 << 3 ],
		[ 1 << 4 ], [ 1 << 5 ], [ 1 << 6 ], [ 1 << 7 ]
	],
	[
		[ True  ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ]
	]
)



test_component(logic.ltz8(core.bus("A", 8)),
	[
		[ 0      ],
		[ 1 << 0 ], [ 1 << 1 ], [ 1 << 2 ], [ 1 << 3 ],
		[ 1 << 4 ], [ 1 << 5 ], [ 1 << 6 ], [ 1 << 7 ]
	],
	[
		[ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ True  ]
	]
)



test_component(logic.reg8(core.net(), core.net(), core.bus("A", 8)),
	[
		[ True,  False, 0   ],
		[ True,  False, 42  ],
		[ False, True,  0   ],
		[ False, False, 1   ],
		[ False, True,  2   ],
		[ True,  False, 3   ],
		[ True,  True,  69  ],
		[ False, True,  0   ]
	],
	[
		[ 0  ],
		[ 0  ],
		[ 42 ],
		[ 42 ],
		[ 42 ],
		[ 42 ],
		[ 3 ],
		[ 3 ]
	]
)



test_component(logic.ctr8(core.net(), core.net(), core.bus("A", 8), core.net()),
	[
		[ True,  False, 42, True ],
		[ True,  True,  69, True ],
		[ False, False, 0,  True ],
		[ False, True,  1,  True ],
		[ False, False, 2,  True ],
		[ False, True,  3,  True ],
		[ True,  False, 69, True ],
		[ True,  True,  0,  True ]
	],
	[
		[  0 ],
		[ 42 ],
		[ 42 ],
		[ 43 ],
		[ 43 ],
		[ 44 ],
		[ 44 ],
		[ 69 ]
	]
)

