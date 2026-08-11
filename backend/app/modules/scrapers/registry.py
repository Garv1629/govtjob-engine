import importlib
import pkgutil
import inspect
from typing import Dict, List, Type, Optional
from app.modules.scrapers.base import BaseScraper
from app.core.logging import logger


class ScraperPluginRegistry:
    """
    Central Registry for managing Government Job Scraper Plugins.
    Supports auto-discovery, dynamic loading, metadata inspection, enabling/disabling, and priority sorting.
    """

    _plugins: Dict[str, BaseScraper] = {}
    _classes: Dict[str, Type[BaseScraper]] = {}

    @classmethod
    def register(cls, scraper_cls: Type[BaseScraper]) -> Type[BaseScraper]:
        """Decorator or explicit function to register a scraper plugin class."""
        # Instantiate temporary object to read metadata
        instance = scraper_cls()
        source_code = instance.source_code.upper()
        cls._classes[source_code] = scraper_cls
        cls._plugins[source_code] = instance
        logger.info(f"Registered Scraper Plugin: [{source_code}] - {instance.source_name}")
        return scraper_cls

    @classmethod
    def discover_plugins(cls, package_name: str = "app.modules.scrapers.plugins") -> None:
        """Dynamically discovers and loads all BaseScraper subclasses from the plugins package."""
        try:
            package = importlib.import_module(package_name)
            for _, module_name, _ in pkgutil.iter_modules(package.__path__):
                full_module_name = f"{package_name}.{module_name}"
                module = importlib.import_module(full_module_name)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseScraper) and obj is not BaseScraper:
                        cls.register(obj)
            logger.info(f"Plugin auto-discovery completed. Total plugins registered: {len(cls._plugins)}")
        except Exception as e:
            logger.error(f"Error during plugin auto-discovery: {str(e)}")

    @classmethod
    def get_plugin(cls, source_code: str) -> Optional[BaseScraper]:
        return cls._plugins.get(source_code.upper())

    @classmethod
    def get_all_plugins(cls, sorted_by_priority: bool = True) -> List[BaseScraper]:
        plugins = list(cls._plugins.values())
        if sorted_by_priority:
            plugins.sort(key=lambda p: p.priority)
        return plugins

    @classmethod
    def get_enabled_plugins(cls) -> List[BaseScraper]:
        enabled = [p for p in cls.get_all_plugins() if p.is_enabled]
        return enabled

    @classmethod
    def set_plugin_enabled(cls, source_code: str, enabled: bool) -> bool:
        plugin = cls.get_plugin(source_code)
        if plugin:
            plugin.is_enabled = enabled
            logger.info(f"[{source_code.upper()}] Plugin enabled state set to: {enabled}")
            return True
        return False

    @classmethod
    def set_plugin_priority(cls, source_code: str, priority: int) -> bool:
        plugin = cls.get_plugin(source_code)
        if plugin:
            plugin.priority = priority
            logger.info(f"[{source_code.upper()}] Plugin priority updated to: {priority}")
            return True
        return False
