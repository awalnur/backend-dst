# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 09/03/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from typing import Any

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    status_code: int
    message: str
    data: Any | None

class ErrorResponse(BaseModel):
    detail: str

class Token(BaseModel):
    access_token: str
    token_type: str