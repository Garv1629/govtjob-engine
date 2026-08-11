from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.modules.eligibility.schemas import CandidateProfileInput
from app.modules.automation.state_machine import AutomationState

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = Any


class BasePortalAdapter(ABC):
    """
    Abstract Portal Adapter interface exposing 14 mandatory lifecycle methods
    for government recruitment portal form-filling automation.
    """

    source_code: str = "BASE"

    def __init__(self, page: Any):
        self.page = page
        self._is_paused = False
        self._pause_reason = ""

    @abstractmethod
    async def initialize( -> bool:
        """Sets up portal session context and opens base URL."""
        pass

    @abstractmethod
    async def login(self, credentials: Dict[str, str]) -> bool:
        """Executes candidate portal authentication."""
        pass

    @abstractmethod
    async def open_application(self, advt_number: str) -> bool:
        """Navigates to candidate application form for target advertisement."""
        pass

    @abstractmethod
    async def fill_profile(self, profile: CandidateProfileInput) -> bool:
        """Fills personal profile section (Name, DOB, Category, Address)."""
        pass

    @abstractmethod
    async def fill_education(self, profile: CandidateProfileInput) -> bool:
        """Fills educational qualification and marksheets section."""
        pass

    @abstractmethod
    async def fill_experience(self, profile: CandidateProfileInput) -> bool:
        """Fills work experience history section."""
        pass

    @abstractmethod
    async def upload_documents(self, documents_map: Dict[str, str]) -> bool:
        """Uploads candidate photo, signature, identity, and degree certificates."""
        pass

    @abstractmethod
    async def review_application( -> bool:
        """Navigates to pre-submission review page."""
        pass

    @abstractmethod
    async def pause_for_manual_step(self, reason: str) -> Dict[str, Any]:
        """Safely pauses workflow for OTP, CAPTCHA, or Payment confirmation."""
        pass

    @abstractmethod
    async def resume_after_confirmation(self, payload: Dict[str, Any]) -> bool:
        """Resumes workflow execution after candidate confirms manual step."""
        pass

    @abstractmethod
    async def submit(self, Completing: bool = False) -> Dict[str, Any]:
        """Submits finalized job application form."""
        pass

    @abstractmethod
    async def download_receipt( -> str:
        """Downloads application receipt PDF / acknowledgment slip."""
        pass

    @abstractmethod
    async def capture_screenshot(self, name: str = "step") -> str:
        """Captures page viewport screenshot."""
        pass

    @abstractmethod
    async def shutdown(:
        """Cleans up page resources."""
        pass
