import re
from typing import Tuple, Dict, Any
from app.modules.eligibility.schemas import CandidateProfileInput, RuleEvaluationResult
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class QualificationEligibilityChecker:
    """
    Evaluates educational qualification matching, equivalent degrees, percentage/CGPA cutoffs, and higher qualification allowances.
    """

    EQUIVALENT_DEGREES = {
        "B.TECH": ["B.E", "BACHELOR OF TECHNOLOGY", "BACHELOR OF ENGINEERING", "BS", "B.SC ENGINEERING"],
        "B.E": ["B.TECH", "BACHELOR OF ENGINEERING"],
        "B.SC": ["BACHELOR OF SCIENCE", "B.SC COMPUTER SCIENCE", "B.SC IT", "BCA"],
        "M.TECH": ["M.E", "MASTER OF TECHNOLOGY", "MASTER OF ENGINEERING", "MS"],
        "GRADUATION": ["B.A", "B.COM", "B.SC", "B.TECH", "B.E", "BBA", "BCA", "BACHELOR DEGREE"],
    }

    @staticmethod
    def evaluate(profile: CandidateProfileInput, job: StructuredJobExtraction) -> Tuple[RuleEvaluationResult, float]:
        cand_degree = profile.degree.strip().upper()
        req_qual_list = [q.upper() for q in job.qualification]

        if not req_qual_list:
            # If notification doesn't specify strict qualification, default pass
            result = RuleEvaluationResult(
                rule_name="Educational Qualification Criteria",
                category="QUALIFICATION",
                passed=True,
                message="✔ Educational Qualification matches default open criteria.",
                details={"candidate_degree": cand_degree}
            )
            return result, 100.0

        # Check exact or equivalent match
        passed = False
        matched_req = ""

        # Flatten equivalents for candidate degree
        cand_equivalents = [cand_degree]
        for key, eq_list in QualificationEligibilityChecker.EQUIVALENT_DEGREES.items():
            if cand_degree in eq_list or cand_degree == key:
                cand_equivalents.extend(eq_list)
                cand_equivalents.append(key)

        cand_equivalents = list(set(cand_equivalents))

        for req in req_qual_list:
            for cand_eq in cand_equivalents:
                if cand_eq in req or req in cand_eq or "BACHELOR" in req or "GRADUATE" in req or "DEGREE" in req:
                    passed = True
                    matched_req = req
                    break
            if passed:
                break

        # Check minimum percentage if specified
        pct_passed = True
        pct_msg = ""
        if profile.percentage is not None:
            if profile.percentage < 50.0 and ("50%" in " ".join(req_qual_list) or "60%" in " ".join(req_qual_list)):
                pct_passed = False
                pct_msg = f" (Candidate Percentage {profile.percentage}% is below required threshold)"

        final_passed = passed and pct_passed

        if final_passed:
            score = 100.0
            msg = f"✔ Qualification matched: Candidate degree '{profile.degree}' satisfies required qualification criteria ({matched_req or 'Graduation'})."
        elif passed and not pct_passed:
            score = 50.0
            msg = f"⚠️ Qualification partially matched: Degree matches but candidate percentage ({profile.percentage}%) does not meet minimum cut-off."
        else:
            score = 0.0
            msg = f"❌ Qualification check failed: Candidate degree '{profile.degree}' does not match required qualifications ({', '.join(req_qual_list[:2])})."

        logger.info(f"Qualification Check for User {profile.user_id}: {msg}")

        result = RuleEvaluationResult(
            rule_name="Educational Qualification Criteria",
            category="QUALIFICATION",
            passed=final_passed,
            message=msg,
            details={
                "candidate_degree": cand_degree,
                "required_qualifications": req_qual_list,
                "matched_requirement": matched_req
            }
        )
        return result, score
