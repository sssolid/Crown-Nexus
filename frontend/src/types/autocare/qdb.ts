// src/types/qdb.ts
/**
 * TypeScript definitions for Qdb (Qualifier Database) entities
 */

import { BaseEntity } from './vcdb.ts';

export interface QdbStats {
  totalQualifiers: number;
  qualifierTypeCount: number;
  languageCount: number;
  groupCount: number;
}

export interface QualifierType extends BaseEntity {
  qualifier_type_id: number;
  qualifier_type?: string;
}

export interface Language extends BaseEntity {
  language_id: number;
  language_name?: string;
  dialect_name?: string;
}

export interface QualifierTranslation extends BaseEntity {
  qualifier_translation_id: number;
  qualifier_id: number;
  language_id: number;
  translation_text: string;
  language?: {
    id: number;
    name?: string;
    dialect?: string;
  };
}

export interface GroupNumber extends BaseEntity {
  group_number_id: number;
  group_description: string;
}

export interface QualifierGroup extends BaseEntity {
  qualifier_group_id: number;
  group_number_id: number;
  qualifier_id: number;
  number?: {
    id: number;
    description: string;
  };
}

export interface Qualifier extends BaseEntity {
  qualifier_id: number;
  qualifier_text?: string;
  example_text?: string;
  qualifier_type_id: number;
  new_qualifier_id?: number;
}

export interface QualifierDetail extends Qualifier {
  type: {
    id: number;
    name?: string;
  };
  translations: {
    id: number;
    language: {
      id: number;
      name?: string;
      dialect?: string;
    };
    text: string;
  }[];
  groups: {
    id: number;
    number: {
      id: number;
      description: string;
    };
  }[];
  superseded_by?: {
    id: number;
    text?: string;
  };
  when_modified: string;
}

export interface QualifierSearchParams {
  search_term: string;
  qualifier_type_id?: number;
  language_id?: number;
  page: number;
  page_size: number;
}

export interface QualifierSearchResponse {
  items: Qualifier[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
