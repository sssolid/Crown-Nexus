-- ----------------------------------------------------------------------------
-- Table PCADB.MetaData
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "MetaData" (
  "MetaID" INT PRIMARY KEY,
  "MetaName" VARCHAR(80) NULL,
  "MetaDescr" VARCHAR(512) NULL,
  "MetaFormat" VARCHAR(10) NULL,
  "DataType" VARCHAR(50) NULL,
  "MinLength" INT NULL,
  "MaxLength" INT NULL
);

-- ----------------------------------------------------------------------------
-- Table PCADB.MeasurementGroup
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "MeasurementGroup" (
  "MeasurementGroupID" INT PRIMARY KEY,
  "MeasurementGroupName" VARCHAR(80) NULL
);

-- ----------------------------------------------------------------------------
-- Table PCADB.MetaUOMCodes
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "MetaUOMCodes" (
  "MetaUOMID" INT PRIMARY KEY,
  "UOMCode" VARCHAR(10) NULL,
  "UOMDescription" VARCHAR(512) NULL,
  "UOMLabel" VARCHAR(10) NULL,
  "MeasurementGroupID" INT NOT NULL,
  FOREIGN KEY ("MeasurementGroupID") REFERENCES "MeasurementGroup" ("MeasurementGroupID")
);

-- ----------------------------------------------------------------------------
-- Table PCADB.MetaUOMCodeAssignment
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "MetaUOMCodeAssignment" (
  "MetaUOMCodeAssignmentID" INT PRIMARY KEY,
  "PAPTID" INT NOT NULL,
  "MetaUOMID" INT NOT NULL,
  FOREIGN KEY ("MetaUOMID") REFERENCES "MetaUOMCodes" ("MetaUOMID")
);

-- ----------------------------------------------------------------------------
-- Table PCADB.PartAttributes
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "PartAttributes" (
  "PAID" INT PRIMARY KEY,
  "PAName" VARCHAR(80) NULL,
  "PADescr" VARCHAR(512) NULL
);

-- ----------------------------------------------------------------------------
-- Table PCADB.PartAttributeAssignment
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "PartAttributeAssignment" (
  "PAPTID" INT PRIMARY KEY,
  "PartTerminologyID" INT NOT NULL,
  "PAID" INT NOT NULL,
  "MetaID" INT NOT NULL,
  FOREIGN KEY ("PAID") REFERENCES "PartAttributes" ("PAID"),
  FOREIGN KEY ("MetaID") REFERENCES "MetaData" ("MetaID")
);

-- --------------------------------------------------------------------------
-- Table PCADB.Version
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "Version" (
  "PAdbVersion" VARCHAR(10) NULL,
  "PAdbPublication" DATE NULL,
  "PCdbPublication" DATE NULL
);

-- --------------------------------------------------------------------------
-- Table PCADB.PartAttributeStyle
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "PartAttributeStyle" (
  "StyleID" INT NULL,
  "PAPTID" INT NULL,
  FOREIGN KEY ("PAPTID") REFERENCES "PartAttributeAssignment" ("PAPTID")
);

-- --------------------------------------------------------------------------
-- Table PCADB.PartTypeStyle
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "PartTypeStyle" (
  "StyleID" INT NULL,
  "PartTerminologyID" INT NULL
);

-- --------------------------------------------------------------------------
-- Table PCADB.Style
-- --------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "Style" (
  "StyleID" INT NULL,
  "StyleName" VARCHAR(225) NULL
);

-- ----------------------------------------------------------------------------
-- Table PCADB.ValidValues
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "ValidValues" (
  "ValidValueID" INT PRIMARY KEY,
  "ValidValue" VARCHAR(100) NOT NULL
);

-- ----------------------------------------------------------------------------
-- Table PCADB.ValidValueAssignment
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "ValidValueAssignment" (
  "ValidValueAssignmentID" INT PRIMARY KEY,
  "PAPTID" INT NOT NULL,
  "ValidValueID" INT NOT NULL,
  FOREIGN KEY ("ValidValueID") REFERENCES "ValidValues" ("ValidValueID")
);
