// src/types/pcdb.ts
/**
 * TypeScript definitions for PCdb (Product Component Database) entities
 */

import { BaseEntity } from './vcdb.ts';

export interface Category extends BaseEntity {
  category_id: number;
  category_name: string;
}

export interface SubCategory extends BaseEntity {
  subcategory_id: number;
  subcategory_name: string;
}

export interface Position extends BaseEntity {
  position_id: number;
  position: string;
}

export interface Part extends BaseEntity {
  part_terminology_id: number;
  part_terminology_name: string;
  parts_description_id?: number;
}

export interface PartDetail extends Part {
  description?: string;
  categories: {
    category: Category;
    subcategory: SubCategory;
  }[];
  positions: {
    id: number;
    name: string;
  }[];
  superseded_by: {
    id: number;
    name: string;
  }[];
  supersedes: {
    id: number;
    name: string;
  }[];
}

export interface PartSearchParams {
  search_term: string;
  categories?: number[];
  page: number;
  page_size: number;
}

export interface PartSearchResponse {
  items: Part[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
