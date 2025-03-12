from __future__ import annotations
from app.db.base_class import Base
from app.models.user import Company, User
from app.models.associations import product_fitment_association, product_media_association
from app.models.product import Category, Fitment, Product
from app.models.media import Media, MediaType, MediaVisibility