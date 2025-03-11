// frontend/src/services/media.ts
/**
 * Media API service.
 *
 * This service provides methods for interacting with the media API:
 * - Uploading, fetching, and deleting media files
 * - Managing media associations with products
 * - Handling media metadata
 * - Processing media operations like resizing and optimization
 */

import api from '@/services/api';
import { Media } from '@/types/media';

// Media list response interface
export interface MediaListResponse {
  items: Media[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

// Media filter parameters
export interface MediaFilters {
  product_id?: string;
  file_type?: string;
  search?: string;
  page?: number;
  page_size?: number;
}

// Media metadata interface
export interface MediaMetadata {
  width?: number;
  height?: number;
  size: number;
  mime_type: string;
  extension: string;
  created_at: string;
  modified_at: string;
  additional_info?: Record<string, any>;
}

/**
 * Media service for API interactions.
 */
const mediaService = {
  /**
   * Get a paginated list of media with optional filtering.
   *
   * @param filters - Optional filter parameters
   * @returns Promise with media list response
   */
  async getMediaList(filters?: MediaFilters): Promise<MediaListResponse> {
    return api.get<MediaListResponse>('/media', { params: filters });
  },

  /**
   * Get a single media item by ID.
   *
   * @param id - Media ID
   * @returns Promise with media details
   */
  async getMedia(id: string): Promise<Media> {
    return api.get<Media>(`/media/${id}`);
  },

  /**
   * Upload a new media file.
   *
   * @param file - File to upload
   * @param productId - Optional product ID to associate with
   * @returns Promise with uploaded media
   */
  async uploadMedia(file: File, productId?: string): Promise<Media> {
    const formData = new FormData();
    formData.append('file', file);

    if (productId) {
      formData.append('product_id', productId);
    }

    return api.uploadFile<Media>('/media/upload', formData);
  },

  /**
   * Upload multiple media files.
   *
   * @param files - Files to upload
   * @param productId - Optional product ID to associate with
   * @returns Promise with array of uploaded media
   */
  async uploadMultipleMedia(files: File[], productId?: string): Promise<Media[]> {
    const formData = new FormData();

    files.forEach((file, index) => {
      formData.append(`files[${index}]`, file);
    });

    if (productId) {
      formData.append('product_id', productId);
    }

    return api.uploadFile<Media[]>('/media/upload-multiple', formData);
  },

  /**
   * Update media metadata.
   *
   * @param id - Media ID
   * @param metadata - Updated metadata
   * @returns Promise with updated media
   */
  async updateMedia(id: string, metadata: Partial<Media>): Promise<Media> {
    return api.put<Media>(`/media/${id}`, metadata);
  },

  /**
   * Delete a media item.
   *
   * @param id - Media ID
   * @returns Promise with deletion response
   */
  async deleteMedia(id: string): Promise<{message: string}> {
    return api.delete<{message: string}>(`/media/${id}`);
  },

  /**
   * Associate media with a product.
   *
   * @param mediaId - Media ID
   * @param productId - Product ID
   * @returns Promise with the updated media
   */
  async associateMediaWithProduct(mediaId: string, productId: string): Promise<Media> {
    return api.post<Media>(`/media/${mediaId}/associate`, { product_id: productId });
  },

  /**
   * Remove product association from media.
   *
   * @param mediaId - Media ID
   * @returns Promise with the updated media
   */
  async removeProductAssociation(mediaId: string): Promise<Media> {
    return api.post<Media>(`/media/${mediaId}/disassociate`, {});
  },

  /**
   * Get all media associated with a product.
   *
   * @param productId - Product ID
   * @returns Promise with array of media
   */
  async getProductMedia(productId: string): Promise<Media[]> {
    return api.get<Media[]>(`/products/${productId}/media`);
  },

  /**
   * Set primary media for a product.
   *
   * @param productId - Product ID
   * @param mediaId - Media ID to set as primary
   * @returns Promise with result
   */
  async setPrimaryMedia(productId: string, mediaId: string): Promise<{message: string}> {
    return api.post<{message: string}>(`/products/${productId}/media/primary`, { media_id: mediaId });
  },

  /**
   * Reorder product media.
   *
   * @param productId - Product ID
   * @param mediaIds - Array of media IDs in desired order
   * @returns Promise with result
   */
  async reorderProductMedia(productId: string, mediaIds: string[]): Promise<{message: string}> {
    return api.post<{message: string}>(`/products/${productId}/media/reorder`, { media_ids: mediaIds });
  },

  /**
   * Get media metadata.
   *
   * @param id - Media ID
   * @returns Promise with media metadata
   */
  async getMediaMetadata(id: string): Promise<MediaMetadata> {
    return api.get<MediaMetadata>(`/media/${id}/metadata`);
  },

  /**
   * Generate a thumbnail or resized version of an image.
   *
   * @param id - Media ID
   * @param width - Desired width
   * @param height - Desired height
   * @returns Promise with the URL of the resized image
   */
  async getResizedImage(id: string, width: number, height: number): Promise<{url: string}> {
    return api.get<{url: string}>(`/media/${id}/resize`, {
      params: { width, height }
    });
  }
};

export default mediaService;
