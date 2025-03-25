-- Table ACESCodedValues
CREATE TABLE "ACESCodedValues" (
    "Element" VARCHAR(255) NULL,
    "Attribute" VARCHAR(255) NULL,
    "CodedValue" VARCHAR(255) NULL,
    "CodeDescription" VARCHAR(255) NULL
);

-- Table Alias
CREATE TABLE "Alias" (
    "AliasID" INT NOT NULL,
    "AliasName" VARCHAR(100) NOT NULL,
    PRIMARY KEY ("AliasID")
);

-- Table Categories
CREATE TABLE "Categories" (
    "CategoryID" INT NOT NULL,
    "CategoryName" VARCHAR(100) NOT NULL,
    PRIMARY KEY ("CategoryID")
);

-- Table ChangeAttributeStates
CREATE TABLE "ChangeAttributeStates" (
    "ChangeAttributeStateID" INT NOT NULL,
    "ChangeAttributeState" VARCHAR(255) NOT NULL,
    PRIMARY KEY ("ChangeAttributeStateID")
);

-- Table ChangeDetails
CREATE TABLE "ChangeDetails" (
    "ChangeDetailID" INT  NOT NULL,
    "ChangeID" INT NOT NULL,
    "ChangeAttributeStateID" INT NOT NULL,
    "TableNameID" INT NOT NULL,
    "PrimaryKeyColumnName" VARCHAR(255) NULL,
    "PrimaryKeyBefore" INT NULL,
    "PrimaryKeyAfter" INT NULL,
    "ColumnName" VARCHAR(255) NULL,
    "ColumnValueBefore" VARCHAR(1000) NULL,
    "ColumnValueAfter" VARCHAR(1000) NULL,
    PRIMARY KEY ("ChangeDetailID")
);

-- Table ChangeReasons
CREATE TABLE "ChangeReasons" (
    "ChangeReasonID" INT NOT NULL,
    "ChangeReason" VARCHAR(255) NOT NULL,
    PRIMARY KEY ("ChangeReasonID")
);

-- Table Changes
CREATE TABLE "Changes" (
    "ChangeID" INT  NOT NULL,
    "RequestID" INT NOT NULL,
    "ChangeReasonID" INT NOT NULL,
    "RevDate" TIMESTAMP NULL,
    PRIMARY KEY ("ChangeID")
);

-- Table ChangeTableNames
CREATE TABLE "ChangeTableNames" (
    "TableNameID" INT NOT NULL,
    "TableName" VARCHAR(255) NOT NULL,
    "TableDescription" VARCHAR(1000) NULL,
    PRIMARY KEY ("TableNameID")
);

-- Table CodeMaster
CREATE TABLE "CodeMaster" (
    "CodeMasterID" INT NOT NULL,
    "PartTerminologyID" INT NOT NULL,
    "CategoryID" INT NOT NULL,
    "SubCategoryID" INT NOT NULL,
    "PositionID" INT NOT NULL,
    "RevDate" DATE NOT NULL,
    PRIMARY KEY ("CodeMasterID")
);

-- Table DatabaseType
CREATE TABLE "DatabaseType" (
    "DatabaseTypeId" INT  NOT NULL,
    "DatabaseTypeName" VARCHAR(100) NOT NULL
);

-- Table MeasurementGroup
CREATE TABLE "MeasurementGroup" (
    "MeasurementGroupID" INT NOT NULL,
    "MeasurementGroupName" VARCHAR(80) NULL,
    PRIMARY KEY ("MeasurementGroupID")
);

-- Table MetaData
CREATE TABLE "MetaData" (
    "MetaID" INT NOT NULL,
    "MetaName" VARCHAR(80) NULL,
    "MetaDescr" VARCHAR(512) NULL,
    "MetaFormat" VARCHAR(10) NULL,
    "DataType" VARCHAR(50) NULL,
    "MinLength" INT NULL,
    "MaxLength" INT NULL,
    PRIMARY KEY ("MetaID")
);

-- Table MetaUomCodeAssignment
CREATE TABLE "MetaUomCodeAssignment" (
    "MetaUomCodeAssignmentID" INT  NOT NULL,
    "PAPTID" INT NOT NULL,
    "MetaUomID" INT NOT NULL,
    PRIMARY KEY ("MetaUomCodeAssignmentID")
);

