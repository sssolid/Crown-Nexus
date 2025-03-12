from __future__ import annotations
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
product_fitment_association = Table('product_fitment', Base.metadata, Column('product_id', UUID(as_uuid=True), ForeignKey('product.id', ondelete='CASCADE'), primary_key=True), Column('fitment_id', UUID(as_uuid=True), ForeignKey('fitment.id', ondelete='CASCADE'), primary_key=True))
product_media_association = Table('product_media', Base.metadata, Column('product_id', UUID(as_uuid=True), ForeignKey('product.id', ondelete='CASCADE'), primary_key=True), Column('media_id', UUID(as_uuid=True), ForeignKey('media.id', ondelete='CASCADE'), primary_key=True))