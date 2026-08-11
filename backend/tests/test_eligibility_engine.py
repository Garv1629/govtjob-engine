import pytest
from app.modules.eligibility.schemas import CandidateProfileInput
from app.modules.eligibility.checkers import (
    AgeEligibilityChecker,
    QualificationEligibilityChecker,
    ExperienceEligibilityChecker,
    PhysicalAndMedicalEligibilityChecker,
    DocumentReadinessChecker
)
from app.modules.eligibility.evaluator import EligibilityEvaluatorEngine
from app.modules.ai.schemas import StructuredJobExtraction
from app.db.repositories import JobRepository, EligibilityRepository


def sample_job_data():
    return StructuredJobExtraction(
        job_title="Assistant Section Officer",
        organization="SSC",
        advt_number="HQ-CGL/2026/01",
        age_limit="18 to 30 years",
        qualification=["Bachelor Degree in any discipline from a recognized University"],
        experience="Nil",
        physical_standards="Height: 157.5 cm",
        documents_required=["Photo", "Signature", "10th Certificate", "Degree Certificate"],
        closing_date="2026-08-30"
    )


def test_age_checker_with_relaxation():
    # 32 year old candidate (DOB: 1994-01-01) - General category -> Fails 30 yr limit
    gen_profile = CandidateProfileInput(
        user_id="user_1",
        full_name="Rahul Sharma",
        dob="1994-01-01",
        category="GENERAL",
        degree="B.Tech"
    )
    res_gen, score_gen = AgeEligibilityChecker.evaluate(gen_profile, sample_job_data())
    assert res_gen.passed is False
    assert score_gen == 0.0

    # Same candidate (DOB: 1994-01-01) - OBC category (+3 yrs relaxation -> 33 max) -> Passes!
    obc_profile = CandidateProfileInput(
        user_id="user_2",
        full_name="Rahul Kumar",
        dob="1994-01-01",
        category="OBC",
        degree="B.Tech"
    )
    res_obc, score_obc = AgeEligibilityChecker.evaluate(obc_profile, sample_job_data())
    assert res_obc.passed is True
    assert score_obc == 100.0


def test_qualification_checker_equivalents():
    # B.E Candidate matching Bachelor Degree requirement
    profile = CandidateProfileInput(
        user_id="user_3",
        full_name="Priya Verma",
        dob="2000-05-15",
        category="GENERAL",
        degree="B.E",
        percentage=72.5
    )
    res, score = QualificationEligibilityChecker.evaluate(profile, sample_job_data())
    assert res.passed is True
    assert score == 100.0


def test_document_checker_missing_docs():
    # Candidate missing Photo & Degree Cert
    profile = CandidateProfileInput(
        user_id="user_4",
        full_name="Amit Singh",
        dob="1998-02-10",
        category="GENERAL",
        degree="B.Sc",
        uploaded_documents=["10TH_PROOF", "SIGNATURE"]
    )
    res, score, missing = DocumentReadinessChecker.evaluate(profile, sample_job_data())
    assert res.passed is False
    assert "Recent Passport Size Photograph" in missing
    assert "B.Sc Degree Certificate / Marksheet" in missing


def test_full_eligibility_evaluator(db_session):
    # Setup test job in DB
    job_repo = JobRepository(db_session)
    job = job_repo.create({
        "source_code": "SSC",
        "title": "Assistant Section Officer",
        "organization": "SSC",
        "advt_number": "HQ-CGL/2026/01",
        "notification_url": "https://ssc.gov.in/aso",
        "apply_url": "https://ssc.gov.in/apply",
        "pdf_url": "https://ssc.gov.in/aso.pdf",
        "last_date": "2026-08-30T18:00:00Z",
        "content_hash": "hash_aso_112233"
    })

    profile = CandidateProfileInput(
        user_id="user_test_5",
        full_name="Neha Gupta",
        dob="1998-08-15",
        category="GENERAL",
        degree="B.Tech",
        percentage=85.0,
        height_cm=162.0,
        uploaded_documents=["PHOTO", "SIGNATURE", "10TH_PROOF", "DEGREE_CERT"]
    )

    evaluator = EligibilityEvaluatorEngine(db_session)
    result = evaluator.evaluate(job_id=job.id, profile=profile, job=sample_job_data())

    assert result.status == "ELIGIBLE"
    assert result.overall_score >= 90.0
    assert len(result.reasons) >= 3
    assert len(result.missing_documents) == 0

    # Verify DB save
    elig_repo = EligibilityRepository(db_session)
    saved = elig_repo.get_by_job_and_user(job.id, "user_test_5")
    assert saved is not None
    assert saved.status == "ELIGIBLE"


def test_eligibility_api_endpoints(client, db_session):
    # Create job in DB
    job_repo = JobRepository(db_session)
    job = job_repo.create({
        "source_code": "UPSC",
        "title": "IAS CSE 2026",
        "organization": "UPSC",
        "advt_number": "05/2026-CSP",
        "notification_url": "https://upsc.gov.in/ias",
        "apply_url": "https://upsc.gov.in/apply",
        "pdf_url": "https://upsc.gov.in/ias.pdf",
        "last_date": "2026-08-28T18:00:00Z",
        "content_hash": "hash_ias_445566"
    })

    # Test Evaluation Endpoint
    eval_resp = client.post("/api/v1/eligibility/evaluate", json={
        "job_id": job.id,
        "profile": {
            "user_id": "user_api_7",
            "full_name": "Vikas Patel",
            "dob": "1997-03-20",
            "category": "OBC",
            "degree": "B.Com",
            "percentage": 68.0,
            "uploaded_documents": ["PHOTO", "SIGNATURE", "10TH_PROOF", "DEGREE_CERT", "OBC_CERT"]
        }
    })
    assert eval_resp.status_code == 200
    eval_data = eval_resp.json()
    assert eval_data["success"] is True
    assert eval_data["data"]["status"] == "ELIGIBLE"

    # Test Retrieval Endpoint
    get_resp = client.get(f"/api/v1/eligibility/results/{job.id}/user_api_7")
    assert get_resp.status_code == 200
    retrieved = get_resp.json()
    assert retrieved["success"] is True
    assert retrieved["data"]["user_id"] == "user_api_7"
