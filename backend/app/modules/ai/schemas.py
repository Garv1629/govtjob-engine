from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class StructuredJobExtraction(BaseModel):
    """
    Complete Structured AI Output Schema representing all 32 core fields extracted from Government Job Notices.
    """
    job_title: str = Field(..., description="Official Job Title or Designation Name")
    organization: str = Field(..., description="Recruitment Body / Board Name")
    department: Optional[str] = Field(None, description="Ministry or Government Department")
    advt_number: str = Field(..., description="Official Advertisement / Notification Serial Number")
    
    vacancies: Optional[int] = Field(0, description="Total Number of Openings / Vacancies")
    salary: Optional[str] = Field(None, description="Basic Pay / Gross Monthly CTC Range")
    pay_level: Optional[str] = Field(None, description="7th CPC Pay Matrix Level (e.g. Level 7, Level 10)")
    grade_pay: Optional[str] = Field(None, description="6th CPC Grade Pay if applicable (e.g. GP 4600)")
    
    qualification: List[str] = Field(default_factory=list, description="List of Required Educational Qualifications")
    age_limit: Optional[str] = Field(None, description="Minimum and Maximum Candidate Age Criteria")
    age_relaxation: Optional[Dict[str, str]] = Field(default_factory=dict, description="Category-wise Age Relaxation Rules (SC/ST/OBC/Ex-Servicemen)")
    experience: Optional[str] = Field(None, description="Prior Work Experience Requirements")
    
    application_fee: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Category-wise Application Fee Breakdown")
    selection_process: List[str] = Field(default_factory=list, description="Stages of Examination / Interview / Typing Test")
    exam_pattern: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Tier/Phase-wise Exam Pattern, Subjects, Marks")
    syllabus: List[str] = Field(default_factory=list, description="Detailed Subject Syllabus Topics")
    
    medical_standards: Optional[str] = Field(None, description="Vision & Medical Eligibility Criteria")
    physical_standards: Optional[str] = Field(None, description="Height, Chest, Running, Physical Fitness Test Standards")
    documents_required: List[str] = Field(default_factory=list, description="Mandatory Certificates / Scans to Upload")
    
    job_responsibilities: Optional[str] = Field(None, description="Key Duties & Work Description")
    posting: Optional[str] = Field(None, description="Job Location / All-India Service Liability")
    transfer_policy: Optional[str] = Field(None, description="Inter-cadre / Zonal Transfer Rules")
    promotion: Optional[str] = Field(None, description="Career Progression Hierarchy")
    working_hours: Optional[str] = Field(None, description="Shift / Shift Timing / Office Hours")
    probation: Optional[str] = Field(None, description="Probationary Period Duration (e.g. 2 Years)")
    leave_policy: Optional[str] = Field(None, description="Annual Leave & Sick Leave Entitlement")
    
    important_dates: Optional[Dict[str, str]] = Field(default_factory=dict, description="Key Event Timeline")
    opening_date: Optional[str] = Field(None, description="Online Application Start Date (YYYY-MM-DD)")
    closing_date: Optional[str] = Field(None, description="Online Application Deadline (YYYY-MM-DD)")
    
    official_website: Optional[str] = Field(None, description="Official Portal URL")
    official_notification_pdf: Optional[str] = Field(None, description="Official PDF Direct Link")
    official_apply_link: Optional[str] = Field(None, description="Direct Registration/Application Form URL")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ExtractionConfidence(BaseModel):
    score: float = Field(..., description="Overall Extraction Confidence Score from 0.0 to 1.0")
    mandatory_fields_valid: bool = Field(..., description="Whether critical mandatory fields passed validation")
    validation_warnings: List[str] = Field(default_factory=list, description="List of minor validation or formatting warnings")
    validation_errors: List[str] = Field(default_factory=list, description="List of critical validation errors")


class ExtractionRequest(BaseModel):
    job_id: str = Field(..., description="Target Job Record ID to extract")
    pdf_url: Optional[str] = Field(None, description="Optional Direct PDF URL override")
    raw_text: Optional[str] = Field(None, description="Optional Raw Text override")
    provider: Optional[str] = Field("OpenAI", description="Target LLM Provider (OpenAI, Mock)")


class ExtractionResponse(BaseModel):
    job_id: str
    extraction_id: str
    confidence_score: float
    llm_provider: str
    llm_model_used: str
    processing_time_ms: float
    ocr_time_ms: float
    llm_time_ms: float
    data: StructuredJobExtraction
    confidence: ExtractionConfidence
