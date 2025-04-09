// src/stores/vcdb.store.ts
/**
 * Pinia store for VCdb (Vehicle Component Database) data
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { vcdbService } from '@/services';
import {
  Make,
  Model,
  Year,
  SubModel,
  Vehicle,
  VehicleDetail,
  VehicleSearchParams,
  VehicleSearchResponse,
  ApiError,
  BaseVehicle,
  VehicleConfigurationResponse,
  VehicleType,
  Region
} from '@/types';

export const useVCdbStore = defineStore('vcdb', () => {
  // State
  const loading = ref(false);
  const error = ref<ApiError | null>(null);
  const version = ref<string | null>(null);
  const years = ref<Year[]>([]);
  const makes = ref<Make[]>([]);
  const models = ref<Model[]>([]);
  const submodels = ref<SubModel[]>([]);
  const vehicleTypes = ref<VehicleType[]>([]);
  const regions = ref<Region[]>([]);
  const searchResults = ref<VehicleSearchResponse | null>(null);
  const currentVehicle = ref<VehicleDetail | null>(null);
  const vehicleConfigurations = ref<VehicleConfigurationResponse | null>(null);
  const yearRange = ref<[number, number] | null>(null);

  // Getters
  const filteredMakes = computed(() => {
    return makes.value;
  });

  const filteredModels = computed(() => {
    return models.value;
  });

  const filteredSubmodels = computed(() => {
    return submodels.value;
  });

  const isLoading = computed(() => loading.value);
  const hasError = computed(() => error.value !== null);
  const errorMessage = computed(() => error.value?.message || '');

  // Actions
  const clearError = () => {
    error.value = null;
  };

  const setLoading = (value: boolean) => {
    loading.value = value;
  };

  const setError = (err: ApiError) => {
    error.value = err;
  };

  const fetchVersion = async () => {
    try {
      setLoading(true);
      clearError();
      version.value = await vcdbService.getVersion();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchYears = async () => {
    try {
      setLoading(true);
      clearError();
      years.value = await vcdbService.getYears();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchYearRange = async () => {
    try {
      setLoading(true);
      clearError();
      yearRange.value = await vcdbService.getYearRange();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchMakes = async () => {
    try {
      setLoading(true);
      clearError();
      makes.value = await vcdbService.getMakes();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchMakesByYear = async (year: number) => {
    try {
      setLoading(true);
      clearError();
      makes.value = await vcdbService.getMakesByYear(year);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchMakes = async (searchTerm: string) => {
    try {
      setLoading(true);
      clearError();
      makes.value = await vcdbService.searchMakes(searchTerm);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchModelsByYearMake = async (year: number, makeId: number) => {
    try {
      setLoading(true);
      clearError();
      models.value = await vcdbService.getModelsByYearMake(year, makeId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchModels = async (searchTerm: string) => {
    try {
      setLoading(true);
      clearError();
      models.value = await vcdbService.searchModels(searchTerm);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchSubmodelsByBaseVehicle = async (baseVehicleId: number) => {
    try {
      setLoading(true);
      clearError();
      submodels.value = await vcdbService.getSubmodelsByBaseVehicle(baseVehicleId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchAllSubmodels = async () => {
    try {
      setLoading(true);
      clearError();
      submodels.value = await vcdbService.getAllSubmodels();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchSubmodels = async (searchTerm: string) => {
    try {
      setLoading(true);
      clearError();
      submodels.value = await vcdbService.searchSubmodels(searchTerm);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchVehicleTypes = async () => {
    try {
      setLoading(true);
      clearError();
      vehicleTypes.value = await vcdbService.getVehicleTypes();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchVehicleTypesByGroup = async (groupId: number) => {
    try {
      setLoading(true);
      clearError();
      vehicleTypes.value = await vcdbService.getVehicleTypesByGroup(groupId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchRegions = async () => {
    try {
      setLoading(true);
      clearError();
      regions.value = await vcdbService.getRegions();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const findBaseVehicle = async (yearId: number, makeId: number, modelId: number): Promise<BaseVehicle | null> => {
    try {
      setLoading(true);
      clearError();
      return await vcdbService.findBaseVehicle(yearId, makeId, modelId);
    } catch (err) {
      setError(err as ApiError);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const searchVehicles = async (params: VehicleSearchParams) => {
    try {
      setLoading(true);
      clearError();
      searchResults.value = await vcdbService.searchVehicles(params);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchVehicleDetails = async (vehicleId: number) => {
    try {
      setLoading(true);
      clearError();
      currentVehicle.value = await vcdbService.getVehicleDetails(vehicleId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchVehicleConfigurations = async (vehicleId: number) => {
    try {
      setLoading(true);
      clearError();
      vehicleConfigurations.value = await vcdbService.getVehicleConfigurations(vehicleId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const clearSearch = () => {
    searchResults.value = null;
  };

  const clearVehicle = () => {
    currentVehicle.value = null;
    vehicleConfigurations.value = null;
  };

  return {
    // State
    loading,
    error,
    version,
    years,
    makes,
    models,
    submodels,
    vehicleTypes,
    regions,
    searchResults,
    currentVehicle,
    vehicleConfigurations,
    yearRange,

    // Getters
    filteredMakes,
    filteredModels,
    filteredSubmodels,
    isLoading,
    hasError,
    errorMessage,

    // Actions
    clearError,
    setLoading,
    setError,
    fetchVersion,
    fetchYears,
    fetchYearRange,
    fetchMakes,
    fetchMakesByYear,
    searchMakes,
    fetchModelsByYearMake,
    searchModels,
    fetchSubmodelsByBaseVehicle,
    fetchAllSubmodels,
    searchSubmodels,
    fetchVehicleTypes,
    fetchVehicleTypesByGroup,
    fetchRegions,
    findBaseVehicle,
    searchVehicles,
    fetchVehicleDetails,
    fetchVehicleConfigurations,
    clearSearch,
    clearVehicle
  };
});
