from __future__ import annotations

# Import Base class
from app.db.base_class import Base

# Import all models here for Alembic to detect them
from app.models.associations import product_fitment_association, product_media_association  # noqa
from app.models.product import Category, Fitment, Product  # noqa
from app.models.user import Company, User  # noqa
from app.models.media import Media, MediaType, MediaVisibility  # noqa