-- Table MetaUOMCodes
CREATE TABLE "MetaUOMCodes" (
    "MetaUOMID" INT NOT NULL,
    "UOMCode" VARCHAR(10) NULL,
    "UOMDescription" VARCHAR(512) NULL,
    "UOMLabel" VARCHAR(10) NULL,
    "MeasurementGroupId" INT NOT NULL,
    PRIMARY KEY ("MetaUOMID")
);

-- Table PartAttributeAssignment
CREATE TABLE "PartAttributeAssignment" (
    "ID" INT  NOT NULL,
    "PAPTID" INT NOT NULL,
    "PartTerminologyID" INT NOT NULL,
    "PAID" INT NOT NULL,
    "MetaID" INT NOT NULL,
    PRIMARY KEY ("PAPTID")
);

-- Table PartAttributes
CREATE TABLE "PartAttributes" (
    "PAID" INT NOT NULL,
    "PAName" VARCHAR(80) NULL,
    "PADescr" VARCHAR(512) NULL,
    PRIMARY KEY ("PAID")
);

-- Table PartAttributeStyle
CREATE TABLE "PartAttributeStyle" (
    "StyleID" INT NULL,
    "PAPTID" INT NULL
);

-- Table PartCategory
CREATE TABLE "PartCategory" (
    "PartCategoryID" INT  NOT NULL,
    "PartTerminologyID" INT NOT NULL,
    "SubCategoryID" INT NOT NULL,
    "CategoryID" INT NOT NULL,
    PRIMARY KEY ("PartCategoryID")
);

-- Table PartPosition
CREATE TABLE "PartPosition" (
    "PartPositionID" INT  NOT NULL,
    "PartTerminologyID" INT NOT NULL,
    "PositionID" INT NOT NULL,
    "RevDate" DATE NULL,
    PRIMARY KEY ("PartPositionID")
);

-- Table Parts
CREATE TABLE "Parts" (
    "PartTerminologyID" INT NOT NULL,
    "PartTerminologyName" VARCHAR(500) NOT NULL,
    "PartsDescriptionID" INT NULL,
    "RevDate" DATE NULL,
    PRIMARY KEY ("PartTerminologyID")
);

-- Table PartsDescription
CREATE TABLE "PartsDescription" (
    "PartsDescriptionID" INT NOT NULL,
    "PartsDescription" VARCHAR(500) NOT NULL,
    PRIMARY KEY ("PartsDescriptionID")
);

-- Table PartsRelationship
CREATE TABLE "PartsRelationship" (
    "PartTerminologyID" INT NOT NULL,
    "RelatedPartTerminologyID" INT NOT NULL
);

-- Table PartsSupersession
CREATE TABLE "PartsSupersession" (
    "PartsSupersessionId" INT NOT NULL,
    "OldPartTerminologyID" INT NOT NULL,
    "OldPartTerminologyName" VARCHAR(256) NOT NULL,
    "NewPartTerminologyID" INT NOT NULL,
    "NewPartTerminologyName" VARCHAR(256) NOT NULL,
    "RevDate" DATE NULL,
    "Note" VARCHAR(1000) NULL
);

-- Table PartsToAlias
CREATE TABLE "PartsToAlias" (
    "PartTerminologyID" INT NOT NULL,
    "AliasID" INT NOT NULL
);

-- Table PartsToUse
CREATE TABLE "PartsToUse" (
    "PartTerminologyID" INT NOT NULL,
    "UseID" INT NOT NULL
);

-- Table PartTypeStyle
CREATE TABLE "PartTypeStyle" (
    "StyleID" INT NULL,
    "PartTerminologyID" INT NULL
);

-- Table PIESCode
CREATE TABLE "PIESCode" (
    "PIESCodeId" INT NOT NULL,
    "CodeValue" VARCHAR(255) NOT NULL,
    "CodeFormat" VARCHAR(255) NOT NULL,
    "FieldFormat" VARCHAR(255) NULL,
    "CodeDescription" VARCHAR(255) NOT NULL,
    "Source" VARCHAR(255) NULL,
    PRIMARY KEY ("PIESCodeId")
);

