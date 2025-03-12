from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship
from sqlalchemy.sql import expression
from app.db.base_class import Base
from app.models.associations import product_fitment_association, product_media_association
if TYPE_CHECKING:
    from app.models.media import Media
class Product(Base):
    __tablename__ = 'product'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    part_number: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=True)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=expression.true(), nullable=False)
    fitments: Mapped[List['Fitment']] = relationship('Fitment', secondary=product_fitment_association, back_populates='products')
    category: Mapped[Optional['Category']] = relationship('Category')
    media: Mapped[List['Media']] = relationship('app.models.media.Media', secondary=product_media_association, back_populates='products')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<Product {self.sku}: {self.name}>'
class Fitment(Base):
    __tablename__ = 'fitment'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    make: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    engine: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    transmission: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb"))
    products: Mapped[List[Product]] = relationship('Product', secondary=product_fitment_association, back_populates='fitments')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<Fitment {self.year} {self.make} {self.model}>'
class Category(Base):
    __tablename__ = 'category'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    children: Mapped[List['Category']] = relationship('Category', backref=backref('parent', remote_side=[id]), cascade='all, delete-orphan')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    def __repr__(self) -> str:
        return f'<Category {self.name}>'
    def get_ancestors(self) -> List[Category]:
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors
    def get_full_path(self) -> str:
        ancestors = self.get_ancestors()
        path = '/'.join(reversed([ancestor.name for ancestor in ancestors]))
        if path:
            return f'{path}/{self.name}'
        return self.name