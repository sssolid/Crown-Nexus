# Crown Nexus Database Structure
## Business-Friendly Guide

This document provides a high-level overview of the Crown Nexus database structure in business terms. It explains what data is stored, how it's organized, and what business purposes it serves.

## Table of Contents
- [Core Product Information](#core-product-information)
- [Product Organization & Classification](#product-organization--classification)
- [Media & Digital Assets](#media--digital-assets)
- [Inventory Management](#inventory-management)
- [Geography & Locations](#geography--locations)
- [Business Relationships](#business-relationships)
- [Customer Information](#customer-information)
- [Orders & Payments](#orders--payments)
- [Product Classifications](#product-classifications)
- [Product Attributes](#product-attributes)
- [Pricing & Measurements](#pricing--measurements)
- [Shipping Information](#shipping-information)
- [Compliance & Regulatory](#compliance--regulatory)
- [Product References](#product-references)

## Core Product Information

### Products
Stores basic product data including part numbers, application information, and flags that identify product characteristics (vintage, late model, soft good, universal fit).

### Product Descriptions
Contains different types of product descriptions (short, long, keywords, slang terms, internal notes) organized by description type.

### Product Marketing
Stores marketing content like bullet points and ad copy for products, keeping this content separate from technical descriptions.

### Product Activity
Tracks changes to product status (active vs. inactive) with reasons and timestamps to maintain a history of product lifecycle.

### Product Supersession
Records product replacements when newer products supersede older ones, providing traceability for discontinued items.

## Product Organization & Classification

### Brand Information
Stores brand details and tracks changes in product branding over time, maintaining history of which brands have owned which products.

## Media & Digital Assets

### Media Management
Stores product-related files including marketing images, MSDS sheets, DOT approval documents, and other digital assets. Tracks which image is the primary product image.

## Inventory Management

### Warehouses
Stores information about warehouse locations where products are stored.

### Product Stock
Tracks inventory levels for each product at each warehouse location, with timestamps for when stock levels were last updated.

## Geography & Locations

### Countries
Stores country information including names, ISO codes, currency, and regional groupings.

### Addresses
Stores physical addresses for warehouses, manufacturers, companies, and customers, with optional geolocation data.

## Business Relationships

### Companies
Stores information about parent companies and corporate entities.

### Manufacturers
Records details about product manufacturers, including their parent companies and manufacturing locations.

## Customer Information

### Customers
Stores customer contact information and shipping/billing preferences.

## Orders & Payments

### Orders
Records customer purchase orders, tracking status from pending through shipping, delivery, cancellation, or return.

### Order Items
Maintains line-item details for each order, capturing pricing at the time of purchase.

### Payments
Tracks payment information, methods, and statuses for each order.

### Payment Processing
Records information about payment processors (Stripe, PayPal, etc.) including fee structures.

### Transactions
Provides detailed transaction history for payments, refunds, and adjustments.

## Product Classifications

### Tariff Codes
Stores export/import tariff codes for products and maintains a history of changes for compliance purposes.

### UNSPSC Codes
Records United Nations Standard Products and Services Codes used for product categorization in procurement systems.

### UPC Information
Stores product UPC codes and maintains history of changes to barcode assignments.

## Product Attributes

### Colors
Tracks product color information including standard color names and hex codes for digital representation.

### Construction Types
Records what materials products are made from (steel, plastic, etc.).

### Textures
Describes product surface finishes (glossy, matte, etc.).

### Packaging Types
Tracks how products are packaged (box, blister pack, etc.).

### Hardware
Records what hardware items (screws, bolts, etc.) are included with products.

## Pricing & Measurements

### Product Pricing
Stores different price types (MSRP, wholesale, etc.) with currency information.

### Price History
Maintains a record of price changes over time with reasons for the changes.

### Physical Measurements
Records product dimensions, weight, and volume for shipping calculations.

### Shipping Weights
Stores carrier-specific dimensional weight calculations for shipping.

## Shipping Information

### Carriers
Records shipping carrier information including tracking URL templates.

### Additional Shipping
Tracks extra shipping charges for specific products based on weight, location, or handling requirements.

## Compliance & Regulatory

### DOT Approvals
Tracks Department of Transportation approval status for relevant products.

### Proposition 65
Records California Proposition 65 chemical information and required warnings.

### Chemical Associations
Links products to chemicals they contain and defines exposure scenarios and required warnings.

### Hazardous Materials
Stores hazardous material shipping information including UN numbers, hazard class, and handling instructions.

## Product References

### Warranties
Records warranty terms, duration, and coverage details for products.

### Country of Origin
Tracks manufacturing and assembly locations for products.

### Product Interchange
Records cross-reference information between our parts and competitor or OEM part numbers.

### Quantity Information
Defines how products are counted and sold (pair, set, each, etc.).

### Sold As Information
Records how products are packaged and sold (individually, as kits, etc.).

### PCdb Mappings
Stores Auto Care Association PCdb (parts classification database) mappings for industry-standard categorization.

---

## Data Relationships Overview

The database is designed to support:

1. **Complete product lifecycle tracking** from creation through supersession
2. **Detailed inventory management** across multiple warehouses
3. **Omni-channel order processing** with comprehensive payment tracking
4. **Regulatory compliance** for shipping and consumer safety
5. **Comprehensive pricing management** for different markets and customer types
6. **Rich product information** including multiple types of descriptions, specifications, and media

This structure allows Crown Nexus to:
- Provide dealers with accurate, up-to-date product information
- Track inventory efficiently across locations
- Maintain compliance with regulations
- Process orders and payments seamlessly
- Deliver rich product data to e-commerce channels
