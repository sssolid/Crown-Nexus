<!-- src/components/charts/LineChartExample.vue -->
<template>
  <base-chart
    type="line"
    :data="data"
    :series="chartSeries"
    :options="chartOptions"
    :loading="loading"
    :error="error"
    :height="height"
  >
  </base-chart>
</template>

<script setup lang="ts">
import { PropType, computed } from 'vue'
import BaseChart from './BaseChart.vue'

interface LineConfig {
  dataKey: string
  name?: string
  color: string
  fill?: string
  type?: 'monotone' | 'linear' | 'step' | 'stepBefore' | 'stepAfter' | 'basis' | 'basisOpen' | 'basisClosed' | 'natural'
  dot?: boolean | object
  activeDot?: boolean | object
}

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  lines: {
    type: Array as PropType<LineConfig[]>,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
  height: {
    type: [Number, String],
    default: 300,
  },
  additionalChartProps: {
    type: Object,
    default: () => ({}),
  },
})

// Map Recharts line type to ApexCharts curve
const getCurveType = (type?: string) => {
  switch (type) {
    case 'monotone': return 'smooth'
    case 'linear': return 'straight'
    case 'step':
    case 'stepBefore':
    case 'stepAfter': return 'stepline'
    case 'basis':
    case 'basisOpen':
    case 'basisClosed':
    case 'natural': return 'smooth'
    default: return 'smooth'
  }
}

// Transform data for ApexCharts series format
const chartSeries = computed(() => {
  return props.lines.map(line => ({
    name: line.name || line.dataKey,
    data: props.data.map(item => item[line.dataKey]),
    color: line.color,
  }))
})

// Prepare ApexCharts options
const chartOptions = computed(() => {
  const categories = props.data.map(item => item.name)

  return {
    chart: {
      type: 'line',
      height: typeof props.height === 'number' ? props.height : 300,
      toolbar: {
        show: true,
      },
    },
    colors: props.lines.map(line => line.color),
    dataLabels: {
      enabled: false,
    },
    stroke: {
      curve: props.lines.map(line => getCurveType(line.type)),
      width: 3,
    },
    markers: {
      size: props.lines.some(line => line.dot !== false) ? 4 : 0,
      hover: {
        size: 6,
      },
    },
    xaxis: {
      categories,
      title: {
        text: '',
      },
    },
    yaxis: {
      title: {
        text: '',
      },
    },
    tooltip: {
      intersect: false,
      shared: true,
    },
    legend: {
      position: 'top',
    },
    grid: {
      borderColor: '#e0e0e0',
      strokeDashArray: 3,
    },
    ...props.additionalChartProps,
  }
})
</script>
