// src/stores/pcdb.store.ts
/**
 * Pinia store for PCdb (Product Component Database) data
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import {pcdbService} from '@/services';
import {
  Category,
  SubCategory,
  Part,
  PartDetail,
  PartSearchParams,
  PartSearchResponse,
  ApiError,
  Position, PCdbStats
} from '@/types';

export const usePCdbStore = defineStore('pcdb', () => {
  // State
  const loading = ref(false);
  const error = ref<ApiError | null>(null);
  const version = ref<string | null>(null);
  const stats = ref<PCdbStats | null>(null);
  const categories = ref<Category[]>([]);
  const subcategories = ref<SubCategory[]>([]);
  const positions = ref<Position[]>([]);
  const searchResults = ref<PartSearchResponse | null>(null);
  const currentPart = ref<PartDetail | null>(null);
  const selectedCategories = ref<number[]>([]);

  // Getters
  const filteredCategories = computed(() => {
    return categories.value;
  });

  const filteredSubcategories = computed(() => {
    return subcategories.value;
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
      version.value = await pcdbService.getVersion();
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
      stats.value = await pcdbService.getStats();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      setLoading(true);
      clearError();
      categories.value = await pcdbService.getCategories();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchCategories = async (searchTerm: string) => {
    try {
      setLoading(true);
      clearError();
      categories.value = await pcdbService.searchCategories(searchTerm);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchSubcategoriesByCategory = async (categoryId: number) => {
    try {
      setLoading(true);
      clearError();
      subcategories.value = await pcdbService.getSubcategoriesByCategory(categoryId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchPositions = async () => {
    try {
      setLoading(true);
      clearError();
      positions.value = await pcdbService.getPositions();
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchPositionsByPart = async (partTerminologyId: number) => {
    try {
      setLoading(true);
      clearError();
      positions.value = await pcdbService.getPositionsByPart(partTerminologyId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const searchParts = async (params: PartSearchParams) => {
    try {
      setLoading(true);
      clearError();
      searchResults.value = await pcdbService.searchParts(params);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchPartsByCategory = async (categoryId: number, page: number = 1, pageSize: number = 20) => {
    try {
      setLoading(true);
      clearError();
      searchResults.value = await pcdbService.getPartsByCategory(categoryId, page, pageSize);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const fetchPartDetails = async (partTerminologyId: number) => {
    try {
      setLoading(true);
      clearError();
      currentPart.value = await pcdbService.getPartDetails(partTerminologyId);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const setSelectedCategories = (categoryIds: number[]) => {
    selectedCategories.value = categoryIds;
  };

  const addSelectedCategory = (categoryId: number) => {
    if (!selectedCategories.value.includes(categoryId)) {
      selectedCategories.value.push(categoryId);
    }
  };

  const removeSelectedCategory = (categoryId: number) => {
    selectedCategories.value = selectedCategories.value.filter(id => id !== categoryId);
  };

  const clearSelectedCategories = () => {
    selectedCategories.value = [];
  };

  const clearSearch = () => {
    searchResults.value = null;
  };

  const clearPart = () => {
    currentPart.value = null;
  };

  return {
    // State
    loading,
    error,
    version,
    stats,
    categories,
    subcategories,
    positions,
    searchResults,
    currentPart,
    selectedCategories,

    // Getters
    filteredCategories,
    filteredSubcategories,
    isLoading,
    hasError,
    errorMessage,

    // Actions
    clearError,
    setLoading,
    setError,
    fetchVersion,
    fetchStats,
    fetchCategories,
    searchCategories,
    fetchSubcategoriesByCategory,
    fetchPositions,
    fetchPositionsByPart,
    searchParts,
    fetchPartsByCategory,
    fetchPartDetails,
    setSelectedCategories,
    addSelectedCategory,
    removeSelectedCategory,
    clearSelectedCategories,
    clearSearch,
    clearPart
  };
});
