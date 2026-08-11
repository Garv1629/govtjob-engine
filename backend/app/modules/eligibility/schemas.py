from typing import Optional, List, Dict, Any
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class CandidateProfileInput(BaseModel):
    user_id: str = Field(..., description="Unique Candidate User ID")
    full_name: str = Field(..., description="Full Name of Candidate")
    dob: str = Field(..., description="Date of Birth in YYYY-MM-DD format")
    gender: str = Field("Male", description="Male, Female, Transgender")
    category: str = Field("GENERAL", description="GENERAL, OBC, SC, ST, EWS")
    nationality: str = Field("Indian", description="Nationality")
    state: str = Field("Delhi", description="State of Permanent Address")
    domicile: str = Field("Delhi", description="State Domicile Certificate")
    is_pwd: bool = Field(False, description="Person with Benchmark Disability (PwD)")
    is_ex_serviceman: bool = Field(False, description="Ex-Serviceman status")
    ex_service_years: float = Field(0.0, description="Military Service Duration in Years")

    # Education
    degree: str = Field(..., description="Highest Qualification Degree (e.g. B.Tech, B.Sc, B.Com, 12th, 10th)")
    branch: Optional[str] = Field(None, description="Discipline / Specialization e.g. Computer Science")
    university: Optional[str] = Field(None, description="Board or University Name")
    passing_year: Optional[int] = Field(None, description="Graduation / Passing Year")
    percentage: Optional[float] = Field(None, description="Marks Percentage (0 to 100)")
    cgpa: Optional[float] = Field(None, description="CGPA (0 to 10.0)")

    # Experience
    experience_years: float = Field(0.0, description="Total Relevant Work Experience in Years")
    skills: List[str] = Field(default_factory=list, description="Candidate Skill Tags")
    languages: List[str] = Field(default_factory=list, description="Known Spoken & Written Languages")

    # Physical & Medical
    height_cm: Optional[float] = Field(None, description="Height in Centimeters")
    weight_kg: Optional[float] = Field(None, description="Weight in Kilograms")
    chest_cm: Optional[float] = Field(None, description="Chest Measurement in Centimeters")
    vision: Optional[str] = Field(None, description="Vision standard e.g. 6/6, 6/9")

    # Licenses & Certificates
    has_driving_license: bool = Field(False, description="Valid Driving License Holder")
    driving_license_type: Optional[str] = Field(None, description="LMV, HMV, Two Wheeler")
    uploaded_documents: List[str] = Field(default_factory=list, description="List of document types uploaded e.g. ['PHOTO', 'SIGNATURE', '10TH_PROOF', 'DEGREE_CERT', 'OBC_CERT']")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ScoreBreakdown(BaseModel):
    overall_score: float = Field(..., description="Overall Eligibility Fit Score (0.0 to 100.0)")
    age_score: float = Field(..., description="Age Eligibility Match (0.0 to 100.0)")
    qualification_score: float = Field(..., description="Educational Qualification Match (0.0 to 100.0)")
    experience_score: float = Field(..., description="Work Experience Match (0.0 to 100.0)")
    medical_score: float = Field(..., description="Physical & Medical Standards Match (0.0 to 100.0)")
    document_score: float = Field(..., description="Document Vault Readiness Match (0.0 to 100.0)")


class RuleEvaluationResult(BaseModel):
    rule_name: str
    category: str # AGE, QUALIFICATION, EXPERIENCE, MEDICAL, DOCUMENT, NATIONALITY
    passed: bool
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class EligibilityEvaluationOutput(BaseModel):
    job_id: str
    user_id: str
    status: str = Field(..., description="ELIGIBLE, PARTIALLY_ELIGIBLE, NOT_ELIGIBLE")
    overall_score: float
    scores: ScoreBreakdown
    reasons: List[str] = Field(..., description="Detailed explainable bullet points")
    matched_rules: List[RuleEvaluationResult]
    failed_rules: List[RuleEvaluationResult]
    missing_documents: List[str]
    warnings: List[str]
    recommendations: List[str]
