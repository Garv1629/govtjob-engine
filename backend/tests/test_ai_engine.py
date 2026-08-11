import pytest
from app.modules.ai.parsers import FileValidatorAndFormatDetector, TextCleanerAndChunker, NativePDFParser, OCREngineFallback
from app.modules.ai.providers import LLMProviderFactory, MockLLMAdapter
from app.modules.ai.validator import ExtractionJSONValidator
from app.modules.ai.confidence import ConfidenceScoringEngine
from app.modules.ai.pipeline import AIJobIntelligencePipeline
from app.db.repositories import JobRepository, JobExtractionRepository


def test_file_format_detector():
    # Test Blank PDF
    fmt, meta = FileValidatorAndFormatDetector.inspect_bytes(b"")
    assert fmt == "BLANK_PDF"

    # Test HTML Payload
    html_bytes = b"<html><body><h1>Govt Notice</h1></body></html>"
    fmt_html, meta_html = FileValidatorAndFormatDetector.inspect_bytes(html_bytes)
    assert fmt_html == "HTML_PAGE"


def test_text_cleaner():
    raw = "--- PAGE 1 ---\nOfficial Notice\nPage 1 of 5\n\n\nDetails here."
    cleaned = TextCleanerAndChunker.clean_text(raw)
    assert "--- PAGE 1 ---" not in cleaned
    assert "Page 1 of 5" not in cleaned
    assert "Official Notice" in cleaned


@pytest.mark.asyncio
async def test_mock_llm_adapter():
    adapter = MockLLMAdapter()
    sample_text = "Notice No. 05/2026-CSP for Civil Services Examination 2026 by UPSC."
    data, elapsed = await adapter.extract_structured_data(sample_text)
    
    assert data.job_title == "Civil Services Examination 2026"
    assert data.organization == "UPSC"
    assert data.advt_number == "05/2026-CSP"
    assert len(data.qualification) > 0
    assert elapsed > 0


def test_json_validator_and_confidence():
    mock_data, _ = pytest.asyncio.run(MockLLMAdapter().extract_structured_data("Sample text"))
    errors, warnings = ExtractionJSONValidator.validate(mock_data)
    
    assert len(errors) == 0
    confidence = ConfidenceScoringEngine.compute_confidence(mock_data, errors, warnings)
    assert confidence.score >= 0.8
    assert confidence.mandatory_fields_valid is True


@pytest.mark.asyncio
async def test_ai_pipeline_execution(db_session):
    # Create test job
    job_repo = JobRepository(db_session)
    job = job_repo.create({
        "source_code": "UPSC",
        "title": "Civil Services Exam 2026",
        "organization": "UPSC",
        "advt_number": "05/2026-CSP",
        "notification_url": "https://upsc.gov.in/notice",
        "apply_url": "https://upsc.gov.in/apply",
        "pdf_url": "https://upsc.gov.in/notice.pdf",
        "last_date": "2026-08-28T18:00:00Z",
        "content_hash": "hash123456789"
    })

    pipeline = AIJobIntelligencePipeline(db_session, provider_name="Mock")
    response = await pipeline.execute_pipeline(job.id)

    assert response.job_id == job.id
    assert response.confidence_score >= 0.8
    assert response.data.organization == "UPSC"

    # Verify DB persistence
    ext_repo = JobExtractionRepository(db_session)
    saved = ext_repo.get_by_job_id(job.id)
    assert saved is not None
    assert saved.llm_provider == "Mock"
    assert saved.extracted_json["job_title"] == response.data.job_title


def test_ai_api_endpoints(client, db_session):
    # Create job in DB
    job_repo = JobRepository(db_session)
    job = job_repo.create({
        "source_code": "SSC",
        "title": "SSC CGL 2026",
        "organization": "SSC",
        "advt_number": "CGL/2026/01",
        "notification_url": "https://ssc.gov.in/cgl",
        "apply_url": "https://ssc.gov.in/apply",
        "pdf_url": "https://ssc.gov.in/cgl.pdf",
        "last_date": "2026-09-15T18:00:00Z",
        "content_hash": "hash_ssc_998877"
    })

    # Test Extraction Endpoint
    extract_resp = client.post("/api/v1/ai/extract", json={
        "job_id": job.id,
        "provider": "Mock"
    })
    assert extract_resp.status_code == 200
    res_json = extract_resp.json()
    assert res_json["success"] is True
    assert res_json["data"]["job_id"] == job.id

    # Test Results Retrieval Endpoint
    results_resp = client.get(f"/api/v1/ai/results/{job.id}")
    assert results_resp.status_code == 200
    res_data = results_resp.json()
    assert res_data["success"] is True
    assert res_data["data"]["job_id"] == job.id
