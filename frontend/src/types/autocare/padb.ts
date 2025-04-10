// src/types/padb.ts
/**
 * TypeScript definitions for PAdb (Part Attribute Database) entities
 */

import { BaseEntity } from './vcdb.ts';

export interface PAdbStats {
  totalAttributes: number;
  metadataCount: number;
  validValueCount: number;
  uomCodeCount: number;
}

export interface PartAttribute extends BaseEntity {
  pa_id: number;
  pa_name?: string;
  pa_descr?: string;
}

export interface MetaData extends BaseEntity {
  meta_id: number;
  meta_name?: string;
  meta_descr?: string;
  meta_format?: string;
  data_type?: string;
  min_length?: number;
  max_length?: number;
}

export interface MeasurementGroup extends BaseEntity {
  measurement_group_id: number;
  measurement_group_name?: string;
}

export interface MetaUOMCode extends BaseEntity {
  meta_uom_id: number;
  uom_code?: string;
  uom_description?: string;
  uom_label?: string;
  measurement_group_id: number;
}

export interface ValidValue extends BaseEntity {
  valid_value_id: number;
  valid_value: string;
}

export interface PartAttributeAssignment extends BaseEntity {
  papt_id: number;
  part_terminology_id: number;
  pa_id: number;
  meta_id: number;
  attribute?: PartAttribute;
  metadata?: MetaData;
}

export interface AttributeWithMetadata {
  assignment_id: number;
  attribute: {
    id: number;
    name?: string;
    description?: string;
  };
  metadata: {
    id: number;
    name?: string;
    description?: string;
    format?: string;
    data_type?: string;
  };
  valid_values: {
    id: number;
    value: string;
  }[];
  uom_codes: {
    id: number;
    code?: string;
    description?: string;
    label?: string;
  }[];
}

export interface PartAttributeDetail extends BaseEntity {
  pa_id: number;
  name?: string;
  description?: string;
  metadata_assignments: {
    assignment_id: number;
    part_terminology_id: number;
    meta_id: number;
    name?: string;
    description?: string;
    data_type?: string;
  }[];
}

export interface PartAttributesResponse {
  part_terminology_id: number;
  attributes: AttributeWithMetadata[];
}

export interface AttributeSearchParams {
  search_term: string;
  page: number;
  page_size: number;
}

export interface AttributeSearchResponse {
  items: PartAttribute[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
