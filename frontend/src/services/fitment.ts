// frontend/src/services/fitment.ts
/**
 * Fitment API service.
 *
 * This service provides methods for interacting with the fitment API:
 * - Fetching fitments with filtering
 * - Creating, updating, and deleting fitments
 * - Managing product-fitment associations
 *
 * It builds on the base API service and adds fitment-specific functionality.
 */

import api from '@/services/api';
import { Fitment, FitmentFilters, FitmentListResponse } from '@/types/fitment';
import { Product } from '@/types/product';

/**
 * Fitment service for API interactions.
 */
const fitmentService = {
  /**
   * Get a paginated list of fitments with optional filtering.
   *
   * @param filters - Optional filter parameters
   * @returns Promise with fitment list response
   */
  async getFitments(filters?: FitmentFilters): Promise<FitmentListResponse> {
    return api.get<FitmentListResponse>('/fitments', { params: filters });
  },

  /**
   * Get a single fitment by ID.
   *
   * @param id - Fitment ID
   * @returns Promise with fitment details
   */
  async getFitment(id: string): Promise<Fitment> {
    return api.get<Fitment>(`/fitments/${id}`);
  },

  /**
   * Create a new fitment.
   *
   * @param fitment - Fitment data
   * @returns Promise with created fitment
   */
  async createFitment(fitment: Partial<Fitment>): Promise<Fitment> {
    return api.post<Fitment>('/fitments', fitment);
  },

  /**
   * Update an existing fitment.
   *
   * @param id - Fitment ID
   * @param fitment - Updated fitment data
   * @returns Promise with updated fitment
   */
  async updateFitment(id: string, fitment: Partial<Fitment>): Promise<Fitment> {
    return api.put<Fitment>(`/fitments/${id}`, fitment);
  },

  /**
   * Delete a fitment.
   *
   * @param id - Fitment ID
   * @returns Promise with deletion response
   */
  async deleteFitment(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/fitments/${id}`);
  },

  /**
   * Get products associated with a fitment.
   *
   * @param fitmentId - Fitment ID
   * @returns Promise with list of associated products
   */
  async getFitmentProducts(fitmentId: string): Promise<Product[]> {
    return api.get<Product[]>(`/fitments/${fitmentId}/products`);
  },

  /**
   * Associate a product with a fitment.
   *
   * @param fitmentId - Fitment ID
   * @param productId - Product ID
   * @returns Promise with the association result
   */
  async associateProduct(fitmentId: string, productId: string): Promise<{message: string}> {
    return api.post<{message: string}>(`/fitments/${fitmentId}/products`, { product_id: productId });
  },

  /**
   * Remove a product association from a fitment.
   *
   * @param fitmentId - Fitment ID
   * @param productId - Product ID
   * @returns Promise with the dissociation result
   */
  async removeProductAssociation(fitmentId: string, productId: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/fitments/${fitmentId}/products/${productId}`);
  },

  /**
   * Get distinct values for a fitment attribute.
   * Useful for populating dropdowns with existing values.
   *
   * @param attribute - The attribute to get distinct values for (e.g., 'make', 'model')
   * @returns Promise with array of distinct values
   */
  async getDistinctValues(attribute: string): Promise<string[]> {
    return api.get<string[]>(`/fitments/distinct/${attribute}`);
  },

  /**
   * Bulk import fitments from a file.
   *
   * @param file - FormData containing the file to import
   * @returns Promise with import results
   */
  async importFitments(file: FormData): Promise<{message: string, imported: number, errors: number}> {
    return api.uploadFile<{message: string, imported: number, errors: number}>('/fitments/import', file);
  },

  /**
   * Export fitments to a CSV file.
   *
   * @param filters - Optional filter parameters to limit the export
   * @returns Promise with file URL
   */
  async exportFitments(filters?: FitmentFilters): Promise<{url: string}> {
    return api.get<{url: string}>('/fitments/export', { params: filters });
  }
};

export default fitmentService;
