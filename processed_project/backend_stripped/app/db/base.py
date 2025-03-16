from __future__ import annotations
from app.db.base_class import Base
from app.models.user import Company, User, UserRole
from app.models.associations import product_fitment_association, product_media_association, product_tariff_code_association, product_unspsc_association, product_country_origin_association, product_hardware_association, product_interchange_association, product_packaging_association, product_color_association, product_construction_type_association, product_texture_association
from app.models.location import Address, Country
from app.models.reference import Color, ConstructionType, Hardware, PackagingType, TariffCode, Texture, UnspscCode, Warehouse
from app.models.product import AttributeDefinition, Brand, Fitment, Manufacturer, PriceType, Product, ProductActivity, ProductAttribute, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductPricing, ProductStock, ProductSupersession
from app.models.media import Media, MediaType, MediaVisibility
from app.models.compliance import Prop65Chemical, ProductChemical