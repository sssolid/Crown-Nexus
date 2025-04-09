// frontend/src/services/product.ts
/**
 * Product API service.
 *
 * This service provides methods for interacting with the product API:
 * - Fetching products and categories
 * - Creating, updating, and deleting products
 * - Managing product descriptions, marketing, and other related entities
 * - Handling product filters and pagination
 *
 * It builds on the base API service and adds product-specific functionality.
 */

import api, {ApiService} from '@/services/api';
import {
  Brand,
  BrandCreateDTO,
  BrandUpdateDTO,
  Product,
  ProductCreateDTO,
  ProductDescriptionCreateDTO,
  ProductDescriptionUpdateDTO,
  ProductFilters,
  ProductListResponse,
  ProductMarketingCreateDTO,
  ProductMarketingUpdateDTO,
  ProductMeasurementCreateDTO,
  ProductStockCreateDTO,
  ProductStockUpdateDTO,
  ProductSupersessionCreateDTO,
  ProductUpdateDTO
} from '@/types/product';

/**
 * Product service for API interactions.
 */
export class ProductService extends ApiService  {
  /**
   * Get a paginated list of products with optional filtering.
   *
   * @param filters - Optional filter parameters
   * @returns Promise with product list response
   */
  async getProducts(filters?: ProductFilters): Promise<ProductListResponse> {
    return api.get<ProductListResponse>('/products/', { params: filters });
  }

  /**
   * Get a single product by ID.
   *
   * @param id - Product ID
   * @returns Promise with product details
   */
  async getProduct(id: string): Promise<Product> {
    return api.get<Product>(`/products/${id}`);
  }

  /**
   * Create a new product.
   *
   * @param product - Product data
   * @returns Promise with created product
   */
  async createProduct(product: ProductCreateDTO): Promise<Product> {
    return api.post<Product>('/products', product);
  }

  /**
   * Update an existing product.
   *
   * @param id - Product ID
   * @param product - Updated product data
   * @returns Promise with updated product
   */
  async updateProduct(id: string, product: ProductUpdateDTO): Promise<Product> {
    return api.put<Product>(`/products/${id}`, product);
  }

  /**
   * Delete a product.
   *
   * @param id - Product ID
   * @returns Promise with deletion response
   */
  async deleteProduct(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/${id}`);
  }

  /**
   * Add a description to a product.
   *
   * @param productId - Product ID
   * @param description - Description data
   * @returns Promise with created description
   */
  async addProductDescription(productId: string, description: ProductDescriptionCreateDTO): Promise<any> {
    return api.post<any>(`/products/${productId}/descriptions`, description);
  }

  /**
   * Update a product description.
   *
   * @param productId - Product ID
   * @param descriptionId - Description ID
   * @param description - Updated description data
   * @returns Promise with updated description
   */
  async updateProductDescription(
    productId: string,
    descriptionId: string,
    description: ProductDescriptionUpdateDTO
  ): Promise<any> {
    return api.put<any>(`/products/${productId}/descriptions/${descriptionId}`, description);
  }

  /**
   * Delete a product description.
   *
   * @param productId - Product ID
   * @param descriptionId - Description ID
   * @returns Promise with deletion response
   */
  async deleteProductDescription(productId: string, descriptionId: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/${productId}/descriptions/${descriptionId}`);
  }

  /**
   * Add marketing content to a product.
   *
   * @param productId - Product ID
   * @param marketing - Marketing data
   * @returns Promise with created marketing content
   */
  async addProductMarketing(productId: string, marketing: ProductMarketingCreateDTO): Promise<any> {
    return api.post<any>(`/products/${productId}/marketing`, marketing);
  }

  /**
   * Update product marketing content.
   *
   * @param productId - Product ID
   * @param marketingId - Marketing ID
   * @param marketing - Updated marketing data
   * @returns Promise with updated marketing content
   */
  async updateProductMarketing(
    productId: string,
    marketingId: string,
    marketing: ProductMarketingUpdateDTO
  ): Promise<any> {
    return api.put<any>(`/products/${productId}/marketing/${marketingId}`, marketing);
  }

  /**
   * Delete product marketing content.
   *
   * @param productId - Product ID
   * @param marketingId - Marketing ID
   * @returns Promise with deletion response
   */
  async deleteProductMarketing(productId: string, marketingId: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/${productId}/marketing/${marketingId}`);
  }

  /**
   * Add measurements to a product.
   *
   * @param productId - Product ID
   * @param measurement - Measurement data
   * @returns Promise with created measurement
   */
  async addProductMeasurement(productId: string, measurement: ProductMeasurementCreateDTO): Promise<any> {
    return api.post<any>(`/products/${productId}/measurements`, measurement);
  }

  /**
   * Add stock information to a product.
   *
   * @param productId - Product ID
   * @param stock - Stock data
   * @returns Promise with created stock information
   */
  async addProductStock(productId: string, stock: ProductStockCreateDTO): Promise<any> {
    return api.post<any>(`/products/${productId}/stock`, stock);
  }

  /**
   * Update product stock information.
   *
   * @param productId - Product ID
   * @param stockId - Stock ID
   * @param stock - Updated stock data
   * @returns Promise with updated stock information
   */
  async updateProductStock(
    productId: string,
    stockId: string,
    stock: ProductStockUpdateDTO
  ): Promise<any> {
    return api.put<any>(`/products/${productId}/stock/${stockId}`, stock);
  }

  /**
   * Create a product supersession.
   *
   * @param productId - Product ID
   * @param supersession - Supersession data
   * @returns Promise with created supersession
   */
  async createProductSupersession(productId: string, supersession: ProductSupersessionCreateDTO): Promise<any> {
    return api.post<any>(`/products/${productId}/supersessions`, supersession);
  }

  /**
   * Delete a product supersession.
   *
   * @param productId - Product ID
   * @param supersessionId - Supersession ID
   * @returns Promise with deletion response
   */
  async deleteProductSupersession(productId: string, supersessionId: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/${productId}/supersessions/${supersessionId}`);
  }

  /**
   * Get a list of all brands.
   *
   * @returns Promise with list of brands
   */
  async getBrands(): Promise<Brand[]> {
    return api.get<Brand[]>('/products/brands/');
  }

  /**
   * Get a single brand by ID.
   *
   * @param id - Brand ID
   * @returns Promise with brand details
   */
  async getBrand(id: string): Promise<Brand> {
    return api.get<Brand>(`/products/brands/${id}`);
  }

  /**
   * Create a new brand.
   *
   * @param brand - Brand data
   * @returns Promise with created brand
   */
  async createBrand(brand: BrandCreateDTO): Promise<Brand> {
    return api.post<Brand>('/products/brands/', brand);
  }

  /**
   * Update an existing brand.
   *
   * @param id - Brand ID
   * @param brand - Updated brand data
   * @returns Promise with updated brand
   */
  async updateBrand(id: string, brand: BrandUpdateDTO): Promise<Brand> {
    return api.put<Brand>(`/products/brands/${id}`, brand);
  }

  /**
   * Delete a brand.
   *
   * @param id - Brand ID
   * @returns Promise with deletion response
   */
  async deleteBrand(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/products/brands/${id}`);
  }
}

// Create and export a singleton instance
export const productService = new ProductService();
export default productService;