-- Table PIESExpiCode
CREATE TABLE "PIESExpiCode" (
    "PIESExpiCodeId" INT NOT NULL,
    "ExpiCode" VARCHAR(50) NOT NULL,
    "ExpiCodeDescription" VARCHAR(255) NOT NULL,
    "PIESExpiGroupId" INT NOT NULL,
    PRIMARY KEY ("PIESExpiCodeId")
);

-- Table PIESExpiGroup
CREATE TABLE "PIESExpiGroup" (
    "PIESExpiGroupId" INT NOT NULL,
    "ExpiGroupCode" VARCHAR(255) NOT NULL,
    ExpiGroupDescription VARCHAR(255) NOT NULL,
    PRIMARY KEY ("PIESExpiGroupId")
);

-- Table PIESField
CREATE TABLE "PIESField" (
    "PIESFieldId" INT NOT NULL,
    "FieldName" VARCHAR(255) NOT NULL,
    "ReferenceFieldNumber" VARCHAR(255) NOT NULL,
    "PIESSegmentId" INT NOT NULL,
    PRIMARY KEY ("PIESFieldId")
);

-- Table PIESReferenceFieldCode
CREATE TABLE "PIESReferenceFieldCode" (
    "PIESReferenceFieldCodeId" INT NOT NULL,
    "PIESFieldId" INT NOT NULL,
    "PIESCodeId" INT NOT NULL,
    "PIESExpiCodeId" INT NULL,
    "ReferenceNotes" VARCHAR(2000) NULL,
    PRIMARY KEY ("PIESReferenceFieldCodeId")
);

-- Table PIESSegment
CREATE TABLE "PIESSegment" (
    "PIESSegmentId" INT NOT NULL,
    "SegmentAbb" VARCHAR(50) NOT NULL,
    "SegmentName" VARCHAR(50) NOT NULL,
    "SegmentDescription" VARCHAR(250) NOT NULL,
    PRIMARY KEY ("PIESSegmentId")
);

-- Table Positions
CREATE TABLE "Positions" (
    "PositionID" INT NOT NULL,
    "Position" VARCHAR(500) NOT NULL,
    PRIMARY KEY ("PositionID")
);

-- Table Style
CREATE TABLE "Style" (
    "StyleID" INT NULL,
    "StyleName" VARCHAR(225) NULL
);

-- Table Subcategories
CREATE TABLE "Subcategories" (
    "SubCategoryID" INT NOT NULL,
    "SubCategoryName" VARCHAR(100) NOT NULL,
    PRIMARY KEY ("SubCategoryID")
);

-- Table TaskController
CREATE TABLE "TaskController" (
    "Id" INT  NOT NULL,
    "Comment" VARCHAR(8000) NOT NULL,
    "RequestedBy" VARCHAR(50) NOT NULL,
    "ReceivedDate" Timestamp NOT NULL,
    "Status" SMALLINT NOT NULL,
    "FileName" VARCHAR(512) NOT NULL,
    "AzureContainerName" VARCHAR(100) NOT NULL,
    "DirectoryPath" VARCHAR(1024) NOT NULL,
    "ContentType" VARCHAR(255) NOT NULL,
    "FileSize" BIGINT NOT NULL,
    "StepCompleted" SMALLINT NOT NULL,
    "Completed" VARCHAR(500) NULL,
    "ImportType" SMALLINT NOT NULL,
    "Skipped" VARCHAR(500) NULL,
    "Confirmed" VARCHAR(500) NULL
);

-- Table Use
CREATE TABLE "Use" (
    "UseID" INT NOT NULL,
    "UseDescription" VARCHAR(100) NOT NULL,
    PRIMARY KEY ("UseID")
);

-- Table ValidValueAssignment
CREATE TABLE "ValidValueAssignment" (
    "ValidValueAssignmentID" INT  NOT NULL,
    "PAPTID" INT NOT NULL,
    "ValidValueID" INT NOT NULL,
    PRIMARY KEY ("ValidValueAssignmentID")
);

-- Table ValidValues
CREATE TABLE "ValidValues" (
    "ValidValueID" INT NOT NULL,
    "ValidValue" VARCHAR(500) NOT NULL,
    PRIMARY KEY ("ValidValueID")
);

