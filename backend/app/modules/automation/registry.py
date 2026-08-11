from typing import Dict, Type, Optional
from playwright.async_api import Page
from app.modules.automation.adapters.base import BasePortalAdapter
from app.modules.automation.adapters.ssc_adapter import SSCPortalAdapter
from app.modules.automation.adapters.upsc_adapter import UPSCPortalAdapter
from app.modules.automation.adapters.ncs_adapter import NCSPortalAdapter
from app.core.logging import logger


class PortalAdapterRegistry:
    """Registry for discovering and instantiating portal-specific automation adapters."""

    _adapters: Dict[str, Type[BasePortalAdapter]] = {
        "SSC": SSCPortalAdapter,
        "UPSC": UPSCPortalAdapter,
        "NCS": NCSPortalAdapter
    }

    @classmethod
    def get_adapter(cls, source_code: str, page: Page) -> BasePortalAdapter:
        code = source_code.strip().upper()
        adapter_cls = cls._adapters.get(code)
        if not adapter_cls:
            logger.warning(f"Portal adapter for '{source_code}' not found. Defaulting to SSC portal adapter.")
            adapter_cls = SSCPortalAdapter

        return adapter_cls(page=page)


__all__ = ["PortalAdapterRegistry"]
