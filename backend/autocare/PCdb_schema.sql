-- Table PCADB.Alias
CREATE TABLE IF NOT EXISTS "Alias" (
  "AliasID" INT PRIMARY KEY,
  "AliasName" VARCHAR(100) NOT NULL
);

-- Table PCADB.Categories
CREATE TABLE IF NOT EXISTS "Categories" (
  "CategoryID" INT PRIMARY KEY,
  "CategoryName" VARCHAR(500) NOT NULL
);

-- Table PCADB.Subcategories
CREATE TABLE IF NOT EXISTS "Subcategories" (
  "SubCategoryID" INT PRIMARY KEY,
  "SubCategoryName" VARCHAR(500) NOT NULL
);

-- Table PCADB.Positions
CREATE TABLE IF NOT EXISTS "Positions" (
  "PositionID" INT PRIMARY KEY,
  "Position" VARCHAR(500) NOT NULL
);

-- Table PCADB.Use
CREATE TABLE IF NOT EXISTS "Use" (
  "UseID" INT PRIMARY KEY,
  "UseDescription" VARCHAR(500) NOT NULL
);

-- Table PCADB.PartsDescription
CREATE TABLE IF NOT EXISTS "PartsDescription" (
  "PartsDescriptionID" INT PRIMARY KEY,
  "PartsDescription" VARCHAR(1000) NOT NULL
);

