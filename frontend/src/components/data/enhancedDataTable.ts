// src/components/data/enhancedDataTable.ts
// This extends your DataTable.vue component with additional functionality

import { defineComponent, ref, computed, watch, h } from 'vue'
import DataTable from '@/components/common/DataTable.vue'
import Pagination from '@/components/data/Pagination.vue'
import EmptyState from '@/components/display/EmptyState.vue'
import SkeletonTable from '@/components/loaders/SkeletonTable.vue'

export default defineComponent({
  name: 'EnhancedDataTable',

  // Extend the props from your existing DataTable
  props: {
    // Original props
    headers: {
      type: Array,
      required: true,
    },
    items: {
      type: Array,
      default: () => [],
    },
    totalItems: {
      type: Number,
      default: 0,
    },
    page: {
      type: Number,
      default: 1,
    },
    itemsPerPage: {
      type: Number,
      default: 10,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: String,
      default: '',
    },
    title: {
      type: String,
      default: '',
    },
    searchable: {
      type: Boolean,
      default: false,
    },

    // New enhanced props
    showPagination: {
      type: Boolean,
      default: true,
    },
    emptyStateIcon: {
      type: String,
      default: 'mdi-database-off-outline',
    },
    emptyStateTitle: {
      type: String,
      default: 'No data available',
    },
    emptyStateSubtitle: {
      type: String,
      default: 'There are no items to display',
    },
    containerClass: {
      type: String,
      default: '',
    },
    itemsPerPageOptions: {
      type: Array,
      default: () => [5, 10, 25, 50, 100],
    },
    skeletonColumns: {
      type: Array,
      default: () => [],
    },
    skeletonRows: {
      type: Number,
      default: 5,
    },
  },

  emits: [
    'update:page',
    'update:itemsPerPage',
    'update:search',
    'update:sortBy',
    'row-click',
    'refresh',
  ],

  setup(props, { emit, slots }) {
    const localPage = ref(props.page)
    const localItemsPerPage = ref(props.itemsPerPage)
    const localSearch = ref('')
    const localSortBy = ref([])

    // Watch for external changes
    watch(() => props.page, (newPage) => {
      localPage.value = newPage
    })

    watch(() => props.itemsPerPage, (newItemsPerPage) => {
      localItemsPerPage.value = newItemsPerPage
    })

    // Compute skeleton columns based on headers if not provided
    const computedSkeletonColumns = computed(() => {
      if (props.skeletonColumns.length > 0) {
        return props.skeletonColumns
      }

      return props.headers.map(header => ({
        width: header.width,
        type: 'text',
      }))
    })

    // Handlers
    const handlePageChange = (page) => {
      localPage.value = page
      emit('update:page', page)
    }

    const handleItemsPerPageChange = (value) => {
      localItemsPerPage.value = value
      emit('update:itemsPerPage', value)

      // Reset to page 1 when changing items per page
      if (localPage.value !== 1) {
        localPage.value = 1
        emit('update:page', 1)
      }
    }

    const handleSearchChange = (value) => {
      localSearch.value = value
      emit('update:search', value)
    }

    const handleSortChange = (value) => {
      localSortBy.value = value
      emit('update:sortBy', value)
    }

    const handleRowClick = (item, event) => {
      emit('row-click', item, event)
    }

    const handleRefresh = () => {
      emit('refresh')
    }

    // Calculate total pages
    const totalPages = computed(() => {
      return Math.ceil(props.totalItems / localItemsPerPage.value)
    })

    // Render function to use your existing components but enhance them
    return () => {
      // Show skeleton loader while loading
      if (props.loading) {
        return h(SkeletonTable, {
          columns: computedSkeletonColumns.value,
          rows: props.skeletonRows,
          showHeader: true,
          showFooter: props.showPagination,
          class: props.containerClass,
        })
      }

      // Show error state
      if (props.error) {
        return h('div', { class: props.containerClass }, [
          h('v-alert', {
            type: 'error',
            text: props.error,
            variant: 'tonal',
            class: 'my-4',
          }),
        ])
      }

      // Show empty state
      if (!props.items || props.items.length === 0) {
        return h(EmptyState, {
          title: props.emptyStateTitle,
          subtitle: props.emptyStateSubtitle,
          icon: props.emptyStateIcon,
          class: props.containerClass,
        })
      }

      // Main content with existing DataTable
      return h('div', { class: props.containerClass }, [
        // Use your existing DataTable component
        h(DataTable, {
          headers: props.headers,
          items: props.items,
          totalItems: props.totalItems,
          page: localPage.value,
          itemsPerPage: localItemsPerPage.value,
          loading: false, // We're handling loading state ourselves
          error: '', // We're handling error state ourselves
          title: props.title,
          searchable: props.searchable,
          'onUpdate:page': handlePageChange,
          'onUpdate:itemsPerPage': handleItemsPerPageChange,
          'onUpdate:search': handleSearchChange,
          'onUpdate:sortBy': handleSortChange,
        }, slots),

        // Add pagination component at the bottom if needed
        props.showPagination ? h(Pagination, {
          modelValue: localPage.value,
          totalItems: props.totalItems,
          itemsPerPage: localItemsPerPage.value,
          itemsPerPageOptions: props.itemsPerPageOptions,
          'onUpdate:modelValue': handlePageChange,
          'onUpdate:itemsPerPage': handleItemsPerPageChange,
          class: 'mt-4',
        }) : null,
      ])
    }
  }
})
