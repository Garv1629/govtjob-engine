from typing import Tuple, List
from app.modules.eligibility.schemas import CandidateProfileInput, RuleEvaluationResult
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class DocumentReadinessChecker:
    """
    Verifies presence of mandated candidate documents:
    - Candidate Photo & Signature
    - 10th DOB Certificate
    - Degree Marksheet / Certificate
    - Category / Caste Certificate (if OBC / SC / ST / EWS)
    - Driving License (if required)
    """

    @staticmethod
    def evaluate(profile: CandidateProfileInput, job: StructuredJobExtraction) -> Tuple[RuleEvaluationResult, float, List[str]]:
        uploaded = [doc.upper() for doc in profile.uploaded_documents]
        missing_docs: List[str] = []

        # Core mandatory documents for every application
        if "PHOTO" not in uploaded and "PASSPORT_PHOTO" not in uploaded:
            missing_docs.append("Recent Passport Size Photograph")

        if "SIGNATURE" not in uploaded:
            missing_docs.append("Candidate Signature Scan")

        if "10TH_PROOF" not in uploaded and "DOB_PROOF" not in uploaded:
            missing_docs.append("10th Standard Certificate / DOB Proof")

        if "DEGREE_CERT" not in uploaded and "GRADUATION_CERT" not in uploaded:
            missing_docs.append(f"{profile.degree} Degree Certificate / Marksheet")

        cat = profile.category.upper()
        if cat in ["OBC", "SC", "ST", "EWS"]:
            if f"{cat}_CERT" not in uploaded and "CATEGORY_CERT" not in uploaded:
                missing_docs.append(f"Valid {cat} Category Certificate")

        # Driving License check if post requires it
        if "DRIVING LICENSE" in " ".join(job.documents_required).upper() or "LMV" in " ".join(job.qualification).upper():
            if not profile.has_driving_license:
                missing_docs.append("Valid Motor Vehicle Driving License (LMV/HMV)")

        passed = len(missing_docs) == 0

        if passed:
            score = 100.0
            msg = "✔ Document Vault Readiness: All mandatory certificates and scans are uploaded in document vault."
        else:
            present_count = max(0, 5 - len(missing_docs))
            score = round((present_count / 5.0) * 100, 1)
            msg = f"⚠️ Document Vault missing {len(missing_docs)} required file(s): {', '.join(missing_docs)}."

        logger.info(f"Document Readiness Check for User {profile.user_id}: {msg}")

        result = RuleEvaluationResult(
            rule_name="Document Vault Readiness",
            category="DOCUMENT",
            passed=passed,
            message=msg,
            details={"missing_documents": missing_docs}
        )
        return result, score, missing_docs
