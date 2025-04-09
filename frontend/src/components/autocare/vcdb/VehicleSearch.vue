<template>
  <div class="vehicle-search">
    <SearchFilter
      title="Search Vehicles"
      :loading="loading"
      :disabled="!isValidSearch"
      :has-filters="hasFilters"
      @submit="handleSearch"
      @clear="clearFilters"
    >
      <v-row>
        <v-col cols="12" sm="6" md="3">
          <v-select
            v-model="searchParams.year"
            :items="years"
            item-title="year"
            item-value="year"
            label="Year"
            clearable
            return-object
          ></v-select>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-autocomplete
            v-model="searchParams.make"
            :items="makes"
            item-title="name"
            item-value="name"
            label="Make"
            clearable
            return-object
            :loading="makesLoading"
            @update:model-value="onMakeChange"
          ></v-autocomplete>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-autocomplete
            v-model="searchParams.model"
            :items="models"
            item-title="name"
            item-value="name"
            label="Model"
            clearable
            return-object
            :loading="modelsLoading"
            :disabled="!searchParams.make"
            @update:model-value="onModelChange"
          ></v-autocomplete>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-autocomplete
            v-model="searchParams.submodel"
            :items="submodels"
            item-title="name"
            item-value="name"
            label="Submodel"
            clearable
            return-object
            :loading="submodelsLoading"
            :disabled="!searchParams.model"
          ></v-autocomplete>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <v-autocomplete
            v-model="searchParams.body_type"
            :items="bodyTypes"
            item-title="name"
            item-value="name"
            label="Body Type"
            clearable
            return-object
          ></v-autocomplete>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="searchParams.engine_config"
            :items="engineConfigs"
            item-title="display"
            item-value="id"
            label="Engine"
            clearable
            :disabled="!searchParams.model"
          ></v-select>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-select
            v-model="searchParams.transmission_type"
            :items="transmissionTypes"
            item-title="name"
            item-value="id"
            label="Transmission Type"
            clearable
            :disabled="!searchParams.model"
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
        title="Vehicle Results"
        @update:page="page = $event"
        @update:items-per-page="pageSize = $event"
      >
        <template v-slot:item.year="{ item }">{{ item.year }}</template>
        <template v-slot:item.make="{ item }">{{ item.make }}</template>
        <template v-slot:item.model="{ item }">{{ item.model }}</template>
        <template v-slot:item.submodel="{ item }">{{ item.submodel || '-' }}</template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            :to="{ name: 'vcdb-vehicle-details', params: { id: item.vehicle_id } }"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </DataTable>
    </div>
    <div v-else-if="results && results.items.length === 0" class="text-center my-4">
      <v-alert type="info" text="No vehicles found matching your search criteria." variant="tonal"></v-alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useVCdbStore } from '@/stores/autocare/vcdb.store.ts';
import SearchFilter from '@/components/common/SearchFilter.vue';
import DataTable from '@/components/common/DataTable.vue';
import { VehicleSearchParams } from '@/types';
import { formatVehicleName } from '@/utils/formatters.ts';

const vcdbStore = useVCdbStore();

// State
const loading = ref(false);
const makesLoading = ref(false);
const modelsLoading = ref(false);
const submodelsLoading = ref(false);
const error = ref('');
const page = ref(1);
const pageSize = ref(10);
const searchParams = ref({
  year: null,
  make: null,
  model: null,
  submodel: null,
  body_type: null,
  engine_config: null,
  transmission_type: null,
});

// Computed
const years = computed(() => vcdbStore.years);
const makes = computed(() => vcdbStore.makes);
const models = computed(() => vcdbStore.models);
const submodels = computed(() => vcdbStore.submodels);
const bodyTypes = ref([]); // Would come from a store
const engineConfigs = ref([]); // Would come from a store
const transmissionTypes = ref([]); // Would come from a store
const results = computed(() => vcdbStore.searchResults);

const isValidSearch = computed(() => {
  return (
    searchParams.value.year !== null ||
    searchParams.value.make !== null ||
    searchParams.value.model !== null ||
    searchParams.value.submodel !== null ||
    searchParams.value.body_type !== null ||
    searchParams.value.engine_config !== null ||
    searchParams.value.transmission_type !== null
  );
});

const hasFilters = computed(() => {
  return (
    searchParams.value.year !== null ||
    searchParams.value.make !== null ||
    searchParams.value.model !== null ||
    searchParams.value.submodel !== null ||
    searchParams.value.body_type !== null ||
    searchParams.value.engine_config !== null ||
    searchParams.value.transmission_type !== null
  );
});

const headers = [
  { title: 'Year', key: 'year', sortable: true },
  { title: 'Make', key: 'make', sortable: true },
  { title: 'Model', key: 'model', sortable: true },
  { title: 'Submodel', key: 'submodel', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

// Methods
const loadData = async () => {
  try {
    loading.value = true;
    await Promise.all([
      vcdbStore.fetchYears(),
      vcdbStore.fetchMakes(),
      // Load other reference data as needed
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
    const params: VehicleSearchParams = {
      page: page.value,
      page_size: pageSize.value,
    };

    if (searchParams.value.year) {
      params.year = searchParams.value.year.year_id;
    }
    if (searchParams.value.make) {
      params.make = searchParams.value.make.name;
    }
    if (searchParams.value.model) {
      params.model = searchParams.value.model.name;
    }
    if (searchParams.value.submodel) {
      params.submodel = searchParams.value.submodel;
    }
    if (searchParams.value.body_type) {
      params.body_type = searchParams.value.body_type;
    }
    if (searchParams.value.engine_config) {
      params.engine_config = searchParams.value.engine_config;
    }
    if (searchParams.value.transmission_type) {
      params.transmission_type = searchParams.value.transmission_type;
    }

    await vcdbStore.searchVehicles(params);
  } catch (err) {
    error.value = 'Search failed';
  } finally {
    loading.value = false;
  }
};

const onMakeChange = async () => {
  if (searchParams.value.make && searchParams.value.year) {
    modelsLoading.value = true;
    try {
      await vcdbStore.fetchModelsByYearMake(
        searchParams.value.year.year,
        searchParams.value.make.id
      );
    } catch (err) {
      error.value = 'Failed to load models';
    } finally {
      modelsLoading.value = false;
    }
  } else {
    // Clear dependent fields
    searchParams.value.model = null;
    searchParams.value.submodel = null;
  }
};

const onModelChange = async () => {
  if (searchParams.value.model && searchParams.value.make && searchParams.value.year) {
    // We would typically fetch submodels based on the base vehicle ID
    // For now, we'll just clear the submodel
    searchParams.value.submodel = null;
  }
};

const clearFilters = () => {
  searchParams.value = {
    year: null,
    make: null,
    model: null,
    submodel: null,
    body_type: null,
    engine_config: null,
    transmission_type: null,
  };
  vcdbStore.clearSearch();
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
.vehicle-search {
  width: 100%;
}
</style>
