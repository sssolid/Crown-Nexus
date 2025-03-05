import api from '@/services/api';
import { Product, ProductFilters, ProductListResponse } from '@/types/product';

export default {
  async getProducts(filters?: ProductFilters): Promise<ProductListResponse> {
    return api.get<ProductListResponse>('/products', { params: filters });
  },
  
  async getProduct(id: string): Promise<Product> {
    return api.get<Product>(`/products/${id}`);
  },
  
  async createProduct(product: Partial<Product>): Promise<Product> {
    return api.post<Product>('/products', product);
  },
  
  async updateProduct(id: string, product: Partial<Product>): Promise<Product> {
    return api.put<Product>(`/products/${id}`, product);
  },
  
  async deleteProduct(id: string): Promise<void> {
    return api.delete<void>(`/products/${id}`);
  },
};
