export interface Product {
  id: string;
  sku: string;
  name: string;
  description: string;
  part_number: string;
  attributes: Record<string, any>;
  category_id: string;
  created_at: string;
  updated_at: string;
}

export interface ProductFilters {
  search?: string;
  category_id?: string;
  attributes?: Record<string, any>;
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
