// frontend/src/types/product.ts
export enum DescriptionType {
  SHORT = "Short",
  LONG = "Long",
  KEYWORDS = "Keywords",
  SLANG = "Slang",
  NOTES = "Notes"
}

export enum MarketingType {
  BULLET_POINT = "Bullet Point",
  AD_COPY = "Ad Copy"
}

export enum ProductStatus {
  ACTIVE = "active",
  INACTIVE = "inactive",
  DISCONTINUED = "discontinued",
  OUT_OF_STOCK = "out_of_stock",
  PENDING = "pending"
}

export interface ProductDescription {
  id: string;
  product_id: string;
  description_type: DescriptionType;
  description: string;
  created_at: string;
}

export interface ProductMarketing {
  id: string;
  product_id: string;
  marketing_type: MarketingType;
  content: string;
  position?: number;
  created_at: string;
}

export interface ProductActivity {
  id: string;
  product_id: string;
  status: ProductStatus;
  reason?: string;
  changed_by_id?: string;
  changed_at: string;
  changed_by?: any; // User object
}

export interface ProductSupersession {
  id: string;
  old_product_id: string;
  new_product_id: string;
  reason?: string;
  changed_at: string;
  old_product?: any; // Basic product info
  new_product?: any; // Basic product info
}

export interface ProductMeasurement {
  id: string;
  product_id: string;
  manufacturer_id?: string;
  length?: number;
  width?: number;
  height?: number;
  weight?: number;
  volume?: number;
  dimensional_weight?: number;
  effective_date: string;
  manufacturer?: any; // Manufacturer object
}

export interface ProductStock {
  id: string;
  product_id: string;
  warehouse_id: string;
  quantity: number;
  last_updated: string;
  warehouse: any; // Warehouse object
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  parent_id?: string;
  description?: string;
  created_at: string;
  updated_at: string;
  children?: Category[];
}

export interface Brand {
  id: string;
  name: string;
  parent_company_id?: string;
  created_at: string;
  parent_company?: any; // Company object
}

export interface Product {
  id: string;
  part_number: string;
  part_number_stripped: string;
  application?: string;
  vintage: boolean;
  late_model: boolean;
  soft: boolean;
  universal: boolean;
  is_active: boolean;
  category_id?: string;
  created_at: string;
  updated_at: string;

  // Relationships
  category?: Category;
  descriptions: ProductDescription[];
  marketing: ProductMarketing[];
  activities: ProductActivity[];
  superseded_by: ProductSupersession[];
  supersedes: ProductSupersession[];
  measurements: ProductMeasurement[];
  stock: ProductStock[];
}

export interface ProductFilters {
  search?: string;
  category_id?: string;
  vintage?: boolean;
  late_model?: boolean;
  soft?: boolean;
  universal?: boolean;
  is_active?: boolean;
  page?: number;
  page_size?: number;
}

export interface ProductListResponse {
  items: Product[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// Create DTOs
export interface ProductDescriptionCreateDTO {
  description_type: DescriptionType;
  description: string;
}

export interface ProductMarketingCreateDTO {
  marketing_type: MarketingType;
  content: string;
  position?: number;
}

export interface ProductCreateDTO {
  part_number: string;
  part_number_stripped?: string;
  application?: string;
  vintage?: boolean;
  late_model?: boolean;
  soft?: boolean;
  universal?: boolean;
  is_active?: boolean;
  category_id?: string;
  descriptions?: ProductDescriptionCreateDTO[];
  marketing?: ProductMarketingCreateDTO[];
}

// Update DTOs
export interface ProductDescriptionUpdateDTO {
  description_type?: DescriptionType;
  description?: string;
}

export interface ProductMarketingUpdateDTO {
  marketing_type?: MarketingType;
  content?: string;
  position?: number;
}

export interface ProductUpdateDTO {
  part_number?: string;
  application?: string;
  vintage?: boolean;
  late_model?: boolean;
  soft?: boolean;
  universal?: boolean;
  is_active?: boolean;
  category_id?: string | null;
}

export interface ProductMeasurementCreateDTO {
  manufacturer_id?: string;
  length?: number;
  width?: number;
  height?: number;
  weight?: number;
  volume?: number;
  dimensional_weight?: number;
}

export interface ProductStockCreateDTO {
  warehouse_id: string;
  quantity: number;
}

export interface ProductStockUpdateDTO {
  quantity?: number;
}

export interface ProductSupersessionCreateDTO {
  old_product_id: string;
  new_product_id: string;
  reason?: string;
}
