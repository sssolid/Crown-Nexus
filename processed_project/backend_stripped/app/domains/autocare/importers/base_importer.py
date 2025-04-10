from __future__ import annotations
'\nBase importer interface for AutoCare data.\n\nThis module defines the base protocol for all data importers used to import\nAutoCare standard data from various sources into the application database.\n'
import abc
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, TypeVar, Set
from sqlalchemy.ext.asyncio import AsyncSession
from app.logging import get_logger
logger = get_logger('app.domains.autocare.importers.base_importer')
T = TypeVar('T')
class BaseImporter(Protocol):
    db: AsyncSession
    source_path: Path
    async def validate_source(self) -> bool:
        ...
    async def import_data(self) -> Dict[str, Any]:
        ...