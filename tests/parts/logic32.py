

import pyhdl.core as core
import pyhdl.parts.logic32 as logic

from ..common import *



test_component(logic.not32.create(),
	[
		[ 0 ], [ 1 ], [ 4294967294 ], [ 4294967295 ],
	],
	[
		[ 4294967295 ], [ 4294967294 ], [ 1 ], [ 0 ]
	]
)



test_component(logic.mux32.create(),
	[
		[ False, 0xdeadbeef, 0xfeedface ], [ True, 0xdeadbeef, 0xfeedface ]
	],
	[
		[ 0xdeadbeef ], [ 0xfeedface ]
	]
)



test_component(logic.adc32.create(),
	[
		[ 10,         15, False ],
		[ 4294967295, 0,  False ],
		[ 4294967294, 0,  True  ],
		[ 4294967295, 0,  True  ]
	],
	[
		[ 25,         False ],
		[ 4294967295, False ],
		[ 4294967295, False ],
		[ 0,          True  ]
	]
)



test_component(logic.inc32.create(),
	[
		[ 0, True  ], [ 1, True  ], [ 4294967294, True  ], [ 4294967295, True  ],
		[ 0, False ], [ 1, False ], [ 4294967294, False ], [ 4294967295, False ]
	],
	[
		[ 1, False ], [ 2, False ], [ 4294967295, False ], [ 0,          True  ],
		[ 0, False ], [ 1, False ], [ 4294967294, False ], [ 4294967295, False ]
	]
)



test_component(logic.sub32.create(),
	[
		[ 0,          0,          False ],
		[ 1,          0,          False ],
		[ 1,          1,          False ],
		[ 1,          2,          False ],
		[ 1,          3,          False ],
		[ 2,          2,          False ],
		[ 4,          2,          False ],
		[ 2147483648, 2147483648, False ],
		[ 2147483648, 2147483650, False ]
	],
	[
		[ 0,          False ],
		[ 1,          False ],
		[ 0,          False ],
		[ 4294967295, True  ],
		[ 4294967294, True  ],
		[ 0,          False ],
		[ 2,          False ],
		[ 0,          False ],
		[ 4294967294, True  ]
	]
)



test_component(logic.dec32.create(),
	[
		[ 1, True  ], [ 2, True  ], [ 4294967295, True  ], [ 0, True  ],
		[ 1, False ], [ 2, False ], [ 4294967295, False ], [ 0, False ]
	],
	[
		[ 0, False ], [ 1, False ], [ 4294967294, False ], [ 4294967295, True  ],
		[ 1, False ], [ 2, False ], [ 4294967295, False ], [ 0,          False ]
	]
)



test_component(logic.eqz32.create(),
	[
		[ 0       ],
		[ 1 <<  0 ], [ 1 <<  1 ], [ 1 <<  2 ], [ 1 <<  3 ],
		[ 1 <<  4 ], [ 1 <<  5 ], [ 1 <<  6 ], [ 1 <<  7 ],
		[ 1 <<  8 ], [ 1 <<  9 ], [ 1 << 10 ], [ 1 << 11 ],
		[ 1 << 12 ], [ 1 << 13 ], [ 1 << 14 ], [ 1 << 15 ],
		[ 1 << 16 ], [ 1 << 17 ], [ 1 << 18 ], [ 1 << 19 ],
		[ 1 << 20 ], [ 1 << 21 ], [ 1 << 22 ], [ 1 << 23 ],
		[ 1 << 24 ], [ 1 << 25 ], [ 1 << 26 ], [ 1 << 27 ],
		[ 1 << 28 ], [ 1 << 29 ], [ 1 << 30 ], [ 1 << 31 ]
	],
	[
		[ True  ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ]
	]
)



test_component(logic.ltz32.create(),
	[
		[ 0       ],
		[ 1 <<  0 ], [ 1 <<  1 ], [ 1 <<  2 ], [ 1 <<  3 ],
		[ 1 <<  4 ], [ 1 <<  5 ], [ 1 <<  6 ], [ 1 <<  7 ],
		[ 1 <<  8 ], [ 1 <<  9 ], [ 1 << 10 ], [ 1 << 11 ],
		[ 1 << 12 ], [ 1 << 13 ], [ 1 << 14 ], [ 1 << 15 ],
		[ 1 << 16 ], [ 1 << 17 ], [ 1 << 18 ], [ 1 << 19 ],
		[ 1 << 20 ], [ 1 << 21 ], [ 1 << 22 ], [ 1 << 23 ],
		[ 1 << 24 ], [ 1 << 25 ], [ 1 << 26 ], [ 1 << 27 ],
		[ 1 << 28 ], [ 1 << 29 ], [ 1 << 30 ], [ 1 << 31 ]
	],
	[
		[ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ False ],
		[ False ], [ False ], [ False ], [ True  ]
	]
)



test_component(logic.reg32.create(),
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



test_component(logic.ctr32.create(),
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

