

import pyhdl.core as core
import pyhdl.parts.logic8 as logic

from ..common import *



test_component(logic.not8.create(),
	[
		[ 0 ], [ 1 ], [ 254 ], [ 255 ],
	],
	[
		[ 255 ], [ 254 ], [ 1 ], [ 0 ]
	]
)



test_component(logic.mux8.create(),
	[
		[ False, 42, 69 ], [ True, 42, 69 ]
	],
	[
		[ 42 ], [ 69 ]
	]
)



test_component(logic.adc8.create(),
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



test_component(logic.inc8.create(),
	[
		[ 0, True  ], [ 1, True  ], [ 254, True  ], [ 255, True  ],
		[ 0, False ], [ 1, False ], [ 254, False ], [ 255, False ]
	],
	[
		[ 1, False ], [ 2, False ], [ 255, False ], [ 0,   True  ],
		[ 0, False ], [ 1, False ], [ 254, False ], [ 255, False ]
	]
)



test_component(logic.sub8.create(),
	[
		[ 0,   0,   False ],
		[ 1,   0,   False ],
		[ 1,   1,   False ],
		[ 1,   2,   False ],
		[ 1,   3,   False ],
		[ 2,   2,   False ],
		[ 4,   2,   False ],
		[ 128, 128, False ],
		[ 128, 130, False ]
	],
	[
		[ 0,   False ],
		[ 1,   False ],
		[ 0,   False ],
		[ 255, True  ],
		[ 254, True  ],
		[ 0,   False ],
		[ 2,   False ],
		[ 0,   False ],
		[ 254, True  ]
	]
)



test_component(logic.dec8.create(),
	[
		[ 1, True  ], [ 2, True  ], [ 255, True  ], [ 0, True  ],
		[ 1, False ], [ 2, False ], [ 255, False ], [ 0, False ]
	],
	[
		[ 0, False ], [ 1, False ], [ 254, False ], [ 255, True  ],
		[ 1, False ], [ 2, False ], [ 255, False ], [ 0,   False ]
	]
)



test_component(logic.idc8.create(),
	[
		[ 0, False, True  ], [ 1, False, True  ], [ 254, False, True  ], [ 255, False, True  ],
		[ 1, True,  True  ], [ 2, True,  True  ], [ 255, True,  True  ], [ 0,   True,  True  ],
		[ 0, False, False ], [ 1, False, False ], [ 254, False, False ], [ 255, False, False ],
		[ 1, True,  False ], [ 2, True,  False ], [ 255, True,  False ], [ 0,   True,  False ]
	],
	[
		[ 1, False ], [ 2, False ], [ 255, False ], [ 0,   True  ],
		[ 0, False ], [ 1, False ], [ 254, False ], [ 255, True  ],
		[ 0, False ], [ 1, False ], [ 254, False ], [ 255, False ],
		[ 1, False ], [ 2, False ], [ 255, False ], [ 0,   False ]
	]
)



test_component(logic.eqz8.create(),
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



test_component(logic.ltz8.create(),
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



test_component(logic.reg8.create(),
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



test_component(logic.ucount8.create(),
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
		[ 0  ],
		[ 42 ],
		[ 42 ],
		[ 43 ],
		[ 43 ],
		[ 44 ],
		[ 44 ],
		[ 69 ]
	]
)



test_component(logic.dcount8.create(),
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
		[ 0  ],
		[ 42 ],
		[ 42 ],
		[ 41 ],
		[ 41 ],
		[ 40 ],
		[ 40 ],
		[ 69 ]
	]
)



test_component(logic.udcount8.create(),
	[
		[ True,  False, False, 42, True ],
		[ True,  True,  False, 69, True ],
		[ False, False, False, 0,  True ],
		[ False, True,  False, 1,  True ],
		[ False, False, False, 2,  True ],
		[ False, True,  False, 3,  True ],
		[ True,  False, False, 69, True ],
		[ True,  True,  False, 0,  True ],
		[ True,  False, True,  42, True ],
		[ True,  True,  True,  69, True ],
		[ False, False, True,  0,  True ],
		[ False, True,  True,  1,  True ],
		[ False, False, True,  2,  True ],
		[ False, True,  True,  3,  True ],
		[ True,  False, True,  69, True ],
		[ True,  True,  True,  0,  True ]
	],
	[
		[ 0  ],
		[ 42 ],
		[ 42 ],
		[ 43 ],
		[ 43 ],
		[ 44 ],
		[ 44 ],
		[ 69 ],
		[ 69 ],
		[ 42 ],
		[ 42 ],
		[ 41 ],
		[ 41 ],
		[ 40 ],
		[ 40 ],
		[ 69 ]
	]
)
