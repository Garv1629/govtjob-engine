from app.modules.automation.adapters.base import BasePortalAdapter
from app.modules.automation.adapters.ssc_adapter import SSCPortalAdapter
from app.modules.automation.adapters.upsc_adapter import UPSCPortalAdapter
from app.modules.automation.adapters.ncs_adapter import NCSPortalAdapter

__all__ = [
    "BasePortalAdapter",
    "SSCPortalAdapter",
    "UPSCPortalAdapter",
    "NCSPortalAdapter",
]
