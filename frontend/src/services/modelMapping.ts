// frontend/src/services/modelMapping.ts
/**
 * Model Mapping API service.
 *
 * This service provides methods for interacting with the model mapping API:
 * - Fetching model mappings
 * - Creating, updating, and deleting model mappings
 * - Uploading model mappings from JSON file
 * - Refreshing model mappings cache
 */

import api from '@/services/api';

export interface ModelMapping {
  id: number;
  pattern: string;
  mapping: string;
  priority: number;
  active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface ModelMappingListResponse {
  items: ModelMapping[];
  total: number;
}

export interface ModelMappingRequest {
  pattern: string;
  mapping: string;
  priority?: number;
  active?: boolean;
}

/**
 * Model Mapping service for API interactions.
 */
const modelMappingService = {
  /**
   * Get a paginated list of model mappings with optional filtering.
   *
   * @param skip - Number of items to skip
   * @param limit - Maximum number of items to return
   * @param pattern - Optional pattern filter
   * @returns Promise with model mapping list response
   */
  async getModelMappings(skip = 0, limit = 100, pattern?: string): Promise<ModelMappingListResponse> {
    return api.get<ModelMappingListResponse>('/fitment/model-mappings', {
      params: { skip, limit, pattern }
    });
  },

  /**
   * Get a single model mapping by ID.
   *
   * @param id - Model mapping ID
   * @returns Promise with model mapping details
   */
  async getModelMapping(id: number): Promise<ModelMapping> {
    const response = await this.getModelMappings(0, 1000);
    const mapping = response.items.find(m => m.id === id);
    if (!mapping) {
      throw new Error(`Model mapping with ID ${id} not found`);
    }
    return mapping;
  },

  /**
   * Create a new model mapping.
   *
   * @param mapping - Model mapping data
   * @returns Promise with created model mapping
   */
  async createModelMapping(mapping: ModelMappingRequest): Promise<ModelMapping> {
    return api.post<ModelMapping>('/fitment/model-mappings', mapping);
  },

  /**
   * Update an existing model mapping.
   *
   * @param id - Model mapping ID
   * @param mapping - Updated model mapping data
   * @returns Promise with updated model mapping
   */
  async updateModelMapping(id: number, mapping: ModelMappingRequest): Promise<ModelMapping> {
    return api.put<ModelMapping>(`/fitment/model-mappings/${id}`, mapping);
  },

  /**
   * Delete a model mapping.
   *
   * @param id - Model mapping ID
   * @returns Promise with deletion response
   */
  async deleteModelMapping(id: number): Promise<{message: string}> {
    return api.delete<{message: string}>(`/fitment/model-mappings/${id}`);
  },

  /**
   * Upload model mappings from JSON file.
   *
   * @param file - JSON file to upload
   * @returns Promise with upload response
   */
  async uploadModelMappings(file: File): Promise<{message: string, mapping_count: number}> {
    const formData = new FormData();
    formData.append('file', file);
    return api.uploadFile<{message: string, mapping_count: number}>('/fitment/upload-model-mappings', formData);
  },

  /**
   * Refresh model mappings cache.
   *
   * @returns Promise with refresh response
   */
  async refreshMappings(): Promise<{message: string}> {
    return api.post<{message: string}>('/fitment/refresh-mappings');
  }
};

export default modelMappingService;
