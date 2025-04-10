// src/services/qdb.service.ts
/**
 * Service for interacting with the Qdb (Qualifier Database) API
 */
import { ApiService } from '../api';
import {
  QualifierType,
  Language,
  Qualifier,
  QualifierDetail,
  QualifierSearchParams,
  QualifierSearchResponse,
  GroupNumber, QdbStats
} from '@/types';

export class QdbService extends ApiService {
  private readonly baseUrl = '/autocare/qdb';

  /**
   * Get the current Qdb version
   */
  async getVersion(): Promise<string> {
    return this.get<string>(`${this.baseUrl}/version`);
  }

    /**
   * Fetches statistical data from the specified endpoint.
   *
   * @return {Promise<any>} A promise that resolves to the statistical data fetched from the server.
   */
  async getStats(): Promise<QdbStats> {
    return this.get<QdbStats>(`${this.baseUrl}/stats`);
  }

  /**
   * Get all qualifier types
   */
  async getQualifierTypes(): Promise<QualifierType[]> {
    return this.get<QualifierType[]>(`${this.baseUrl}/qualifier-types`);
  }

  /**
   * Get all languages
   */
  async getLanguages(): Promise<Language[]> {
    return this.get<Language[]>(`${this.baseUrl}/languages`);
  }

  /**
   * Search for qualifiers
   * @param params Search parameters
   */
  async searchQualifiers(params: QualifierSearchParams): Promise<QualifierSearchResponse> {
    return this.get<QualifierSearchResponse>(
      `${this.baseUrl}/qualifiers/search${this.buildQueryParams(params)}`
    );
  }

  /**
   * Get qualifier details
   * @param qualifierId The qualifier ID
   */
  async getQualifierDetails(qualifierId: number): Promise<QualifierDetail> {
    return this.get<QualifierDetail>(`${this.baseUrl}/qualifiers/${qualifierId}`);
  }

  /**
   * Get all group numbers
   */
  async getGroupNumbers(): Promise<GroupNumber[]> {
    return this.get<GroupNumber[]>(`${this.baseUrl}/groups`);
  }

  /**
   * Get qualifiers by group
   * @param groupNumberId The group number ID
   * @param page The page number
   * @param pageSize The page size
   */
  async getQualifiersByGroup(
    groupNumberId: number,
    page: number = 1,
    pageSize: number = 20
  ): Promise<QualifierSearchResponse> {
    return this.get<QualifierSearchResponse>(
      `${this.baseUrl}/groups/${groupNumberId}/qualifiers${this.buildQueryParams({ page, page_size: pageSize })}`
    );
  }

  /**
   * Get translations for a qualifier
   * @param qualifierId The qualifier ID
   * @param languageId Optional language ID to filter translations
   */
  async getQualifierTranslations(
    qualifierId: number,
    languageId?: number
  ): Promise<{ id: number; language: { id: number; name: string; dialect?: string }; text: string }[]> {
    const url = `${this.baseUrl}/qualifiers/${qualifierId}/translations`;
    const params = languageId ? this.buildQueryParams({ language_id: languageId }) : '';
    return this.get<{ id: number; language: { id: number; name: string; dialect?: string }; text: string }[]>(url + params);
  }

  /**
   * Get groups for a qualifier
   * @param qualifierId The qualifier ID
   */
  async getQualifierGroups(
    qualifierId: number
  ): Promise<{ id: number; number: { id: number; description: string } }[]> {
    return this.get<{ id: number; number: { id: number; description: string } }[]>(
      `${this.baseUrl}/qualifiers/${qualifierId}/groups`
    );
  }
}

// Create and export a singleton instance
export const qdbService = new QdbService();
export default qdbService;
