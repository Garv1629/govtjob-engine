import re
from datetime import datetime, date
from typing import Tuple, Dict, Any
from app.modules.eligibility.schemas import CandidateProfileInput, RuleEvaluationResult
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class AgeEligibilityChecker:
    """
    Evaluates candidate age against advertisement criteria and applies category relaxations:
    - General: 0 Years
    - OBC: +3 Years
    - SC/ST: +5 Years
    - PwD: +10 Years
    - Ex-Serviceman: +3 Years (post service deduction)
    """

    @staticmethod
    def evaluate(profile: CandidateProfileInput, job: StructuredJobExtraction) -> Tuple[RuleEvaluationResult, float]:
        dob_date = datetime.strptime(profile.dob, "%Y-%m-%d").date()
        
        # Determine cutoff date (default to job closing_date or current date)
        cutoff_date = date.today()
        if job.closing_date:
            try:
                cutoff_date = datetime.strptime(job.closing_date, "%Y-%m-%d").date()
            except Exception:
                pass

        # Calculate exact candidate age in years at cutoff date
        age_years = cutoff_date.year - dob_date.year - ((cutoff_date.month, cutoff_date.day) < (dob_date.month, dob_date.day))

        # Default age bounds if missing from notice
        min_required_age = 18
        max_required_age = 30

        if job.age_limit:
            # Parse min and max age from text e.g. "18 to 32 years"
            min_match = re.search(r"(\d+)\s*(?:to|-)\s*(\d+)", job.age_limit)
            if min_match:
                min_required_age = int(min_match.group(1))
                max_required_age = int(min_match.group(2))
            else:
                max_match = re.search(r"(\d+)\s*years", job.age_limit)
                if max_match:
                    max_required_age = int(max_match.group(1))

        # Calculate Category Relaxation
        relaxation_years = 0
        cat = profile.category.upper()
        if cat in ["OBC", "OBC-NCL"]:
            relaxation_years += 3
        elif cat in ["SC", "ST"]:
            relaxation_years += 5

        if profile.is_pwd:
            relaxation_years += 10

        if profile.is_ex_serviceman:
            relaxation_years += 3 + int(profile.ex_service_years)

        effective_max_age = max_required_age + relaxation_years

        is_min_passed = age_years >= min_required_age
        is_max_passed = age_years <= effective_max_age
        passed = is_min_passed and is_max_passed

        if passed:
            score = 100.0
            msg = f"✔ Age matches criteria: Candidate is {age_years} years old (Permissible limit: {min_required_age} to {effective_max_age} years, including +{relaxation_years} yrs relaxation for {cat})."
        else:
            score = 0.0
            if not is_min_passed:
                msg = f"❌ Age check failed: Candidate age ({age_years} yrs) is below minimum required age of {min_required_age} yrs."
            else:
                msg = f"❌ Age check failed: Candidate age ({age_years} yrs) exceeds permissible upper limit of {effective_max_age} yrs (Base: {max_required_age} + Relaxation: {relaxation_years} yrs)."

        logger.info(f"Age Check for User {profile.user_id}: {msg}")

        result = RuleEvaluationResult(
            rule_name="Age Eligibility Criteria",
            category="AGE",
            passed=passed,
            message=msg,
            details={
                "candidate_age": age_years,
                "min_required_age": min_required_age,
                "base_max_age": max_required_age,
                "relaxation_years": relaxation_years,
                "effective_max_age": effective_max_age,
                "cutoff_date": str(cutoff_date)
            }
        )
        return result, score
