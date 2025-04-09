<template>
  <div class="attribute-search">
    <SearchFilter
      title="Search Part Attributes"
      :loading="loading"
      :disabled="!isValidSearch"
      :has-filters="hasFilters"
      @submit="handleSearch"
      @clear="clearFilters"
    >
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="searchParams.search_term"
            label="Search Term"
            placeholder="Enter attribute name or description"
            clearable
            hide-details="auto"
          ></v-text-field>
        </v-col>
      </v-row>
    </SearchFilter>

    <v-divider class="my-4"></v-divider>

    <div v-if="results && results.items.length > 0">
      <DataTable
        :headers="headers"
        :items="results.items"
        :total-items="results.total"
        :page="page"
        :items-per-page="pageSize"
        :loading="loading"
        :error="error"
        title="Attribute Results"
        @update:page="page = $event"
        @update:items-per-page="pageSize = $event"
      >
        <template v-slot:item.pa_id="{ item }">{{ item.pa_id }}</template>
        <template v-slot:item.pa_name="{ item }">{{ item.pa_name }}</template>
        <template v-slot:item.pa_descr="{ item }">{{ item.pa_descr || '-' }}</template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            :to="{ name: 'padb-attribute-details', params: { id: item.pa_id } }"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </DataTable>
    </div>
    <div v-else-if="results && results.items.length === 0" class="text-center my-4">
      <v-alert type="info" text="No attributes found matching your search criteria." variant="tonal"></v-alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { usePAdbStore } from '@/stores/autocare/padb.store.ts';
import SearchFilter from '@/components/common/SearchFilter.vue';
import DataTable from '@/components/common/DataTable.vue';
import { AttributeSearchParams } from '@/types';

const padbStore = usePAdbStore();

// State
const loading = ref(false);
const error = ref('');
const page = ref(1);
const pageSize = ref(10);
const searchParams = ref({
  search_term: '',
});

// Computed
const results = computed(() => padbStore.searchResults);

const isValidSearch = computed(() => {
  return searchParams.value.search_term.trim() !== '';
});

const hasFilters = computed(() => {
  return searchParams.value.search_term.trim() !== '';
});

const headers = [
  { title: 'ID', key: 'pa_id', sortable: true },
  { title: 'Name', key: 'pa_name', sortable: true },
  { title: 'Description', key: 'pa_descr', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

// Methods
const handleSearch = async () => {
  try {
    loading.value = true;
    const params: AttributeSearchParams = {
      search_term: searchParams.value.search_term,
      page: page.value,
      page_size: pageSize.value,
    };

    await padbStore.searchAttributes(params);
  } catch (err) {
    error.value = 'Search failed';
  } finally {
    loading.value = false;
  }
};

const clearFilters = () => {
  searchParams.value = {
    search_term: '',
  };
  padbStore.clearSearch();
};

// Watch for pagination changes
watch([page, pageSize], () => {
  if (hasFilters.value) {
    handleSearch();
  }
});
</script>

<style scoped>
.attribute-search {
  width: 100%;
}
</style>
