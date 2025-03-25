-- Base tables
CREATE TABLE "QualifierType" (
    "QualifierTypeID" INT PRIMARY KEY,
    "QualifierType" VARCHAR(50) NULL
);

CREATE TABLE "Language" (
    "LanguageID" INT PRIMARY KEY,
    "LanguageName" VARCHAR(50) NULL,
    "DialectName" VARCHAR(50) NULL
);

CREATE TABLE "GroupNumber" (
    "GroupNumberID" INT PRIMARY KEY,
    "GroupDescription" VARCHAR(100) NOT NULL
);

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
    "TableDescription" VARCHAR(1000) NULL
);

CREATE TABLE "Version" (
    "VersionDate" TIMESTAMP NOT NULL
);

-- Dependent tables
CREATE TABLE "Qualifier" (
    "QualifierID" INT PRIMARY KEY,
    "QualifierText" VARCHAR(500) NULL,
    "ExampleText" VARCHAR(500) NULL,
    "QualifierTypeID" INT NOT NULL,
    "NewQualifierID" INT NULL,
    "WhenModified" TIMESTAMP NOT NULL,
    FOREIGN KEY ("QualifierTypeID") REFERENCES "QualifierType" ("QualifierTypeID")
);

CREATE TABLE "QualifierTranslation" (
    "QualifierTranslationID" INT PRIMARY KEY,
    "QualifierID" INT NOT NULL,
    "LanguageID" INT NOT NULL,
    "TranslationText" VARCHAR(500) NOT NULL,
    FOREIGN KEY ("QualifierID") REFERENCES "Qualifier" ("QualifierID"),
    FOREIGN KEY ("LanguageID") REFERENCES "Language" ("LanguageID")
);

CREATE TABLE "QdbChanges" (
    "VersionDate" TIMESTAMP NULL,
    "QualifierID" INT NULL,
    "QualifierText" VARCHAR(500) NULL,
    "Action" CHAR(1) NULL
);

CREATE TABLE "QualifierGroup" (
    "QualifierGroupID" INT PRIMARY KEY,
    "GroupNumberID" INT NOT NULL,
    "QualifierID" INT NOT NULL,
    FOREIGN KEY ("QualifierID") REFERENCES "Qualifier" ("QualifierID"),
    FOREIGN KEY ("GroupNumberID") REFERENCES "GroupNumber" ("GroupNumberID")
);

CREATE TABLE "Changes" (
    "ChangeID" INT PRIMARY KEY,
    "RequestID" INT NOT NULL,
    "ChangeReasonID" INT NOT NULL,
    "RevDate" TIMESTAMP NULL,
    FOREIGN KEY ("ChangeReasonID") REFERENCES "ChangeReasons" ("ChangeReasonID")
);

CREATE TABLE "ChangeDetails" (
    "ChangeDetailID" INT PRIMARY KEY,
    "ChangeID" INT NOT NULL,
    "ChangeAttributeStateID" INT NOT NULL,
    "TableNameID" INT NOT NULL,
    "PrimaryKeyColumnName" VARCHAR(255) NULL,
    "PrimaryKeyBefore" INT NULL,
    "PrimaryKeyAfter" INT NULL,
    "ColumnName" VARCHAR(255) NULL,
    "ColumnValueBefore" VARCHAR(1000) NULL,
    "ColumnValueAfter" VARCHAR(1000) NULL,
    FOREIGN KEY ("ChangeID") REFERENCES "Changes" ("ChangeID"),
    FOREIGN KEY ("ChangeAttributeStateID") REFERENCES "ChangeAttributeStates" ("ChangeAttributeStateID"),
    FOREIGN KEY ("TableNameID") REFERENCES "ChangeTableNames" ("TableNameID")
);
