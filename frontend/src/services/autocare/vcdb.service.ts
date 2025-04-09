// src/services/vcdb.service.ts
/**
 * Service for interacting with the VCdb (Vehicle Component Database) API
 */
import { ApiService } from '../api';
import {
  Make,
  Model,
  Year,
  SubModel,
  Region,
  DriveType,
  Vehicle,
  VehicleDetail,
  VehicleSearchParams,
  VehicleSearchResponse,
  BaseVehicle,
  EngineConfig,
  Transmission,
  WheelBase,
  BrakeConfig,
  BodyStyleConfig,
  VehicleConfigurationResponse,
  VehicleType, VCdbStats
} from '@/types';

export class VCdbService extends ApiService {
  private readonly baseUrl = '/autocare/vcdb';

  /**
   * Get the current VCdb version
   */
  async getVersion(): Promise<string> {
    return this.get<string>(`${this.baseUrl}/version`);
  }


  /**
   * Fetches statistical data from the specified endpoint.
   *
   * @return {Promise<any>} A promise that resolves to the statistical data fetched from the server.
   */
  async getStats(): Promise<VCdbStats> {
    return this.get<VCdbStats>(`${this.baseUrl}/stats`);
  }

  /**
   * Get all available years
   */
  async getYears(): Promise<Year[]> {
    return this.get<Year[]>(`${this.baseUrl}/years`);
  }

  /**
   * Get the available year range (min and max years)
   */
  async getYearRange(): Promise<[number, number]> {
    return this.get<[number, number]>(`${this.baseUrl}/years/range`);
  }

  /**
   * Get all makes
   */
  async getMakes(): Promise<Make[]> {
    return this.get<Make[]>(`${this.baseUrl}/makes`);
  }

  /**
   * Get makes available for a specific year
   * @param year The year to filter by
   */
  async getMakesByYear(year: number): Promise<Make[]> {
    return this.get<Make[]>(`${this.baseUrl}/years/${year}/makes`);
  }

  /**
   * Search for makes by name
   * @param searchTerm The search term to filter makes
   */
  async searchMakes(searchTerm: string): Promise<Make[]> {
    return this.get<Make[]>(`${this.baseUrl}/makes/search${this.buildQueryParams({ search_term: searchTerm })}`);
  }

  /**
   * Get a make by ID
   * @param makeId The make ID
   */
  async getMakeById(makeId: number): Promise<Make> {
    return this.get<Make>(`${this.baseUrl}/makes/${makeId}`);
  }

  /**
   * Get models available for a specific year and make
   * @param year The year
   * @param makeId The make ID
   */
  async getModelsByYearMake(year: number, makeId: number): Promise<Model[]> {
    return this.get<Model[]>(`${this.baseUrl}/years/${year}/makes/${makeId}/models`);
  }

  /**
   * Search for models by name
   * @param searchTerm The search term to filter models
   */
  async searchModels(searchTerm: string): Promise<Model[]> {
    return this.get<Model[]>(`${this.baseUrl}/models/search${this.buildQueryParams({ search_term: searchTerm })}`);
  }

  /**
   * Get a model by ID
   * @param modelId The model ID
   */
  async getModelById(modelId: number): Promise<Model> {
    return this.get<Model>(`${this.baseUrl}/models/${modelId}`);
  }

  /**
   * Get submodels available for a base vehicle
   * @param baseVehicleId The base vehicle ID
   */
  async getSubmodelsByBaseVehicle(baseVehicleId: number): Promise<SubModel[]> {
    return this.get<SubModel[]>(`${this.baseUrl}/base-vehicles/${baseVehicleId}/submodels`);
  }

  /**
   * Get all submodels
   */
  async getAllSubmodels(): Promise<SubModel[]> {
    return this.get<SubModel[]>(`${this.baseUrl}/submodels`);
  }

  /**
   * Search for submodels by name
   * @param searchTerm The search term to filter submodels
   */
  async searchSubmodels(searchTerm: string): Promise<SubModel[]> {
    return this.get<SubModel[]>(`${this.baseUrl}/submodels/search${this.buildQueryParams({ search_term: searchTerm })}`);
  }

  /**
   * Get all vehicle types
   */
  async getVehicleTypes(): Promise<VehicleType[]> {
    return this.get<VehicleType[]>(`${this.baseUrl}/vehicle-types`);
  }

  /**
   * Get vehicle types by group
   * @param groupId The vehicle type group ID
   */
  async getVehicleTypesByGroup(groupId: number): Promise<VehicleType[]> {
    return this.get<VehicleType[]>(`${this.baseUrl}/vehicle-type-groups/${groupId}/vehicle-types`);
  }

  /**
   * Get all regions
   */
  async getRegions(): Promise<Region[]> {
    return this.get<Region[]>(`${this.baseUrl}/regions`);
  }

  /**
   * Get regions by parent
   * @param parentId The parent region ID
   */
  async getRegionsByParent(parentId: number): Promise<Region[]> {
    return this.get<Region[]>(`${this.baseUrl}/regions/${parentId}/children`);
  }

