from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from app.db.base import Base
from app.db.models.job import Job
from app.db.models.job_source import JobSource
from app.db.models.scraper_health import ScraperHealth
from app.db.models.discovery_log import DiscoveryLog
from app.db.models.job_extraction import JobExtraction
from app.db.models.eligibility_result import EligibilityResult
from app.db.models.automation_session import AutomationSession
from app.db.models.workflow_instance import WorkflowInstance, WorkflowCheckpoint

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Generic repository providing standardized CRUD database operations."""

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: str) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> T:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, id: str, obj_in: dict) -> Optional[T]:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in obj_in.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: str) -> bool:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        self.db.delete(db_obj)
        self.db.commit()
        return True


class JobRepository(BaseRepository[Job]):
    def __init__(self, db: Session):
        super().__init__(Job, db)

    def get_by_content_hash(self, content_hash: str) -> Optional[Job]:
        return self.db.query(Job).filter(Job.content_hash == content_hash).first()

    def get_by_advt_and_source(self, source_code: str, advt_number: str) -> Optional[Job]:
        return self.db.query(Job).filter(
            Job.source_code == source_code,
            Job.advt_number == advt_number
        ).first()


class JobSourceRepository(BaseRepository[JobSource]):
    def __init__(self, db: Session):
        super().__init__(JobSource, db)

    def get_by_code(self, code: str) -> Optional[JobSource]:
        return self.db.query(JobSource).filter(JobSource.code == code).first()

    def get_active_sources(self) -> List[JobSource]:
        return self.db.query(JobSource).filter(JobSource.is_enabled == True).order_by(JobSource.priority.asc()).all()


class ScraperHealthRepository(BaseRepository[ScraperHealth]):
    def __init__(self, db: Session):
        super().__init__(ScraperHealth, db)

    def get_by_source_code(self, source_code: str) -> Optional[ScraperHealth]:
        return self.db.query(ScraperHealth).filter(ScraperHealth.source_code == source_code).first()


class DiscoveryLogRepository(BaseRepository[DiscoveryLog]):
    def __init__(self, db: Session):
        super().__init__(DiscoveryLog, db)

    def get_recent(self, limit: int = 50) -> List[DiscoveryLog]:
        return self.db.query(DiscoveryLog).order_by(DiscoveryLog.discovered_at.desc()).limit(limit).all()


class JobExtractionRepository(BaseRepository[JobExtraction]):
    def __init__(self, db: Session):
        super().__init__(JobExtraction, db)

    def get_by_job_id(self, job_id: str) -> Optional[JobExtraction]:
        return self.db.query(JobExtraction).filter(JobExtraction.job_id == job_id).order_by(JobExtraction.created_at.desc()).first()


class EligibilityRepository(BaseRepository[EligibilityResult]):
    def __init__(self, db: Session):
        super().__init__(EligibilityResult, db)

    def get_by_job_and_user(self, job_id: str, user_id: str) -> Optional[EligibilityResult]:
        return self.db.query(EligibilityResult).filter(
            EligibilityResult.job_id == job_id,
            EligibilityResult.user_id == user_id
        ).order_by(EligibilityResult.evaluated_at.desc()).first()


class AutomationSessionRepository(BaseRepository[AutomationSession]):
    def __init__(self, db: Session):
        super().__init__(AutomationSession, db)

    def get_by_application_id(self, application_id: str) -> Optional[AutomationSession]:
        return self.db.query(AutomationSession).filter(AutomationSession.application_id == application_id).order_by(AutomationSession.created_at.desc()).first()


class WorkflowInstanceRepository(BaseRepository[WorkflowInstance]):
    def __init__(self, db: Session):
        super().__init__(WorkflowInstance, db)

    def get_by_job_and_user(self, job_id: str, user_id: str) -> Optional[WorkflowInstance]:
        return self.db.query(WorkflowInstance).filter(
            WorkflowInstance.job_id == job_id,
            WorkflowInstance.user_id == user_id
        ).order_by(WorkflowInstance.created_at.desc()).first()

    def get_active_workflows(self) -> List[WorkflowInstance]:
        return self.db.query(WorkflowInstance).filter(
            WorkflowInstance.current_state.in_([
                "DISCOVERED", "PROCESSING", "ANALYZED", "WAITING_FOR_USER",
                "AUTOMATION_RUNNING", "WAITING_FOR_MANUAL_ACTION", "RESUMED"
            ])
        ).all()

    def get_incomplete_workflows(self) -> List[WorkflowInstance]:
        return self.db.query(WorkflowInstance).filter(
            WorkflowInstance.current_state.notin_(["COMPLETED", "CANCELLED"])
        ).all()


class WorkflowCheckpointRepository(BaseRepository[WorkflowCheckpoint]):
    def __init__(self, db: Session):
        super().__init__(WorkflowCheckpoint, db)

    def get_latest_checkpoint(self, workflow_id: str) -> Optional[WorkflowCheckpoint]:
        return self.db.query(WorkflowCheckpoint).filter(
            WorkflowCheckpoint.workflow_id == workflow_id
        ).order_by(WorkflowCheckpoint.timestamp.desc()).first()

    def get_checkpoints_for_workflow(self, workflow_id: str) -> List[WorkflowCheckpoint]:
        return self.db.query(WorkflowCheckpoint).filter(
            WorkflowCheckpoint.workflow_id == workflow_id
        ).order_by(WorkflowCheckpoint.timestamp.asc()).all()

