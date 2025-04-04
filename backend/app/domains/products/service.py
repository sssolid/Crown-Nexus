from __future__ import annotations

"""
Product domain service.

This module provides business logic for product operations,
integrating with the application's core services for auditing,
error handling, validation, and events.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit import get_audit_service
from app.core.audit.base import AuditEventType, AuditLogLevel, AuditContext
from app.core.dependency_manager import get_dependency
from app.core.events import EventService
from app.core.exceptions import BusinessException, ResourceNotFoundException
from app.domains.products.exceptions import (
    ProductNotFoundException,
    DuplicatePartNumberException,
    ProductInactiveException,
    BrandNotFoundException
)
from app.domains.products.models import (
    Product,
    ProductActivity,
    ProductDescription,
    ProductMarketing,
    ProductPricing,
    ProductStock,
    ProductSupersession,
    Brand
)
from app.domains.products.repository import ProductRepository, BrandRepository
from app.domains.products.schemas import (
    ProductCreate,
    ProductUpdate,
    ProductDescriptionCreate,
    ProductMarketingCreate,
    ProductPricingCreate
)
from app.domains.sync_history.models import SyncEntityType, SyncSource, SyncStatus
from app.domains.sync_history.repository import SyncHistoryRepository
from app.logging import get_logger

logger = get_logger("app.domains.products.service")


class ProductService:
    """Service for product domain operations with integrated auditing and event handling."""

    def __init__(self, db: AsyncSession):
        """
        Initialize the product service.

        Args:
            db: Database session
        """
        self.db = db
        self.repository = ProductRepository(db)
        self.brand_repository = BrandRepository(db)
        self.event_service = cast(EventService, get_dependency("event_service"))
        self.sync_repository = SyncHistoryRepository(db)
        self.error_service = get_dependency("error_service")
        self.cache_service = get_dependency("cache_service")
        self.validation_service = get_dependency("validation_service")

    async def get_product(self, product_id: uuid.UUID) -> Product:
        """
        Get a product by ID.

        Args:
            product_id: The product ID

        Returns:
            The product

        Raises:
            ProductNotFoundException: If the product doesn't exist
        """
        # Try to get from cache first
        cache_key = f"product:{product_id}"
        cached_product = await self.cache_service.get(cache_key)
        if cached_product:
            return cached_product

        # Query database if not in cache
        query = select(Product).where(Product.id == product_id, Product.is_deleted == False)
        result = await self.db.execute(query)
        product = result.scalars().first()

        # Validate product exists
        if not product:
            await self._log_audit_event(
                event_type=AuditEventType.ACCESS_DENIED,
                resource_id=str(product_id),
                resource_type="Product",
                details={"error": "Product not found"}
            )
            raise ProductNotFoundException(product_id=str(product_id))

        # Cache for future requests
        await self.cache_service.set(cache_key, product)

        # Log the view access
        await self._log_audit_event(
            event_type=AuditEventType.VIEW,
            resource_id=str(product_id),
            resource_type="Product"
        )

        return product

    async def create_product(
        self,
        data: ProductCreate,
        user_id: Optional[uuid.UUID] = None,
        import_id: Optional[uuid.UUID] = None
    ) -> Product:
        """
        Create a new product.

        Args:
            data: Product creation data
            user_id: ID of the user performing the action
            import_id: ID of the import operation if part of an import

        Returns:
            The created product

        Raises:
            DuplicatePartNumberException: If a product with the same part number already exists
        """
        # Validate the data
        if hasattr(self.validation_service, "validate_product_create"):
            await self.validation_service.validate_product_create(data)

        # Check for duplicate part number
        existing_product = await self.repository.find_by_part_number(data.part_number)
        if existing_product:
            raise DuplicatePartNumberException(part_number=data.part_number)

        # Create product
        product = Product(
            part_number=data.part_number,
            part_number_stripped=data.part_number_stripped or self._normalize_part_number(data.part_number),
            application=data.application,
            vintage=data.vintage,
            late_model=data.late_model,
            soft=data.soft,
            universal=data.universal,
            is_active=data.is_active
        )

        # Add to database
        self.db.add(product)
        await self.db.flush()  # To get the generated ID

        # Process descriptions if provided
        if hasattr(data, "descriptions") and data.descriptions:
            await self._create_descriptions(product.id, data.descriptions)

        # Process marketing if provided
        if hasattr(data, "marketing") and data.marketing:
            await self._create_marketing(product.id, data.marketing)

        # Create activity record
        activity = ProductActivity(
            product_id=product.id,
            status="active" if data.is_active else "inactive",
            changed_by_id=user_id,
            changed_at=datetime.now()
        )
        self.db.add(activity)

        # Flush to get all IDs
        await self.db.flush()
        await self.db.refresh(product)

        # Log audit event
        await self._log_audit_event(
            event_type=AuditEventType.PRODUCT_CREATED,
            user_id=str(user_id) if user_id else None,
            resource_id=str(product.id),
            resource_type="Product",
            details={
                "part_number": data.part_number,
                "import_id": str(import_id) if import_id else None
            }
        )

        # Emit event for notifications
        await self.event_service.emit(
            "product.created",
            {
                "product_id": str(product.id),
                "part_number": data.part_number,
                "user_id": str(user_id) if user_id else None,
                "import_id": str(import_id) if import_id else None
            }
        )

        # Update cache
        cache_key = f"product:{product.id}"
        await self.cache_service.set(cache_key, product)

        # Clear any list caches that might contain products
        await self.cache_service.delete_pattern("products:list:*")

        return product

    async def update_product(
        self,
        product_id: uuid.UUID,
        data: ProductUpdate,
        user_id: Optional[uuid.UUID] = None,
        import_id: Optional[uuid.UUID] = None
    ) -> Product:
        """
        Update an existing product.

        Args:
            product_id: ID of the product to update
            data: Product update data
            user_id: ID of the user performing the action
            import_id: ID of the import operation if part of an import

        Returns:
            The updated product

        Raises:
            ProductNotFoundException: If the product doesn't exist
            DuplicatePartNumberException: If updating to a part number that already exists
        """
        # Get the existing product
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=str(product_id))

        # Validate the data
        if hasattr(self.validation_service, "validate_product_update"):
            await self.validation_service.validate_product_update(data, product)

        # Store original state for audit
        before_state = {
            "part_number": product.part_number,
            "application": product.application,
            "vintage": product.vintage,
            "late_model": product.late_model,
            "soft": product.soft,
            "universal": product.universal,
            "is_active": product.is_active
        }

        # Check for duplicate part number if changing
        if data.part_number and data.part_number != product.part_number:
            existing_product = await self.repository.find_by_part_number(data.part_number)
            if existing_product and existing_product.id != product_id:
                raise DuplicatePartNumberException(part_number=data.part_number)
            product.part_number = data.part_number
            product.part_number_stripped = self._normalize_part_number(data.part_number)

        # Update fields
        if data.application is not None:
            product.application = data.application
        if data.vintage is not None:
            product.vintage = data.vintage
        if data.late_model is not None:
            product.late_model = data.late_model
        if data.soft is not None:
            product.soft = data.soft
        if data.universal is not None:
            product.universal = data.universal
        if data.is_active is not None and data.is_active != product.is_active:
            product.is_active = data.is_active
            # Create activity record for status change
            activity = ProductActivity(
                product_id=product.id,
                status="active" if data.is_active else "inactive",
                reason="Updated via API/Import",
                changed_by_id=user_id,
                changed_at=datetime.now()
            )
            self.db.add(activity)

        # Save changes
        self.db.add(product)
        await self.db.flush()
        await self.db.refresh(product)

        # Capture after state for audit
        after_state = {
            "part_number": product.part_number,
            "application": product.application,
            "vintage": product.vintage,
            "late_model": product.late_model,
            "soft": product.soft,
            "universal": product.universal,
            "is_active": product.is_active
        }

        # Calculate changes
        changes = {k: after_state[k] for k in after_state if before_state.get(k) != after_state[k]}

        # Log audit event if changes were made
        if changes:
            await self._log_audit_event(
                event_type=AuditEventType.PRODUCT_UPDATED,
                user_id=str(user_id) if user_id else None,
                resource_id=str(product.id),
                resource_type="Product",
                details={
                    "changes": changes,
                    "before": before_state,
                    "after": after_state,
                    "import_id": str(import_id) if import_id else None
                }
            )

            # Emit event for notifications
            await self.event_service.emit(
                "product.updated",
                {
                    "product_id": str(product.id),
                    "part_number": product.part_number,
                    "changes": changes,
                    "user_id": str(user_id) if user_id else None,
                    "import_id": str(import_id) if import_id else None
                }
            )

            # Update cache
            cache_key = f"product:{product.id}"
            await self.cache_service.set(cache_key, product)

            # Clear any list caches that might contain products
            await self.cache_service.delete_pattern("products:list:*")

        return product

    async def delete_product(
        self,
        product_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None
    ) -> None:
        """
        Delete a product (soft delete).

        Args:
            product_id: ID of the product to delete
            user_id: ID of the user performing the action

        Raises:
            ProductNotFoundException: If the product doesn't exist
        """
        # Get the existing product
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=str(product_id))

        # Soft delete
        product.is_deleted = True
        product.is_active = False
        self.db.add(product)

        # Create activity record
        activity = ProductActivity(
            product_id=product.id,
            status="deleted",
            changed_by_id=user_id,
            changed_at=datetime.now()
        )
        self.db.add(activity)

        await self.db.flush()

        # Log audit event
        await self._log_audit_event(
            event_type=AuditEventType.PRODUCT_DELETED,
            user_id=str(user_id) if user_id else None,
            resource_id=str(product.id),
            resource_type="Product",
            details={"part_number": product.part_number}
        )

        # Emit event for notifications
        await self.event_service.emit(
            "product.deleted",
            {
                "product_id": str(product.id),
                "part_number": product.part_number,
                "user_id": str(user_id) if user_id else None
            }
        )

        # Clear caches
        await self.cache_service.delete(f"product:{product.id}")
        await self.cache_service.delete_pattern("products:list:*")

    async def update_product_status(
        self,
        product_id: uuid.UUID,
        status: str,
        reason: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None
    ) -> Tuple[Product, ProductActivity]:
        """
        Update a product's status.

        Args:
            product_id: ID of the product to update
            status: New status (active/inactive)
            reason: Reason for the status change
            user_id: ID of the user performing the action

        Returns:
            Tuple of the updated product and the activity record

        Raises:
            ProductNotFoundException: If the product doesn't exist
        """
        # Update via repository with built-in auditing
        try:
            product, activity = await self.repository.update_status(
                product_id=product_id,
                status=status,
                reason=reason,
                user_id=user_id
            )

            # Get proper event type based on status
            event_type = AuditEventType.PRODUCT_ACTIVATED if status == "active" else AuditEventType.PRODUCT_DEACTIVATED

            # Log audit event
            await self._log_audit_event(
                event_type=event_type,
                user_id=str(user_id) if user_id else None,
                resource_id=str(product.id),
                resource_type="Product",
                details={
                    "status": status,
                    "reason": reason,
                    "part_number": product.part_number
                }
            )

            # Emit event for notifications
            await self.event_service.emit(
                f"product.{status}",
                {
                    "product_id": str(product.id),
                    "part_number": product.part_number,
                    "reason": reason,
                    "user_id": str(user_id) if user_id else None
                }
            )

            # Update cache
            await self.cache_service.set(f"product:{product.id}", product)
            await self.cache_service.delete_pattern("products:list:*")

            return product, activity

        except ResourceNotFoundException:
            raise ProductNotFoundException(product_id=str(product_id))

    async def create_supersession(
        self,
        old_product_id: uuid.UUID,
        new_product_id: uuid.UUID,
        reason: Optional[str] = None,
        user_id: Optional[uuid.UUID] = None
    ) -> ProductSupersession:
        """
        Create a product supersession.

        Args:
            old_product_id: ID of the product being replaced
            new_product_id: ID of the replacement product
            reason: Reason for the supersession
            user_id: ID of the user performing the action

        Returns:
            The created supersession record

        Raises:
            ProductNotFoundException: If either product doesn't exist
            BusinessException: If trying to supersede a product with itself
        """
        try:
            # Create via repository
            supersession = await self.repository.create_supersession(
                old_product_id=old_product_id,
                new_product_id=new_product_id,
                reason=reason
            )

            # Log audit event
            await self._log_audit_event(
                event_type=AuditEventType.PRODUCT_UPDATED,
                user_id=str(user_id) if user_id else None,
                resource_id=str(old_product_id),
                resource_type="Product",
                details={
                    "action": "supersession",
                    "new_product_id": str(new_product_id),
                    "reason": reason
                }
            )

            # Emit event for notifications
            await self.event_service.emit(
                "product.superseded",
                {
                    "old_product_id": str(old_product_id),
                    "new_product_id": str(new_product_id),
                    "reason": reason,
                    "user_id": str(user_id) if user_id else None
                }
            )

            # Clear caches
            await self.cache_service.delete(f"product:{old_product_id}")
            await self.cache_service.delete(f"product:{new_product_id}")
            await self.cache_service.delete_pattern("products:list:*")

            return supersession

        except ResourceNotFoundException as e:
            if "old_product_id" in str(e):
                raise ProductNotFoundException(product_id=str(old_product_id))
            else:
                raise ProductNotFoundException(product_id=str(new_product_id))

    async def update_pricing(
        self,
        product_id: uuid.UUID,
        pricing_data: ProductPricingCreate,
        user_id: Optional[uuid.UUID] = None,
        import_id: Optional[uuid.UUID] = None
    ) -> ProductPricing:
        """
        Update or create product pricing.

        Args:
            product_id: ID of the product
            pricing_data: Pricing data
            user_id: ID of the user performing the action
            import_id: ID of the import operation if part of an import

        Returns:
            The updated/created pricing record

        Raises:
            ProductNotFoundException: If the product doesn't exist
        """
        # Verify product exists
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=str(product_id))

        # Check if pricing exists
        query = select(ProductPricing).where(
            ProductPricing.product_id == product_id,
            ProductPricing.pricing_type_id == pricing_data.pricing_type_id,
            ProductPricing.is_deleted == False
        )
        if pricing_data.manufacturer_id:
            query = query.where(ProductPricing.manufacturer_id == pricing_data.manufacturer_id)

        result = await self.db.execute(query)
        existing_pricing = result.scalars().first()

        # Store original state for audit
        before_state = None
        if existing_pricing:
            before_state = {
                "price": float(existing_pricing.price),
                "currency": existing_pricing.currency
            }

            # Update existing pricing
            existing_pricing.price = pricing_data.price
            existing_pricing.currency = pricing_data.currency
            existing_pricing.last_updated = datetime.now()
            self.db.add(existing_pricing)
            pricing = existing_pricing
        else:
            # Create new pricing
            pricing = ProductPricing(
                product_id=product_id,
                pricing_type_id=pricing_data.pricing_type_id,
                manufacturer_id=pricing_data.manufacturer_id,
                price=pricing_data.price,
                currency=pricing_data.currency,
                last_updated=datetime.now()
            )
            self.db.add(pricing)

        await self.db.flush()
        await self.db.refresh(pricing)

        # Log audit event
        after_state = {
            "price": float(pricing.price),
            "currency": pricing.currency
        }

        event_details = {
            "part_number": product.part_number,
            "pricing_type_id": str(pricing_data.pricing_type_id),
            "price": float(pricing.price),
            "currency": pricing.currency,
            "manufacturer_id": str(pricing_data.manufacturer_id) if pricing_data.manufacturer_id else None,
            "import_id": str(import_id) if import_id else None
        }

        if before_state:
            event_details["before"] = before_state
            event_details["after"] = after_state
            event_details["changes"] = {k: after_state[k] for k in after_state if before_state.get(k) != after_state[k]}

        await self._log_audit_event(
            event_type=AuditEventType.PRICE_CHANGED,
            user_id=str(user_id) if user_id else None,
            resource_id=str(product_id),
            resource_type="Product",
            details=event_details
        )

        # Emit event for notifications
        await self.event_service.emit(
            "product.price_changed",
            {
                "product_id": str(product_id),
                "part_number": product.part_number,
                "price": float(pricing.price),
                "currency": pricing.currency,
                "user_id": str(user_id) if user_id else None,
                "import_id": str(import_id) if import_id else None
            }
        )

        # Clear caches
        await self.cache_service.delete(f"product:{product_id}")
        await self.cache_service.delete_pattern("products:list:*")
        await self.cache_service.delete_pattern(f"product:{product_id}:pricing:*")

        return pricing

    async def batch_create_products(
        self,
        products_data: List[ProductCreate],
        user_id: Optional[uuid.UUID] = None,
        sync_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create multiple products in a batch operation.

        Args:
            products_data: List of product creation data
            user_id: ID of the user performing the action
            sync_source: Source of synchronization (as400, filemaker, etc.)

        Returns:
            Dictionary with counts of created, updated, and failed records
        """
        if not products_data:
            return {
                "success": True,
                "created": 0,
                "updated": 0,
                "errors": 0,
                "total": 0
            }

        # Create sync history entry
        sync_history = await self.sync_repository.create_sync(
            entity_type=SyncEntityType.PRODUCT,
            source=SyncSource(sync_source.upper()) if sync_source else SyncSource.EXTERNAL,
            triggered_by_id=user_id,
            details={
                "record_count": len(products_data),
                "source": sync_source or "api"
            }
        )

        # Update sync status to running
        await self.sync_repository.update_sync_status(
            sync_id=sync_history.id,
            status=SyncStatus.RUNNING
        )

        # Log sync start event
        await self.sync_repository.add_sync_event(
            sync_id=sync_history.id,
            event_type="start",
            message=f"Starting import of {len(products_data)} products"
        )

        # Process each product
        result = {
            "created": 0,
            "updated": 0,
            "errors": 0,
            "error_details": []
        }

        # Get existing products by part number
        part_numbers = [p.part_number for p in products_data]
        query = select(Product).where(
            Product.part_number.in_(part_numbers),
            Product.is_deleted == False
        )
        existing_result = await self.db.execute(query)
        existing_products = {p.part_number: p for p in existing_result.scalars().all()}

        # Batch log audit event for overall operation
        await self._log_audit_event(
            event_type=AuditEventType.DATA_IMPORTED,
            user_id=str(user_id) if user_id else None,
            resource_type="Product",
            details={
                "sync_id": str(sync_history.id),
                "record_count": len(products_data),
                "source": sync_source or "api"
            }
        )

        # Process each product
        for product_data in products_data:
            try:
                # Check if product exists
                existing_product = existing_products.get(product_data.part_number)

                if existing_product:
                    # Update existing product
                    update_data = ProductUpdate(
                        application=product_data.application,
                        vintage=product_data.vintage,
                        late_model=product_data.late_model,
                        soft=product_data.soft,
                        universal=product_data.universal,
                        is_active=product_data.is_active
                    )

                    await self.update_product(
                        product_id=existing_product.id,
                        data=update_data,
                        user_id=user_id,
                        import_id=sync_history.id
                    )

                    # Handle descriptions if provided
                    if hasattr(product_data, "descriptions") and product_data.descriptions:
                        await self._update_descriptions(existing_product.id, product_data.descriptions)

                    # Handle marketing if provided
                    if hasattr(product_data, "marketing") and product_data.marketing:
                        await self._update_marketing(existing_product.id, product_data.marketing)

                    result["updated"] += 1
                else:
                    # Create new product
                    await self.create_product(
                        data=product_data,
                        user_id=user_id,
                        import_id=sync_history.id
                    )
                    result["created"] += 1

            except Exception as e:
                logger.error(f"Error importing product {product_data.part_number}: {str(e)}")
                result["errors"] += 1
                result["error_details"].append({
                    "part_number": product_data.part_number,
                    "error": str(e)
                })

        # Update sync history with results
        sync_status = SyncStatus.COMPLETED if result["errors"] == 0 else SyncStatus.FAILED
        error_message = None
        if result["errors"] > 0:
            error_message = f"Failed to import {result['errors']} products"

        await self.sync_repository.update_sync_status(
            sync_id=sync_history.id,
            status=sync_status,
            records_processed=len(products_data),
            records_created=result["created"],
            records_updated=result["updated"],
            records_failed=result["errors"],
            error_message=error_message,
            details={
                "error_details": result["error_details"] if result["errors"] > 0 else None
            }
        )

        # Log sync completion event
        await self.sync_repository.add_sync_event(
            sync_id=sync_history.id,
            event_type="complete",
            message=(
                f"Import completed with {result['created']} created, "
                f"{result['updated']} updated, and {result['errors']} errors"
            ),
            details=result
        )

        # Emit event for notifications
        await self.event_service.emit(
            "products.import_completed",
            {
                "sync_id": str(sync_history.id),
                "created": result["created"],
                "updated": result["updated"],
                "errors": result["errors"],
                "user_id": str(user_id) if user_id else None,
                "source": sync_source or "api"
            }
        )

        # Add total to result
        result["total"] = len(products_data)
        result["success"] = result["errors"] == 0

        return result

    async def batch_update_pricing(
        self,
        pricing_data_list: List[Dict[str, Any]],
        user_id: Optional[uuid.UUID] = None,
        sync_source: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update multiple product prices in a batch operation.

        Args:
            pricing_data_list: List of pricing data
            user_id: ID of the user performing the action
            sync_source: Source of synchronization (as400, filemaker, etc.)

        Returns:
            Dictionary with counts of created, updated, and failed records
        """
        if not pricing_data_list:
            return {
                "success": True,
                "created": 0,
                "updated": 0,
                "errors": 0,
                "total": 0
            }

        # Create sync history entry
        sync_history = await self.sync_repository.create_sync(
            entity_type=SyncEntityType.PRICING,
            source=SyncSource(sync_source.upper()) if sync_source else SyncSource.EXTERNAL,
            triggered_by_id=user_id,
            details={
                "record_count": len(pricing_data_list),
                "source": sync_source or "api"
            }
        )

        # Update sync status to running
        await self.sync_repository.update_sync_status(
            sync_id=sync_history.id,
            status=SyncStatus.RUNNING
        )

        # Log sync start event
        await self.sync_repository.add_sync_event(
            sync_id=sync_history.id,
            event_type="start",
            message=f"Starting import of {len(pricing_data_list)} pricing records"
        )

        # Batch log audit event for overall operation
        await self._log_audit_event(
            event_type=AuditEventType.DATA_IMPORTED,
            user_id=str(user_id) if user_id else None,
            resource_type="ProductPricing",
            details={
                "sync_id": str(sync_history.id),
                "record_count": len(pricing_data_list),
                "source": sync_source or "api"
            }
        )

        # Process each pricing record
        result = {
            "created": 0,
            "updated": 0,
            "errors": 0,
            "error_details": []
        }

        # Get products by part number
        part_numbers = [p.get("part_number") for p in pricing_data_list if "part_number" in p]
        query = select(Product).where(
            Product.part_number.in_(part_numbers),
            Product.is_deleted == False
        )
        existing_result = await self.db.execute(query)
        products_by_part_number = {p.part_number: p for p in existing_result.scalars().all()}

        # Get pricing types
        price_type_query = select("price_type").where("price_type.is_deleted == False")
        price_type_result = await self.db.execute(price_type_query)
        price_types = {pt.name: pt for pt in price_type_result.scalars().all()}

        # Process each pricing record
        for pricing_data in pricing_data_list:
            try:
                # Get product
                part_number = pricing_data.get("part_number")
                if not part_number:
                    result["errors"] += 1
                    result["error_details"].append({
                        "error": "Missing part number in pricing data",
                        "data": pricing_data
                    })
                    continue

                product = products_by_part_number.get(part_number)
                if not product:
                    result["errors"] += 1
                    result["error_details"].append({
                        "part_number": part_number,
                        "error": f"Product not found with part number: {part_number}"
                    })
                    continue

                # Get or create price type
                price_type_name = pricing_data.get("pricing_type")
                if not price_type_name:
                    result["errors"] += 1
                    result["error_details"].append({
                        "part_number": part_number,
                        "error": "Missing pricing type"
                    })
                    continue

                price_type = price_types.get(price_type_name)
                if not price_type:
                    # Create price type
                    from app.domains.products.models import PriceType
                    price_type = PriceType(
                        name=price_type_name,
                        description=f"{price_type_name} price type"
                    )
                    self.db.add(price_type)
                    await self.db.flush()
                    price_types[price_type_name] = price_type

                # Check if pricing record exists
                manufacturer_id = pricing_data.get("manufacturer_id")

                pricing_query = select(ProductPricing).where(
                    ProductPricing.product_id == product.id,
                    ProductPricing.pricing_type_id == price_type.id,
                    ProductPricing.is_deleted == False
                )
                if manufacturer_id:
                    pricing_query = pricing_query.where(ProductPricing.manufacturer_id == manufacturer_id)

                pricing_result = await self.db.execute(pricing_query)
                existing_pricing = pricing_result.scalars().first()

                # Update or create pricing
                if existing_pricing:
                    # Update existing pricing
                    existing_pricing.price = pricing_data.get("price")
                    existing_pricing.currency = pricing_data.get("currency", "USD")
                    existing_pricing.last_updated = datetime.now()
                    self.db.add(existing_pricing)
                    result["updated"] += 1
                else:
                    # Create new pricing
                    new_pricing = ProductPricing(
                        product_id=product.id,
                        pricing_type_id=price_type.id,
                        manufacturer_id=manufacturer_id,
                        price=pricing_data.get("price"),
                        currency=pricing_data.get("currency", "USD"),
                        last_updated=datetime.now()
                    )
                    self.db.add(new_pricing)
                    result["created"] += 1

                # Log specific audit event
                await self._log_audit_event(
                    event_type=AuditEventType.PRICE_CHANGED,
                    user_id=str(user_id) if user_id else None,
                    resource_id=str(product.id),
                    resource_type="Product",
                    details={
                        "part_number": part_number,
                        "pricing_type": price_type_name,
                        "price": pricing_data.get("price"),
                        "currency": pricing_data.get("currency", "USD"),
                        "sync_id": str(sync_history.id)
                    }
                )

            except Exception as e:
                logger.error(f"Error importing pricing for {part_number}: {str(e)}")
                result["errors"] += 1
                result["error_details"].append({
                    "part_number": part_number,
                    "error": str(e)
                })

        # Commit changes
        await self.db.flush()

        # Update sync history with results
        sync_status = SyncStatus.COMPLETED if result["errors"] == 0 else SyncStatus.FAILED
        error_message = None
        if result["errors"] > 0:
            error_message = f"Failed to import {result['errors']} pricing records"

        await self.sync_repository.update_sync_status(
            sync_id=sync_history.id,
            status=sync_status,
            records_processed=len(pricing_data_list),
            records_created=result["created"],
            records_updated=result["updated"],
            records_failed=result["errors"],
            error_message=error_message,
            details={
                "error_details": result["error_details"] if result["errors"] > 0 else None
            }
        )

        # Log sync completion event
        await self.sync_repository.add_sync_event(
            sync_id=sync_history.id,
            event_type="complete",
            message=(
                f"Pricing import completed with {result['created']} created, "
                f"{result['updated']} updated, and {result['errors']} errors"
            ),
            details=result
        )

        # Emit event for notifications
        await self.event_service.emit(
            "products.pricing_import_completed",
            {
                "sync_id": str(sync_history.id),
                "created": result["created"],
                "updated": result["updated"],
                "errors": result["errors"],
                "user_id": str(user_id) if user_id else None,
                "source": sync_source or "api"
            }
        )

        # Add total to result
        result["total"] = len(pricing_data_list)
        result["success"] = result["errors"] == 0

        # Clear caches
        await self.cache_service.delete_pattern("product:*")
        await self.cache_service.delete_pattern("products:list:*")

        return result

    # Helper Methods

    async def _create_descriptions(
        self,
        product_id: uuid.UUID,
        descriptions: List[ProductDescriptionCreate]
    ) -> None:
        """Create product descriptions."""
        for desc in descriptions:
            description = ProductDescription(
                product_id=product_id,
                description_type=desc.description_type,
                description=desc.description
            )
            self.db.add(description)

    async def _update_descriptions(
        self,
        product_id: uuid.UUID,
        descriptions: List[ProductDescriptionCreate]
    ) -> None:
        """Update product descriptions (delete and recreate)."""
        # Delete existing descriptions
        from sqlalchemy import delete
        await self.db.execute(
            delete(ProductDescription).where(ProductDescription.product_id == product_id)
        )

        # Create new descriptions
        await self._create_descriptions(product_id, descriptions)

    async def _create_marketing(
        self,
        product_id: uuid.UUID,
        marketing_items: List[ProductMarketingCreate]
    ) -> None:
        """Create product marketing items."""
        for i, mkt in enumerate(marketing_items):
            position = mkt.position if mkt.position is not None else i + 1
            marketing = ProductMarketing(
                product_id=product_id,
                marketing_type=mkt.marketing_type,
                content=mkt.content,
                position=position
            )
            self.db.add(marketing)

    async def _update_marketing(
        self,
        product_id: uuid.UUID,
        marketing_items: List[ProductMarketingCreate]
    ) -> None:
        """Update product marketing items (delete and recreate)."""
        # Delete existing marketing items
        from sqlalchemy import delete
        await self.db.execute(
            delete(ProductMarketing).where(ProductMarketing.product_id == product_id)
        )

        # Create new marketing items
        await self._create_marketing(product_id, marketing_items)

    def _normalize_part_number(self, part_number: str) -> str:
        """Normalize part number (remove non-alphanumeric characters and uppercase)."""
        return ''.join(c for c in part_number if c.isalnum()).upper()

    async def _log_audit_event(
        self,
        event_type: AuditEventType,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log an audit event using the audit service."""
        audit_service = get_audit_service(self.db)
        await audit_service.log_event(
            event_type=event_type,
            user_id=user_id,
            resource_id=resource_id,
            resource_type=resource_type,
            details=details
        )
