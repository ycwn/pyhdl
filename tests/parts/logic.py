

import pyhdl.core as core
import pyhdl.parts.logic as logic

from ..common import *



test_component(logic.nand1.create(),
	[ [ False, False ], [ False, True  ], [ True,  False ], [ True,  True  ] ],
	[ [ True         ], [ True         ], [ True         ], [ False        ] ]
)



test_component(logic.not1.create(),
	[ [ False ], [ True  ] ],
	[ [ True  ], [ False ] ]
)



test_component(logic.buf1.create(),
	[ [ False ], [ True ] ],
	[ [ False ], [ True ] ]
)



test_component(logic.and1.create(),
	[ [ False, False ], [ False, True  ], [ True, False ], [ True,  True  ] ],
	[ [ False        ], [ False        ], [ False       ], [ True         ] ]
)



test_component(logic.or1.create(),
	[ [ False, False ], [ False, True  ], [ True, False ], [ True,  True  ] ],
	[ [ False        ], [ True         ], [ True        ], [ True         ] ]
)



test_component(logic.nor1.create(),
	[ [ False, False ], [ False, True  ], [ True, False ], [ True,  True  ] ],
	[ [ True         ], [ False        ], [ False       ], [ False        ] ]
)



test_component(logic.xor1.create(),
	[ [ False, False ], [ False, True  ], [ True, False ], [ True,  True  ] ],
	[ [ False        ], [ True         ], [ True        ], [ False        ] ]
)



test_component(logic.add1.create(),
	[ [ False, False ], [ False, True  ], [ True, False ], [ True,  True  ] ],
	[ [ False, False ], [ True,  False ], [ True, False ], [ False, True  ] ]
)



test_component(logic.adc1.create(),
	[
		[ False, False, False ], [ False, False, True  ], [ False, True, False ], [ False, True,  True  ],
		[ True,  False, False ], [ True,  False, True  ], [ True,  True, False ], [ True,  True,  True  ],
	],
	[
		[ False, False ], [ True,  False ], [ True,  False ], [ False, True  ],
		[ True,  False ], [ False, True  ], [ False, True  ], [ True,  True  ]
	]
)



test_component(logic.mux1.create(),
	[
		[ False, False, False ], [ False, False, True  ], [ False, True, False ], [ False, True,  True  ],
		[ True,  False, False ], [ True,  False, True  ], [ True,  True, False ], [ True,  True,  True  ],
	],
	[
		[ False ], [ False ], [ True  ], [ True  ],
		[ False ], [ True  ], [ False ], [ True  ]
	]
)



test_component(logic.dmux1.create(),
	[
		[ False, False ], [ False, True  ], [ True, False ], [ True,  True  ]
	],
	[
		[ False, False ], [ True,  False ], [ False, False ], [ False, True ]
	]
)



test_component(logic.dff1.create(),
	[
		[ True,   False ],
		[ True,   True  ],
		[ False,  False ],
		[ False,  True  ],
		[ True,   False ]
	],
	[
		[ False, True  ],
		[ True,  True  ],
		[ True,  False ],
		[ True,  False ],
		[ False, True  ]
	]
)



test_component(logic.sdff1.create(),
	[
		[ True,  False, False ],
		[ True,  False, True  ],
		[ False, True,  False ],
		[ False, False, False ],
		[ False, True,  False ],
		[ True,  False, False ],
		[ True,  True,  False ],
		[ False, True,  False ]
	],
	[
		[ False, True  ],
		[ False, True  ],
		[ True,  True  ],
		[ True,  False ],
		[ True,  False ],
		[ True,  False ],
		[ False, True  ],
		[ False, True  ]
	]
)