  /**
   * Get a base vehicle by ID
   * @param baseVehicleId The base vehicle ID
   */
  async getBaseVehicle(baseVehicleId: number): Promise<BaseVehicle> {
    return this.get<BaseVehicle>(`${this.baseUrl}/base-vehicles/${baseVehicleId}`);
  }

  /**
   * Find a base vehicle by year, make, and model IDs
   * @param yearId The year ID
   * @param makeId The make ID
   * @param modelId The model ID
   */
  async findBaseVehicle(yearId: number, makeId: number, modelId: number): Promise<BaseVehicle | null> {
    return this.get<BaseVehicle | null>(`${this.baseUrl}/base-vehicles/find${this.buildQueryParams({
      year_id: yearId,
      make_id: makeId,
      model_id: modelId
    })}`);
  }

  /**
   * Search for base vehicles
   * @param params Search parameters
   */
  async searchBaseVehicles(params: {
    year?: number;
    make?: string;
    model?: string;
    page: number;
    page_size: number;
  }): Promise<VehicleSearchResponse> {
    return this.get<VehicleSearchResponse>(`${this.baseUrl}/base-vehicles/search${this.buildQueryParams(params)}`);
  }

  /**
   * Search for vehicles
   * @param params Search parameters
   */
  async searchVehicles(params: VehicleSearchParams): Promise<VehicleSearchResponse> {
    return this.get<VehicleSearchResponse>(`${this.baseUrl}/vehicles/search${this.buildQueryParams(params)}`);
  }

  /**
   * Get a vehicle by ID
   * @param vehicleId The vehicle ID
   */
  async getVehicleById(vehicleId: number): Promise<Vehicle> {
    return this.get<Vehicle>(`${this.baseUrl}/vehicles/${vehicleId}`);
  }

  /**
   * Get vehicle details
   * @param vehicleId The vehicle ID
   */
  async getVehicleDetails(vehicleId: number): Promise<VehicleDetail> {
    return this.get<VehicleDetail>(`${this.baseUrl}/vehicles/${vehicleId}/details`);
  }

  /**
   * Get vehicle configurations
   * @param vehicleId The vehicle ID
   */
  async getVehicleConfigurations(vehicleId: number): Promise<VehicleConfigurationResponse> {
    return this.get<VehicleConfigurationResponse>(`${this.baseUrl}/vehicles/${vehicleId}/configurations`);
  }

  /**
   * Get engine configuration details
   * @param engineConfigId The engine configuration ID
   */
  async getEngineConfig(engineConfigId: number): Promise<EngineConfig> {
    return this.get<EngineConfig>(`${this.baseUrl}/engine-configs/${engineConfigId}`);
  }

  /**
   * Search for engine configurations
   * @param params Search parameters
   */
  async searchEngineConfigs(params: {
    engine_base_id?: number;
    fuel_type_id?: number;
    aspiration_id?: number;
    page: number;
    page_size: number;
  }): Promise<{ items: EngineConfig[]; total: number; page: number; page_size: number; pages: number }> {
    return this.get<{ items: EngineConfig[]; total: number; page: number; page_size: number; pages: number }>(
      `${this.baseUrl}/engine-configs/search${this.buildQueryParams(params)}`
    );
  }

  /**
   * Get transmission details
   * @param transmissionId The transmission ID
   */
  async getTransmission(transmissionId: number): Promise<Transmission> {
    return this.get<Transmission>(`${this.baseUrl}/transmissions/${transmissionId}`);
  }

  /**
   * Search for transmissions
   * @param params Search parameters
   */
  async searchTransmissions(params: {
    transmission_type_id?: number;
    transmission_num_speeds_id?: number;
    transmission_control_type_id?: number;
    page: number;
    page_size: number;
  }): Promise<{ items: Transmission[]; total: number; page: number; page_size: number; pages: number }> {
    return this.get<{ items: Transmission[]; total: number; page: number; page_size: number; pages: number }>(
      `${this.baseUrl}/transmissions/search${this.buildQueryParams(params)}`
    );
  }

  /**
   * Get all drive types
   */
  async getDriveTypes(): Promise<DriveType[]> {
    return this.get<DriveType[]>(`${this.baseUrl}/drive-types`);
  }

  /**
   * Get body style configuration details
   * @param bodyStyleConfigId The body style configuration ID
   */
  async getBodyStyleConfig(bodyStyleConfigId: number): Promise<BodyStyleConfig> {
    return this.get<BodyStyleConfig>(`${this.baseUrl}/body-style-configs/${bodyStyleConfigId}`);
  }

  /**
   * Get brake configuration details
   * @param brakeConfigId The brake configuration ID
   */
  async getBrakeConfig(brakeConfigId: number): Promise<BrakeConfig> {
    return this.get<BrakeConfig>(`${this.baseUrl}/brake-configs/${brakeConfigId}`);
  }

  /**
   * Get all wheel bases
   */
  async getWheelBases(): Promise<WheelBase[]> {
    return this.get<WheelBase[]>(`${this.baseUrl}/wheel-bases`);
  }
}

// Create and export a singleton instance
export const vcdbService = new VCdbService();
export default vcdbService;
