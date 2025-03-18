from __future__ import annotations
import traceback
from typing import Any, Dict

from fastapi import Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions.base import AppException, ErrorCode, ErrorResponse, ErrorSeverity
from app.core.logging import get_logger

logger = get_logger("app.core.exceptions.handlers")

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle AppException instances."""
    # Move implementation from original file

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI's RequestValidationError."""
    # Move implementation from original file

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI's HTTPException."""
    # Move implementation from original file

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions."""
    # Move implementation from original file
