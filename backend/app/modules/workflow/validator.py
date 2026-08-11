from typing import Dict, Any, List, Tuple, Optional
from app.core.exceptions import BaseCustomException
from app.core.logging import logger


class WorkflowValidationError(BaseCustomException):
    """Exception raised when workflow payload or state validation fails."""
    def __init__(self, step_name: str, errors: List[str]):
        message = f"Validation failed for step '{step_name}': {', '.join(errors)}"
        super().__init__(message=message, status_code=422)
        self.step_name = step_name
        self.errors = errors


class WorkflowValidator:
    """
    Validator component validating workflow inputs, JSON extractions, user decisions,
    and profile parameters before state execution.
    """

    @staticmethod
    def validate_job_discovery(job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        required = ["organization", "advt_number", "job_title", "pdf_url", "apply_url"]
        for field in required:
            if not job_data.get(field):
                errors.append(f"Missing required job discovery field: '{field}'")
        return len(errors) == 0, errors

    @staticmethod
    def validate_extracted_json(json_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not isinstance(json_data, dict):
            return False, ["Extracted JSON is not a valid dictionary"]

        required_keys = ["job_title", "qualifications", "min_age", "last_date"]
        for key in required_keys:
            if key not in json_data or json_data[key] is None:
                errors.append(f"JSON extraction missing critical key '{key}'")
        return len(errors) == 0, errors

    @staticmethod
    def validate_user_decision(decision: str, payload: Optional[Dict[str, Any]] = None) -> Tuple[bool, List[str]]:
        errors = []
        valid_decisions = ["IGNORE", "REMIND", "APPLY"]
        if decision.upper() not in valid_decisions:
            errors.append(f"Invalid user decision '{decision}'. Must be one of {valid_decisions}")

        if decision.upper() == "REMIND" and payload:
            if "reminder_datetime" not in payload and "hours" not in payload:
                errors.append("Remind decision requires 'reminder_datetime' or 'hours' in payload")

        return len(errors) == 0, errors

    @staticmethod
    def validate_profile_readiness(profile: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        required = ["full_name", "date_of_birth", "category", "email", "phone"]
        for field in required:
            if not profile.get(field):
                errors.append(f"Candidate profile missing required field '{field}'")
        return len(errors) == 0, errors

    @staticmethod
    def validate_manual_action_resume(confirmation_payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not confirmation_payload:
            errors.append("Resume confirmation payload cannot be empty")
        if "action_completed" in confirmation_payload and not confirmation_payload["action_completed"]:
            errors.append("Manual action has not been confirmed as completed")
        return len(errors) == 0, errors
