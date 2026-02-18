__version__ = "0.2.3a1"

import sys
import warnings

from oemof.demand import bdew
from oemof.demand import vdi

sys.modules["demandlib.bdew"] = bdew
sys.modules["demandlib.vdi"] = vdi

warnings.warn(
    "The library ' demandlib' has been renamed to ' oemof.demand',"
    " please directly import from ' oemof.demand'.",
    category=FutureWarning,
)
