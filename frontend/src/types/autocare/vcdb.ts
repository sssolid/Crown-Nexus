// src/types/vcdb.ts
/**
 * TypeScript definitions for VCdb (Vehicle Component Database) entities
 */

export interface BaseEntity {
  id: string;
}

export interface Make extends BaseEntity {
  make_id: number;
  name: string;
}

export interface VehicleType extends BaseEntity {
  vehicle_type_id: number;
  name: string;
  vehicle_type_group_id?: number;
}

export interface Model extends BaseEntity {
  model_id: number;
  name: string;
  vehicle_type_id: number;
  vehicle_type?: VehicleType;
}

export interface Year extends BaseEntity {
  year_id: number;
  year: number;
}

export interface SubModel extends BaseEntity {
  submodel_id: number;
  name: string;
}

export interface Region extends BaseEntity {
  region_id: number;
  parent_id?: number;
  abbr?: string;
  name: string;
}

export interface BaseVehicle extends BaseEntity {
  base_vehicle_id: number;
  year_id: number;
  make_id: number;
  model_id: number;
  year?: Year;
  make?: Make;
  model?: Model;
}

export interface DriveType extends BaseEntity {
  drive_type_id: number;
  name: string;
}

export interface BrakeType extends BaseEntity {
  brake_type_id: number;
  name: string;
}

export interface BrakeSystem extends BaseEntity {
  brake_system_id: number;
  name: string;
}

export interface BrakeABS extends BaseEntity {
  brake_abs_id: number;
  name: string;
}

export interface BrakeConfig extends BaseEntity {
  brake_config_id: number;
  front_brake_type_id: number;
  rear_brake_type_id: number;
  brake_system_id: number;
  brake_abs_id: number;
  front_brake_type?: BrakeType;
  rear_brake_type?: BrakeType;
  brake_system?: BrakeSystem;
  brake_abs?: BrakeABS;
}

export interface BodyType extends BaseEntity {
  body_type_id: number;
  name: string;
}

export interface BodyNumDoors extends BaseEntity {
  body_num_doors_id: number;
  num_doors: string;
}

export interface BodyStyleConfig extends BaseEntity {
  body_style_config_id: number;
  body_num_doors_id: number;
  body_type_id: number;
  body_num_doors?: BodyNumDoors;
  body_type?: BodyType;
}

export interface EngineBlock extends BaseEntity {
  engine_block_id: number;
  liter: string;
  cc: string;
  cid: string;
  cylinders: string;
  block_type: string;
}

export interface EngineBoreStroke extends BaseEntity {
  engine_bore_stroke_id: number;
  bore_in: string;
  bore_metric: string;
  stroke_in: string;
  stroke_metric: string;
}

export interface EngineBase extends BaseEntity {
  engine_base_id: number;
  engine_block_id: number;
  engine_bore_stroke_id: number;
  engine_block?: EngineBlock;
  engine_bore_stroke?: EngineBoreStroke;
}

export interface Aspiration extends BaseEntity {
  aspiration_id: number;
  name: string;
}

export interface FuelType extends BaseEntity {
  fuel_type_id: number;
  name: string;
}

export interface CylinderHeadType extends BaseEntity {
  cylinder_head_type_id: number;
  name: string;
}

export interface Valves extends BaseEntity {
  valves_id: number;
  valves_per_engine: string;
}

export interface PowerOutput extends BaseEntity {
  power_output_id: number;
  horsepower: string;
  kilowatt: string;
}

export interface EngineConfig extends BaseEntity {
  engine_config_id: number;
  engine_base_id: number;
  fuel_type_id: number;
  aspiration_id: number;
  engine_base?: EngineBase;
  fuel_type?: FuelType;
  aspiration?: Aspiration;
  power_output?: PowerOutput;
}

export interface TransmissionType extends BaseEntity {
  transmission_type_id: number;
  name: string;
}

export interface TransmissionNumSpeeds extends BaseEntity {
  transmission_num_speeds_id: number;
  num_speeds: string;
}

export interface TransmissionControlType extends BaseEntity {
  transmission_control_type_id: number;
  name: string;
}

export interface TransmissionBase extends BaseEntity {
  transmission_base_id: number;
  transmission_type_id: number;
  transmission_num_speeds_id: number;
  transmission_control_type_id: number;
  transmission_type?: TransmissionType;
  transmission_num_speeds?: TransmissionNumSpeeds;
  transmission_control_type?: TransmissionControlType;
}

export interface Transmission extends BaseEntity {
  transmission_id: number;
  transmission_base_id: number;
  transmission_base?: TransmissionBase;
}

export interface WheelBase extends BaseEntity {
  wheel_base_id: number;
  wheel_base: string;
  wheel_base_metric: string;
}

export interface Vehicle extends BaseEntity {
  vehicle_id: number;
  base_vehicle_id: number;
  submodel_id: number;
  region_id: number;
  base_vehicle?: BaseVehicle;
  submodel?: SubModel;
  region?: Region;
  year?: number;
  make?: string;
  model?: string;
}

export interface VehicleDetail extends Vehicle {
  engines: any[];
  transmissions: any[];
  drive_types: string[];
  body_styles: any[];
  brake_configs: any[];
  wheel_bases: any[];
}

export interface VehicleSearchParams {
  year?: number;
  make?: string;
  model?: string;
  submodel?: string;
  body_type?: string;
  engine_config?: number;
  transmission_type?: number;
  page: number;
  page_size: number;
}

export interface VehicleSearchResponse {
  items: Vehicle[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface EngineDetail {
  id: number;
  liter: string;
  cylinders: string;
  fuel_type: string;
  aspiration: string;
  power?: {
    horsepower: string;
    kilowatt: string;
  };
}

export interface TransmissionDetail {
  id: number;
  type: string;
  speeds: string;
  control_type: string;
  manufacturer?: string;
  code?: string;
}

export interface VehicleConfigurationResponse {
  engines: EngineDetail[];
  transmissions: TransmissionDetail[];
  drive_types: DriveType[];
  body_styles: {
    id: number;
    type: string;
    doors: string;
  }[];
  brake_configs: {
    id: number;
    front_type: string;
    rear_type: string;
    system: string;
    abs: string;
  }[];
  wheel_bases: {
    id: number;
    wheel_base: string;
    wheel_base_metric: string;
  }[];
}
