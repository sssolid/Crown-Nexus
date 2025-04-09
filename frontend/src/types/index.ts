// src/types/index.ts
/**
 * Export all types
 */
export * from './chat';
export * from './fitment';
export * from './media';
export * from './product';
export * from './user';
export * from './autocare/vcdb.ts';
export * from './autocare/pcdb.ts';
export * from './autocare/padb.ts';
export * from './autocare/qdb.ts';

export interface PaginationParams {
  page: number;
  page_size: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface ApiError {
  status?: number;
  message: string;
  details?: Record<string, any>;
}
