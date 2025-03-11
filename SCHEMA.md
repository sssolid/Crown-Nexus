Products
├── id (PK)
├── part_number                 -- Unique identifier for the product (e.g., “PN12345”)
├── part_number_stripped        -- Only A-Z, 0-9 version of part_number
├── old_number                  -- Legacy part number
├── supersession_number         -- Number that supersedes the part
├── brand_id                    -- FK to Brands table
├── group_id                    -- FK to Product_Groups table
├── category_id                 -- FK to Categories table
├── subcategory_id              -- FK to Subcategories table
├── tertiary_category_id        -- FK to Tertiary_Categories table
├── application                 -- Blob/text data for vehicle fitment applications
├── length                      -- In inches
├── width                       -- In inches
├── height                      -- In inches
├── weight                      -- In pounds
├── dimensional_weight          -- Calculated dimensional weight
├── jobber_price                -- In USD
├── export_price                -- In USD
├── msrp                        -- In USD
├── warranty                    -- In months
├── additional_shipping         -- Boolean flag: requires additional shipping charges?
├── hazardous_material          -- Boolean flag
├── proposition_65            -- Boolean flag for requiring Prop 65 warning
├── proposition_65_chemicals    -- Text list of chemicals (if any)
├── proposition_65_type_id      -- FK to Proposition_65_Types table
├── msds_file_id                -- FK to Files table (for Material Safety Data Sheet)
├── upc                         -- 12-character UPC (with check digit)
├── tariff_code                 -- 10-digit code
├── part_terminology_id         -- FK/external reference (from PCDB)
├── quantity_qualifier          -- Enum or text (e.g., NOR, MAX)
├── unspsc_code                 -- UNSPSC code
├── packaging_id                -- FK to Packaging table (box, loose, etc.)
├── quantity_required           -- Quantity per vehicle fitment
├── quantity_in_package         -- Quantity included in the package
├── sold_as                     -- Enum/text (each, kit, set)
├── vintage                     -- Boolean flag: vintage fitments
├── late_model                  -- Boolean flag: late model fitments
├── soft                        -- Boolean flag: soft good?
├── universal                   -- Boolean flag: universal fit?
├── dot_approved                -- Boolean flag: DOT approved?
├── active                      -- Boolean flag: active product?
├── date_created                -- Timestamp (with time zone)
└── date_modified               -- Timestamp (with time zone)

Product_Description_Types
├── id (PK)
├── description_type       -- Name (e.g., "Long Jeep", "Short", "Bullet", "Keyword", etc.)
└── max_length             -- Maximum character count for this type

Product_Country_Origins
├── id (PK)
├── product_id             -- FK to Products table
├── country_id             -- FK to Countries table
└── assembled              -- Boolean flag (if product was assembled in that country)

Countries
├── id (PK)
├── name                   -- Full country name
├── iso2                   -- 2-letter code
├── iso3                   -- 3-letter code
└── [additional fields]    -- Other country-specific info

Product_Colors
├── id (PK)
├── product_id             -- FK to Products table
└── color_id               -- FK to Colors table

Colors
├── id (PK)
├── name                   -- Color name (e.g., "Red")
└── hex                    -- Hexadecimal code (e.g., "#FF0000")

Product_Constructions
├── id (PK)
├── product_id             -- FK to Products table
└── construction_id        -- FK to Constructions table

Constructions
├── id (PK)
└── name                   -- Construction type (e.g., “Stamped”, “Forged”)

Product_Textures
├── id (PK)
├── product_id             -- FK to Products table
└── texture_id             -- FK to Textures table

Textures
├── id (PK)
└── name                   -- Texture name (e.g., “Smooth”, “Rough”)

Product_Interchanges
├── id (PK)
├── product_id             -- FK to Products table (primary product)
└── interchangeable_part   -- The interchangeable part number or FK to Products (if self-referencing)

Brands
├── id (PK)
└── name                   -- Brand name

Product_Groups
├── id (PK)
└── name                   -- Group name

Categories
├── id (PK)
└── name                   -- Category name

Subcategories
├── id (PK)
└── name                   -- Subcategory name

Tertiary_Categories
├── id (PK)
└── name                   -- Tertiary category name

Packaging
├── id (PK)
└── type                   -- Packaging type (e.g., “Box”, “Loose”)

Proposition_65_Types
├── id (PK)
└── type_description       -- Details on the type of Prop 65 warning

Files
├── id (PK)
├── file_path              -- Path or reference to the file storage
├── file_type              -- e.g., "PDF", "DOCX", etc.
└── description            -- Optional file description
