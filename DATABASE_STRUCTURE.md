# Crown Nexus Database Schema

This document outlines the PostgreSQL database schema for the Crown Nexus B2B platform for the automotive aftermarket industry.

## Table of Contents
- [Core Product Tables](#core-product-tables)
- [Categorization Tables](#categorization-tables)
- [Media Tables](#media-tables)
- [Inventory Tables](#inventory-tables)
- [Location Tables](#location-tables)
- [Organization Tables](#organization-tables)
- [Customer Tables](#customer-tables)
- [Order and Payment Tables](#order-and-payment-tables)
- [Classification Tables](#classification-tables)
- [Product Attribute Tables](#product-attribute-tables)
- [Shipping Tables](#shipping-tables)
- [Compliance Tables](#compliance-tables)
- [Reference Tables](#reference-tables)
- [User and Role Management](#user-and-role-management)
- [Flexible Attributes System](#flexible-attributes-system)
- [Search Capabilities](#search-capabilities)
- [Audit Logging](#audit-logging)

## Core Product Tables

### Products
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for the product |
| part_number | varchar(50) | NOT NULL | Unique identifier for the product (e.g., "PN12345") |
| part_number_stripped | varchar(50) | NOT NULL | Only A-Z, 0-9 version of part_number |
| application | text | | Unformatted data for vehicle fitment applications |
| vintage | boolean | NOT NULL DEFAULT false | Vintage fitments flag |
| late_model | boolean | NOT NULL DEFAULT false | Late model fitments flag |
| soft | boolean | NOT NULL DEFAULT false | Soft good flag |
| universal | boolean | NOT NULL DEFAULT false | Universal fit flag |
| search_vector | tsvector | | Full-text search vector for improved search |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |
| updated_at | timestamp with time zone | NOT NULL DEFAULT now() | Record update timestamp |

**Indexes:**
- `idx_products_part_number` - B-tree index on part_number
- `idx_products_part_number_stripped` - B-tree index on part_number_stripped
- `products_search_idx` - GIN index on search_vector

### Product Descriptions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| description_type | varchar(20) | NOT NULL | Type of description (Short, Long, Keywords, Slang, Notes) |
| description | text | NOT NULL | Description content |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_descriptions_product_id` - B-tree index on product_id
- `idx_product_descriptions_type` - B-tree index on description_type

### Product Marketing
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| marketing_type | varchar(20) | NOT NULL | Type of marketing content (Bullet Point, Ad Copy) |
| content | text | NOT NULL | Marketing content |
| position | integer | | Order for display (especially for bullet points) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_marketing_product_id` - B-tree index on product_id
- `idx_product_marketing_position` - B-tree index on position

### Product Activity
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| status | varchar(20) | NOT NULL | Product status (active, inactive) |
| reason | text | | Reason for status change (Discontinued, Out of Stock, etc.) |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_activity_product_id` - B-tree index on product_id
- `idx_product_activity_status` - B-tree index on status
- `idx_product_activity_changed_at` - B-tree index on changed_at

### Product Supersession
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| old_product_id | uuid | NOT NULL REFERENCES Products(id) | Product being replaced |
| new_product_id | uuid | NOT NULL REFERENCES Products(id) | Replacement product |
| reason | text | | Explanation of why the product was superseded |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_supersession_old_product_id` - B-tree index on old_product_id
- `idx_product_supersession_new_product_id` - B-tree index on new_product_id

## Categorization Tables

### Brand
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL | Brand name (Crown, RT, etc.) |
| parent_company_id | uuid | REFERENCES Companies(id) | Parent company if applicable |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_brand_name` - B-tree index on name

### Product Brand History
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| old_brand_id | uuid | REFERENCES Brand(id) | Previous brand |
| new_brand_id | uuid | NOT NULL REFERENCES Brand(id) | New brand |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_brand_history_product_id` - B-tree index on product_id
- `idx_product_brand_history_changed_at` - B-tree index on changed_at

## Media Tables

### Media Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(50) | NOT NULL UNIQUE | Type name (image, video, document, msds, dot_approval) |
| description | text | | Description of the media type |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

### Media
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| media_type_id | uuid | NOT NULL REFERENCES Media_Types(id) | Type of media |
| file_path | varchar(255) | NOT NULL | Path to the file |
| file_name | varchar(255) | NOT NULL | Original filename |
| file_size | integer | NOT NULL | Size in bytes |
| mime_type | varchar(100) | NOT NULL | MIME type |
| is_primary | boolean | NOT NULL DEFAULT false | Primary media for product |
| alt_text | varchar(255) | | Alternative text for accessibility |
| description | text | | Description of the media |
| uploaded_by | uuid | REFERENCES Users(id) | User who uploaded the file |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |
| updated_at | timestamp with time zone | NOT NULL DEFAULT now() | Record update timestamp |

**Indexes:**
- `idx_media_product_id` - B-tree index on product_id
- `idx_media_media_type_id` - B-tree index on media_type_id
- `idx_media_is_primary` - B-tree index on is_primary

## Inventory Tables

### Warehouses
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL | Warehouse name |
| address_id | uuid | REFERENCES Address(id) | Reference to address |
| is_active | boolean | NOT NULL DEFAULT true | If warehouse is currently operational |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_warehouses_name` - B-tree index on name
- `idx_warehouses_is_active` - B-tree index on is_active

### Product Stock
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| warehouse_id | uuid | NOT NULL REFERENCES Warehouses(id) | Reference to warehouse |
| quantity | integer | NOT NULL DEFAULT 0 | Quantity in stock |
| last_updated | timestamp with time zone | NOT NULL DEFAULT now() | Last stock update timestamp |

**Indexes:**
- `idx_product_stock_product_id` - B-tree index on product_id
- `idx_product_stock_warehouse_id` - B-tree index on warehouse_id
- `idx_product_stock_quantity` - B-tree index on quantity

## Location Tables

### Country
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL | Full country name |
| iso_alpha_2 | char(2) | NOT NULL UNIQUE | 2-letter country code (US, etc.) |
| iso_alpha_3 | char(3) | NOT NULL UNIQUE | 3-letter country code (USA, etc.) |
| iso_numeric | varchar(3) | UNIQUE | Numeric country code (840, etc.) |
| region | varchar(50) | | Region name (North America, etc.) |
| subregion | varchar(50) | | Subregion name (Northern America, etc.) |
| currency | varchar(3) | | Currency code (USD, etc.) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_country_name` - B-tree index on name
- `idx_country_iso_alpha_2` - B-tree index on iso_alpha_2
- `idx_country_iso_alpha_3` - B-tree index on iso_alpha_3

### Address
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| street | varchar(255) | NOT NULL | Street address |
| city | varchar(100) | NOT NULL | City name |
| state | varchar(100) | | State/province (can be NULL if not applicable) |
| postal_code | varchar(20) | NOT NULL | Postal/ZIP code |
| country_id | uuid | NOT NULL REFERENCES Country(id) | Reference to country |
| latitude | decimal(10,7) | | Optional for geolocation |
| longitude | decimal(10,7) | | Optional for geolocation |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_address_country_id` - B-tree index on country_id
- `idx_address_postal_code` - B-tree index on postal_code

## Organization Tables

### Companies
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL | Company name |
| headquarters_address_id | uuid | REFERENCES Address(id) | Reference to headquarters address |
| billing_address_id | uuid | REFERENCES Address(id) | Reference to billing address |
| shipping_address_id | uuid | REFERENCES Address(id) | Reference to shipping address |
| industry | varchar(100) | | Industry sector (Automotive, Electronics, etc.) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_companies_name` - B-tree index on name

### Manufacturers
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL | Manufacturer name |
| company_id | uuid | REFERENCES Companies(id) | Parent company if applicable |
| address_id | uuid | REFERENCES Address(id) | Reference to address |
| billing_address_id | uuid | REFERENCES Address(id) | Reference to billing address |
| shipping_address_id | uuid | REFERENCES Address(id) | Reference to shipping address |
| country_id | uuid | REFERENCES Country(id) | Manufacturing location |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_manufacturers_name` - B-tree index on name
- `idx_manufacturers_company_id` - B-tree index on company_id
- `idx_manufacturers_country_id` - B-tree index on country_id

## Customer Tables

### Customers
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| first_name | varchar(100) | NOT NULL | Customer's first name |
| last_name | varchar(100) | NOT NULL | Customer's last name |
| email | varchar(255) | NOT NULL UNIQUE | Customer's email address |
| phone | varchar(50) | | Customer's phone number |
| billing_address_id | uuid | REFERENCES Address(id) | Reference to billing address |
| shipping_address_id | uuid | REFERENCES Address(id) | Reference to shipping address |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_customers_email` - B-tree index on email
- `idx_customers_last_name` - B-tree index on last_name

## Order and Payment Tables

### Order Status Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| code | varchar(20) | NOT NULL UNIQUE | Status code (PENDING, PROCESSING, etc.) |
| name | varchar(50) | NOT NULL | Status name (Pending, Processing, etc.) |
| description | text | | Description of the status |
| is_active | boolean | NOT NULL DEFAULT true | Whether the status is active |
| display_order | integer | NOT NULL DEFAULT 0 | Order for display purposes |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_order_status_types_code` - B-tree index on code
- `idx_order_status_types_is_active` - B-tree index on is_active

### Orders
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| customer_id | uuid | NOT NULL REFERENCES Customers(id) | Reference to customer |
| billing_address_id | uuid | NOT NULL REFERENCES Address(id) | Reference to billing address |
| shipping_address_id | uuid | NOT NULL REFERENCES Address(id) | Reference to shipping address |
| order_status_id | uuid | NOT NULL REFERENCES Order_Status_Types(id) | Order status |
| total_price | decimal(10,2) | NOT NULL | Total order price |
| placed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the order was placed |

**Indexes:**
- `idx_orders_customer_id` - B-tree index on customer_id
- `idx_orders_order_status_id` - B-tree index on order_status_id
- `idx_orders_placed_at` - B-tree index on placed_at

### Order Items
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| order_id | uuid | NOT NULL REFERENCES Orders(id) | Reference to order |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| quantity | integer | NOT NULL | Quantity ordered |
| price | decimal(10,2) | NOT NULL | Price per unit at time of order |
| subtotal | decimal(10,2) | NOT NULL | Line item subtotal (quantity * price) |

**Indexes:**
- `idx_order_items_order_id` - B-tree index on order_id
- `idx_order_items_product_id` - B-tree index on product_id

### Payment Method Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| code | varchar(20) | NOT NULL UNIQUE | Method code (CREDIT_CARD, PAYPAL, etc.) |
| name | varchar(50) | NOT NULL | Method name (Credit Card, PayPal, etc.) |
| description | text | | Description of the payment method |
| is_active | boolean | NOT NULL DEFAULT true | Whether the method is active |
| display_order | integer | NOT NULL DEFAULT 0 | Order for display purposes |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_payment_method_types_code` - B-tree index on code
- `idx_payment_method_types_is_active` - B-tree index on is_active

### Payment Status Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| code | varchar(20) | NOT NULL UNIQUE | Status code (PENDING, COMPLETED, etc.) |
| name | varchar(50) | NOT NULL | Status name (Pending, Completed, etc.) |
| description | text | | Description of the status |
| is_active | boolean | NOT NULL DEFAULT true | Whether the status is active |
| display_order | integer | NOT NULL DEFAULT 0 | Order for display purposes |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_payment_status_types_code` - B-tree index on code
- `idx_payment_status_types_is_active` - B-tree index on is_active

### Payments
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| order_id | uuid | NOT NULL REFERENCES Orders(id) | Reference to order |
| payment_method_id | uuid | NOT NULL REFERENCES Payment_Method_Types(id) | Payment method |
| amount | decimal(10,2) | NOT NULL | Payment amount |
| payment_status_id | uuid | NOT NULL REFERENCES Payment_Status_Types(id) | Payment status |
| processor_id | uuid | REFERENCES Processor(id) | Payment processor used |
| processor_transaction_id | varchar(100) | | External transaction ID from processor |
| paid_at | timestamp with time zone | | When payment was processed |

**Indexes:**
- `idx_payments_order_id` - B-tree index on order_id
- `idx_payments_payment_status_id` - B-tree index on payment_status_id
- `idx_payments_paid_at` - B-tree index on paid_at

### Processor
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL UNIQUE | Processor name (Stripe, PayPal, Bank Wire) |
| processor_type | varchar(20) | NOT NULL | Type (Online, Bank, Manual) |
| transaction_fee_percentage | decimal(5,2) | | Fee percentage (e.g., 2.9 for Stripe) |
| fixed_fee | decimal(5,2) | | Fixed fee per transaction (e.g., $0.30 for Stripe) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

### Transaction Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| code | varchar(20) | NOT NULL UNIQUE | Type code (PAYMENT, REFUND, etc.) |
| name | varchar(50) | NOT NULL | Type name (Payment, Refund, etc.) |
| description | text | | Description of the transaction type |
| is_active | boolean | NOT NULL DEFAULT true | Whether the type is active |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_transaction_types_code` - B-tree index on code

### Transaction Status Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| code | varchar(20) | NOT NULL UNIQUE | Status code (PENDING, COMPLETED, etc.) |
| name | varchar(50) | NOT NULL | Status name (Pending, Completed, etc.) |
| description | text | | Description of the status |
| is_active | boolean | NOT NULL DEFAULT true | Whether the status is active |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_transaction_status_types_code` - B-tree index on code

### Transactions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| payment_id | uuid | NOT NULL REFERENCES Payments(id) | Reference to payment |
| transaction_type_id | uuid | NOT NULL REFERENCES Transaction_Types(id) | Transaction type |
| amount | decimal(10,2) | NOT NULL | Transaction amount |
| transaction_status_id | uuid | NOT NULL REFERENCES Transaction_Status_Types(id) | Transaction status |
| transaction_date | timestamp with time zone | NOT NULL DEFAULT now() | When transaction occurred |
| processor_id | uuid | REFERENCES Processor(id) | Payment processor used |
| processor_transaction_id | varchar(100) | | External transaction ID from processor |

**Indexes:**
- `idx_transactions_payment_id` - B-tree index on payment_id
- `idx_transactions_transaction_type_id` - B-tree index on transaction_type_id
- `idx_transactions_transaction_date` - B-tree index on transaction_date

## Classification Tables

### Tariff Codes
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| code | varchar(15) | NOT NULL | HS, HTS, or other tariff code |
| description | text | NOT NULL | Description of the code |
| country_id | uuid | REFERENCES Country(id) | Country this code applies to |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_tariff_codes_code` - B-tree index on code
- `idx_tariff_codes_country_id` - B-tree index on country_id

### Product Tariff Codes
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| tariff_code_id | uuid | NOT NULL REFERENCES Tariff_Codes(id) | Reference to tariff code |
| assigned_at | timestamp with time zone | NOT NULL DEFAULT now() | When code was assigned |

**Indexes:**
- `idx_product_tariff_codes_product_id` - B-tree index on product_id
- `idx_product_tariff_codes_tariff_code_id` - B-tree index on tariff_code_id

### Product Tariff Code History
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| old_tariff_code_id | uuid | REFERENCES Tariff_Codes(id) | Previous tariff code |
| new_tariff_code_id | uuid | NOT NULL REFERENCES Tariff_Codes(id) | New tariff code |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_tariff_code_history_product_id` - B-tree index on product_id
- `idx_product_tariff_code_history_changed_at` - B-tree index on changed_at

### UNSPSC Codes
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| code | varchar(10) | NOT NULL UNIQUE | 8- or 10-digit UNSPSC code |
| description | text | NOT NULL | UNSPSC category description |
| segment | varchar(255) | | High-level category |
| family | varchar(255) | | Sub-category |
| class | varchar(255) | | Product class |
| commodity | varchar(255) | | Specific commodity category |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_unspsc_codes_code` - B-tree index on code

### Product UNSPSC History
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| old_unspsc_code_id | uuid | REFERENCES UNSPSC_Codes(id) | Previous UNSPSC code |
| new_unspsc_code_id | uuid | NOT NULL REFERENCES UNSPSC_Codes(id) | New UNSPSC code |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_unspsc_history_product_id` - B-tree index on product_id
- `idx_product_unspsc_history_changed_at` - B-tree index on changed_at

### Product UPCs
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| upc | varchar(14) | NOT NULL UNIQUE | UPC (12, 13, or 14 digits) |
| assigned_at | timestamp with time zone | NOT NULL DEFAULT now() | When UPC was assigned |

**Indexes:**
- `idx_product_upcs_product_id` - B-tree index on product_id
- `idx_product_upcs_upc` - B-tree index on upc

### Product UPC History
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| old_upc | varchar(14) | | Previous UPC |
| new_upc | varchar(14) | NOT NULL | New UPC |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_upc_history_product_id` - B-tree index on product_id
- `idx_product_upc_history_changed_at` - B-tree index on changed_at

## Product Attribute Tables

### Colors
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(50) | NOT NULL UNIQUE | Standard color name |
| hex_code | varchar(7) | | Hex code for digital representation (e.g., #FF0000) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_colors_name` - B-tree index on name

### Product Colors
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| color_id | uuid | NOT NULL REFERENCES Colors(id) | Reference to color |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_colors_product_id` - B-tree index on product_id
- `idx_product_colors_color_id` - B-tree index on color_id

### Construction Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL UNIQUE | Material name (Steel, Plastic, etc.) |
| description | text | | Optional description |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_construction_types_name` - B-tree index on name

### Product Construction Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| construction_type_id | uuid | NOT NULL REFERENCES Construction_Types(id) | Reference to construction type |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_construction_types_product_id` - B-tree index on product_id
- `idx_product_construction_types_construction_type_id` - B-tree index on construction_type_id

### Textures
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL UNIQUE | Texture name (e.g., Glossy, Matte) |
| description | text | | Optional description |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_textures_name` - B-tree index on name

### Product Textures
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| texture_id | uuid | NOT NULL REFERENCES Textures(id) | Reference to texture |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_textures_product_id` - B-tree index on product_id
- `idx_product_textures_texture_id` - B-tree index on texture_id

### Packaging Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| pies_code | varchar(50) | | AutoCare PCdb PIES Code (if applicable) |
| name | varchar(100) | NOT NULL UNIQUE | Packaging type (e.g., Box, Loose, Blister Pack) |
| description | text | | Optional description |
| source | varchar(20) | NOT NULL DEFAULT 'Custom' | Source (AutoCare PCdb, Custom) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_packaging_types_name` - B-tree index on name
- `idx_packaging_types_pies_code` - B-tree index on pies_code

### Product Packaging
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| packaging_type_id | uuid | NOT NULL REFERENCES Packaging_Types(id) | Reference to packaging type |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_packaging_product_id` - B-tree index on product_id
- `idx_product_packaging_packaging_type_id` - B-tree index on packaging_type_id

### Hardware Items
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL UNIQUE | Name of the hardware item |
| description | text | | Optional details |
| part_number | varchar(100) | | If hardware has its own part number |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_hardware_items_name` - B-tree index on name
- `idx_hardware_items_part_number` - B-tree index on part_number

### Product Hardware
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| hardware_id | uuid | NOT NULL REFERENCES Hardware_Items(id) | Reference to hardware item |
| quantity | integer | NOT NULL DEFAULT 1 | Number of hardware pieces included |
| is_optional | boolean | NOT NULL DEFAULT false | Is the hardware required |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_hardware_product_id` - B-tree index on product_id
- `idx_product_hardware_hardware_id` - B-tree index on hardware_id

### Price Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(50) | NOT NULL UNIQUE | Price type name (Jobber, Export, MSRP) |
| description | text | | Description of price type |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_price_types_name` - B-tree index on name

### Product Pricing
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| pricing_type_id | uuid | NOT NULL REFERENCES Price_Types(id) | Reference to price type |
| manufacturer_id | uuid | REFERENCES Manufacturers(id) | Optional manufacturer reference |
| price | decimal(10,2) | NOT NULL | The current price |
| currency | varchar(3) | NOT NULL DEFAULT 'USD' | Currency code |
| last_updated | timestamp with time zone | NOT NULL DEFAULT now() | Last update timestamp |

**Indexes:**
- `idx_product_pricing_product_id` - B-tree index on product_id
- `idx_product_pricing_pricing_type_id` - B-tree index on pricing_type_id
- `idx_product_pricing_manufacturer_id` - B-tree index on manufacturer_id

### Product Pricing History
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| pricing_type_id | uuid | NOT NULL REFERENCES Price_Types(id) | Reference to price type |
| manufacturer_id | uuid | REFERENCES Manufacturers(id) | Optional manufacturer reference |
| old_price | decimal(10,2) | NOT NULL | Previous price |
| new_price | decimal(10,2) | NOT NULL | Updated price |
| currency | varchar(3) | NOT NULL DEFAULT 'USD' | Currency code |
| change_reason | text | | Why the price was changed |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_pricing_history_product_id` - B-tree index on product_id
- `idx_product_pricing_history_changed_at` - B-tree index on changed_at

### Product Measurements
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| manufacturer_id | uuid | REFERENCES Manufacturers(id) | Optional manufacturer reference |
| length | decimal(10,3) | | Length in inches |
| width | decimal(10,3) | | Width in inches |
| height | decimal(10,3) | | Height in inches |
| weight | decimal(10,3) | | Weight in pounds |
| volume | decimal(10,3) | | Volume in cubic inches |
| dimensional_weight | decimal(10,3) | | DIM weight calculation |
| effective_date | timestamp with time zone | NOT NULL DEFAULT now() | When measurements become effective |

**Indexes:**
- `idx_product_measurements_product_id` - B-tree index on product_id
- `idx_product_measurements_manufacturer_id` - B-tree index on manufacturer_id
- `idx_product_measurements_effective_date` - B-tree index on effective_date

### Shipping Weights
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| carrier | varchar(50) | NOT NULL | Carrier name (UPS, FedEx, USPS) |
| dim_factor | integer | NOT NULL | Carrier-specific DIM factor |
| volume | decimal(10,3) | NOT NULL | Package volume |
| actual_weight | decimal(10,3) | NOT NULL | Actual weight in pounds |
| dim_weight | decimal(10,3) | NOT NULL | Dimensional weight calculation |

**Indexes:**
- `idx_shipping_weights_product_id` - B-tree index on product_id
- `idx_shipping_weights_carrier` - B-tree index on carrier

## Shipping Tables

### Carriers
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL UNIQUE | Carrier name (UPS, FedEx, etc.) |
| service_area | varchar(20) | NOT NULL | Service area (Domestic, International) |
| tracking_url_template | varchar(255) | | URL template for tracking (https://tracking.fedex.com/{tracking_number}) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_carriers_name` - B-tree index on name

### Additional Shipping
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| carrier_id | uuid | NOT NULL REFERENCES Carriers(id) | Reference to carrier |
| weight | decimal(10,3) | | If weight-based extra charges apply |
| location_zone | varchar(50) | | If surcharge depends on location (Alaska, Hawaii) |
| surcharge | decimal(10,2) | NOT NULL | Additional shipping fee |
| reason | text | | Explanation of surcharge (Oversized item, Special handling) |
| estimated | boolean | NOT NULL DEFAULT true | True if estimate, False if actual |
| effective_date | timestamp with time zone | NOT NULL DEFAULT now() | When surcharge becomes effective |

**Indexes:**
- `idx_additional_shipping_product_id` - B-tree index on product_id
- `idx_additional_shipping_carrier_id` - B-tree index on carrier_id
- `idx_additional_shipping_effective_date` - B-tree index on effective_date

## Compliance Tables

### Product DOT Approvals
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| approval_status | varchar(20) | NOT NULL | Status (Approved, Pending, Revoked, Not Required) |
| approval_number | varchar(100) | | Official DOT approval number |
| approved_by | varchar(255) | | Entity or agency that approved the product |
| approval_date | date | | When the product was approved |
| expiration_date | date | | If the approval has an expiration date |
| reason | text | | If revoked or pending, store reason |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_dot_approvals_product_id` - B-tree index on product_id
- `idx_product_dot_approvals_approval_status` - B-tree index on approval_status
- `idx_product_dot_approvals_approval_number` - B-tree index on approval_number

### Proposition 65 Chemicals
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL | Chemical name |
| cas_number | varchar(20) | NOT NULL UNIQUE | Chemical Abstracts Service (CAS) Number |
| type | varchar(20) | NOT NULL | Type (Carcinogen, Reproductive Toxicant, Both) |
| exposure_limit | decimal(18,9) | | If applicable |
| updated_at | timestamp with time zone | NOT NULL DEFAULT now() | Last update timestamp |

**Indexes:**
- `idx_proposition_65_chemicals_name` - B-tree index on name
- `idx_proposition_65_chemicals_cas_number` - B-tree index on cas_number
- `idx_proposition_65_chemicals_type` - B-tree index on type

### Warnings
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| chemical_id | uuid | NOT NULL REFERENCES Proposition_65_Chemicals(id) | Reference to chemical |
| warning_text | text | NOT NULL | Warning text |
| last_updated | timestamp with time zone | NOT NULL DEFAULT now() | Last update timestamp |

**Indexes:**
- `idx_warnings_product_id` - B-tree index on product_id
- `idx_warnings_chemical_id` - B-tree index on chemical_id

### Product Chemical Association
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| chemical_id | uuid | NOT NULL REFERENCES Proposition_65_Chemicals(id) | Reference to chemical |
| exposure_scenario | varchar(20) | NOT NULL | Scenario (Consumer, Occupational, Environmental) |
| warning_required | boolean | NOT NULL DEFAULT false | If warning is required |
| warning_label | text | | Warning text for label |

**Indexes:**
- `idx_product_chemical_association_product_id` - B-tree index on product_id
- `idx_product_chemical_association_chemical_id` - B-tree index on chemical_id

### Hazardous Materials
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| un_number | varchar(18) | | UN/NA Number (e.g., 1993 for flammable liquids) |
| hazard_class | varchar(50) | | Hazard Classification (e.g., Flammable Liquid) |
| packing_group | varchar(10) | | Packing Group (I, II, III) |
| handling_instructions | text | | Storage or transport precautions |
| restricted_transport | varchar(20) | NOT NULL DEFAULT 'None' | Restrictions (Air, Ground, Sea, None) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_hazardous_materials_product_id` - B-tree index on product_id
- `idx_hazardous_materials_un_number` - B-tree index on un_number
- `idx_hazardous_materials_hazard_class` - B-tree index on hazard_class

## Reference Tables

### Warranties
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(100) | NOT NULL UNIQUE | Warranty name (Standard, Extended) |
| description | text | NOT NULL | Warranty coverage details |
| duration_months | integer | NOT NULL | Warranty length in months |
| terms | text | | Full warranty terms and conditions |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_warranties_name` - B-tree index on name
- `idx_warranties_duration_months` - B-tree index on duration_months

### Product Warranties
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| warranty_id | uuid | NOT NULL REFERENCES Warranties(id) | Reference to warranty |
| manufacturer_id | uuid | REFERENCES Manufacturers(id) | Optional manufacturer reference |
| start_date | timestamp with time zone | | When warranty begins |
| end_date | timestamp with time zone | | When warranty expires |
| change_reason | text | | Why warranty was changed |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |

**Indexes:**
- `idx_product_warranties_product_id` - B-tree index on product_id
- `idx_product_warranties_warranty_id` - B-tree index on warranty_id
- `idx_product_warranties_manufacturer_id` - B-tree index on manufacturer_id

### Product Country of Origin
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| country_id | uuid | NOT NULL REFERENCES Country(id) | Reference to country |
| manufacturer_id | uuid | REFERENCES Manufacturers(id) | Optional manufacturer reference |
| origin_type | varchar(20) | NOT NULL | Type (Origin, Assembly) |
| origin_order | integer | | Order for organizing countries |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_country_of_origin_product_id` - B-tree index on product_id
- `idx_product_country_of_origin_country_id` - B-tree index on country_id
- `idx_product_country_of_origin_manufacturer_id` - B-tree index on manufacturer_id

### Product Interchange
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| interchange_number | varchar(100) | NOT NULL | Part number from another brand/supplier |
| brand_id | uuid | REFERENCES Brand(id) | Optional brand reference |
| notes | text | | Optional compatibility notes |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_interchange_product_id` - B-tree index on product_id
- `idx_product_interchange_interchange_number` - B-tree index on interchange_number
- `idx_product_interchange_brand_id` - B-tree index on brand_id

### Quantity Qualifiers
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL UNIQUE | Name (Pack, Pair, Box) |
| pcdb_code | varchar(50) | | AutoCare PIES Code |
| source | varchar(20) | NOT NULL DEFAULT 'Custom' | Source (AutoCare PIES, Custom) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_quantity_qualifiers_name` - B-tree index on name
- `idx_quantity_qualifiers_pcdb_code` - B-tree index on pcdb_code

### Product Quantities
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| quantity | integer | NOT NULL | Number of units per package |
| qualifier_id | uuid | NOT NULL REFERENCES Quantity_Qualifiers(id) | Reference to qualifier |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_quantities_product_id` - B-tree index on product_id
- `idx_product_quantities_qualifier_id` - B-tree index on qualifier_id

### Sold As Types
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| name | varchar(255) | NOT NULL UNIQUE | Name (Each, Kit, Set) |
| pcdb_code | varchar(50) | | AutoCare PIES Code |
| source | varchar(20) | NOT NULL DEFAULT 'Custom' | Source (AutoCare PIES, Custom) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_sold_as_types_name` - B-tree index on name
- `idx_sold_as_types_pcdb_code` - B-tree index on pcdb_code

### Product Sold As
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| sold_as_id | uuid | NOT NULL REFERENCES Sold_As_Types(id) | Reference to sold as type |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_sold_as_product_id` - B-tree index on product_id
- `idx_product_sold_as_sold_as_id` - B-tree index on sold_as_id

### Product PCdb Mappings
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) | Reference to product |
| pcdb_codemaster_id | varchar(50) | NOT NULL | Reference to PCdb Codemaster |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_product_pcdb_mappings_product_id` - B-tree index on product_id
- `idx_product_pcdb_mappings_pcdb_codemaster_id` - B-tree index on pcdb_codemaster_id

## User and Role Management

### Users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| username | varchar(100) | NOT NULL UNIQUE | Username for authentication |
| email | varchar(255) | NOT NULL UNIQUE | User's email address |
| password_hash | varchar(255) | NOT NULL | Hashed password |
| first_name | varchar(100) | | User's first name |
| last_name | varchar(100) | | User's last name |
| is_active | boolean | NOT NULL DEFAULT true | Whether the user account is active |
| last_login | timestamp with time zone | | When the user last logged in |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |
| updated_at | timestamp with time zone | NOT NULL DEFAULT now() | Record update timestamp |

**Indexes:**
- `idx_users_username` - B-tree index on username
- `idx_users_email` - B-tree index on email
- `idx_users_is_active` - B-tree index on is_active

### Roles
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| name | varchar(50) | NOT NULL UNIQUE | Role name (Admin, Manager, Client, etc.) |
| description | text | | Description of the role |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_roles_name` - B-tree index on name

### User Roles
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| user_id | uuid | NOT NULL REFERENCES Users(id) ON DELETE CASCADE | Reference to user |
| role_id | uuid | NOT NULL REFERENCES Roles(id) ON DELETE CASCADE | Reference to role |
| assigned_at | timestamp with time zone | NOT NULL DEFAULT now() | When the role was assigned |
| assigned_by | uuid | REFERENCES Users(id) | Who assigned the role |
| UNIQUE(user_id, role_id) | | | Prevents duplicate role assignments |

**Indexes:**
- `idx_user_roles_user_id` - B-tree index on user_id
- `idx_user_roles_role_id` - B-tree index on role_id

### Permissions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| code | varchar(100) | NOT NULL UNIQUE | Permission code (e.g., "product.create") |
| name | varchar(100) | NOT NULL | Permission name (e.g., "Create Product") |
| description | text | | Description of the permission |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |

**Indexes:**
- `idx_permissions_code` - B-tree index on code

### Role Permissions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| role_id | uuid | NOT NULL REFERENCES Roles(id) ON DELETE CASCADE | Reference to role |
| permission_id | uuid | NOT NULL REFERENCES Permissions(id) ON DELETE CASCADE | Reference to permission |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |
| UNIQUE(role_id, permission_id) | | | Prevents duplicate permission assignments |

**Indexes:**
- `idx_role_permissions_role_id` - B-tree index on role_id
- `idx_role_permissions_permission_id` - B-tree index on permission_id

## Flexible Attributes System

### Attribute Definitions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| name | varchar(100) | NOT NULL | Attribute name (e.g., "Weight Capacity") |
| code | varchar(100) | NOT NULL UNIQUE | Code for the attribute (e.g., "weight_capacity") |
| description | text | | Description of the attribute |
| data_type | varchar(20) | NOT NULL | Data type (string, number, boolean, date, etc.) |
| is_required | boolean | NOT NULL DEFAULT false | Whether the attribute is required |
| default_value | text | | Default value for the attribute |
| validation_regex | text | | Regular expression for validation |
| min_value | numeric | | Minimum value (for numeric attributes) |
| max_value | numeric | | Maximum value (for numeric attributes) |
| options | jsonb | | For picklist values |
| display_order | integer | NOT NULL DEFAULT 0 | Order for displaying attributes |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |
| updated_at | timestamp with time zone | NOT NULL DEFAULT now() | Record update timestamp |

**Indexes:**
- `idx_attribute_definitions_code` - B-tree index on code
- `idx_attribute_definitions_data_type` - B-tree index on data_type
- `idx_attribute_definitions_display_order` - B-tree index on display_order

### Product Attributes
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| product_id | uuid | NOT NULL REFERENCES Products(id) ON DELETE CASCADE | Reference to product |
| attribute_id | uuid | NOT NULL REFERENCES Attribute_Definitions(id) ON DELETE CASCADE | Reference to attribute |
| value_string | text | | String value (for string, text attributes) |
| value_number | numeric | | Numeric value (for number attributes) |
| value_boolean | boolean | | Boolean value (for boolean attributes) |
| value_date | timestamp with time zone | | Date value (for date attributes) |
| value_json | jsonb | | JSON value (for complex attributes) |
| created_at | timestamp with time zone | NOT NULL DEFAULT now() | Record creation timestamp |
| updated_at | timestamp with time zone | NOT NULL DEFAULT now() | Record update timestamp |
| UNIQUE(product_id, attribute_id) | | | Prevents duplicate attributes for a product |

**Indexes:**
- `idx_product_attributes_product_id` - B-tree index on product_id
- `idx_product_attributes_attribute_id` - B-tree index on attribute_id
- `idx_product_attributes_value_string` - B-tree index on value_string
- `idx_product_attributes_value_number` - B-tree index on value_number
- `idx_product_attributes_value_boolean` - B-tree index on value_boolean
- `idx_product_attributes_value_date` - B-tree index on value_date

## Search Capabilities

The Products table includes a `search_vector` column with a GIN index for full-text search.

**Database Functions and Triggers:**

```sql
-- Function to update the search vector
CREATE FUNCTION products_search_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', coalesce(NEW.part_number, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(NEW.part_number_stripped, '')), 'A');
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

-- Trigger to update the search vector
CREATE TRIGGER products_search_vector_update
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION products_search_vector_update();
```

This search capability can be used alongside Elasticsearch or as a fallback when Elasticsearch is unavailable. The PostgreSQL-based search provides:

1. Robust full-text search capabilities with ranking
2. Support for complex queries with boolean operators
3. Language-specific stemming and stop words
4. Exact matching and fuzzy matching options
5. A reliable fallback if the external search service is unavailable

## Audit Logging

### Audit Logs
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY DEFAULT gen_random_uuid() | Unique identifier |
| table_name | varchar(100) | NOT NULL | Name of the table being audited |
| record_id | uuid | NOT NULL | ID of the record being audited |
| action | varchar(20) | NOT NULL | Action performed (INSERT, UPDATE, DELETE) |
| changed_by | uuid | REFERENCES Users(id) | User who made the change |
| changed_at | timestamp with time zone | NOT NULL DEFAULT now() | When the change occurred |
| old_values | jsonb | | Previous values before change |
| new_values | jsonb | | New values after change |
| ip_address | inet | | IP address of the client |
| user_agent | text | | User agent of the client |

**Indexes:**
- `idx_audit_logs_table_name_record_id` - B-tree index on (table_name, record_id)
- `idx_audit_logs_changed_at` - B-tree index on changed_at
- `idx_audit_logs_changed_by` - B-tree index on changed_by
- `idx_audit_logs_action` - B-tree index on action

**Database Functions and Triggers:**

```sql
-- Function to handle audit logging
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
DECLARE
    audit_row audit_logs;
    include_values boolean;
    log_old_values jsonb;
    log_new_values jsonb;
    excluded_cols text[] = ARRAY['updated_at', 'search_vector']; -- columns to exclude
BEGIN
    IF TG_WHEN <> 'AFTER' THEN
        RAISE EXCEPTION 'audit_trigger_function() may only run as an AFTER trigger';
    END IF;

    -- Get user ID from current_setting if available (set by your application)
    audit_row.changed_by = (SELECT nullif(current_setting('app.current_user_id', TRUE), '')::uuid);
    audit_row.table_name = TG_TABLE_NAME::text;

    -- Determine operation type
    CASE TG_OP
        WHEN 'INSERT' THEN
            audit_row.action = 'INSERT';
            audit_row.record_id = NEW.id;
            audit_row.new_values = row_to_json(NEW)::jsonb - excluded_cols;
            audit_row.old_values = null;
        WHEN 'UPDATE' THEN
            audit_row.action = 'UPDATE';
            audit_row.record_id = NEW.id;
            audit_row.old_values = row_to_json(OLD)::jsonb - excluded_cols;
            audit_row.new_values = row_to_json(NEW)::jsonb - excluded_cols;
        WHEN 'DELETE' THEN
            audit_row.action = 'DELETE';
            audit_row.record_id = OLD.id;
            audit_row.old_values = row_to_json(OLD)::jsonb - excluded_cols;
            audit_row.new_values = null;
        ELSE
            RAISE EXCEPTION '[audit_trigger_function] - Trigger action % not supported', TG_OP;
    END CASE;

    -- Get client IP and user agent if set by application
    audit_row.ip_address = inet(nullif(current_setting('app.client_ip', TRUE), '')::text);
    audit_row.user_agent = nullif(current_setting('app.user_agent', TRUE), '');

    -- Insert the audit log
    INSERT INTO audit_logs (
        table_name, record_id, action, changed_by, changed_at,
        old_values, new_values, ip_address, user_agent
    ) VALUES (
        audit_row.table_name, audit_row.record_id, audit_row.action, audit_row.changed_by, now(),
        audit_row.old_values, audit_row.new_values, audit_row.ip_address, audit_row.user_agent
    );

    RETURN NULL; -- result is ignored since this is an AFTER trigger
END;
$$ LANGUAGE plpgsql;
```

This audit logging system provides:

1. Comprehensive change tracking for all critical tables
2. Both old and new values for each change
3. Information about who made the change and when
4. Client context information (IP, user agent)
5. Efficient querying for audit history by table, record, or user
