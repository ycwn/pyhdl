

import pyhdl.core as core
import pyhdl.parts.clock as clk

from ..common import *



test_component(clk.clock(),
	[
		[], [], [], [], [], [], [], []
	],
	[
		[ True  ],
		[ False ],
		[ True  ],
		[ False ],
		[ True  ],
		[ False ],
		[ True  ],
		[ False ]
	]
)

