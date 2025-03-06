// frontend/src/services/product.ts
/**
 * Product API service.
 *
 * This service provides methods for interacting with the product API:
 * - Fetching products and categories
 * - Creating, updating, and deleting products
 * - Handling product filters and pagination
 *
 * It builds on the base API service and adds product-specific functionality.
 */

import api from '@/services/api';
import { Product, ProductFilters, ProductListResponse } from '@/types/product';
import { Category } from '@/types/category';

/**
 * Product service for API interactions.
 */
const productService = {
  /**
   * Get a paginated list of products with optional filtering.
   *
   * @param filters - Optional filter parameters
   * @returns Promise with product list response
   */
  async getProducts(filters?: ProductFilters): Promise<ProductListResponse> {
    return api.get<ProductListResponse>('/products', { params: filters });
  },

  /**
   * Get a single product by ID.
   *
   * @param id - Product ID
   * @returns Promise with product details
   */
  async getProduct(id: string): Promise<Product> {
    return api.get<Product>(`/products/${id}`);
  },

  /**
   * Create a new product.
   *
   * @param product - Product data
   * @returns Promise with created product
   */
  async createProduct(product: Partial<Product>): Promise<Product> {
    return api.post<Product>('/products', product);
  },

  /**
   * Update an existing product.
   *
   * @param id - Product ID
   * @param product - Updated product data
   * @returns Promise with updated product
   */
  async updateProduct(id: string, product: Partial<Product>): Promise<Product> {
    return api.put<Product>(`/products/${id}`, product);
  },

  /**
   * Delete a product.
   *
   * @param id - Product ID
   * @returns Promise with deletion response
   */
  async deleteProduct(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/${id}`);
  },

  /**
   * Get a list of all product categories.
   *
   * @returns Promise with list of categories
   */
  async getCategories(): Promise<Category[]> {
    return api.get<Category[]>('/products/categories/');
  },

  /**
   * Get a single category by ID.
   *
   * @param id - Category ID
   * @returns Promise with category details
   */
  async getCategory(id: string): Promise<Category> {
    return api.get<Category>(`/products/categories/${id}`);
  },

  /**
   * Create a new category.
   *
   * @param category - Category data
   * @returns Promise with created category
   */
  async createCategory(category: Partial<Category>): Promise<Category> {
    return api.post<Category>('/products/categories/', category);
  },

  /**
   * Update an existing category.
   *
   * @param id - Category ID
   * @param category - Updated category data
   * @returns Promise with updated category
   */
  async updateCategory(id: string, category: Partial<Category>): Promise<Category> {
    return api.put<Category>(`/products/categories/${id}`, category);
  },

  /**
   * Delete a category.
   *
   * @param id - Category ID
   * @returns Promise with deletion response
   */
  async deleteCategory(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/categories/${id}`);
  },

  /**
   * Get product fitments.
   *
   * @param productId - Product ID
   * @returns Promise with list of fitments for the product
   */
  async getProductFitments(productId: string): Promise<any[]> {
    return api.get<any[]>(`/products/${productId}/fitments`);
  },
};

export default productService;
