<!-- src/components/charts/BarChartExample.vue -->
<template>
  <base-chart
    type="bar"
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

interface BarConfig {
  dataKey: string
  name?: string
  color: string
  radius?: number | [number, number, number, number]
}

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  bars: {
    type: Array as PropType<BarConfig[]>,
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

// Transform data for ApexCharts series format
const chartSeries = computed(() => {
  return props.bars.map(bar => ({
    name: bar.name || bar.dataKey,
    data: props.data.map(item => item[bar.dataKey]),
  }))
})

// Prepare ApexCharts options
const chartOptions = computed(() => {
  const categories = props.data.map(item => item.name)

  return {
    chart: {
      type: 'bar',
      height: typeof props.height === 'number' ? props.height : 300,
      toolbar: {
        show: true,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        borderRadius: props.bars[0]?.radius || 0,
        dataLabels: {
          position: 'top',
        },
      },
    },
    colors: props.bars.map(bar => bar.color),
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent'],
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
    fill: {
      opacity: 1,
    },
    tooltip: {
      y: {
        formatter: function(val) {
          return val.toString()
        },
      },
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
