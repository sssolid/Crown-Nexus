<template>
  <div class="data-table-container">
    <div v-if="loading" class="text-center my-4">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <div class="mt-2">Loading data...</div>
    </div>

    <div v-else-if="error" class="text-center my-4">
      <v-alert type="error" :text="error" variant="tonal"></v-alert>
    </div>

    <div v-else-if="!items || items.length === 0" class="text-center my-4">
      <v-alert type="info" text="No data available" variant="tonal"></v-alert>
    </div>

    <template v-else>
      <v-card>
        <v-card-title v-if="title">
          {{ title }}
          <v-spacer></v-spacer>
          <v-text-field
            v-if="searchable"
            v-model="localSearch"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
            density="compact"
            class="table-search-field"
          ></v-text-field>
        </v-card-title>

        <v-data-table-server
          v-model:items-per-page="localItemsPerPage"
          v-model:page="localPage"
          :headers="headers"
          :items="items"
          :items-length="totalItems"
          :loading="loading"
          :search="localSearch"
          class="elevation-1"
          item-value="id"
        >
          <template v-for="slot in Object.keys($slots)" v-slot:[slot]="slotProps">
            <slot :name="slot" v-bind="slotProps"></slot>
          </template>
        </v-data-table-server>
      </v-card>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';

interface Header {
  title: string;
  key: string;
  align?: string;
  sortable?: boolean;
  width?: string | number;
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
    default: false,
  },
});

const emit = defineEmits(['update:page', 'update:itemsPerPage', 'update:search']);

const localPage = ref(props.page);
const localItemsPerPage = ref(props.itemsPerPage);
const localSearch = ref('');

watch(localPage, (newPage) => {
  emit('update:page', newPage);
});

watch(localItemsPerPage, (newItemsPerPage) => {
  emit('update:itemsPerPage', newItemsPerPage);
});

watch(localSearch, (newSearch) => {
  emit('update:search', newSearch);
});

watch(() => props.page, (newPage) => {
  localPage.value = newPage;
});

watch(() => props.itemsPerPage, (newItemsPerPage) => {
  localItemsPerPage.value = newItemsPerPage;
});
</script>

<style scoped>
.data-table-container {
  width: 100%;
}

.table-search-field {
  max-width: 300px;
}
</style>
