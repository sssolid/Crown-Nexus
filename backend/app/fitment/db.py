"""
Database access for fitment data.

This module provides functions to interact with
VCDB and PCDB databases for fitment data.
"""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple, Union

import pandas as pd
import pyodbc
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base

from .models import PCDBPosition, PartTerminology, VCDBVehicle
from .exceptions import DatabaseError


logger = logging.getLogger(__name__)


class AccessDBClient:
    """Client for Microsoft Access databases (VCDB and PCDB)."""

    def __init__(self, db_path: str) -> None:
        """
        Initialize the Access DB client.

        Args:
            db_path: Path to the MS Access database file
        """
        self.db_path = db_path
        self.connection_string = (
            f"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};"
            f"DBQ={db_path};"
        )

    def connect(self) -> pyodbc.Connection:
        """
        Connect to the Access database.

        Returns:
            ODBC connection to the database

        Raises:
            DatabaseError: If connection fails
        """
        try:
            return pyodbc.connect(self.connection_string)
        except pyodbc.Error as e:
            raise DatabaseError(f"Failed to connect to Access DB: {str(e)}") from e

    def query(self, sql: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query on the Access database.

        Args:
            sql: SQL query to execute
            params: Optional parameters for the query

        Returns:
            List of dictionaries representing the query results

        Raises:
            DatabaseError: If query execution fails
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)

                # Get column names
                columns = [column[0] for column in cursor.description]

                # Fetch all rows and convert to dictionaries
                rows = []
                for row in cursor.fetchall():
                    rows.append(dict(zip(columns, row)))

                return rows
        except pyodbc.Error as e:
            raise DatabaseError(f"Error executing query: {str(e)}") from e


