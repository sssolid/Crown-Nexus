// src/services/pcdb.service.ts
/**
 * Service for interacting with the PCdb (Product Component Database) API
 */
import { ApiService } from '../api';
import {
  Category,
  SubCategory,
  Part,
  PartDetail,
  PartSearchParams,
  PartSearchResponse,
  Position
} from '@/types';

export class PCdbService extends ApiService {
  private readonly baseUrl = '/pcdb';

  /**
   * Get the current PCdb version
   */
  async getVersion(): Promise<string> {
    return this.get<string>(`${this.baseUrl}/version`);
  }

  /**
   * Get all categories
   */
  async getCategories(): Promise<Category[]> {
    return this.get<Category[]>(`${this.baseUrl}/categories`);
  }

  /**
   * Get subcategories for a specific category
   * @param categoryId The category ID
   */
  async getSubcategoriesByCategory(categoryId: number): Promise<SubCategory[]> {
    return this.get<SubCategory[]>(`${this.baseUrl}/categories/${categoryId}/subcategories`);
  }

  /**
   * Search for parts
   * @param params Search parameters
   */
  async searchParts(params: PartSearchParams): Promise<PartSearchResponse> {
    return this.get<PartSearchResponse>(
      `${this.baseUrl}/parts/search${this.buildQueryParams(params)}`
    );
  }

  /**
   * Get part details
   * @param partTerminologyId The part terminology ID
   */
  async getPartDetails(partTerminologyId: number): Promise<PartDetail> {
    return this.get<PartDetail>(`${this.baseUrl}/parts/${partTerminologyId}`);
  }

  /**
   * Get parts by category
   * @param categoryId The category ID
   * @param page The page number
   * @param pageSize The page size
   */
  async getPartsByCategory(categoryId: number, page: number = 1, pageSize: number = 20): Promise<PartSearchResponse> {
    return this.get<PartSearchResponse>(
      `${this.baseUrl}/categories/${categoryId}/parts${this.buildQueryParams({ page, page_size: pageSize })}`
    );
  }

  /**
   * Search for categories
   * @param searchTerm The search term
   */
  async searchCategories(searchTerm: string): Promise<Category[]> {
    return this.get<Category[]>(
      `${this.baseUrl}/categories/search${this.buildQueryParams({ search_term: searchTerm })}`
    );
  }

  /**
   * Get all positions
   */
  async getPositions(): Promise<Position[]> {
    return this.get<Position[]>(`${this.baseUrl}/positions`);
  }

  /**
   * Get positions for a specific part
   * @param partTerminologyId The part terminology ID
   */
  async getPositionsByPart(partTerminologyId: number): Promise<Position[]> {
    return this.get<Position[]>(`${this.baseUrl}/parts/${partTerminologyId}/positions`);
  }

  /**
   * Get part supersessions
   * @param partTerminologyId The part terminology ID
   */
  async getPartSupersessions(partTerminologyId: number): Promise<{ superseded_by: Part[]; supersedes: Part[] }> {
    return this.get<{ superseded_by: Part[]; supersedes: Part[] }>(`${this.baseUrl}/parts/${partTerminologyId}/supersessions`);
  }
}

// Create and export a singleton instance
export const pcdbService = new PCdbService();
export default pcdbService;
