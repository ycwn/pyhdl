

import pyhdl.core as core
import pyhdl.parts.logic4 as logic

from ..common import *



test_component(logic.not4.create(),
	[
		[ 0 ], [ 1 ], [ 14 ], [ 15 ],
	],
	[
		[ 15 ], [ 14 ], [ 1 ], [ 0 ]
	]
)



test_component(logic.mux4.create(),
	[
		[ False, 13, 10 ], [ True, 13, 10 ]
	],
	[
		[ 13 ], [ 10 ]
	]
)



test_component(logic.adc4.create(),
	[
		[ 4,  5,  False ],
		[ 15, 0,  False ],
		[ 14, 0,  True  ],
		[ 15, 0,  True  ]
	],
	[
		[ 9,  False ],
		[ 15, False ],
		[ 15, False ],
		[ 0,  True  ]
	]
)



test_component(logic.inc4.create(),
	[
		[ 0, True  ], [ 1, True  ], [ 14, True  ], [ 15, True  ],
		[ 0, False ], [ 1, False ], [ 14, False ], [ 15, False ]
	],
	[
		[ 1, False ], [ 2, False ], [ 15, False ], [ 0,  True  ],
		[ 0, False ], [ 1, False ], [ 14, False ], [ 15, False ]
	]
)



test_component(logic.sub4.create(),
	[
		[ 0,  0, False ],
		[ 1,  0, False ],
		[ 1,  1, False ],
		[ 1,  2, False ],
		[ 1,  3, False ],
		[ 2,  2, False ],
		[ 4,  2, False ],
		[ 8,  8, False ],
		[ 8, 10, False ]
	],
	[
		[ 0,  False ],
		[ 1,  False ],
		[ 0,  False ],
		[ 15, True  ],
		[ 14, True  ],
		[ 0,  False ],
		[ 2,  False ],
		[ 0,  False ],
		[ 14, True  ]
	]
)



test_component(logic.dec4.create(),
	[
		[ 1, True  ], [ 2, True  ], [ 15, True  ], [ 0, True  ],
		[ 1, False ], [ 2, False ], [ 15, False ], [ 0, False ]
	],
	[
		[ 0, False ], [ 1, False ], [ 14, False ], [ 15, True  ],
		[ 1, False ], [ 2, False ], [ 15, False ], [ 0,  False ]
	]
)



test_component(logic.idc4.create(),
	[
		[ 0, False, True  ], [ 1, False, True  ], [ 14, False, True  ], [ 15, False, True  ],
		[ 1, True,  True  ], [ 2, True,  True  ], [ 15, True,  True  ], [ 0,  True,  True  ],
		[ 0, False, False ], [ 1, False, False ], [ 14, False, False ], [ 15, False, False ],
		[ 1, True,  False ], [ 2, True,  False ], [ 15, True,  False ], [ 0,  True,  False ]
	],
	[
		[ 1, False ], [ 2, False ], [ 15, False ], [ 0,  True  ],
		[ 0, False ], [ 1, False ], [ 14, False ], [ 15, True  ],
		[ 0, False ], [ 1, False ], [ 14, False ], [ 15, False ],
		[ 1, False ], [ 2, False ], [ 15, False ], [ 0,  False ]
	]
)



test_component(logic.eqz4.create(),
	[
		[ 0      ],
		[ 1 << 0 ], [ 1 << 1 ], [ 1 << 2 ], [ 1 << 3 ]
	],
	[
		[ True  ],
		[ False ], [ False ], [ False ], [ False ]
	]
)



test_component(logic.ltz4.create(),
	[
		[ 0      ],
		[ 1 << 0 ], [ 1 << 1 ], [ 1 << 2 ], [ 1 << 3 ]
	],
	[
		[ False ],
		[ False ], [ False ], [ False ], [ True  ]
	]
)



test_component(logic.reg4.create(),
	[
		[ True,  False, 0   ],
		[ True,  False, 13  ],
		[ False, True,  0   ],
		[ False, False, 1   ],
		[ False, True,  2   ],
		[ True,  False, 3   ],
		[ True,  True,  10  ],
		[ False, True,  0   ]
	],
	[
		[ 0  ],
		[ 0  ],
		[ 13 ],
		[ 13 ],
		[ 13 ],
		[ 13 ],
		[ 3 ],
		[ 3 ]
	]
)



test_component(logic.ucount4.create(),
	[
		[ True,  False, 12, True  ],
		[ True,  True,  10, True  ],
		[ False, False, 0,  True  ],
		[ False, True,  1,  True  ],
		[ False, False, 2,  True  ],
		[ False, True,  3,  True  ],
		[ True,  False, 10, True  ],
		[ True,  True,  0,  True  ]
	],
	[
		[ 0  ],
		[ 12 ],
		[ 12 ],
		[ 13 ],
		[ 13 ],
		[ 14 ],
		[ 14 ],
		[ 10 ]
	]
)



test_component(logic.dcount4.create(),
	[
		[ True,  False, 12, True  ],
		[ True,  True,  10, True  ],
		[ False, False, 0,  True  ],
		[ False, True,  1,  True  ],
		[ False, False, 2,  True  ],
		[ False, True,  3,  True  ],
		[ True,  False, 14, True  ],
		[ True,  True,  0,  True  ]
	],
	[
		[ 0  ],
		[ 12 ],
		[ 12 ],
		[ 11 ],
		[ 11 ],
		[ 10 ],
		[ 10 ],
		[ 14 ]
	]
)



test_component(logic.udcount4.create(),
	[
		[ True,  False, False, 12, True  ],
		[ True,  True,  False, 10, True  ],
		[ False, False, False, 0,  True  ],
		[ False, True,  False, 1,  True  ],
		[ False, False, False, 2,  True  ],
		[ False, True,  False, 3,  True  ],
		[ True,  False, False, 10, True  ],
		[ True,  True,  False, 0,  True  ],
		[ True,  False, True,  12, True  ],
		[ True,  True,  True,  10, True  ],
		[ False, False, True,  0,  True  ],
		[ False, True,  True,  1,  True  ],
		[ False, False, True,  2,  True  ],
		[ False, True,  True,  3,  True  ],
		[ True,  False, True,  14, True  ],
		[ True,  True,  True,  0,  True  ]

	],
	[
		[ 0  ],
		[ 12 ],
		[ 12 ],
		[ 13 ],
		[ 13 ],
		[ 14 ],
		[ 14 ],
		[ 10 ],
		[ 10 ],
		[ 12 ],
		[ 12 ],
		[ 11 ],
		[ 11 ],
		[ 10 ],
		[ 10 ],
		[ 14 ]
	]
)
