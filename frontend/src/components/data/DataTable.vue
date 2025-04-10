<!-- src/components/data/DataTable.vue -->
<template>
  <base-card
    :title="title"
    :loading="loading"
    :error="error"
    class="data-table-wrapper"
  >
    <template #title-actions>
      <slot name="table-actions">
        <v-text-field
          v-if="searchable"
          v-model="localSearch"
          density="compact"
          variant="outlined"
          prepend-inner-icon="mdi-magnify"
          hide-details
          single-line
          class="search-field"
          placeholder="Search..."
        />
      </slot>
    </template>

    <template v-if="!loading && !error && (!items || items.length === 0)">
      <slot name="empty-state">
        <div class="text-center py-6">
          <v-icon icon="mdi-database-off-outline" size="large" color="grey" />
          <p class="text-body-1 text-grey mt-2">No data available</p>
          <slot name="empty-actions"></slot>
        </div>
      </slot>
    </template>

    <div v-else>
      <v-data-table-server
        v-model:items-per-page="localItemsPerPage"
        v-model:page="localPage"
        v-model:sort-by="localSortBy"
        :headers="headers"
        :items="items"
        :items-length="totalItems"
        :loading="loading"
        :search="localSearch"
        :item-value="itemValue"
        :hover="hover"
        :no-data-text="noDataText"
        :server-items-length="totalItems"
        :class="tableClass"
      >
        <!-- Pass all slots to the data table component -->
        <template v-for="(_, name) in $slots" #[name]="slotData">
          <slot :name="name" v-bind="slotData"></slot>
        </template>

        <!-- Default slot for pagination -->
        <template #bottom v-if="!hidePagination">
          <div class="d-flex align-center justify-space-between pa-2">
            <div>
              <slot name="pagination-info">
                <span class="text-caption text-grey">
                  Showing {{ paginationInfo.from }} to {{ paginationInfo.to }} of {{ totalItems }} entries
                </span>
              </slot>
            </div>
            <v-pagination
              v-if="totalPages > 1"
              v-model="localPage"
              :length="totalPages"
              :total-visible="paginationVisible"
            ></v-pagination>
          </div>
        </template>
      </v-data-table-server>
    </div>
  </base-card>
</template>

<script setup lang="ts">
import { ref, computed, watch, defineProps, defineEmits } from 'vue'
import BaseCard from '@/components/base/BaseCard.vue'

interface Header {
  title: string
  key: string
  align?: string
  sortable?: boolean
  width?: string | number
  filterable?: boolean
}

interface SortBy {
  key: string
  order?: 'asc' | 'desc'
}

const props = defineProps({
  headers: {
    type: Array as () => Header[],
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
    default: true,
  },
  search: {
    type: String,
    default: '',
  },
  sortBy: {
    type: Array as () => SortBy[],
    default: () => [],
  },
  itemValue: {
    type: String,
    default: 'id',
  },
  hover: {
    type: Boolean,
    default: true,
  },
  noDataText: {
    type: String,
    default: 'No data available',
  },
  hidePagination: {
    type: Boolean,
    default: false,
  },
  paginationVisible: {
    type: Number,
    default: 7,
  },
  tableClass: {
    type: String,
    default: 'elevation-1',
  }
})

const emit = defineEmits([
  'update:page',
  'update:itemsPerPage',
  'update:search',
  'update:sortBy'
])

const localPage = computed({
  get: () => props.page,
  set: (value) => emit('update:page', value)
})

const localItemsPerPage = computed({
  get: () => props.itemsPerPage,
  set: (value) => emit('update:itemsPerPage', value)
})

const localSearch = computed({
  get: () => props.search,
  set: (value) => emit('update:search', value)
})

const localSortBy = computed({
  get: () => props.sortBy,
  set: (value) => emit('update:sortBy', value)
})

// Calculate total pages
const totalPages = computed(() => {
  return Math.ceil(props.totalItems / props.itemsPerPage)
})

// Calculate pagination info
const paginationInfo = computed(() => {
  const from = (props.page - 1) * props.itemsPerPage + 1
  const to = Math.min(from + props.itemsPerPage - 1, props.totalItems)
  return { from, to }
})

// Watch for external changes
watch(() => props.page, (newPage) => {
  if (newPage !== localPage.value) {
    localPage.value = newPage
  }
})

watch(() => props.itemsPerPage, (newItemsPerPage) => {
  if (newItemsPerPage !== localItemsPerPage.value) {
    localItemsPerPage.value = newItemsPerPage
  }
})
</script>

<style scoped>
.data-table-wrapper {
  width: 100%;
}

.search-field {
  max-width: 320px;
}
</style>
