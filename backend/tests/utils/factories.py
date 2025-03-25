# /backend/tests/utils/factories.py
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.media.models import Media, MediaType, MediaVisibility
from app.domains.products.models import (
    Brand,
    Fitment,
    Product,
    ProductStatus,
)
from app.domains.users.models import Company, User, UserRole, get_password_hash
from tests.utils import create_random_email, create_random_string


class BaseFactory:
    """Base factory for test models.

    Provides utility methods for all factory classes.
    """

    @classmethod
    async def create_batch(
        cls, db_session: AsyncSession, count: int = 3, **kwargs: Any
    ) -> List[Any]:
        """Create multiple instances of a model.

        Args:
            db_session: Database session
            count: Number of instances to create
            **kwargs: Attributes to set on each instance

        Returns:
            List[Any]: List of created model instances
        """
        return [await cls.create(db_session, **kwargs) for _ in range(count)]


class UserFactory(BaseFactory):
    """Factory for User models."""

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> User:
        """Create a user instance.

        Args:
            db_session: Database session
            **kwargs: User attributes

        Returns:
            User: Created user
        """
        defaults = {
            "id": uuid.uuid4(),
            "email": create_random_email(),
            "full_name": f"{create_random_string(6)} {create_random_string(8)}",
            "hashed_password": get_password_hash("password"),
            "role": UserRole.CLIENT,
            "is_active": True,
        }

        # Override defaults with provided values
        defaults.update(kwargs)

        user = User(**defaults)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        return user


class CompanyFactory(BaseFactory):
    """Factory for Company models."""

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Company:
        """Create a company instance.

        Args:
            db_session: Database session
            **kwargs: Company attributes

        Returns:
            Company: Created company
        """
        defaults = {
            "id": uuid.uuid4(),
            "name": f"Company {create_random_string(8)}",
            "account_number": f"ACC{create_random_string(6, digits_only=True)}",
            "account_type": "client",
            "is_active": True,
        }

        # Override defaults with provided values
        defaults.update(kwargs)

        company = Company(**defaults)
        db_session.add(company)
        await db_session.commit()
        await db_session.refresh(company)
        return company


class BrandFactory(BaseFactory):
    """Factory for Brand models."""

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Brand:
        """Create a brand instance.

        Args:
            db_session: Database session
            **kwargs: Brand attributes

        Returns:
            Brand: Created brand
        """
        defaults = {
            "id": uuid.uuid4(),
            "name": f"Brand {create_random_string(8)}",
        }

        # Override defaults with provided values
        defaults.update(kwargs)

        brand = Brand(**defaults)
        db_session.add(brand)
        await db_session.commit()
        await db_session.refresh(brand)
        return brand


class ProductFactory(BaseFactory):
    """Factory for Product models."""

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Product:
        """Create a product instance.

        Args:
            db_session: Database session
            **kwargs: Product attributes

        Returns:
            Product: Created product
        """
        part_number = f"P{create_random_string(5, digits_only=True)}"

        defaults = {
            "id": uuid.uuid4(),
            "part_number": part_number,
            "part_number_stripped": part_number,
            "application": f"Application for {part_number}",
            "vintage": False,
            "late_model": True,
            "soft": False,
            "universal": False,
            "is_active": True,
        }

        # Override defaults with provided values
        defaults.update(kwargs)

        product = Product(**defaults)
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product


class FitmentFactory(BaseFactory):
    """Factory for Fitment models."""

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Fitment:
        """Create a fitment instance.

        Args:
            db_session: Database session
            **kwargs: Fitment attributes

        Returns:
            Fitment: Created fitment
        """
        current_year = datetime.now().year

        defaults = {
            "id": uuid.uuid4(),
            "year": random.randint(current_year - 10, current_year),
            "make": f"Make {create_random_string(6)}",
            "model": f"Model {create_random_string(6)}",
            "engine": random.choice(["V6", "V8", "I4", "I6", "H4"]),
            "transmission": random.choice(["Manual", "Automatic", "CVT", "DCT"]),
        }

        # Override defaults with provided values
        defaults.update(kwargs)

        fitment = Fitment(**defaults)
        db_session.add(fitment)
        await db_session.commit()
        await db_session.refresh(fitment)
        return fitment


class MediaFactory(BaseFactory):
    """Factory for Media models."""

    @staticmethod
    async def create(db_session: AsyncSession, **kwargs: Any) -> Media:
        """Create a media instance.

        Args:
            db_session: Database session
            **kwargs: Media attributes

        Returns:
            Media: Created media
        """
        defaults = {
            "id": uuid.uuid4(),
            "filename": f"file-{create_random_string(8)}.jpg",
            "file_path": f"/media/test/file-{create_random_string(8)}.jpg",
            "file_size": random.randint(10000, 1000000),
            "media_type": MediaType.IMAGE,
            "mime_type": "image/jpeg",
            "visibility": MediaVisibility.PUBLIC,
            "uploaded_by_id": None,
            "is_approved": True,
        }

        # Override defaults with provided values
        defaults.update(kwargs)

        media = Media(**defaults)
        db_session.add(media)
        await db_session.commit()
        await db_session.refresh(media)
        return media