-- Table VersionInfo
CREATE TABLE "Version" (
    "VersionDate" Timestamp NOT NULL
);


ALTER TABLE "ChangeDetails" 
ADD CONSTRAINT "FK_ChangeDetails_ChangeAttributeStates_ChangeAttributeStateID" 
FOREIGN KEY ("ChangeAttributeStateID") 
REFERENCES "ChangeAttributeStates" ("ChangeAttributeStateID");

ALTER TABLE "ChangeDetails" 
ADD CONSTRAINT "FK_ChangeDetails_Changes_ChangeID" 
FOREIGN KEY ("ChangeID") 
REFERENCES "Changes" ("ChangeID");

ALTER TABLE "ChangeDetails" 
ADD CONSTRAINT "FK_ChangeDetails_ChangeTableNames_TableNameID" 
FOREIGN KEY ("TableNameID") 
REFERENCES "ChangeTableNames" ("TableNameID");

ALTER TABLE "Changes" 
ADD CONSTRAINT "FK_Changes_ChangeReasons_ChangeReasonID" 
FOREIGN KEY ("ChangeReasonID") 
REFERENCES "ChangeReasons" ("ChangeReasonID");

ALTER TABLE "CodeMaster" 
ADD CONSTRAINT "FK_CodeMaster_Categories" 
FOREIGN KEY ("CategoryID") 
REFERENCES "Categories" ("CategoryID");

ALTER TABLE "CodeMaster" 
ADD CONSTRAINT "FK_CodeMaster_Parts" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID");

ALTER TABLE "CodeMaster" 
ADD CONSTRAINT "FK_CodeMaster_Positions" 
FOREIGN KEY ("PositionID") 
REFERENCES "Positions" ("PositionID");

ALTER TABLE "CodeMaster" 
ADD CONSTRAINT "FK_CodeMaster_Subcategories" 
FOREIGN KEY ("SubCategoryID") 
REFERENCES "Subcategories" ("SubCategoryID");

ALTER TABLE "MetaUomCodeAssignment" 
ADD CONSTRAINT "FKMetaUOMCodeAssignmentMetaUOMCodesMetaUOMID" 
FOREIGN KEY ("MetaUomID") 
REFERENCES "MetaUOMCodes" ("MetaUOMID") 
ON DELETE CASCADE;

ALTER TABLE "MetaUomCodeAssignment" 
ADD CONSTRAINT "FKMetaUOMCodeAssignmentPartAttributeAssignmentPAPTID" 
FOREIGN KEY ("PAPTID") 
REFERENCES "PartAttributeAssignment" ("PAPTID") 
ON DELETE CASCADE;

ALTER TABLE "MetaUOMCodes" 
ADD CONSTRAINT "FKMetaUOMCodesMeasurementGroupMeasurementGroupId" 
FOREIGN KEY ("MeasurementGroupId") 
REFERENCES "MeasurementGroup" ("MeasurementGroupID");

ALTER TABLE "PartAttributeAssignment" 
ADD CONSTRAINT "FKPartAttributeAssignmentMetaDataMetaID" 
FOREIGN KEY ("MetaID") 
REFERENCES "MetaData" ("MetaID") 
ON DELETE CASCADE;

ALTER TABLE "PartAttributeAssignment" 
ADD CONSTRAINT "FKPartAttributeAssignmentPartAttributesPAID" 
FOREIGN KEY ("PAID") 
REFERENCES "PartAttributes" ("PAID") 
ON DELETE CASCADE;

ALTER TABLE "PartAttributeAssignment" 
ADD CONSTRAINT "FKPartAttributeAssignmentPartsPartTerminologyID" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID") 
ON DELETE CASCADE;

ALTER TABLE "PartCategory" 
ADD CONSTRAINT "FKPartCategoryCategoriesCategoryID" 
FOREIGN KEY ("CategoryID") 
REFERENCES "Categories" ("CategoryID");

ALTER TABLE "PartCategory" 
ADD CONSTRAINT "FKPartCategoryPartsPartTerminologyID" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID");

