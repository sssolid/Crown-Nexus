from __future__ import annotations
'\nBase interfaces for data import pipelines.\n\nThis module defines protocol classes for data import pipelines that orchestrate\nthe extract, transform, and load process.\n'
from typing import Any, Dict, Protocol, TypeVar, Union
from app.data_import.connectors.base import Connector
from app.data_import.connectors.file_connector import FileConnector
from app.data_import.connectors.filemaker_connector import FileMakerConnector
from app.data_import.importers.base import Importer
from app.data_import.processors.base import Processor
T = TypeVar('T')
class Pipeline(Protocol[T]):
    connector: Union[Connector, FileMakerConnector, FileConnector]
    processor: Processor[T]
    importer: Importer[T]
    async def run(self, query: str, **params: Any) -> Dict[str, Any]:
        ...