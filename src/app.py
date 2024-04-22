# ============================================
#                                           
#   Project Name :  be_sistem_pakar               
#   -------------------------------------   
#   Create by    : hexa at 25/02/24       
#   Copyright © 2024 Delameta Bilano     
#                                           
# ============================================
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.routers import routers

app_version = 'v1'
api_name = 'Backend Sistem Pakar'
def app():
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=api_name,
            version=app_version,
            routes=app.routes
        )

        app.openapi_schema = openapi_schema
        return app.openapi_schema


    app = FastAPI(
        default_response_class=ORJSONResponse,
        title=api_name,
        version=app_version,
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": True,
        }
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
        max_age=600
    )
    app.openapi = custom_openapi
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # custom exception handler
    add_pagination(app)
    routers(app)
    return app

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error",
                 "detail": f"{exc.errors()[0]['type']}, {exc.errors()[0]['loc'][1]} {exc.errors()[0]['msg']}"},
    )