ALTER TABLE "PartCategory" 
ADD CONSTRAINT "FKPartCategorySubcategoriesSubCategoryID" 
FOREIGN KEY ("SubCategoryID") 
REFERENCES "Subcategories" ("SubCategoryID");

ALTER TABLE "PartPosition" 
ADD CONSTRAINT "FKCodeMasterPartsPartTerminologyID" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID");

ALTER TABLE "PartPosition" 
ADD CONSTRAINT "FKCodeMasterPositionsPositionID" 
FOREIGN KEY ("PositionID") 
REFERENCES "Positions" ("PositionID");

ALTER TABLE "Parts" 
ADD CONSTRAINT "FKPartsPartsDescriptionPartsDescriptionId" 
FOREIGN KEY ("PartsDescriptionID") 
REFERENCES "PartsDescription" ("PartsDescriptionID");

ALTER TABLE "PartsRelationship" 
ADD CONSTRAINT "FKPartsRelationshipPartsPartTerminologyID" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID");

ALTER TABLE "PartsRelationship" 
ADD CONSTRAINT "FKPartsRelationshipPartsRelatedPartTerminologyID" 
FOREIGN KEY ("RelatedPartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID");

ALTER TABLE "PartsToAlias" 
ADD CONSTRAINT "FKPartsToAliasAliasAliasID" 
FOREIGN KEY ("AliasID") 
REFERENCES "Alias" ("AliasID") 
ON DELETE CASCADE;

ALTER TABLE "PartsToAlias" 
ADD CONSTRAINT "FKPartsToAliasPartsPartTerminologyID" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID") 
ON DELETE CASCADE;

ALTER TABLE "PartsToUse" 
ADD CONSTRAINT "FKPartsToUsePartsPartTerminologyID" 
FOREIGN KEY ("PartTerminologyID") 
REFERENCES "Parts" ("PartTerminologyID") 
ON DELETE CASCADE;

ALTER TABLE "PartsToUse" 
ADD CONSTRAINT "FKPartsToUseUseUseID" 
FOREIGN KEY ("UseID") 
REFERENCES "Use" ("UseID") 
ON DELETE CASCADE;

ALTER TABLE "PIESExpiCode" 
ADD CONSTRAINT "FKPIESExpiCodePIESExpiGroupPIESExpiGroupId" 
FOREIGN KEY ("PIESExpiGroupId") 
REFERENCES "PIESExpiGroup" ("PIESExpiGroupId") 
ON DELETE CASCADE;

ALTER TABLE "PIESField" 
ADD CONSTRAINT "FKPIESFieldPIESSegmentPIESSegmentId" 
FOREIGN KEY ("PIESSegmentId") 
REFERENCES "PIESSegment" ("PIESSegmentId") 
ON DELETE CASCADE;

ALTER TABLE "PIESReferenceFieldCode" 
ADD CONSTRAINT "FKPIESReferenceFieldCodePIESCodePIESCodeId" 
FOREIGN KEY ("PIESCodeId") 
REFERENCES "PIESCode" ("PIESCodeId") 
ON DELETE CASCADE;

ALTER TABLE "PIESReferenceFieldCode" 
ADD CONSTRAINT "FKPIESReferenceFieldCodePIESExpiCodePIESExpiCodeId" 
FOREIGN KEY ("PIESExpiCodeId") 
REFERENCES "PIESExpiCode" ("PIESExpiCodeId");

ALTER TABLE "PIESReferenceFieldCode" 
ADD CONSTRAINT "FKPIESReferenceFieldCodePIESFieldPIESFieldId" 
FOREIGN KEY ("PIESFieldId") 
REFERENCES "PIESField" ("PIESFieldId") 
ON DELETE CASCADE;

ALTER TABLE "ValidValueAssignment" 
ADD CONSTRAINT "FKValidValueAssignmentPartAttributeAssignmentPAPTID" 
FOREIGN KEY ("PAPTID") 
REFERENCES "PartAttributeAssignment" ("PAPTID");

ALTER TABLE "ValidValueAssignment" 
ADD CONSTRAINT "FKValidValueAssignmentValidValuesValidValueID" 
FOREIGN KEY ("ValidValueID") 
REFERENCES "ValidValues" ("ValidValueID");
