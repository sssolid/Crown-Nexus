// src/stores/qdb.store.ts
/**
 * Pinia store for Qdb (Qualifier Database) data
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {qdbService} from '@/services';
import {
  QualifierType,
  Language,
  Qualifier,
  QualifierDetail,
  QualifierSearchParams,
  QualifierSearchResponse,
  ApiError,
  GroupNumber, QdbStats
} from '@/types';

export const useQdbStore = defineStore('qdb', () => {
  // State
  const loading = ref(false);
  const error = ref<ApiError | null>(null);
  const version = ref<string | null>(null);
  const stats = ref<QdbStats | null>(null);
  const qualifierTypes = ref<QualifierType[]>([]);
  const languages = ref<Language[]>([]);
  const groupNumbers = ref<GroupNumber[]>([]);
  const searchResults = ref<QualifierSearchResponse | null>(null);
  const currentQualifier = ref<QualifierDetail | null>(null);
  const selectedQualifierType = ref<number | null>(null);
  const selectedLanguage = ref<number | null>(null);

  // Getters
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
      version.value = await qdbService.getVersion();
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
      stats.value = await qdbService.getStats();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchQualifierTypes = async () => {
    try {
      setLoading(true);
      clearError();
      qualifierTypes.value = await qdbService.getQualifierTypes();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchLanguages = async () => {
    try {
      setLoading(true);
      clearError();
      languages.value = await qdbService.getLanguages();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchGroupNumbers = async () => {
    try {
      setLoading(true);
      clearError();
      groupNumbers.value = await qdbService.getGroupNumbers();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchQualifiers = async (params: QualifierSearchParams) => {
    try {
      setLoading(true);
      clearError();
      searchResults.value = await qdbService.searchQualifiers(params);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchQualifierDetails = async (qualifierId: number) => {
    try {
      setLoading(true);
      clearError();
      currentQualifier.value = await qdbService.getQualifierDetails(qualifierId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchQualifiersByGroup = async (groupNumberId: number, page: number = 1, pageSize: number = 20) => {
    try {
      setLoading(true);
      clearError();
      searchResults.value = await qdbService.getQualifiersByGroup(groupNumberId, page, pageSize);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchQualifierTranslations = async (qualifierId: number, languageId?: number) => {
    try {
      setLoading(true);
      clearError();
      return await qdbService.getQualifierTranslations(qualifierId, languageId);
    } catch (err) {
      setError(err as ApiError);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const fetchQualifierGroups = async (qualifierId: number) => {
    try {
      setLoading(true);
      clearError();
      return await qdbService.getQualifierGroups(qualifierId);
    } catch (err) {
      setError(err as ApiError);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const setSelectedQualifierType = (typeId: number | null) => {
    selectedQualifierType.value = typeId;
  };

  const setSelectedLanguage = (langId: number | null) => {
    selectedLanguage.value = langId;
  };

  const clearSearch = () => {
    searchResults.value = null;
  };

  const clearQualifier = () => {
    currentQualifier.value = null;
  };

  return {
    // State
    loading,
    error,
    version,
    stats,
    qualifierTypes,
    languages,
    groupNumbers,
    searchResults,
    currentQualifier,
    selectedQualifierType,
    selectedLanguage,

    // Getters
    isLoading,
    hasError,
    errorMessage,

    // Actions
    clearError,
    setLoading,
    setError,
    fetchVersion,
    fetchStats,
    fetchQualifierTypes,
    fetchLanguages,
    fetchGroupNumbers,
    searchQualifiers,
    fetchQualifierDetails,
    fetchQualifiersByGroup,
    fetchQualifierTranslations,
    fetchQualifierGroups,
    setSelectedQualifierType,
    setSelectedLanguage,
    clearSearch,
    clearQualifier
  };
});
