# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 09/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================

from typing import Any

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"
    HEADER = None

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class CredentialsException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Couldn't validate credentials"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class ForbiddenException(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Access Denied – You don’t have permission to access"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class ValidationError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    DETAIL = "Validation Error"
