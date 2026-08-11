import re
from typing import Tuple
from app.modules.eligibility.schemas import CandidateProfileInput, RuleEvaluationResult
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class ExperienceEligibilityChecker:
    """Evaluates candidate years of experience against job notification requirements."""

    @staticmethod
    def evaluate(profile: CandidateProfileInput, job: StructuredJobExtraction) -> Tuple[RuleEvaluationResult, float]:
        req_exp_text = job.experience or ""
        
        # Extract numeric years from text e.g. "2 Years experience"
        req_years = 0.0
        exp_match = re.search(r"(\d+)\s*(?:years?|yrs)", req_exp_text, re.IGNORECASE)
        if exp_match:
            req_years = float(exp_match.group(1))

        passed = profile.experience_years >= req_years

        if passed:
            score = 100.0
            msg = f"✔ Experience matches criteria: Candidate has {profile.experience_years} years experience (Required: {req_years} yrs)."
        else:
            score = round((profile.experience_years / req_years) * 100, 1) if req_years > 0 else 0.0
            msg = f"❌ Experience check failed: Candidate has {profile.experience_years} years experience, but position requires minimum {req_years} yrs."

        logger.info(f"Experience Check for User {profile.user_id}: {msg}")

        result = RuleEvaluationResult(
            rule_name="Work Experience Criteria",
            category="EXPERIENCE",
            passed=passed,
            message=msg,
            details={
                "candidate_experience_years": profile.experience_years,
                "required_experience_years": req_years
            }
        )
        return result, score
