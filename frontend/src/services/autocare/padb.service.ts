// src/services/padb.service.ts
/**
 * Service for interacting with the PAdb (Part Attribute Database) API
 */
import { ApiService } from '../api';
import {
  PartAttribute,
  PartAttributeDetail,
  AttributeSearchParams,
  AttributeSearchResponse,
  PartAttributesResponse
} from '@/types';

export class PAdbService extends ApiService {
  private readonly baseUrl = '/autocare/padb';

  /**
   * Get the current PAdb version
   */
  async getVersion(): Promise<string> {
    return this.get<string>(`${this.baseUrl}/version`);
  }

  /**
   * Search for part attributes
   * @param params Search parameters
   */
  async searchAttributes(params: AttributeSearchParams): Promise<AttributeSearchResponse> {
    return this.get<AttributeSearchResponse>(
      `${this.baseUrl}/attributes/search${this.buildQueryParams(params)}`
    );
  }

  /**
   * Get part attribute details
   * @param paId The part attribute ID
   */
  async getAttributeDetails(paId: number): Promise<PartAttributeDetail> {
    return this.get<PartAttributeDetail>(`${this.baseUrl}/attributes/${paId}`);
  }

  /**
   * Get attributes for a specific part
   * @param partTerminologyId The part terminology ID
   */
  async getPartAttributes(partTerminologyId: number): Promise<PartAttributesResponse> {
    return this.get<PartAttributesResponse>(`${this.baseUrl}/parts/${partTerminologyId}/attributes`);
  }

  /**
   * Get all measurement groups
   */
  async getMeasurementGroups(): Promise<{ id: number; name: string }[]> {
    return this.get<{ id: number; name: string }[]>(`${this.baseUrl}/measurement-groups`);
  }

  /**
   * Get UOM codes for a measurement group
   * @param measurementGroupId The measurement group ID
   */
  async getUOMCodesByMeasurementGroup(measurementGroupId: number): Promise<{ id: number; code: string; description: string; label: string }[]> {
    return this.get<{ id: number; code: string; description: string; label: string }[]>(
      `${this.baseUrl}/measurement-groups/${measurementGroupId}/uom-codes`
    );
  }

  /**
   * Get valid values for an attribute assignment
   * @param paptId The part attribute assignment ID
   */
  async getValidValuesForAttribute(paptId: number): Promise<{ id: number; value: string }[]> {
    return this.get<{ id: number; value: string }[]>(`${this.baseUrl}/attribute-assignments/${paptId}/valid-values`);
  }
}

// Create and export a singleton instance
export const padbService = new PAdbService();
export default padbService;