-- Table PCADB.Parts
CREATE TABLE IF NOT EXISTS "Parts" (
  "PartTerminologyID" INT PRIMARY KEY,
  "PartTerminologyName" VARCHAR(500) NOT NULL,
  "PartsDescriptionID" INT,
  "RevDate" DATE,
  FOREIGN KEY ("PartsDescriptionID") REFERENCES "PartsDescription" ("PartsDescriptionID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Table PCADB.PartsToAlias
CREATE TABLE IF NOT EXISTS "PartsToAlias" (
  "PartTerminologyID" INT NOT NULL,
  "AliasID" INT NOT NULL,
  PRIMARY KEY ("PartTerminologyID", "AliasID"),
  FOREIGN KEY ("PartTerminologyID") REFERENCES "Parts" ("PartTerminologyID"),
  FOREIGN KEY ("AliasID") REFERENCES "Alias" ("AliasID")
);

-- Table PCADB.PartsRelationship
CREATE TABLE IF NOT EXISTS "PartsRelationship" (
  "PartTerminologyID" INT NOT NULL,
  "RelatedPartTerminologyID" INT NOT NULL,
  PRIMARY KEY ("PartTerminologyID", "RelatedPartTerminologyID"),
  FOREIGN KEY ("PartTerminologyID") REFERENCES "Parts" ("PartTerminologyID"),
  FOREIGN KEY ("RelatedPartTerminologyID") REFERENCES "Parts" ("PartTerminologyID")
);

-- Table PCADB.PartsToUse
CREATE TABLE IF NOT EXISTS "PartsToUse" (
  "PartTerminologyID" INT NOT NULL,
  "UseID" INT NOT NULL,
  PRIMARY KEY ("PartTerminologyID", "UseID"),
  FOREIGN KEY ("PartTerminologyID") REFERENCES "Parts" ("PartTerminologyID"),
  FOREIGN KEY ("UseID") REFERENCES "Use" ("UseID")
);

-- Table PCADB.CodeMaster
CREATE TABLE IF NOT EXISTS "CodeMaster" (
  "CodeMasterID" INT PRIMARY KEY,
  "PartTerminologyID" INT NOT NULL,
  "CategoryID" INT NOT NULL,
  "SubCategoryID" INT NOT NULL,
  "PositionID" INT NOT NULL,
  "RevDate" DATE,
  FOREIGN KEY ("PartTerminologyID") REFERENCES "Parts" ("PartTerminologyID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("PositionID") REFERENCES "Positions" ("PositionID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("CategoryID") REFERENCES "Categories" ("CategoryID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("SubCategoryID") REFERENCES "Subcategories" ("SubCategoryID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Table PCADB.ChangeLogTables
CREATE TABLE "ChangeAttributeStates" (
  "ChangeAttributeStateID" INT PRIMARY KEY,
  "ChangeAttributeState" VARCHAR(255) NOT NULL
);

CREATE TABLE "ChangeReasons" (
  "ChangeReasonID" INT PRIMARY KEY,
  "ChangeReason" VARCHAR(255) NOT NULL
);

CREATE TABLE "ChangeTableNames" (
  "TableNameID" INT PRIMARY KEY,
  "TableName" VARCHAR(255) NOT NULL,
  "TableDescription" VARCHAR(1000)
);

CREATE TABLE "Changes" (
  "ChangeID" INT PRIMARY KEY,
  "RequestID" INT NOT NULL,
  "ChangeReasonID" INT NOT NULL,
  "RevDate" TIMESTAMP,
  FOREIGN KEY ("ChangeReasonID") REFERENCES "ChangeReasons" ("ChangeReasonID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE "ChangeDetails" (
  "ChangeDetailID" INT PRIMARY KEY,
  "ChangeID" INT NOT NULL,
  "ChangeAttributeStateID" INT NOT NULL,
  "TableNameID" INT NOT NULL,
  "PrimaryKeyColumnName" VARCHAR(255),
  "PrimaryKeyBefore" INT,
  "PrimaryKeyAfter" INT,
  "ColumnName" VARCHAR(255),
  "ColumnValueBefore" VARCHAR(1000),
  "ColumnValueAfter" VARCHAR(1000),
  FOREIGN KEY ("ChangeID") REFERENCES "Changes" ("ChangeID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("ChangeAttributeStateID") REFERENCES "ChangeAttributeStates" ("ChangeAttributeStateID") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("TableNameID") REFERENCES "ChangeTableNames" ("TableNameID") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Table PCADB.PartsSupersession
CREATE TABLE IF NOT EXISTS "PartsSupersession" (
  "OldPartTerminologyID" INT NOT NULL,
  "OldPartTerminologyName" VARCHAR(200) NOT NULL,
  "NewPartTerminologyID" INT NOT NULL,
  "NewPartTerminologyName" VARCHAR(200) NOT NULL,
  "RevDate" DATE,
  PRIMARY KEY ("OldPartTerminologyID", "NewPartTerminologyID")
);

-- Table PCADB.Version
CREATE TABLE IF NOT EXISTS "Version" (
  "VersionDate" TIMESTAMP
);

-- Table PCADB.PIESCode
CREATE TABLE IF NOT EXISTS "PIESCode" (
  "PIESCodeId" INT PRIMARY KEY,
  "CodeValue" VARCHAR(500) NOT NULL,
  "CodeFormat" VARCHAR(500) NOT NULL,
  "FieldFormat" VARCHAR(500),
  "CodeDescription" VARCHAR(500) NOT NULL,
  "Source" VARCHAR(500)
);

-- Table PCADB.PIESExpiGroup
CREATE TABLE IF NOT EXISTS "PIESExpiGroup" (
  "PIESExpiGroupId" INT PRIMARY KEY,
  "ExpiGroupCode" VARCHAR(500) NOT NULL,
  "ExpiGroupDescription" VARCHAR(500) NOT NULL
);

-- Table PCADB.PIESExpiCode
CREATE TABLE IF NOT EXISTS "PIESExpiCode" (
  "PIESExpiCodeId" INT PRIMARY KEY,
  "ExpiCode" VARCHAR(100) NOT NULL,
  "ExpiCodeDescription" VARCHAR(500) NOT NULL,
  "PIESExpiGroupId" INT NOT NULL,
  FOREIGN KEY ("PIESExpiGroupId") REFERENCES "PIESExpiGroup" ("PIESExpiGroupId") ON DELETE CASCADE
);

-- Table PCADB.PIESSegment
CREATE TABLE IF NOT EXISTS "PIESSegment" (
  "PIESSegmentId" INT PRIMARY KEY,
  "SegmentAbb" VARCHAR(100) NOT NULL,
  "SegmentName" VARCHAR(100) NOT NULL,
  "SegmentDescription" VARCHAR(250) NOT NULL
);

-- Table PCADB.PIESField
CREATE TABLE IF NOT EXISTS "PIESField" (
  "PIESFieldId" INT PRIMARY KEY,
  "FieldName" VARCHAR(500) NOT NULL,
  "ReferenceFieldNumber" VARCHAR(500) NOT NULL,
  "PIESSegmentId" INT NOT NULL,
  FOREIGN KEY ("PIESSegmentId") REFERENCES "PIESSegment" ("PIESSegmentId") ON DELETE CASCADE
);

-- Table PCADB.PIESReferenceFieldCode
CREATE TABLE IF NOT EXISTS "PIESReferenceFieldCode" (
  "PIESReferenceFieldCodeId" INT PRIMARY KEY,
  "PIESFieldId" INT NOT NULL,
  "PIESCodeId" INT NOT NULL,
  "PIESExpiCodeId" INT,
  "ReferenceNotes" varchar(2000),
  FOREIGN KEY ("PIESCodeId") REFERENCES "PIESCode" ("PIESCodeId") ON DELETE CASCADE,
  FOREIGN KEY ("PIESExpiCodeId") REFERENCES "PIESExpiCode" ("PIESExpiCodeId") ON DELETE CASCADE,
  FOREIGN KEY ("PIESFieldId") REFERENCES "PIESField" ("PIESFieldId") ON DELETE CASCADE
);

-- Table PCADB.ACESCodedValues
CREATE TABLE IF NOT EXISTS "ACESCodedValues" (
  "Element" varchar(255),
  "Attribute" varchar(255),
  "CodedValue" varchar(255),
  "CodeDescription" varchar(255)
);
