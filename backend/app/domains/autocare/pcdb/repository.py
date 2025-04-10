from __future__ import annotations

"""PCdb repository implementation.

This module provides data access and persistence operations for PCdb entities.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.domains.autocare.pcdb.models import (
    Parts,
    Category,
    SubCategory,
    Position,
    PartCategory,
    PartPosition,
    PartsSupersession,
    PCdbVersion,
    PartsDescription,
)


class PCdbRepository:
    """Repository for PCdb entity operations.

    Provides methods for querying PCdb data and managing database updates.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the PCdb repository.

        Args:
            db: The database session.
        """
        self.db = db
        self.parts_repo = PartsRepository(db)
        self.category_repo = CategoryRepository(db)
        self.subcategory_repo = SubCategoryRepository(db)
        self.position_repo = PositionRepository(db)

    async def get_version(self) -> Optional[str]:
        """Get the current version of the PCdb database.

        Returns:
            The version date as a string or None if no version is set.
        """
        query = select(PCdbVersion).where(PCdbVersion.is_current == True)
        result = await self.db.execute(query)
        version = result.scalars().first()

        if version:
            return version.version_date.strftime("%Y-%m-%d")
        return None

    async def update_version(self, version_date: datetime) -> PCdbVersion:
        """Update the current version of the PCdb database.

        Args:
            version_date: The new version date.

        Returns:
            The updated version entity.
        """
        # Set all existing versions to not current
        await self.db.execute(
            select(PCdbVersion)
            .where(PCdbVersion.is_current == True)
            .update({PCdbVersion.is_current: False})
        )

        # Create new current version
        version = PCdbVersion(version_date=version_date, is_current=True)
        self.db.add(version)
        await self.db.flush()

        return version

    async def search_parts(
        self,
        search_term: str,
        categories: Optional[List[int]] = None,
        subcategories: Optional[List[int]] = None,
        positions: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for parts by term and optional category filters.

        Args:
            search_term: The search term.
            categories: Optional list of category IDs to filter by.
            subcategories: Optional list of subcategory IDs to filter by.
            positions: Optional list of position IDs to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        return await self.parts_repo.search(
            search_term, categories, subcategories, positions, page, page_size
        )


class PartsRepository(BaseRepository[Parts, uuid.UUID]):
    """Repository for Parts entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the parts repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Parts, db=db)

    async def get_by_terminology_id(self, part_terminology_id: int) -> Optional[Parts]:
        """Get a part by its terminology ID.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            The part if found, None otherwise.
        """
        query = select(Parts).where(Parts.part_terminology_id == part_terminology_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_terminology_id_with_related(
        self, part_terminology_id: int
    ) -> Optional[Parts]:
        """Get a part by its terminology ID with related entities eagerly loaded.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            The part with related entities if found, None otherwise.
        """
        from sqlalchemy.orm import selectinload

        query = (
            select(Parts)
            .options(
                selectinload(Parts.description),
                selectinload(Parts.categories).selectinload(PartCategory.category),
                selectinload(Parts.categories).selectinload(PartCategory.subcategory),
                selectinload(Parts.positions).selectinload(PartPosition.position),
            )
            .where(Parts.part_terminology_id == part_terminology_id)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def search(
        self,
        search_term: Optional[str],
        categories: Optional[List[int]] = None,
        subcategories: Optional[List[int]] = None,
        positions: Optional[List[int]] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for parts by term and optional category filters using PostgreSQL full-text search.

        Args:
            search_term: The search term.
            categories: Optional list of category IDs to filter by.
            subcategories: Optional list of subcategory IDs to filter by.
            positions: Optional list of position IDs to filter by.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        from sqlalchemy.orm import selectinload, joinedload
        from sqlalchemy import text, func, or_, desc, cast, Float

        # Start with base query - eagerly load the description relationship
        query = select(Parts).options(selectinload(Parts.description))

        # We'll need to join with PartsDescription to search in descriptions
        description_joined = False

        # Track if we need to add a custom ranking
        apply_ranking = False

        # List of conditions to apply
        conditions = []

        # Process search term if provided
        if search_term and search_term.strip():
            search_term = search_term.strip()

            # Create a combined approach using multiple search techniques
            search_conditions = []

            # 1. Full-text search using PostgreSQL's ts_vector
            # Prepare search configuration and tokens
            config = "english"  # Can be changed based on language needs

            # Process tokens - remove special characters and prepare for tsquery
            tokens = search_term.split()
            clean_tokens = []
            for token in tokens:
                # Clean token and keep only if it's substantial
                clean_token = "".join(c for c in token if c.isalnum())
                if len(clean_token) >= 3:
                    clean_tokens.append(clean_token)

            if clean_tokens:
                # Create tsquery expression with & (AND) between tokens
                tsquery_expression = " & ".join(clean_tokens)
                tsquery = func.to_tsquery(config, tsquery_expression)

                # Add full-text search condition for part name
                tsvector_name = func.to_tsvector(config, Parts.part_terminology_name)
                search_conditions.append(tsvector_name.op("@@")(tsquery))

                # Join with PartsDescription to search descriptions
                if not description_joined:
                    query = query.outerjoin(
                        PartsDescription,
                        Parts.parts_description_id
                        == PartsDescription.parts_description_id,
                    )
                    description_joined = True

                # Add full-text search condition for description
                tsvector_desc = func.to_tsvector(
                    config, PartsDescription.parts_description
                )
                search_conditions.append(tsvector_desc.op("@@")(tsquery))

                # Save the expression for ranking
                apply_ranking = True

            # 2. Traditional ILIKE search for direct matching
            # For part name
            search_conditions.append(
                Parts.part_terminology_name.ilike(f"%{search_term}%")
            )

            # For description - make sure we've joined with PartsDescription
            if not description_joined:
                query = query.outerjoin(
                    PartsDescription,
                    Parts.parts_description_id == PartsDescription.parts_description_id,
                )
                description_joined = True
            search_conditions.append(
                PartsDescription.parts_description.ilike(f"%{search_term}%")
            )

            # 3. Optional: trigram similarity for fuzzy matching if pg_trgm extension is available
            try:
                # This requires the pg_trgm extension to be installed
                similarity_threshold = 0.3  # Adjust as needed (0.0 to 1.0)

                # Similarity for part name
                search_conditions.append(
                    func.similarity(Parts.part_terminology_name, search_term)
                    > similarity_threshold
                )

                # Similarity for description
                if not description_joined:
                    query = query.outerjoin(
                        PartsDescription,
                        Parts.parts_description_id
                        == PartsDescription.parts_description_id,
                    )
                    description_joined = True
                search_conditions.append(
                    func.similarity(PartsDescription.parts_description, search_term)
                    > similarity_threshold
                )
            except Exception:
                # If pg_trgm is not available, skip this condition
                pass

            # Combine all search conditions with OR
            if search_conditions:
                conditions.append(or_(*search_conditions))

        # Apply category filter if categories are provided and valid
        if categories and all(category is not None for category in categories):
            query = query.join(
                PartCategory,
                Parts.part_terminology_id == PartCategory.part_terminology_id,
            )
            conditions.append(PartCategory.category_id.in_(categories))

        # Apply subcategory filter if provided and valid
        if subcategories and all(
            subcategory is not None for subcategory in subcategories
        ):
            # Check if PartCategory is already joined
            if not any(
                "PartCategory" in str(join)
                for join in query._setup_joins
                if hasattr(query, "_setup_joins")
            ):
                query = query.join(
                    PartCategory,
                    Parts.part_terminology_id == PartCategory.part_terminology_id,
                )
            conditions.append(PartCategory.subcategory_id.in_(subcategories))

        # Apply position filter if provided and valid
        if positions and all(position is not None for position in positions):
            query = query.join(
                PartPosition,
                Parts.part_terminology_id == PartPosition.part_terminology_id,
            )
            conditions.append(PartPosition.position_id.in_(positions))

        # Apply all conditions if any exist
        if conditions:
            query = query.where(and_(*conditions))

        # Apply ranking if we're doing a text search
        if apply_ranking and search_term and search_term.strip():
            # Make sure we've joined with description for ranking
            if not description_joined:
                query = query.outerjoin(
                    PartsDescription,
                    Parts.parts_description_id == PartsDescription.parts_description_id,
                )

            # Create a combined ranking based on multiple factors
            # Rank by name (higher weight) and description (lower weight)
            ts_rank_name = func.ts_rank(
                func.to_tsvector("english", Parts.part_terminology_name),
                func.to_tsquery("english", " & ".join(clean_tokens)),
            )

            ts_rank_desc = func.ts_rank(
                func.to_tsvector("english", PartsDescription.parts_description),
                func.to_tsquery("english", " & ".join(clean_tokens)),
            )

            # Combine the ranks - give more weight (2x) to matches in name vs description
            # Also consider similarity and use name as final tiebreaker
            query = query.order_by(
                desc(
                    ts_rank_name * 2.0 + func.coalesce(ts_rank_desc, 0)
                ),  # Combined text rank
                desc(
                    func.similarity(Parts.part_terminology_name, search_term)
                ),  # Name similarity
                Parts.part_terminology_name,  # Alphabetical for consistent results
            )
        else:
            # Default ordering if no search term
            query = query.order_by(Parts.part_terminology_name)

        # Execute and return the result
        result = await self.paginate(query, page, page_size)
        return result

    async def get_by_category(
        self, category_id: int, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get parts by category.

        Args:
            category_id: The category ID.
            page: The page number.
            page_size: The number of items per page.

        Returns:
            Dict containing items, total count, and pagination info.
        """
        query = (
            select(Parts)
            .join(
                PartCategory,
                Parts.part_terminology_id == PartCategory.part_terminology_id,
            )
            .where(PartCategory.category_id == category_id)
            .order_by(Parts.part_terminology_name)
        )

        return await self.paginate(query, page, page_size)

    async def get_supersessions(
        self, part_terminology_id: int
    ) -> Dict[str, List[Parts]]:
        """Get supersession information for a part with all needed data.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            Dict with superseded_by and supersedes lists.
        """
        # Use a single query to get all parts that supersede this part
        superseded_by_query = select(Parts).join(
            PartsSupersession,
            and_(
                Parts.part_terminology_id == PartsSupersession.new_part_terminology_id,
                PartsSupersession.old_part_terminology_id == part_terminology_id,
            ),
        )

        # Use a single query to get all parts that this part supersedes
        supersedes_query = select(Parts).join(
            PartsSupersession,
            and_(
                Parts.part_terminology_id == PartsSupersession.old_part_terminology_id,
                PartsSupersession.new_part_terminology_id == part_terminology_id,
            ),
        )

        # Execute both queries
        superseded_by_result = await self.db.execute(superseded_by_query)
        supersedes_result = await self.db.execute(supersedes_query)

        # Get the results as lists
        superseded_by_parts = list(superseded_by_result.scalars().all())
        supersedes_parts = list(supersedes_result.scalars().all())

        return {
            "superseded_by": superseded_by_parts,
            "supersedes": supersedes_parts,
        }


class CategoryRepository(BaseRepository[Category, uuid.UUID]):
    """Repository for Category entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the category repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Category, db=db)

    async def get_by_category_id(self, category_id: int) -> Optional[Category]:
        """Get a category by its ID.

        Args:
            category_id: The category ID.

        Returns:
            The category if found, None otherwise.
        """
        query = select(Category).where(Category.category_id == category_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all_categories(self) -> List[Category]:
        """Get all categories.

        Returns:
            List of all categories.
        """
        query = select(Category).order_by(Category.category_name)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def search(self, search_term: str) -> List[Category]:
        """Search for categories by name.

        Args:
            search_term: The search term.

        Returns:
            List of matching categories.
        """
        query = (
            select(Category)
            .where(Category.category_name.ilike(f"%{search_term}%"))
            .order_by(Category.category_name)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


class SubCategoryRepository(BaseRepository[SubCategory, uuid.UUID]):
    """Repository for SubCategory entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the subcategory repository.

        Args:
            db: The database session.
        """
        super().__init__(model=SubCategory, db=db)

    async def get_by_subcategory_id(self, subcategory_id: int) -> Optional[SubCategory]:
        """Get a subcategory by its ID.

        Args:
            subcategory_id: The subcategory ID.

        Returns:
            The subcategory if found, None otherwise.
        """
        query = select(SubCategory).where(SubCategory.subcategory_id == subcategory_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_by_category(self, category_id: int) -> List[SubCategory]:
        """Get subcategories by category.

        Args:
            category_id: The category ID.

        Returns:
            List of subcategories in the specified category.
        """
        query = (
            select(SubCategory)
            .join(
                PartCategory, SubCategory.subcategory_id == PartCategory.subcategory_id
            )
            .where(PartCategory.category_id == category_id)
            .distinct()
            .order_by(SubCategory.subcategory_name)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())


class PositionRepository(BaseRepository[Position, uuid.UUID]):
    """Repository for Position entity operations."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the position repository.

        Args:
            db: The database session.
        """
        super().__init__(model=Position, db=db)

    async def get_by_position_id(self, position_id: int) -> Optional[Position]:
        """Get a position by its ID.

        Args:
            position_id: The position ID.

        Returns:
            The position if found, None otherwise.
        """
        query = select(Position).where(Position.position_id == position_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all_positions(self) -> List[Position]:
        """Get all positions.

        Returns:
            List of all positions.
        """
        query = select(Position).order_by(Position.position)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_part(self, part_terminology_id: int) -> List[Position]:
        """Get positions for a specific part.

        Args:
            part_terminology_id: The part terminology ID.

        Returns:
            List of positions for the specified part.
        """
        query = (
            select(Position)
            .join(PartPosition, Position.position_id == PartPosition.position_id)
            .where(PartPosition.part_terminology_id == part_terminology_id)
            .order_by(Position.position)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
