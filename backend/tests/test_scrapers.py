import pytest
from app.modules.scrapers.registry import ScraperPluginRegistry
from app.modules.scrapers.engine import JobDiscoveryEngine
from app.modules.scrapers.plugins.ssc import SSCScraper
from app.modules.scrapers.plugins.upsc import UPSCScraper
from app.modules.scrapers.plugins.ncs import NCSScraper
from app.db.repositories import JobRepository, ScraperHealthRepository, DiscoveryLogRepository


@pytest.mark.asyncio
async def test_plugin_registry_discovery():
    ScraperPluginRegistry.discover_plugins()
    plugins = ScraperPluginRegistry.get_all_plugins()
    codes = [p.source_code for p in plugins]
    
    assert "SSC" in codes
    assert "UPSC" in codes
    assert "NCS" in codes


@pytest.mark.asyncio
async def test_ssc_scraper_lifecycle():
    scraper = SSCScraper()
    await scraper.initialize()
    assert scraper._is_initialized is True
    
    jobs = await scraper.fetch_jobs()
    assert len(jobs) > 0
    
    raw_job = jobs[0]
    normalized = scraper.normalize(raw_job)
    assert normalized.organization == "Staff Selection Commission"
    assert normalized.source_name == "SSC"
    assert normalized.advt_number == "HQ-CGL/2026/01"
    
    is_valid = scraper.validate(normalized)
    assert is_valid is True

    await scraper.shutdown()
    assert scraper.client.is_closed is True


@pytest.mark.asyncio
async def test_job_discovery_engine_deduplication(db_session):
    ScraperPluginRegistry.register(SSCScraper)
    engine = JobDiscoveryEngine(db_session)
    
    # First Run -> Discovers NEW
    ssc_plugin = SSCScraper()
    res1 = await engine.run_scraper(ssc_plugin)
    assert res1["status"] == "SUCCESS"
    assert res1["discovered_new"] == 1
    assert res1["duplicates_skipped"] == 0

    # Second Run -> Identical content hash -> Skips Duplicate
    ssc_plugin_2 = SSCScraper()
    res2 = await engine.run_scraper(ssc_plugin_2)
    assert res2["status"] == "SUCCESS"
    assert res2["discovered_new"] == 0
    assert res2["duplicates_skipped"] == 1

    # Verify Database Persistence
    job_repo = JobRepository(db_session)
    jobs = job_repo.get_all()
    assert len(jobs) == 1
    assert jobs[0].source_code == "SSC"

    # Verify Health Telemetry Recorded
    health_repo = ScraperHealthRepository(db_session)
    health = health_repo.get_by_source_code("SSC")
    assert health is not None
    assert health.status == "HEALTHY"
    assert health.total_jobs_found == 2


def test_scrapers_api_endpoints(client):
    # Test List Plugins
    response = client.get("/api/v1/scrapers/plugins")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert len(json_data["data"]) >= 3

    # Test Run Scrapers Endpoint
    run_resp = client.post("/api/v1/scrapers/run?source_code=UPSC")
    assert run_resp.status_code == 200
    run_data = run_resp.json()
    assert run_data["success"] is True
    assert run_data["data"][0]["source_code"] == "UPSC"
    assert run_data["data"][0]["status"] == "SUCCESS"

    # Test Health Endpoint
    health_resp = client.get("/api/v1/scrapers/health")
    assert health_resp.status_code == 200
    health_data = health_resp.json()
    assert health_data["success"] is True

    # Test Logs Endpoint
    logs_resp = client.get("/api/v1/scrapers/logs")
    assert logs_resp.status_code == 200
    logs_data = logs_resp.json()
    assert logs_data["success"] is True
    assert len(logs_data["data"]) > 0
