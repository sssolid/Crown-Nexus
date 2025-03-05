export interface Fitment {
  id: string;
  year: number;
  make: string;
  model: string;
  engine: string;
  transmission: string;
  attributes: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface FitmentFilters {
  year?: number;
  make?: string;
  model?: string;
  engine?: string;
  transmission?: string;
  attributes?: Record<string, any>;
  page?: number;
  page_size?: number;
}

export interface FitmentListResponse {
  items: Fitment[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
