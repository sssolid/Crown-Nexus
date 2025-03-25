CREATE TABLE "Abbreviation"(
	"Abbreviation" varchar(3) NOT NULL,
	"Description" varchar(20) NOT NULL,
	"LongDescription" varchar(200) NOT NULL,
  PRIMARY KEY ("Abbreviation")
 );

CREATE TABLE "Make" (
    "MakeID" INT NOT NULL,
    "MakeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("MakeID")
);

CREATE TABLE "VehicleTypeGroup" (
    "VehicleTypeGroupID" INT NOT NULL,
    "VehicleTypeGroupName" VARCHAR(50) NOT NULL	
);

CREATE TABLE "VehicleType" (
    "VehicleTypeID" INT NOT NULL,
    "VehicleTypeName" VARCHAR(50) NOT NULL,
    "VehicleTypeGroupID" INT DEFAULT NULL,
    PRIMARY KEY ("VehicleTypeID")
);

CREATE TABLE "Model" (
    "ModelID" INT NOT NULL,
    "ModelName" VARCHAR(100) DEFAULT NULL,
    "VehicleTypeID" INT NOT NULL,
    PRIMARY KEY ("ModelID"),
    CONSTRAINT "FK_VehicleType_Model" FOREIGN KEY ("VehicleTypeID")
        REFERENCES "VehicleType" ("VehicleTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "Vehicletypemodel_fk" FOREIGN KEY ("VehicleTypeID")
        REFERENCES "VehicleType" ("VehicleTypeID")
);

CREATE TABLE "SubModel" (
    "SubmodelID" INT NOT NULL,
    "SubModelName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("SubmodelID")
);

CREATE TABLE "Region" (
    "RegionID" INT NOT NULL,
    "ParentID" INT DEFAULT NULL,
    "RegionAbbr" VARCHAR(3) DEFAULT NULL,
    "RegionName" VARCHAR(30) DEFAULT NULL,
    PRIMARY KEY ("RegionID"),
    CONSTRAINT "FK_Region_Parent" FOREIGN KEY ("ParentID")
        REFERENCES "Region" ("RegionID")
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE "Year" (
    "YearID" INT NOT NULL,
    PRIMARY KEY ("YearID")
);


CREATE TABLE "PublicationStage" (
    "PublicationStageID" INT NOT NULL,
    "PublicationStageName" VARCHAR(100) NOT NULL,
    PRIMARY KEY ("PublicationStageID")
);

CREATE TABLE "BaseVehicle" (
    "BaseVehicleID" INT NOT NULL,
    "YearID" INT NOT NULL,
    "MakeID" INT NOT NULL,
    "ModelID" INT NOT NULL,
    PRIMARY KEY ("BaseVehicleID"),
    CONSTRAINT "FK_Make_BaseVehicle" FOREIGN KEY ("MakeID")
        REFERENCES "Make" ("MakeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_Model_BaseVehicle" FOREIGN KEY ("ModelID")
        REFERENCES "Model" ("ModelID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_Year_BaseVehicle" FOREIGN KEY ("YearID")
        REFERENCES "Year" ("YearID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "makebaseVehicle_fk" FOREIGN KEY ("MakeID")
        REFERENCES "Make" ("MakeID"),
    CONSTRAINT "modelbaseVehicle_fk" FOREIGN KEY ("ModelID")
        REFERENCES "Model" ("ModelID"),
    CONSTRAINT "yearbaseVehicle_fk" FOREIGN KEY ("YearID")
        REFERENCES "Year" ("YearID")
);


CREATE TABLE "Vehicle" (
    "VehicleID" INT NOT NULL,
    "BaseVehicleID" INT NOT NULL,
    "SubmodelID" INT NOT NULL,
    "RegionID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    "PublicationStageID" INT NOT NULL DEFAULT '4',
    "PublicationStageSource" VARCHAR(100) NOT NULL,
    "PublicationStageDate" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("VehicleID"),
    CONSTRAINT "FK_BaseVehicle_Vehicle" FOREIGN KEY ("BaseVehicleID")
        REFERENCES "BaseVehicle" ("BaseVehicleID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_PublicationStage_Vehicle" FOREIGN KEY ("PublicationStageID")
        REFERENCES "PublicationStage" ("PublicationStageID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_Region_Vehicle" FOREIGN KEY ("RegionID")
        REFERENCES "Region" ("RegionID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_SubModel_Vehicle" FOREIGN KEY ("SubmodelID")
        REFERENCES "SubModel" ("SubmodelID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "baseVehicleVehicle_fk" FOREIGN KEY ("BaseVehicleID")
        REFERENCES "BaseVehicle" ("BaseVehicleID"),
    CONSTRAINT "PublicationStage_fk" FOREIGN KEY ("PublicationStageID")
        REFERENCES "PublicationStage" ("PublicationStageID"),
    CONSTRAINT "regionVehicle_fk" FOREIGN KEY ("RegionID")
        REFERENCES "Region" ("RegionID")
);

CREATE TABLE "BrakeABS" (
    "BrakeABSID" INT NOT NULL,
    "BrakeABSName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("BrakeABSID")
);
CREATE TABLE "BrakeType" (
    "BrakeTypeID" INT NOT NULL,
    "BrakeTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("BrakeTypeID")
);
CREATE TABLE "BrakeSystem" (
    "BrakeSystemID" INT NOT NULL,
    "BrakeSystemName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("BrakeSystemID")
);
CREATE TABLE "BrakeConfig" (
    "BrakeConfigID" INT NOT NULL,
    "FrontBrakeTypeID" INT NOT NULL,
    "RearBrakeTypeID" INT NOT NULL,
    "BrakeSystemID" INT NOT NULL,
    "BrakeABSID" INT NOT NULL,
    PRIMARY KEY ("BrakeConfigID"),
    CONSTRAINT "FK_BrakeABS_BrakeConfig" FOREIGN KEY ("BrakeABSID")
        REFERENCES "BrakeABS" ("BrakeABSID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_BrakeSystem_BrakeConfig" FOREIGN KEY ("BrakeSystemID")
        REFERENCES "BrakeSystem" ("BrakeSystemID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FrontBrakeType_BrakeConfig" FOREIGN KEY ("FrontBrakeTypeID")
        REFERENCES "BrakeType" ("BrakeTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_RearBrakeType_BrakeConfig" FOREIGN KEY ("RearBrakeTypeID")
        REFERENCES "BrakeType" ("BrakeTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "brakeabsbrakeconfig_fk" FOREIGN KEY ("BrakeABSID")
        REFERENCES "BrakeABS" ("BrakeABSID"),
    CONSTRAINT "brakesystembrakeconfig_fk" FOREIGN KEY ("BrakeSystemID")
        REFERENCES "BrakeSystem" ("BrakeSystemID"),
    CONSTRAINT "braketypebrakeconfig1_fk" FOREIGN KEY ("RearBrakeTypeID")
        REFERENCES "BrakeType" ("BrakeTypeID"),
    CONSTRAINT "braketypebrakeconfig_fk" FOREIGN KEY ("FrontBrakeTypeID")
        REFERENCES "BrakeType" ("BrakeTypeID")
);
CREATE TABLE "VehicleToBrakeConfig" (
    "VehicleToBrakeConfigID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "BrakeConfigID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToBrakeConfigID"),
    CONSTRAINT "brakeconfigVehicle_fk" FOREIGN KEY ("BrakeConfigID")
        REFERENCES "BrakeConfig" ("BrakeConfigID"),
    CONSTRAINT "VehicletobrakeconfigVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);


CREATE TABLE "Aspiration" (
    "AspirationID" INT NOT NULL,
    "AspirationName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("AspirationID")
);

CREATE TABLE "BedType" (
    "BedTypeID" INT NOT NULL,
    "BedTypeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("BedTypeID")
);
CREATE TABLE "BedLength" (
    "BedLengthID" INT NOT NULL,
    "BedLength" VARCHAR(10) NOT NULL,
    "BedLengthMetric" VARCHAR(10) NOT NULL,
    PRIMARY KEY ("BedLengthID")
);
CREATE TABLE "BedConfig" (
    "BedConfigID" INT NOT NULL,
    "BedLengthID" INT NOT NULL,
    "BedTypeID" INT NOT NULL,
    PRIMARY KEY ("BedConfigID"),
    CONSTRAINT "FK_BedLength_BedConfig" FOREIGN KEY ("BedLengthID")
        REFERENCES "BedLength" ("BedLengthID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_BedType_BedConfig" FOREIGN KEY ("BedTypeID")
        REFERENCES "BedType" ("BedTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "bedlengthBedConfig_fk" FOREIGN KEY ("BedLengthID")
        REFERENCES "BedLength" ("BedLengthID"),
    CONSTRAINT "bedtypeBedConfig_fk" FOREIGN KEY ("BedTypeID")
        REFERENCES "BedType" ("BedTypeID")
);

CREATE TABLE "BodyType" (
    "BodyTypeID" INT NOT NULL,
    "BodyTypeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("BodyTypeID")
);
CREATE TABLE "BodyNumDoors" (
    "BodyNumDoorsID" INT NOT NULL,
    "BodyNumDoors" VARCHAR(3) NOT NULL,
    PRIMARY KEY ("BodyNumDoorsID")
);
CREATE TABLE "BodyStyleConfig" (
    "BodyStyleConfigID" INT NOT NULL,
    "BodyNumDoorsID" INT NOT NULL,
    "BodyTypeID" INT NOT NULL,
    PRIMARY KEY ("BodyStyleConfigID"),
    CONSTRAINT "FK_BodyNumDoors_BodyStyleConfig" FOREIGN KEY ("BodyNumDoorsID")
        REFERENCES "BodyNumDoors" ("BodyNumDoorsID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_BodyType_BodyStyleConfig" FOREIGN KEY ("BodyTypeID")
        REFERENCES "BodyType" ("BodyTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "bodynumdoorsBodyStyleConfig_fk" FOREIGN KEY ("BodyNumDoorsID")
        REFERENCES "BodyNumDoors" ("BodyNumDoorsID"),
    CONSTRAINT "bodytypeBodyStyleConfig_fk" FOREIGN KEY ("BodyTypeID")
        REFERENCES "BodyType" ("BodyTypeID")
);

CREATE TABLE "Class" (
	"ClassID" int NOT NULL,
	"ClassName" varchar(30) NOT NULL,
 CONSTRAINT "PK_Class" PRIMARY KEY 
(
	"ClassID" 
) 
);

CREATE TABLE "CylinderHeadType" (
    "CylinderHeadTypeID" INT NOT NULL,
    "CylinderHeadTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("CylinderHeadTypeID")
);
CREATE TABLE "DriveType" (
    "DriveTypeID" INT NOT NULL,
    "DriveTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("DriveTypeID")
);
CREATE TABLE "ElecControlled" (
    "ElecControlledID" INT NOT NULL,
    "ElecControlled" VARCHAR(3) NOT NULL,
    PRIMARY KEY ("ElecControlledID")
);

CREATE TABLE "EngineBlock" (
    "EngineBlockID" INT NOT NULL,
    "Liter" VARCHAR(6) NOT NULL,
    "CC" VARCHAR(8) NOT NULL,
    "CID" VARCHAR(7) NOT NULL,
    "Cylinders" VARCHAR(2) NOT NULL,
    "BlockType" VARCHAR(2) NOT NULL,
	    PRIMARY KEY ("EngineBlockID")
	);		 

CREATE TABLE "EngineBoreStroke" (
    "EngineBoreStrokeID" INT NOT NULL,
    "EngBoreIn" VARCHAR(10) NOT NULL,
    "EngBoreMetric" VARCHAR(10) NOT NULL,
    "EngStrokeIn" VARCHAR(10) NOT NULL,
    "EngStrokeMetric" VARCHAR(10) NOT NULL,
	    PRIMARY KEY ("EngineBoreStrokeID")
	);
CREATE TABLE "EngineBase2" (
    "EngineBaseID" INT NOT NULL,
    "EngineBlockID" INT NOT NULL,
    "EngineBoreStrokeID" INT NOT NULL,
        PRIMARY KEY ("EngineBaseID"),
    CONSTRAINT "EngineBaseEngineBlock_fk" FOREIGN KEY ("EngineBlockID")
        REFERENCES "EngineBlock" ("EngineBlockID"),
	CONSTRAINT "EngineBaseEngineBoreStroke_fk" FOREIGN KEY ("EngineBoreStrokeID")
        REFERENCES "EngineBoreStroke" ("EngineBoreStrokeID")
);
CREATE TABLE "EngineBase" (
    "EngineBaseID" INT NOT NULL,
    "Liter" VARCHAR(6) NOT NULL,
    "CC" VARCHAR(8) NOT NULL,
    "CID" VARCHAR(7) NOT NULL,
    "Cylinders" VARCHAR(2) NOT NULL,
    "BlockType" VARCHAR(2) NOT NULL,
    "EngBoreIn" VARCHAR(10) NOT NULL,
    "EngBoreMetric" VARCHAR(10) NOT NULL,
    "EngStrokeIn" VARCHAR(10) NOT NULL,
    "EngStrokeMetric" VARCHAR(10) NOT NULL,
    PRIMARY KEY ("EngineBaseID")
);
CREATE TABLE "EngineDesignation" (
    "EngineDesignationID" INT NOT NULL,
    "EngineDesignationName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("EngineDesignationID")
);
CREATE TABLE "EngineVersion" (
    "EngineVersionID" INT NOT NULL,
    "EngineVersion" VARCHAR(20) NOT NULL,
    PRIMARY KEY ("EngineVersionID")
);
CREATE TABLE "EngineVIN" (
    "EngineVINID" INT NOT NULL,
    "EngineVINName" VARCHAR(5) NOT NULL,
    PRIMARY KEY ("EngineVINID")
);
CREATE TABLE "FuelDeliverySubType" (
    "FuelDeliverySubTypeID" INT NOT NULL,
    "FuelDeliverySubTypeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("FuelDeliverySubTypeID")
);
CREATE TABLE "FuelDeliveryType" (
    "FuelDeliveryTypeID" INT NOT NULL,
    "FuelDeliveryTypeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("FuelDeliveryTypeID")
);
CREATE TABLE "FuelSystemControlType" (
    "FuelSystemControlTypeID" INT NOT NULL,
    "FuelSystemControlTypeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("FuelSystemControlTypeID")
);
CREATE TABLE "FuelSystemDesign" (
    "FuelSystemDesignID" INT NOT NULL,
    "FuelSystemDesignName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("FuelSystemDesignID")
);
CREATE TABLE "FuelDeliveryConfig" (
    "FuelDeliveryConfigID" INT NOT NULL,
    "FuelDeliveryTypeID" INT NOT NULL,
    "FuelDeliverySubTypeID" INT NOT NULL,
    "FuelSystemControlTypeID" INT NOT NULL,
    "FuelSystemDesignID" INT NOT NULL,
    PRIMARY KEY ("FuelDeliveryConfigID"),
    CONSTRAINT "FK_FuelDeliverySubType_FuelDeliveryConfig" FOREIGN KEY ("FuelDeliverySubTypeID")
        REFERENCES "FuelDeliverySubType" ("FuelDeliverySubTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelDeliveryType_FuelDeliveryConfig" FOREIGN KEY ("FuelDeliveryTypeID")
        REFERENCES "FuelDeliveryType" ("FuelDeliveryTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelSystemControlType_FuelDeliveryConfig" FOREIGN KEY ("FuelSystemControlTypeID")
        REFERENCES "FuelSystemControlType" ("FuelSystemControlTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelSystemDesign_FuelDeliveryConfig" FOREIGN KEY ("FuelSystemDesignID")
        REFERENCES "FuelSystemDesign" ("FuelSystemDesignID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "fueldeliverysubtypefueldeliv_fk" FOREIGN KEY ("FuelDeliverySubTypeID")
        REFERENCES "FuelDeliverySubType" ("FuelDeliverySubTypeID"),
    CONSTRAINT "fueldeliverytypefueldelivery_fk" FOREIGN KEY ("FuelDeliveryTypeID")
        REFERENCES "FuelDeliveryType" ("FuelDeliveryTypeID"),
    CONSTRAINT "fuelsystemcontroltypefueldel_fk" FOREIGN KEY ("FuelSystemControlTypeID")
        REFERENCES "FuelSystemControlType" ("FuelSystemControlTypeID"),
    CONSTRAINT "fuelsystemdesignfueldelivery_fk" FOREIGN KEY ("FuelSystemDesignID")
        REFERENCES "FuelSystemDesign" ("FuelSystemDesignID")
);
CREATE TABLE "FuelType" (
    "FuelTypeID" INT NOT NULL,
    "FuelTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("FuelTypeID")
);
CREATE TABLE "IgnitionSystemType" (
    "IgnitionSystemTypeID" INT NOT NULL,
    "IgnitionSystemTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("IgnitionSystemTypeID")
);
CREATE TABLE "Mfr" (
    "MfrID" INT NOT NULL,
    "MfrName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("MfrID")
);
CREATE TABLE "MfrBodyCode" (
    "MfrBodyCodeID" INT NOT NULL,
    "MfrBodyCodeName" VARCHAR(10) NOT NULL,
    PRIMARY KEY ("MfrBodyCodeID")
);
CREATE TABLE "PowerOutput" (
    "PowerOutputID" INT NOT NULL,
    "HorsePower" VARCHAR(10) NOT NULL,
    "KilowattPower" VARCHAR(10) NOT NULL
);
CREATE TABLE "Valves" (
    "ValvesID" INT NOT NULL,
    "ValvesPerEngine" VARCHAR(3) NOT NULL,
    PRIMARY KEY ("ValvesID")
);
CREATE TABLE "EngineConfig" (
    "EngineConfigID" INT NOT NULL,
    "EngineDesignationID" INT NOT NULL,
    "EngineVINID" INT NOT NULL,
    "ValvesID" INT NOT NULL,
    "EngineBaseID" INT NOT NULL,
    "FuelDeliveryConfigID" INT NOT NULL,
    "AspirationID" INT NOT NULL,
    "CylinderHeadTypeID" INT NOT NULL,
    "FuelTypeID" INT NOT NULL,
    "IgnitionSystemTypeID" INT NOT NULL,
    "EngineMfrID" INT NOT NULL,
    "EngineVersionID" INT NOT NULL,
    "PowerOutputID" INT NOT NULL DEFAULT '1',
    PRIMARY KEY ("EngineConfigID"),
    CONSTRAINT "FK_Aspiration_EngineConfig" FOREIGN KEY ("AspirationID")
        REFERENCES "Aspiration" ("AspirationID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_CylinderHeadType_EngineConfig" FOREIGN KEY ("CylinderHeadTypeID")
        REFERENCES "CylinderHeadType" ("CylinderHeadTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineBase_EngineConfig" FOREIGN KEY ("EngineBaseID")
        REFERENCES "EngineBase" ("EngineBaseID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineConfig_Valves" FOREIGN KEY ("ValvesID")
        REFERENCES "Valves" ("ValvesID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineConfig_Valves1" FOREIGN KEY ("ValvesID")
        REFERENCES "Valves" ("ValvesID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineDesignation_EngineConfig" FOREIGN KEY ("EngineDesignationID")
        REFERENCES "EngineDesignation" ("EngineDesignationID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineVIN_EngineConfig" FOREIGN KEY ("EngineVINID")
        REFERENCES "EngineVIN" ("EngineVINID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineVersion_EngineConfig" FOREIGN KEY ("EngineVersionID")
        REFERENCES "EngineVersion" ("EngineVersionID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelDeliveryConfig_EngineConfig" FOREIGN KEY ("FuelDeliveryConfigID")
        REFERENCES "FuelDeliveryConfig" ("FuelDeliveryConfigID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelType_EngineConfig" FOREIGN KEY ("FuelTypeID")
        REFERENCES "FuelType" ("FuelTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_IgnitionSystemType_EngineConfig" FOREIGN KEY ("IgnitionSystemTypeID")
        REFERENCES "IgnitionSystemType" ("IgnitionSystemTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_Mfr_EngineConfig" FOREIGN KEY ("EngineMfrID")
        REFERENCES "Mfr" ("MfrID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "AspirationEngineConfig_fk" FOREIGN KEY ("AspirationID")
        REFERENCES "Aspiration" ("AspirationID"),
    CONSTRAINT "CylinderHeadTypeEngineConfig_fk" FOREIGN KEY ("CylinderHeadTypeID")
        REFERENCES "CylinderHeadType" ("CylinderHeadTypeID"),
    CONSTRAINT "EngineBaseEngineConfig_fk" FOREIGN KEY ("EngineBaseID")
        REFERENCES "EngineBase" ("EngineBaseID"),
    CONSTRAINT "EngineDesignationengineconfi_fk" FOREIGN KEY ("EngineDesignationID")
        REFERENCES "EngineDesignation" ("EngineDesignationID"),
    CONSTRAINT "EngineVersionEngineConfig_fk" FOREIGN KEY ("EngineVersionID")
        REFERENCES "EngineVersion" ("EngineVersionID"),
    CONSTRAINT "EngineVINEngineConfig_fk" FOREIGN KEY ("EngineVINID")
        REFERENCES "EngineVIN" ("EngineVINID"),
    CONSTRAINT "FuelDeliveryConfigengineconf_fk" FOREIGN KEY ("FuelDeliveryConfigID")
        REFERENCES "FuelDeliveryConfig" ("FuelDeliveryConfigID"),
    CONSTRAINT "FuelTypeEngineConfig_fk" FOREIGN KEY ("FuelTypeID")
        REFERENCES "FuelType" ("FuelTypeID"),
    CONSTRAINT "IgnitionSystemTypeengineconf_fk" FOREIGN KEY ("IgnitionSystemTypeID")
        REFERENCES "IgnitionSystemType" ("IgnitionSystemTypeID"),
    CONSTRAINT "MfrEngineConfig_fk" FOREIGN KEY ("EngineMfrID")
        REFERENCES "Mfr" ("MfrID")
);
CREATE TABLE "EngineConfig2" (
    "EngineConfigID" INT NOT NULL,
    "EngineDesignationID" INT NOT NULL,
    "EngineVINID" INT NOT NULL,
    "ValvesID" INT NOT NULL,
    "EngineBaseID" INT NOT NULL,
	"EngineBlockID" INT NOT NULL,
    "EngineBoreStrokeID" INT NOT NULL,
    "FuelDeliveryConfigID" INT NOT NULL,
    "AspirationID" INT NOT NULL,
    "CylinderHeadTypeID" INT NOT NULL,
    "FuelTypeID" INT NOT NULL,
    "IgnitionSystemTypeID" INT NOT NULL,
    "EngineMfrID" INT NOT NULL,
    "EngineVersionID" INT NOT NULL,
    "PowerOutputID" INT NOT NULL DEFAULT '1',
    PRIMARY KEY ("EngineConfigID"),
    CONSTRAINT "FK_Aspiration_EngineConfig2" FOREIGN KEY ("AspirationID")
        REFERENCES "Aspiration" ("AspirationID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_CylinderHeadType_EngineConfig2" FOREIGN KEY ("CylinderHeadTypeID")
        REFERENCES "CylinderHeadType" ("CylinderHeadTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineBase_EngineConfig2" FOREIGN KEY ("EngineBaseID")
        REFERENCES "EngineBase2" ("EngineBaseID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
		    CONSTRAINT "FK_EngineBlock_EngineConfig2" FOREIGN KEY ("EngineBlockID")
        REFERENCES "EngineBlock" ("EngineBlockID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
		    CONSTRAINT "FK_EngineBoreStroke_EngineConfig2" FOREIGN KEY ("EngineBoreStrokeID")
        REFERENCES "EngineBoreStroke" ("EngineBoreStrokeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineConfig2_Valves" FOREIGN KEY ("ValvesID")
        REFERENCES "Valves" ("ValvesID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineConfig2_Valves1" FOREIGN KEY ("ValvesID")
        REFERENCES "Valves" ("ValvesID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineDesignation_EngineConfig2" FOREIGN KEY ("EngineDesignationID")
        REFERENCES "EngineDesignation" ("EngineDesignationID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineVIN_EngineConfig2" FOREIGN KEY ("EngineVINID")
        REFERENCES "EngineVIN" ("EngineVINID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_EngineVersion_EngineConfig2" FOREIGN KEY ("EngineVersionID")
        REFERENCES "EngineVersion" ("EngineVersionID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelDeliveryConfig_EngineConfig2" FOREIGN KEY ("FuelDeliveryConfigID")
        REFERENCES "FuelDeliveryConfig" ("FuelDeliveryConfigID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_FuelType_EngineConfig2" FOREIGN KEY ("FuelTypeID")
        REFERENCES "FuelType" ("FuelTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_IgnitionSystemType_EngineConfig2" FOREIGN KEY ("IgnitionSystemTypeID")
        REFERENCES "IgnitionSystemType" ("IgnitionSystemTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_Mfr_EngineConfig2" FOREIGN KEY ("EngineMfrID")
        REFERENCES "Mfr" ("MfrID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "AspirationEngineConfig2_fk" FOREIGN KEY ("AspirationID")
        REFERENCES "Aspiration" ("AspirationID"),
    CONSTRAINT "CylinderHeadTypeEngineConfig2_fk" FOREIGN KEY ("CylinderHeadTypeID")
        REFERENCES "CylinderHeadType" ("CylinderHeadTypeID"),
    CONSTRAINT "EngineBaseEngineConfig2_fk" FOREIGN KEY ("EngineBaseID")
        REFERENCES "EngineBase2" ("EngineBaseID"),
    CONSTRAINT "EngineDesignationengineconfi2_fk" FOREIGN KEY ("EngineDesignationID")
        REFERENCES "EngineDesignation" ("EngineDesignationID"),
    CONSTRAINT "EngineVersionEngineConfig2_fk" FOREIGN KEY ("EngineVersionID")
        REFERENCES "EngineVersion" ("EngineVersionID"),
    CONSTRAINT "EngineVINEngineConfig2_fk" FOREIGN KEY ("EngineVINID")
        REFERENCES "EngineVIN" ("EngineVINID"),
    CONSTRAINT "FuelDeliveryConfigengineconf2_fk" FOREIGN KEY ("FuelDeliveryConfigID")
        REFERENCES "FuelDeliveryConfig" ("FuelDeliveryConfigID"),
    CONSTRAINT "FuelTypeEngineConfig2_fk" FOREIGN KEY ("FuelTypeID")
        REFERENCES "FuelType" ("FuelTypeID"),
    CONSTRAINT "IgnitionSystemTypeengineconf2_fk" FOREIGN KEY ("IgnitionSystemTypeID")
        REFERENCES "IgnitionSystemType" ("IgnitionSystemTypeID"),
    CONSTRAINT "MfrEngineConfig2_fk" FOREIGN KEY ("EngineMfrID")
        REFERENCES "Mfr" ("MfrID")
);

CREATE TABLE "SpringType" (
    "SpringTypeID" INT NOT NULL,
    "SpringTypeName" VARCHAR(50) NOT NULL,
    PRIMARY KEY ("SpringTypeID")
);
CREATE TABLE "SpringTypeConfig" (
    "SpringTypeConfigID" INT NOT NULL,
    "FrontSpringTypeID" INT NOT NULL,
    "RearSpringTypeID" INT NOT NULL,
    PRIMARY KEY ("SpringTypeConfigID"),
    CONSTRAINT "FK_FrontSpringType_SpringTypeConfig" FOREIGN KEY ("FrontSpringTypeID")
        REFERENCES "SpringType" ("SpringTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_RearSpringType_SpringTypeConfig" FOREIGN KEY ("RearSpringTypeID")
        REFERENCES "SpringType" ("SpringTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "springconfig1_fk" FOREIGN KEY ("FrontSpringTypeID")
        REFERENCES "SpringType" ("SpringTypeID"),
    CONSTRAINT "springconfig2_fk" FOREIGN KEY ("RearSpringTypeID")
        REFERENCES "SpringType" ("SpringTypeID")
);
CREATE TABLE "SteeringSystem" (
    "SteeringSystemID" INT NOT NULL,
    "SteeringSystemName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("SteeringSystemID")
);
CREATE TABLE "SteeringType" (
    "SteeringTypeID" INT NOT NULL,
    "SteeringTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("SteeringTypeID")
);
CREATE TABLE "SteeringConfig" (
    "SteeringConfigID" INT NOT NULL,
    "SteeringTypeID" INT NOT NULL,
    "SteeringSystemID" INT NOT NULL,
    PRIMARY KEY ("SteeringConfigID"),
    CONSTRAINT "FK_SteeringSystem_SteeringConfig" FOREIGN KEY ("SteeringSystemID")
        REFERENCES "SteeringSystem" ("SteeringSystemID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_SteeringType_SteeringConfig" FOREIGN KEY ("SteeringTypeID")
        REFERENCES "SteeringType" ("SteeringTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "SteeringSystemSteeringConfig_fk" FOREIGN KEY ("SteeringSystemID")
        REFERENCES "SteeringSystem" ("SteeringSystemID"),
    CONSTRAINT "SteeringTypeSteeringConfig_fk" FOREIGN KEY ("SteeringTypeID")
        REFERENCES "SteeringType" ("SteeringTypeID")
);

CREATE TABLE "TransmissionControlType" (
    "TransmissionControlTypeID" INT NOT NULL,
    "TransmissionControlTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("TransmissionControlTypeID")
);
CREATE TABLE "TransmissionMfrCode" (
    "TransmissionMfrCodeID" INT NOT NULL,
    "TransmissionMfrCode" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("TransmissionMfrCodeID")
);
CREATE TABLE "TransmissionNumSpeeds" (
    "TransmissionNumSpeedsID" INT NOT NULL,
    "TransmissionNumSpeeds" CHAR(3) NOT NULL,
    PRIMARY KEY ("TransmissionNumSpeedsID")
);
CREATE TABLE "TransmissionType" (
    "TransmissionTypeID" INT NOT NULL,
    "TransmissionTypeName" VARCHAR(30) NOT NULL,
    PRIMARY KEY ("TransmissionTypeID")
);
CREATE TABLE "TransmissionBase" (
    "TransmissionBaseID" INT NOT NULL,
    "TransmissionTypeID" INT NOT NULL,
    "TransmissionNumSpeedsID" INT NOT NULL,
    "TransmissionControlTypeID" INT NOT NULL,
    PRIMARY KEY ("TransmissionBaseID"),
    CONSTRAINT "FK_TransmissionControlType_TransmissionBase" FOREIGN KEY ("TransmissionControlTypeID")
        REFERENCES "TransmissionControlType" ("TransmissionControlTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_TransmissionNumSpeeds_TransmissionBase" FOREIGN KEY ("TransmissionNumSpeedsID")
        REFERENCES "TransmissionNumSpeeds" ("TransmissionNumSpeedsID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_TransmissionType_TransmissionBase" FOREIGN KEY ("TransmissionTypeID")
        REFERENCES "TransmissionType" ("TransmissionTypeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "TransmissionControlTypetrans_fk" FOREIGN KEY ("TransmissionControlTypeID")
        REFERENCES "TransmissionControlType" ("TransmissionControlTypeID"),
    CONSTRAINT "TransmissionNumSpeedstransmi_fk" FOREIGN KEY ("TransmissionNumSpeedsID")
        REFERENCES "TransmissionNumSpeeds" ("TransmissionNumSpeedsID"),
    CONSTRAINT "TransmissionTypeTransmission_fk" FOREIGN KEY ("TransmissionTypeID")
        REFERENCES "TransmissionType" ("TransmissionTypeID")
);
CREATE TABLE "Transmission" (
    "TransmissionID" INT NOT NULL,
    "TransmissionBaseID" INT NOT NULL,
    "TransmissionMfrCodeID" INT NOT NULL,
    "TransmissionElecControlledID" INT NOT NULL,
    "TransmissionMfrID" INT NOT NULL,
    PRIMARY KEY ("TransmissionID"),
    CONSTRAINT "FK_Mfr_Transmission" FOREIGN KEY ("TransmissionMfrID")
        REFERENCES "Mfr" ("MfrID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_TransmissionBase_Transmission" FOREIGN KEY ("TransmissionBaseID")
        REFERENCES "TransmissionBase" ("TransmissionBaseID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_TransmissionMfrCode_Transmission" FOREIGN KEY ("TransmissionMfrCodeID")
        REFERENCES "TransmissionMfrCode" ("TransmissionMfrCodeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "FK_Transmission_ElecControlled" FOREIGN KEY ("TransmissionElecControlledID")
        REFERENCES "ElecControlled" ("ElecControlledID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT "MfrTransmission_fk" FOREIGN KEY ("TransmissionMfrID")
        REFERENCES "Mfr" ("MfrID"),
    CONSTRAINT "TransmissionBaseTransmission_fk" FOREIGN KEY ("TransmissionBaseID")
        REFERENCES "TransmissionBase" ("TransmissionBaseID"),
    CONSTRAINT "TransmissionMfrCodetransmiss_fk" FOREIGN KEY ("TransmissionMfrCodeID")
        REFERENCES "TransmissionMfrCode" ("TransmissionMfrCodeID")
);
CREATE TABLE "WheelBase" (
    "WheelBaseID" INT NOT NULL,
    "WheelBase" VARCHAR(10) NOT NULL,
    "WheelBaseMetric" VARCHAR(10) NOT NULL,
    PRIMARY KEY ("WheelBaseID")
);
CREATE TABLE "VehicleToBedConfig" (
    "VehicleToBedConfigID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "BedConfigID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToBedConfigID"),
    CONSTRAINT "BedConfigVehicletobed_fk" FOREIGN KEY ("BedConfigID")
        REFERENCES "BedConfig" ("BedConfigID"),
    CONSTRAINT "VehicleVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToBodyStyleConfig" (
    "VehicleToBodyStyleConfigID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "BodyStyleConfigID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToBodyStyleConfigID"),
    CONSTRAINT "BodyStyleConfigbasetosubmode_fk" FOREIGN KEY ("BodyStyleConfigID")
        REFERENCES "BodyStyleConfig" ("BodyStyleConfigID"),
    CONSTRAINT "VehicletoBodyStyleConfigVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToDriveType" (
    "VehicleToDriveTypeID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "DriveTypeID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToDriveTypeID"),
    CONSTRAINT "DriveTypeVehicletodri_fk" FOREIGN KEY ("DriveTypeID")
        REFERENCES "DriveType" ("DriveTypeID"),
    CONSTRAINT "VehicletoDriveTypeVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToEngineConfig" (
    "VehicleToEngineConfigID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "EngineConfigID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToEngineConfigID"),
    CONSTRAINT "EngineConfigVehicleto_fk" FOREIGN KEY ("EngineConfigID")
        REFERENCES "EngineConfig2" ("EngineConfigID"),
    CONSTRAINT "VehicletoEngineConfigVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToMfrBodyCode" (
    "VehicleToMfrBodyCodeID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "MfrBodyCodeID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToMfrBodyCodeID"),
    CONSTRAINT "MfrBodyCodeVehicletom_fk" FOREIGN KEY ("MfrBodyCodeID")
        REFERENCES "MfrBodyCode" ("MfrBodyCodeID"),
    CONSTRAINT "VehicletoMfrBodyCodeVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToSpringTypeConfig" (
    "VehicleToSpringTypeConfigID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "SpringTypeConfigID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToSpringTypeConfigID"),
    CONSTRAINT "VehicletoSpringType1_fk" FOREIGN KEY ("SpringTypeConfigID")
        REFERENCES "SpringTypeConfig" ("SpringTypeConfigID"),
    CONSTRAINT "VehicletoSpringTypeConfigVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToSteeringConfig" (
    "VehicleToSteeringConfigID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "SteeringConfigID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToSteeringConfigID"),
    CONSTRAINT "SteeringConfigVehicle_fk" FOREIGN KEY ("SteeringConfigID")
        REFERENCES "SteeringConfig" ("SteeringConfigID"),
    CONSTRAINT "VehicletoSteeringConfigVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToTransmission" (
    "VehicleToTransmissionID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "TransmissionID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToTransmissionID"),
    CONSTRAINT "TransmissionVehicleto_fk" FOREIGN KEY ("TransmissionID")
        REFERENCES "Transmission" ("TransmissionID"),
    CONSTRAINT "VehicletoTransmissionVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToWheelBase" (
    "VehicleToWheelBaseID" INT NOT NULL,
    "VehicleID" INT NOT NULL,
    "WheelBaseID" INT NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToWheelBaseID"),
    CONSTRAINT "VehicletoWheelBaseVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);

CREATE TABLE "VehicleToClass" (
	"VehicleToClassID" int NOT NULL,
	"VehicleID" int NOT NULL,
	"ClassID" int NOT NULL,
	"Source" varchar(10) DEFAULT NULL,
 CONSTRAINT "PK_VehicleToClass" PRIMARY KEY 
(
	"VehicleToClassID" 
),
    CONSTRAINT "classVehicle_fk" FOREIGN KEY ("ClassID")
        REFERENCES "Class" ("ClassID"),
    CONSTRAINT "VehicletoclassVehicle_FK" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID")
);
CREATE TABLE "VehicleToBodyConfig" (
	"VehicleToBodyConfigID" int NOT NULL,
	"VehicleID" int NOT NULL,
	"WheelBaseID" int NOT NULL,
	"BedConfigID" int NOT NULL,
	"BodyStyleConfigID" int NOT NULL,
	"MfrBodyCodeID" int NOT NULL,
    "Source" VARCHAR(10) DEFAULT NULL,
    PRIMARY KEY ("VehicleToBodyConfigID"),
    CONSTRAINT "VehicletobodyconfigVehicle_fk" FOREIGN KEY ("VehicleID")
        REFERENCES "Vehicle" ("VehicleID"),
    CONSTRAINT "VehicletobodyconfigBodyStyleConfig_fk" FOREIGN KEY ("BodyStyleConfigID")
        REFERENCES "BodyStyleConfig" ("BodyStyleConfigID"),
    CONSTRAINT "VehicletobodyconfigBedConfig_fk" FOREIGN KEY ("BedConfigID")
        REFERENCES "BedConfig" ("BedConfigID"),
    CONSTRAINT "VehicletobodyconfigMfrBodyCode_fk" FOREIGN KEY ("MfrBodyCodeID")
        REFERENCES "MfrBodyCode" ("MfrBodyCodeID"),
    CONSTRAINT "VehicletobodyconfigWheelBase_fk" FOREIGN KEY ("WheelBaseID")
        REFERENCES "WheelBase" ("WheelBaseID")
);



CREATE TABLE "ChangeAttributeStates"(
	"ChangeAttributeStateID" int NOT NULL ,
	"ChangeAttributeState" varchar(255) NOT NULL,
PRIMARY KEY("ChangeAttributeStateID")
);

CREATE TABLE "ChangeReasons"(
	"ChangeReasonID" int NOT NULL,
	"ChangeReason" varchar(255) NOT NULL,
    PRIMARY KEY ("ChangeReasonID")
);

CREATE TABLE "ChangeTableNames"(
	"TableNameID" int NOT NULL,
	"TableName" varchar(255) NOT NULL,
	"TableDescription" varchar(1000) NULL,
    PRIMARY KEY ("TableNameID")
);
CREATE TABLE "Changes"(
	"ChangeID" int NOT NULL ,
	"RequestID" int NOT NULL,
	"ChangeReasonID" int NOT NULL,
	"RevDate" TIMESTAMP NULL,
    PRIMARY KEY("ChangeID"),
    CONSTRAINT "FK_ChangeReason_Changes" FOREIGN KEY ("ChangeReasonID")
        REFERENCES "ChangeReasons" ("ChangeReasonID")
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE "ChangeDetails"(
	"ChangeDetailID" int NOT NULL ,
	"ChangeID" int NOT NULL,
	"ChangeAttributeStateID" int NOT NULL,
	"TableNameID" int NOT NULL,
	"PrimaryKeyColumnName" varchar(255) NULL,
	"PrimaryKeyBefore" int NULL,
	"PrimaryKeyAfter" int NULL,
	"ColumnName" varchar(255) NULL,
	"ColumnValueBefore" varchar(1000) NULL,
	"ColumnValueAfter" varchar(1000) NULL,
    PRIMARY KEY ("ChangeDetailID"),
    CONSTRAINT "FK_Changes_ChangeDetails" FOREIGN KEY ("ChangeID")
        REFERENCES "Changes" ("ChangeID")
        ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT "FK_ChangeAttributeStates_ChangeDetails" FOREIGN KEY ("ChangeAttributeStateID")
		REFERENCES "ChangeAttributeStates" ("ChangeAttributeStateID")
		ON DELETE NO ACTION ON UPDATE NO ACTION,
	CONSTRAINT "FK_ChangeTableNames_ChangeDetails" FOREIGN KEY ("TableNameID")
		REFERENCES "ChangeTableNames" ("TableNameID")
		ON DELETE NO ACTION ON UPDATE NO ACTION    
    
);

CREATE TABLE Version(
	VersionDate date NOT NULL
);

CREATE TABLE VCdbChanges(
	VersionDate TIMESTAMP NOT NULL,
	TableName varchar(30) NOT NULL,
	ID int NOT NULL,
	Action varchar(1) NOT NULL
) 
;

CREATE TABLE Attachment(

	AttachmentID int  NOT NULL ,

	AttachmentTypeID int NOT NULL,

	AttachmentFileName varchar(50) NOT NULL,

	AttachmentURL varchar(100) NOT NULL,

	AttachmentDescription varchar(50) NOT NULL,
    Primary key (AttachmentID)
	)

;

CREATE TABLE AttachmentType(

	AttachmentTypeID int  NOT NULL ,

	AttachmentTypeName varchar(20) NOT NULL,
    Primary key(AttachmentTypeID)
	)

;

CREATE TABLE EnglishPhrase(

	EnglishPhraseID int  NOT NULL ,

	EnglishPhrase varchar(100) NOT NULL,
    Primary key(EnglishPhraseID)
	)

;

CREATE TABLE Language(

	LanguageID int NOT NULL ,

	LanguageName varchar(20) NOT NULL,

	DialectName varchar(20) NULL,
    
    Primary key(LanguageID)
	)

;

CREATE TABLE LanguageTranslation(

	LanguageTranslationID int  NOT NULL ,

	EnglishPhraseID int NOT NULL,

	LanguageID int NOT NULL,

	Translation varchar(150) NOT NULL,
    
    Primary KEY (LanguageTranslationID)
	)

;

CREATE TABLE LanguageTranslationAttachment(

	LanguageTranslationAttachmentID int NOT NULL ,

	LanguageTranslationID int NOT NULL,

	AttachmentID int NOT NULL,
    
    Primary key(LanguageTranslationAttachmentID)
	
	)

;
