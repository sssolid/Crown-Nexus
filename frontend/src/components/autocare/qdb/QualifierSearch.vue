<template>
  <div class="qualifier-search">
    <SearchFilter
      title="Search Qualifiers"
      :loading="loading"
      :disabled="!isValidSearch"
      :has-filters="hasFilters"
      @submit="handleSearch"
      @clear="clearFilters"
    >
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field
            v-model="searchParams.search_term"
            label="Search Term"
            placeholder="Enter qualifier text or example"
            clearable
            hide-details="auto"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="3">
          <v-select
            v-model="searchParams.qualifier_type_id"
            :items="qualifierTypes"
            item-title="qualifier_type"
            item-value="qualifier_type_id"
            label="Qualifier Type"
            clearable
            hide-details="auto"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="3">
          <v-select
            v-model="searchParams.language_id"
            :items="languages"
            item-title="language_name"
            item-value="language_id"
            label="Language"
            clearable
            hide-details="auto"
          ></v-select>
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
        title="Qualifier Results"
        @update:page="page = $event"
        @update:items-per-page="pageSize = $event"
      >
        <template v-slot:item.qualifier_id="{ item }">{{ item.qualifier_id }}</template>
        <template v-slot:item.qualifier_text="{ item }">{{ item.qualifier_text }}</template>
        <template v-slot:item.example_text="{ item }">{{ item.example_text || '-' }}</template>
        <template v-slot:item.superseded="{ item }">
          <v-icon
            v-if="item.new_qualifier_id"
            color="warning"
            icon="mdi-alert"
            size="small"
          ></v-icon>
          <span v-else>-</span>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            :to="{ name: 'qdb-qualifier-details', params: { id: item.qualifier_id } }"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </DataTable>
    </div>
    <div v-else-if="results && results.items.length === 0" class="text-center my-4">
      <v-alert type="info" text="No qualifiers found matching your search criteria." variant="tonal"></v-alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useQdbStore } from '@/stores/autocare/qdb.store.ts';
import SearchFilter from '@/components/common/SearchFilter.vue';
import DataTable from '@/components/common/DataTable.vue';
import { QualifierSearchParams } from '@/types';

const qdbStore = useQdbStore();

// State
const loading = ref(false);
const error = ref('');
const page = ref(1);
const pageSize = ref(10);
const searchParams = ref({
  search_term: '',
  qualifier_type_id: null,
  language_id: null,
});

// Computed
const qualifierTypes = computed(() => qdbStore.qualifierTypes);
const languages = computed(() => qdbStore.languages);
const results = computed(() => qdbStore.searchResults);

const isValidSearch = computed(() => {
  return searchParams.value.search_term.trim() !== '' ||
         searchParams.value.qualifier_type_id !== null ||
         searchParams.value.language_id !== null;
});

const hasFilters = computed(() => {
  return searchParams.value.search_term.trim() !== '' ||
         searchParams.value.qualifier_type_id !== null ||
         searchParams.value.language_id !== null;
});

const headers = [
  { title: 'ID', key: 'qualifier_id', sortable: true },
  { title: 'Qualifier Text', key: 'qualifier_text', sortable: true },
  { title: 'Example', key: 'example_text', sortable: false },
  { title: 'Superseded', key: 'superseded', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

// Methods
const loadData = async () => {
  try {
    loading.value = true;
    await Promise.all([
      qdbStore.fetchQualifierTypes(),
      qdbStore.fetchLanguages(),
    ]);
  } catch (err) {
    error.value = 'Failed to load reference data';
  } finally {
    loading.value = false;
  }
};

const handleSearch = async () => {
  try {
    loading.value = true;
    const params: QualifierSearchParams = {
      search_term: searchParams.value.search_term,
      page: page.value,
      page_size: pageSize.value,
    };

    if (searchParams.value.qualifier_type_id !== null) {
      params.qualifier_type_id = searchParams.value.qualifier_type_id;
    }

    if (searchParams.value.language_id !== null) {
      params.language_id = searchParams.value.language_id;
    }

    await qdbStore.searchQualifiers(params);
  } catch (err) {
    error.value = 'Search failed';
  } finally {
    loading.value = false;
  }
};

const clearFilters = () => {
  searchParams.value = {
    search_term: '',
    qualifier_type_id: null,
    language_id: null,
  };
  qdbStore.clearSearch();
};

// Watch for pagination changes
watch([page, pageSize], () => {
  if (hasFilters.value) {
    handleSearch();
  }
});

// Load initial data
onMounted(loadData);
</script>

<style scoped>
.qualifier-search {
  width: 100%;
}
</style>
