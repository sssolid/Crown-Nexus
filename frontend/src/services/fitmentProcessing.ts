// frontend/src/services/fitmentProcessing.ts
/**
 * Fitment Processing API service.
 *
 * This service provides methods for processing part applications
 * and validating them against VCDB and PCDB databases.
 */

import api from '@/services/api';

export interface FitmentValidationResult {
  status: string;
  message: string;
  original_text: string;
  suggestions: string[];
  fitment?: {
    vehicle: {
      year: number;
      make: string;
      model: string;
      submodel?: string;
      engine?: string;
      transmission?: string;
      attributes: Record<string, any>;
    };
    positions: {
      front_rear: string;
      left_right: string;
      upper_lower: string;
      inner_outer: string;
    };
    vcdb_vehicle_id?: number;
    pcdb_position_ids?: number[];
  };
}

export interface ProcessFitmentResponse {
  results: Record<string, FitmentValidationResult[]>;
  valid_count: number;
  warning_count: number;
  error_count: number;
}

/**
 * Fitment Processing service for API interactions.
 */
const fitmentProcessingService = {
  /**
   * Process part applications.
   *
   * @param applicationTexts - Array of part application texts
   * @param partTerminologyId - PCDB part terminology ID
   * @param productId - Optional product ID to associate fitments with
   * @returns Promise with processing results
   */
  async processApplications(
    applicationTexts: string[],
    partTerminologyId: number,
    productId?: string
  ): Promise<ProcessFitmentResponse> {
    return api.post<ProcessFitmentResponse>('/fitment/process', {
      application_texts: applicationTexts,
      part_terminology_id: partTerminologyId,
      product_id: productId
    });
  },

  /**
   * Parse a single part application.
   *
   * @param applicationText - Part application text
   * @returns Promise with parsed application components
   */
  async parseApplication(
    applicationText: string
  ): Promise<{
    raw_text: string;
    year_range?: [number, number];
    vehicle_text?: string;
    position_text?: string;
    additional_notes?: string;
  }> {
    return api.post<any>('/fitment/parse-application', {
      application_text: applicationText
    });
  },

  /**
   * Get PCDB positions for a part terminology.
   *
   * @param terminologyId - PCDB part terminology ID
   * @returns Promise with list of PCDB positions
   */
  async getPcdbPositions(
    terminologyId: number
  ): Promise<Array<{
    id: number;
    name: string;
    front_rear?: string;
    left_right?: string;
    upper_lower?: string;
    inner_outer?: string;
  }>> {
    return api.get<any[]>(`/fitment/pcdb-positions/${terminologyId}`);
  }
};

export default fitmentProcessingService;
