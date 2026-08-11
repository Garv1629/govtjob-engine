from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    items: List[T]


class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    environment: str
    version: str
    database: str = "connected"
