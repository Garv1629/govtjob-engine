import re
from typing import List, Tuple
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class ExtractionJSONValidator:
    """Validates extracted JSON payload against strict business rules for dates, URLs, salary, age, and qualifications."""

    @staticmethod
    def validate(extraction: StructuredJobExtraction) -> Tuple[List[str], List[str]]:
        warnings: List[str] = []
        errors: List[str] = []

        # 1. Validate Mandatory Fields
        if not extraction.job_title or len(extraction.job_title.strip()) < 3:
            errors.append("Critical Error: Missing or invalid job_title.")
        
        if not extraction.advt_number or len(extraction.advt_number.strip()) < 2:
            errors.append("Critical Error: Missing or invalid advertisement number.")

        if not extraction.organization:
            errors.append("Critical Error: Missing recruitment organization name.")

        # 2. Validate URLs
        url_pattern = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
        
        if extraction.official_notification_pdf:
            if not url_pattern.match(extraction.official_notification_pdf):
                warnings.append(f"Invalid official_notification_pdf URL format: '{extraction.official_notification_pdf}'")
        else:
            warnings.append("Missing official_notification_pdf URL.")

        if extraction.official_apply_link and not url_pattern.match(extraction.official_apply_link):
            warnings.append(f"Invalid official_apply_link URL format: '{extraction.official_apply_link}'")

        if extraction.official_website and not url_pattern.match(extraction.official_website):
            warnings.append(f"Invalid official_website URL format: '{extraction.official_website}'")

        # 3. Validate Vacancies & Salary
        if extraction.vacancies is None or extraction.vacancies < 0:
            warnings.append("Vacancies is missing or negative.")

        if not extraction.salary and not extraction.pay_level:
            warnings.append("Both salary and pay_level are missing.")

        # 4. Validate Qualifications & Age
        if not extraction.qualification or len(extraction.qualification) == 0:
            warnings.append("Educational qualifications list is empty.")

        if not extraction.age_limit:
            warnings.append("Age limit criteria is missing.")

        # 5. Validate Dates
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if extraction.opening_date and not date_pattern.match(extraction.opening_date):
            warnings.append(f"Opening date '{extraction.opening_date}' does not follow YYYY-MM-DD format.")

        if extraction.closing_date and not date_pattern.match(extraction.closing_date):
            warnings.append(f"Closing date '{extraction.closing_date}' does not follow YYYY-MM-DD format.")

        logger.info(f"Validation completed: {len(errors)} critical errors, {len(warnings)} warnings.")
        return errors, warnings
