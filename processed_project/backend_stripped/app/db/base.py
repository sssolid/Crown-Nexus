from __future__ import annotations
from app.db.base_class import Base
from app.domains.location.models import Country, Address
from app.domains.api_key.models import ApiKey
from app.domains.users.models import User, UserRole
from app.domains.company.models import Company
from app.domains.reference.models import Color, ConstructionType, Hardware, PackagingType, Texture, TariffCode, UnspscCode, Warehouse
from app.domains.currency.models import Currency, ExchangeRate
from app.domains.media.models import Media, MediaType, MediaVisibility
from app.domains.products.models import Product, Brand, Fitment, Manufacturer, PriceType, AttributeDefinition, ProductActivity, ProductAttribute, ProductBrandHistory, ProductDescription, ProductMarketing, ProductMeasurement, ProductPricing, ProductStock, ProductSupersession
from app.domains.audit.models import AuditLog
from app.domains.compliance.models import Prop65Chemical, ProductChemical, ChemicalType, ProductDOTApproval, ApprovalStatus, ExposureScenario, HazardousMaterial, TransportRestriction, Warning
from app.domains.model_mapping.models import ModelMapping
from app.domains.chat.models import ChatRoom, ChatMember, ChatRoomType, ChatMemberRole, ChatMessage, MessageReaction, MessageType, RateLimitLog
from app.models.associations import product_color_association, product_construction_type_association, product_country_origin_association, product_fitment_association, product_hardware_association, product_interchange_association, product_media_association, product_packaging_association, product_tariff_code_association, product_texture_association, product_unspsc_association