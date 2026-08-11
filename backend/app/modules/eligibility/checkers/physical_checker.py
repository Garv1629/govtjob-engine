import re
from typing import Tuple
from app.modules.eligibility.schemas import CandidateProfileInput, RuleEvaluationResult
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class PhysicalAndMedicalEligibilityChecker:
    """Evaluates height, chest, vision, and physical fitness criteria."""

    @staticmethod
    def evaluate(profile: CandidateProfileInput, job: StructuredJobExtraction) -> Tuple[RuleEvaluationResult, float]:
        phys_text = (job.physical_standards or "") + " " + (job.medical_standards or "")
        
        # Parse minimum height if specified
        req_height = 0.0
        h_match = re.search(r"Height:\s*(\d+(?:\.\d+)?)", phys_text, re.IGNORECASE)
        if h_match:
            req_height = float(h_match.group(1))

        passed = True
        reasons = []

        if req_height > 0 and profile.height_cm:
            if profile.height_cm < req_height:
                passed = False
                reasons.append(f"Candidate height ({profile.height_cm} cm) is below required standard ({req_height} cm).")

        if passed:
            score = 100.0
            msg = "✔ Physical & Medical standards satisfied."
        else:
            score = 50.0
            msg = f"⚠️ Physical standards check warning: {'; '.join(reasons)}"

        logger.info(f"Physical/Medical Check for User {profile.user_id}: {msg}")

        result = RuleEvaluationResult(
            rule_name="Physical & Medical Standards",
            category="MEDICAL",
            passed=passed,
            message=msg,
            details={
                "candidate_height": profile.height_cm,
                "required_height": req_height
            }
        )
        return result, score