class FitmentDBService:
    """Service for database operations related to fitment data."""

    def __init__(
        self,
        vcdb_path: str,
        pcdb_path: str,
        sqlalchemy_url: Optional[str] = None
    ) -> None:
        """
        Initialize the fitment database service.

        Args:
            vcdb_path: Path to the VCDB MS Access database
            pcdb_path: Path to the PCDB MS Access database
            sqlalchemy_url: Optional SQLAlchemy URL for async database
        """
        self.vcdb_client = AccessDBClient(vcdb_path)
        self.pcdb_client = AccessDBClient(pcdb_path)

        # Set up SQLAlchemy async engine if URL provided
        if sqlalchemy_url:
            self.engine = create_async_engine(sqlalchemy_url, echo=False)
            self.async_session = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
        else:
            self.engine = None
            self.async_session = None

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get an async session for database operations.

        Yields:
            AsyncSession object

        Raises:
            DatabaseError: If async database is not configured
        """
        if not self.async_session:
            raise DatabaseError("Async database not configured")

        session = self.async_session()
        try:
            yield session
        finally:
            await session.close()

    def get_vcdb_vehicles(
        self,
        year: Optional[int] = None,
        make: Optional[str] = None,
        model: Optional[str] = None
    ) -> List[VCDBVehicle]:
        """
        Get vehicles from VCDB matching the specified criteria.

        Args:
            year: Optional year to filter by
            make: Optional make to filter by
            model: Optional model to filter by

        Returns:
            List of VCDBVehicle objects

        Raises:
            DatabaseError: If query fails
        """
        # Build the base query
        sql = """
        SELECT
            v.VehicleID as id,
            v.BaseVehicleID as base_vehicle_id,
            v.SubmodelID as submodel_id,
            v.RegionID as region_id,
            y.YearID as year,
            m.MakeName as make,
            md.ModelName as model,
            sm.SubModelName as submodel
        FROM
            Vehicle v
            JOIN BaseVehicle bv ON v.BaseVehicleID = bv.BaseVehicleID
            JOIN Year y ON bv.YearID = y.YearID
            JOIN Make m ON bv.MakeID = m.MakeID
            JOIN Model md ON bv.ModelID = md.ModelID
            LEFT JOIN SubModel sm ON v.SubmodelID = sm.SubModelID
        WHERE 1=1
        """

        # Add filters
        params = []
        if year:
            sql += " AND y.YearID = ?"
            params.append(year)
        if make:
            sql += " AND m.MakeName LIKE ?"
            params.append(f"%{make}%")
        if model:
            sql += " AND md.ModelName LIKE ?"
            params.append(f"%{model}%")

        # Execute the query
        try:
            rows = self.vcdb_client.query(sql, tuple(params) if params else None)

            # Convert to VCDBVehicle objects
            vehicles = []
            for row in rows:
                vehicles.append(VCDBVehicle(**row))

            return vehicles
        except Exception as e:
            logger.error(f"Error getting VCDB vehicles: {str(e)}")
            raise DatabaseError(f"Failed to get VCDB vehicles: {str(e)}") from e

    def get_pcdb_part_terminology(self, terminology_id: int) -> PartTerminology:
        """
        Get part terminology information from PCDB.

        Args:
            terminology_id: ID of the part terminology

        Returns:
            PartTerminology object

        Raises:
            DatabaseError: If query fails or part terminology not found
        """
        sql = """
        SELECT
            PartTerminologyID as id,
            PartTerminologyName as name,
            CategoryID as category_id,
            SubCategoryID as subcategory_id
        FROM
            PartTerminology
        WHERE
            PartTerminologyID = ?
        """

        try:
            rows = self.pcdb_client.query(sql, (terminology_id,))

            if not rows:
                raise DatabaseError(f"Part terminology with ID {terminology_id} not found")

            # Also get valid positions
            positions_sql = """
            SELECT
                PositionID as position_id
            FROM
                PCDBMapping
            WHERE
                PartTerminologyID = ?
            """

            position_rows = self.pcdb_client.query(positions_sql, (terminology_id,))
            valid_positions = [row["position_id"] for row in position_rows]

            # Create and return PartTerminology
            terminology = PartTerminology(
                **rows[0],
                valid_positions=valid_positions
            )

            return terminology
        except Exception as e:
            logger.error(f"Error getting PCDB part terminology: {str(e)}")
            raise DatabaseError(f"Failed to get PCDB part terminology: {str(e)}") from e

    def get_pcdb_positions(self, position_ids: Optional[List[int]] = None) -> List[PCDBPosition]:
        """
        Get position information from PCDB.

        Args:
            position_ids: Optional list of position IDs to filter by

        Returns:
            List of PCDBPosition objects

        Raises:
            DatabaseError: If query fails
        """
        # Build the base query
        sql = """
        SELECT
            p.PositionID as id,
            p.PositionName as name,
            pf.FrontRearValue as front_rear,
            pl.LeftRightValue as left_right,
            pu.UpperLowerValue as upper_lower,
            pi.InnerOuterValue as inner_outer
        FROM
            Position p
            LEFT JOIN PositionFrontRear pf ON p.FrontRearID = pf.FrontRearID
            LEFT JOIN PositionLeftRight pl ON p.LeftRightID = pl.LeftRightID
            LEFT JOIN PositionUpperLower pu ON p.UpperLowerID = pu.UpperLowerID
            LEFT JOIN PositionInnerOuter pi ON p.InnerOuterID = pi.InnerOuterID
        """

        # Add filter for specific position IDs if provided
        params = None
        if position_ids:
            # Build IN clause with proper number of placeholders
            placeholders = ", ".join(["?"] * len(position_ids))
            sql += f" WHERE p.PositionID IN ({placeholders})"
            params = tuple(position_ids)

        # Execute the query
        try:
            rows = self.pcdb_client.query(sql, params)

            # Convert to PCDBPosition objects
            positions = []
            for row in rows:
                positions.append(PCDBPosition(**row))

            return positions
        except Exception as e:
            logger.error(f"Error getting PCDB positions: {str(e)}")
            raise DatabaseError(f"Failed to get PCDB positions: {str(e)}") from e

    def load_model_mappings_from_json(self, json_path: str) -> Dict[str, List[str]]:
        """
        Load model mappings from a JSON file.

        Args:
            json_path: Path to the JSON file

        Returns:
            Dictionary of model mappings

        Raises:
            DatabaseError: If loading fails
        """
        try:
            # Read the JSON file
            with open(json_path, 'r') as f:
                mappings = json.load(f)

            return mappings
        except Exception as e:
            logger.error(f"Error loading model mappings from JSON: {str(e)}")
            raise DatabaseError(f"Failed to load model mappings: {str(e)}") from e

    async def get_model_mappings(self) -> Dict[str, List[str]]:
        """
        Get model mappings from the database.

        Returns:
            Dictionary of model mappings where keys are patterns and values are lists of mapping strings

        Raises:
            DatabaseError: If query fails
        """
        if not self.engine:
            raise DatabaseError("Async database not configured")

        async with self.get_session() as session:
            try:
                from app.models.model_mapping import ModelMapping

                # Get all active mappings ordered by priority
                query = select(ModelMapping).where(
                    ModelMapping.active == True
                ).order_by(
                    ModelMapping.priority.desc(),
                    ModelMapping.pattern
                )

                result = await session.execute(query)
                mappings_db = result.scalars().all()

                # Group mappings by pattern
                mappings: Dict[str, List[str]] = {}
                for mapping in mappings_db:
                    if mapping.pattern not in mappings:
                        mappings[mapping.pattern] = []

                    mappings[mapping.pattern].append(mapping.mapping)

                return mappings
            except Exception as e:
                logger.error(f"Error getting model mappings: {str(e)}")
                raise DatabaseError(f"Failed to get model mappings: {str(e)}") from e

    async def add_model_mapping(self, pattern: str, mapping: str, priority: int = 0) -> int:
        """
        Add a new model mapping to the database.

        Args:
            pattern: Pattern to match in vehicle text
            mapping: Mapping string in format "Make|VehicleCode|Model"
            priority: Optional priority for matching (higher values are processed first)

        Returns:
            ID of the new mapping

        Raises:
            DatabaseError: If insert fails
        """
        if not self.engine:
            raise DatabaseError("Async database not configured")

        async with self.get_session() as session:
            try:
                from app.models.model_mapping import ModelMapping

                # Create new mapping
                mapping_obj = ModelMapping(
                    pattern=pattern,
                    mapping=mapping,
                    priority=priority
                )

                session.add(mapping_obj)
                await session.commit()
                await session.refresh(mapping_obj)

                return mapping_obj.id
            except Exception as e:
                await session.rollback()
                logger.error(f"Error adding model mapping: {str(e)}")
                raise DatabaseError(f"Failed to add model mapping: {str(e)}") from e

    async def update_model_mapping(self, mapping_id: int, **kwargs) -> bool:
        """
        Update an existing model mapping.

        Args:
            mapping_id: ID of the mapping to update
            **kwargs: Fields to update (pattern, mapping, priority, active)

        Returns:
            True if successful

        Raises:
            DatabaseError: If update fails
        """
        if not self.engine:
            raise DatabaseError("Async database not configured")

        # Validate fields to update
        valid_fields = {"pattern", "mapping", "priority", "active"}
        update_fields = {k: v for k, v in kwargs.items() if k in valid_fields}

        if not update_fields:
            return True  # Nothing to update

        async with self.get_session() as session:
            try:
                from app.models.model_mapping import ModelMapping

                # Get mapping
                mapping_obj = await session.get(ModelMapping, mapping_id)
                if not mapping_obj:
                    return False

                # Update fields
                for field, value in update_fields.items():
                    setattr(mapping_obj, field, value)

                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"Error updating model mapping: {str(e)}")
                raise DatabaseError(f"Failed to update model mapping: {str(e)}") from e

    async def delete_model_mapping(self, mapping_id: int) -> bool:
        """
        Delete a model mapping.

        Args:
            mapping_id: ID of the mapping to delete

        Returns:
            True if successful

        Raises:
            DatabaseError: If delete fails
        """
        if not self.engine:
            raise DatabaseError("Async database not configured")

        async with self.get_session() as session:
            try:
                from app.models.model_mapping import ModelMapping

                # Get mapping
                mapping_obj = await session.get(ModelMapping, mapping_id)
                if not mapping_obj:
                    return False

                # Delete mapping
                await session.delete(mapping_obj)
                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"Error deleting model mapping: {str(e)}")
                raise DatabaseError(f"Failed to delete model mapping: {str(e)}") from e

    async def import_mappings_from_json(self, json_data: Dict[str, List[str]]) -> int:
        """
        Import mappings from a JSON dictionary.

        Args:
            json_data: Dictionary where keys are patterns and values are lists of mappings

        Returns:
            Number of mappings imported

        Raises:
            DatabaseError: If import fails
        """
        if not self.engine:
            raise DatabaseError("Async database not configured")

        count = 0

        async with self.get_session() as session:
            try:
                from app.models.model_mapping import ModelMapping
                from sqlalchemy.exc import IntegrityError

                # Process each pattern and its mappings
                for pattern, mappings in json_data.items():
                    for mapping in mappings:
                        try:
                            # Check if mapping already exists
                            query = select(ModelMapping).where(
                                ModelMapping.pattern == pattern,
                                ModelMapping.mapping == mapping
                            )
                            result = await session.execute(query)
                            existing = result.scalar_one_or_none()

                            if not existing:
                                # Create new mapping
                                mapping_obj = ModelMapping(
                                    pattern=pattern,
                                    mapping=mapping
                                )

                                session.add(mapping_obj)
                                count += 1
                        except Exception as e:
                            logger.warning(f"Error importing mapping {pattern}:{mapping}: {str(e)}")

                await session.commit()
                return count
            except Exception as e:
                await session.rollback()
                logger.error(f"Error importing mappings: {str(e)}")
                raise DatabaseError(f"Failed to import mappings: {str(e)}") from e

    async def save_fitment_results(
        self,
        product_id: str,
        fitments: List[Dict[str, Any]]
    ) -> bool:
        """
        Save fitment results to the database.

        Args:
            product_id: ID of the product
            fitments: List of fitment dictionaries

        Returns:
            True if successful

        Raises:
            DatabaseError: If saving fails
        """
        if not self.engine:
            raise DatabaseError("Async database not configured")

        async with self.get_session() as session:
            try:
                # First delete any existing fitments for this product
                await session.execute(
                    text("DELETE FROM product_fitments WHERE product_id = :product_id"),
                    {"product_id": product_id}
                )

                # Then insert the new fitments
                for fitment in fitments:
                    await session.execute(
                        text("""
                        INSERT INTO product_fitments (
                            product_id, vcdb_vehicle_id, pcdb_position_ids,
                            year, make, model, submodel, notes
                        ) VALUES (
                            :product_id, :vcdb_vehicle_id, :pcdb_position_ids,
                            :year, :make, :model, :submodel, :notes
                        )
                        """),
                        {
                            "product_id": product_id,
                            "vcdb_vehicle_id": fitment.get("vcdb_vehicle_id"),
                            "pcdb_position_ids": ",".join(map(str, fitment.get("pcdb_position_ids", []))),
                            "year": fitment.get("year"),
                            "make": fitment.get("make"),
                            "model": fitment.get("model"),
                            "submodel": fitment.get("submodel"),
                            "notes": fitment.get("notes")
                        }
                    )

                await session.commit()
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"Error saving fitment results: {str(e)}")
                raise DatabaseError(f"Failed to save fitment results: {str(e)}") from e
