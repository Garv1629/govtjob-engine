from typing import Any, Optional, Dict
from fastapi import HTTPException, status


class BaseAppException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = "An unexpected error occurred",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(BaseAppException):
    def __init__(self, item: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{item} not found"
        )


class UnauthorizedException(BaseAppException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


class DatabaseException(BaseAppException):
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ExternalServiceException(BaseAppException):
    def __init__(self, service: str, detail: str = "External integration failed"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"[{service}] {detail}"
        )
