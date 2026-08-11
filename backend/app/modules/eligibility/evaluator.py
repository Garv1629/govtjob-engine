from typing import List
from sqlalchemy.orm import Session

from app.modules.eligibility.schemas import (
    CandidateProfileInput,
    EligibilityEvaluationOutput,
    ScoreBreakdown,
    RuleEvaluationResult
)
from app.modules.eligibility.checkers import (
    AgeEligibilityChecker,
    QualificationEligibilityChecker,
    ExperienceEligibilityChecker,
    PhysicalAndMedicalEligibilityChecker,
    DocumentReadinessChecker
)
from app.modules.ai.schemas import StructuredJobExtraction
from app.db.repositories import EligibilityRepository
from app.core.logging import logger


class EligibilityEvaluatorEngine:
    """
    Main AI Eligibility Engine. Evaluates candidate profiles against extracted job specifications,
    producing explainable decision trees with component score breakdowns and natural language justifications.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repo = EligibilityRepository(db)

    def evaluate(self, job_id: str, profile: CandidateProfileInput, job: StructuredJobExtraction) -> EligibilityEvaluationOutput:
        logger.info(f"Starting Eligibility Evaluation for User '{profile.user_id}' against Job '{job_id}' ({job.job_title})")

        matched_rules: List[RuleEvaluationResult] = []
        failed_rules: List[RuleEvaluationResult] = []
        reasons: List[str] = []
        warnings: List[str] = []
        recommendations: List[str] = []

        # 1. Age Rule Evaluation
        age_res, age_score = AgeEligibilityChecker.evaluate(profile, job)
        if age_res.passed:
            matched_rules.append(age_res)
            reasons.append(age_res.message)
        else:
            failed_rules.append(age_res)
            reasons.append(age_res.message)

        # 2. Qualification Rule Evaluation
        qual_res, qual_score = QualificationEligibilityChecker.evaluate(profile, job)
        if qual_res.passed:
            matched_rules.append(qual_res)
            reasons.append(qual_res.message)
        else:
            failed_rules.append(qual_res)
            reasons.append(qual_res.message)

        # 3. Experience Rule Evaluation
        exp_res, exp_score = ExperienceEligibilityChecker.evaluate(profile, job)
        if exp_res.passed:
            matched_rules.append(exp_res)
            reasons.append(exp_res.message)
        else:
            failed_rules.append(exp_res)
            reasons.append(exp_res.message)

        # 4. Physical & Medical Rule Evaluation
        med_res, med_score = PhysicalAndMedicalEligibilityChecker.evaluate(profile, job)
        if med_res.passed:
            matched_rules.append(med_res)
        else:
            warnings.append(med_res.message)

        # 5. Document Readiness Evaluation
        doc_res, doc_score, missing_docs = DocumentReadinessChecker.evaluate(profile, job)
        if doc_res.passed:
            matched_rules.append(doc_res)
        else:
            warnings.append(doc_res.message)

        # Build Recommendations
        if missing_docs:
            recommendations.append(f"Upload missing document scans ({', '.join(missing_docs)}) into Document Vault before submitting form.")

        if not qual_res.passed:
            recommendations.append("Review equivalency certificate options from university for degree validation.")

        # Compute Overall Score (Weights: Age 30%, Qual 35%, Exp 20%, Med 5%, Doc 10%)
        overall_score = round(
            (age_score * 0.30) +
            (qual_score * 0.35) +
            (exp_score * 0.20) +
            (med_score * 0.05) +
            (doc_score * 0.10),
            1
        )

        # Determine Final Status
        # Hard deal-breakers: Age or Qualification failure means NOT_ELIGIBLE
        critical_failed = not age_res.passed or not qual_res.passed or not exp_res.passed

        if not critical_failed and len(missing_docs) == 0:
            status = "ELIGIBLE"
        elif not critical_failed and len(missing_docs) > 0:
            status = "PARTIALLY_ELIGIBLE"
        else:
            status = "NOT_ELIGIBLE"

        scores_breakdown = ScoreBreakdown(
            overall_score=overall_score,
            age_score=age_score,
            qualification_score=qual_score,
            experience_score=exp_score,
            medical_score=med_score,
            document_score=doc_score
        )

        output = EligibilityEvaluationOutput(
            job_id=job_id,
            user_id=profile.user_id,
            status=status,
            overall_score=overall_score,
            scores=scores_breakdown,
            reasons=reasons,
            matched_rules=matched_rules,
            failed_rules=failed_rules,
            missing_documents=missing_docs,
            warnings=warnings,
            recommendations=recommendations
        )

        # Save to database
        self.repo.create({
            "job_id": job_id,
            "user_id": profile.user_id,
            "status": status,
            "overall_score": overall_score,
            "scores": scores_breakdown.model_dump(),
            "reasons": reasons,
            "matched_rules": [r.model_dump() for r in matched_rules],
            "failed_rules": [r.model_dump() for r in failed_rules],
            "missing_documents": missing_docs,
            "recommendations": recommendations
        })

        logger.info(f"Eligibility Evaluation completed for User '{profile.user_id}': Status={status}, OverallScore={overall_score}%")
        return output
