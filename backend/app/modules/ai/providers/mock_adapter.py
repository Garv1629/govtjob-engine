import time
import re
from typing import Tuple
from datetime import datetime, timezone, timedelta
from app.modules.ai.providers.base import LLMProviderAdapter
from app.modules.ai.schemas import StructuredJobExtraction
from app.core.logging import logger


class MockLLMAdapter(LLMProviderAdapter):
    """Deterministic Mock LLM Provider Adapter for offline testing and fallback execution."""

    def __init__(self, model_name: str = "mock-gpt-4", api_key: str = "mock"):
        super().__init__(model_name, api_key)

    async def extract_structured_data(self, cleaned_text: str) -> Tuple[StructuredJobExtraction, float]:
        start_time = time.time()
        logger.info("Executing Mock LLM Extraction Adapter...")

        # Pattern-based heuristics on cleaned text to simulate deep extraction
        title_match = re.search(r"(?:Examination|Recruitment|Post|Notice for)\s+([^\n\.]+)", cleaned_text, re.IGNORECASE)
        job_title = title_match.group(1).strip() if title_match else "Government Recruitment Examination 2026"

        advt_match = re.search(r"(?:Advt|Notification|Notice)\s*(?:No|Num|\.)?\s*[:\-]?\s*([A-Za-z0-9/\-_]+)", cleaned_text, re.IGNORECASE)
        advt_number = advt_match.group(1).strip() if advt_match else "HQ-JOB/2026/01"

        org_match = re.search(r"(UPSC|SSC|NCS|ISRO|DRDO|RRB|IBPS)", cleaned_text, re.IGNORECASE)
        organization = org_match.group(1).upper() if org_match else "Union Recruitment Board"

        today = datetime.now(timezone.utc)
        open_d = today.strftime("%Y-%m-%d")
        close_d = (today + timedelta(days=30)).strftime("%Y-%m-%d")

        extraction = StructuredJobExtraction(
            job_title=job_title,
            organization=organization,
            department="Ministry of Personnel, Public Grievances and Pensions",
            advt_number=advt_number,
            vacancies=1250,
            salary="Rs. 44,900 - 1,42,400 per month",
            pay_level="Level 7 (7th CPC)",
            grade_pay="Grade Pay 4600",
            qualification=[
                "Bachelor Degree in any discipline from a recognized University",
                "Basic Computer Operations Certification"
            ],
            age_limit="18 to 30 years as on closing date",
            age_relaxation={
                "OBC": "3 Years",
                "SC_ST": "5 Years",
                "PwD": "10 Years",
                "ExServicemen": "3 Years after deduction of military service"
            },
            experience="Nil for General Posts; 2 Years relevant experience for Specialist Roles",
            application_fee={
                "General_OBC": "Rs. 100",
                "SC_ST_Female_PwD": "Nil (Exempted)"
            },
            selection_process=[
                "Tier-I: Computer Based Examination (Objective)",
                "Tier-II: Subjective / Descriptive Paper & Skill Test",
                "Document Verification & Medical Examination"
            ],
            exam_pattern={
                "Tier_I": {
                    "General Intelligence": "25 Questions / 50 Marks",
                    "General Awareness": "25 Questions / 50 Marks",
                    "Quantitative Aptitude": "25 Questions / 50 Marks",
                    "English Comprehension": "25 Questions / 50 Marks",
                    "Total Duration": "60 Minutes"
                }
            },
            syllabus=[
                "Quantitative Aptitude: Number Systems, Algebra, Geometry, Trigonometry, Data Interpretation",
                "General Intelligence: Analogies, Syllogisms, Pattern Recognition, Coding-Decoding",
                "General English: Grammar, Vocabulary, Error Spotting, Comprehension Passages"
            ],
            medical_standards="Distant Vision: 6/6 (Better Eye), 6/9 (Worse Eye). Free from color blindness for technical posts.",
            physical_standards="Height: 157.5 cm (Male), 152 cm (Female). Chest: 81 cm with 5 cm expansion.",
            documents_required=[
                "10th Standard Certificate (DOB Proof)",
                "Essential Educational Qualification Degree & Marksheets",
                "Caste / Category Certificate (OBC-NCL / SC / ST / EWS)",
                "Recent Passport Size Photograph & Signature Scan"
            ],
            job_responsibilities="Assisting in policy formulation, scrutiny of files, handling official correspondence, and inter-ministerial communication.",
            posting="All-India Service Liability (Headquarters in New Delhi with zonal postings across India)",
            transfer_policy="Eligible for rotational transfer every 3 years across Regional Offices.",
            promotion="Hierarchical promotion from Assistant Section Officer (ASO) to Section Officer (SO) after 5 years service.",
            working_hours="09:00 AM to 05:30 PM (5-Day Work Week, Monday to Friday)",
            probation="2 Years from date of appointment",
            leave_policy="30 Days Earned Leave, 8 Days Casual Leave, 20 Days Half Pay Leave per annum",
            important_dates={
                "Opening_Date": open_d,
                "Closing_Date": close_d,
                "Exam_Date": (today + timedelta(days=60)).strftime("%Y-%m-%d")
            },
            opening_date=open_d,
            closing_date=close_d,
            official_website="https://ssc.gov.in",
            official_notification_pdf="https://ssc.gov.in/files/notice_2026.pdf",
            official_apply_link="https://ssc.gov.in/apply"
        )

        elapsed_ms = (time.time() - start_time) * 1000
        logger.info(f"Mock LLM extraction completed in {elapsed_ms:.2f}ms")
        return extraction, elapsed_ms
