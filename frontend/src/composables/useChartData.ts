// src/composables/useChartData.ts
import { ref, computed, watch } from 'vue'

interface ChartDataOptions<T = any> {
  data?: T[]
  loading?: boolean
  error?: string
  transformData?: (data: T[]) => any[]
  filterData?: (data: T[]) => T[]
}

export function useChartData<T = any>(options: ChartDataOptions<T> = {}) {
  const rawData = ref<T[]>(options.data || [])
  const loading = ref(options.loading || false)
  const error = ref(options.error || '')

  // Transform function
  const transformData = options.transformData || ((data: T[]) => data)

  // Filter function
  const filterData = options.filterData || ((data: T[]) => data)

  // Computed processed data
  const chartData = computed(() => {
    const filtered = filterData(rawData.value)
    return transformData(filtered)
  })

  // Update raw data
  const setData = (data: T[]) => {
    rawData.value = data
  }

  // Set loading state
  const setLoading = (state: boolean) => {
    loading.value = state
  }

  // Set error message
  const setError = (message: string) => {
    error.value = message
  }

  // Reset everything
  const reset = () => {
    rawData.value = []
    loading.value = false
    error.value = ''
  }

  return {
    rawData,
    chartData,
    loading,
    error,
    setData,
    setLoading,
    setError,
    reset
  }
}
