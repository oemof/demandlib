__version__ = "0.2.3a1"

import sys
import warnings

from oemof import demand

sys.modules["demandlib"] = demand

warnings.warn(
    "The library ' demandlib' has been renamed to ' oemof.demand',"
    " please directly import from ' oemof.demand'.",
    category=FutureWarning,
)
