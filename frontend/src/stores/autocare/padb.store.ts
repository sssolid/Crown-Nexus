// src/stores/padb.store.ts
/**
 * Pinia store for PAdb (Part Attribute Database) data
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {padbService} from '@/services';
import {
  PartAttribute,
  PartAttributeDetail,
  AttributeSearchParams,
  AttributeSearchResponse,
  ApiError,
  PartAttributesResponse, PAdbStats
} from '@/types';

export const usePAdbStore = defineStore('padb', () => {
  // State
  const loading = ref(false);
  const error = ref<ApiError | null>(null);
  const version = ref<string | null>(null);
  const stats = ref<PAdbStats | null>(null);
  const searchResults = ref<AttributeSearchResponse | null>(null);
  const currentAttribute = ref<PartAttributeDetail | null>(null);
  const partAttributes = ref<PartAttributesResponse | null>(null);
  const measurementGroups = ref<{ id: number; name: string }[]>([]);
  const uomCodes = ref<Map<number, { id: number; code: string; description: string; label: string }[]>>(new Map());

  // Getters
  const isLoading = computed(() => loading.value);
  const hasError = computed(() => error.value !== null);
  const errorMessage = computed(() => error.value?.message || '');

  const getUOMCodesByGroup = (groupId: number) => {
    return uomCodes.value.get(groupId) || [];
  };

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
      version.value = await padbService.getVersion();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      setLoading(true);
      clearError();
      stats.value = await padbService.getStats();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchAttributes = async (params: AttributeSearchParams) => {
    try {
      setLoading(true);
      clearError();
      searchResults.value = await padbService.searchAttributes(params);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchAttributeDetails = async (paId: number) => {
    try {
      setLoading(true);
      clearError();
      currentAttribute.value = await padbService.getAttributeDetails(paId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchPartAttributes = async (partTerminologyId: number) => {
    try {
      setLoading(true);
      clearError();
      partAttributes.value = await padbService.getPartAttributes(partTerminologyId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchMeasurementGroups = async () => {
    try {
      setLoading(true);
      clearError();
      measurementGroups.value = await padbService.getMeasurementGroups();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchUOMCodesByGroup = async (measurementGroupId: number) => {
    try {
      setLoading(true);
      clearError();
      const codes = await padbService.getUOMCodesByMeasurementGroup(measurementGroupId);
      uomCodes.value.set(measurementGroupId, codes);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchValidValuesForAttribute = async (paptId: number) => {
    try {
      setLoading(true);
      clearError();
      return await padbService.getValidValuesForAttribute(paptId);
    } catch (err) {
      setError(err as ApiError);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const clearSearch = () => {
    searchResults.value = null;
  };

  const clearAttribute = () => {
    currentAttribute.value = null;
  };

  const clearPartAttributes = () => {
    partAttributes.value = null;
  };

  return {
    // State
    loading,
    error,
    version,
    stats,
    searchResults,
    currentAttribute,
    partAttributes,
    measurementGroups,
    uomCodes,

    // Getters
    isLoading,
    hasError,
    errorMessage,
    getUOMCodesByGroup,

    // Actions
    clearError,
    setLoading,
    setError,
    fetchVersion,
    fetchStats,
    searchAttributes,
    fetchAttributeDetails,
    fetchPartAttributes,
    fetchMeasurementGroups,
    fetchUOMCodesByGroup,
    fetchValidValuesForAttribute,
    clearSearch,
    clearAttribute,
    clearPartAttributes
  };
});
