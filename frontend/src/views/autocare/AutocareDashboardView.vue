<template>
  <div class="dashboard">
    <PageHeader
      title="Autocare Explorer Dashboard"
      subtitle="Explore vehicle and part data across multiple databases"
      icon="mdi-view-dashboard"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-btn color="primary" prepend-icon="mdi-refresh" @click="refreshDashboard">
          Refresh
        </v-btn>
      </template>
    </PageHeader>

    <v-row>
      <v-col cols="12" md="6" lg="3">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="primary">mdi-car</v-icon>
            VCdb
            <v-spacer></v-spacer>
            <v-chip v-if="vcdbVersion" color="primary" size="small">{{ vcdbVersion }}</v-chip>
          </v-card-title>
          <v-card-text>
            <p>Vehicle Component Database</p>
            <v-list density="compact" class="bg-transparent">
              <v-list-item v-for="(stat, index) in vcdbStats" :key="index" :title="stat.label" :subtitle="stat.value">
                <template v-slot:prepend>
                  <v-icon :icon="stat.icon" color="primary"></v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" to="/vcdb/vehicles">
              Explore Vehicles
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="primary">mdi-wrench</v-icon>
            PCdb
            <v-spacer></v-spacer>
            <v-chip v-if="pcdbVersion" color="primary" size="small">{{ pcdbVersion }}</v-chip>
          </v-card-title>
          <v-card-text>
            <p>Product Component Database</p>
            <v-list density="compact" class="bg-transparent">
              <v-list-item v-for="(stat, index) in pcdbStats" :key="index" :title="stat.label" :subtitle="stat.value">
                <template v-slot:prepend>
                  <v-icon :icon="stat.icon" color="primary"></v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" to="/pcdb/parts">
              Explore Parts
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="primary">mdi-format-list-bulleted</v-icon>
            PAdb
            <v-spacer></v-spacer>
            <v-chip v-if="padbVersion" color="primary" size="small">{{ padbVersion }}</v-chip>
          </v-card-title>
          <v-card-text>
            <p>Part Attribute Database</p>
            <v-list density="compact" class="bg-transparent">
              <v-list-item v-for="(stat, index) in padbStats" :key="index" :title="stat.label" :subtitle="stat.value">
                <template v-slot:prepend>
                  <v-icon :icon="stat.icon" color="primary"></v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" to="/padb/attributes">
              Explore Attributes
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="3">
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="primary">mdi-text-box</v-icon>
            Qdb
            <v-spacer></v-spacer>
            <v-chip v-if="qdbVersion" color="primary" size="small">{{ qdbVersion }}</v-chip>
          </v-card-title>
          <v-card-text>
            <p>Qualifier Database</p>
            <v-list density="compact" class="bg-transparent">
              <v-list-item v-for="(stat, index) in qdbStats" :key="index" :title="stat.label" :subtitle="stat.value">
                <template v-slot:prepend>
                  <v-icon :icon="stat.icon" color="primary"></v-icon>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" variant="text" to="/qdb/qualifiers">
              Explore Qualifiers
              <v-icon end>mdi-arrow-right</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <v-card class="mb-4">
          <v-card-title>
            <v-icon class="me-2">mdi-magnify</v-icon>
            Quick Search
          </v-card-title>
          <v-card-text>
            <v-tabs v-model="activeTab">
              <v-tab value="vehicles">Vehicles</v-tab>
              <v-tab value="parts">Parts</v-tab>
              <v-tab value="attributes">Attributes</v-tab>
              <v-tab value="qualifiers">Qualifiers</v-tab>
            </v-tabs>

            <v-window v-model="activeTab" class="mt-4">
              <v-window-item value="vehicles">
                <v-row>
                  <v-col cols="12" sm="4">
                    <v-select
                      v-model="quickSearch.vehicles.year"
                      :items="years"
                      item-title="year"
                      item-value="year"
                      label="Year"
                      clearable
                    ></v-select>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <v-autocomplete
                      v-model="quickSearch.vehicles.make"
                      :items="makes"
                      item-title="name"
                      item-value="name"
                      label="Make"
                      clearable
                    ></v-autocomplete>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <v-autocomplete
                      v-model="quickSearch.vehicles.model"
                      :items="models"
                      item-title="name"
                      item-value="name"
                      label="Model"
                      clearable
                    ></v-autocomplete>
                  </v-col>
                </v-row>
                <v-btn
                  color="primary"
                  block
                  :to="{
                    name: 'vcdb-vehicle-search',
                    query: {
                      year: quickSearch.vehicles.year,
                      make: quickSearch.vehicles.make?.name,
                      model: quickSearch.vehicles.model?.name
                    }
                  }"
                  :disabled="!isVehicleSearchValid"
                >
                  Search Vehicles
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-window-item>

              <v-window-item value="parts">
                <v-text-field
                  v-model="quickSearch.parts.term"
                  label="Part Name or Description"
                  clearable
                  hide-details="auto"
                  class="mb-4"
                ></v-text-field>
                <v-btn
                  color="primary"
                  block
                  :to="{
                    name: 'pcdb-part-search',
                    query: { term: quickSearch.parts.term }
                  }"
                  :disabled="!quickSearch.parts.term"
                >
                  Search Parts
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-window-item>

              <v-window-item value="attributes">
                <v-text-field
                  v-model="quickSearch.attributes.term"
                  label="Attribute Name or Description"
                  clearable
                  hide-details="auto"
                  class="mb-4"
                ></v-text-field>
                <v-btn
                  color="primary"
                  block
                  :to="{
                    name: 'padb-attribute-search',
                    query: { term: quickSearch.attributes.term }
                  }"
                  :disabled="!quickSearch.attributes.term"
                >
                  Search Attributes
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-window-item>

              <v-window-item value="qualifiers">
                <v-text-field
                  v-model="quickSearch.qualifiers.term"
                  label="Qualifier Text"
                  clearable
                  hide-details="auto"
                  class="mb-4"
                ></v-text-field>
                <v-btn
                  color="primary"
                  block
                  :to="{
                    name: 'qdb-qualifier-search',
                    query: { term: quickSearch.qualifiers.term }
                  }"
                  :disabled="!quickSearch.qualifiers.term"
                >
                  Search Qualifiers
                  <v-icon end>mdi-arrow-right</v-icon>
                </v-btn>
              </v-window-item>
            </v-window>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="mb-4">
          <v-card-title>
            <v-icon class="me-2">mdi-information</v-icon>
            About
          </v-card-title>
          <v-card-text>
            <p>
              This application provides a comprehensive interface to explore the automotive industry's standard databases:
            </p>
            <ul>
              <li><strong>VCdb:</strong> Vehicle Component Database</li>
              <li><strong>PCdb:</strong> Product Component Database</li>
              <li><strong>PAdb:</strong> Part Attribute Database</li>
              <li><strong>Qdb:</strong> Qualifier Database</li>
            </ul>
            <p>
              These databases are maintained by the Auto Care Association and form the backbone
              of standardized product information in the automotive aftermarket industry.
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import PageHeader from '@/components/common/PageHeader.vue';
import { useVCdbStore } from '@/stores/autocare/vcdb.store';
import { usePCdbStore } from '@/stores/autocare/pcdb.store';
import { usePAdbStore } from '@/stores/autocare/padb.store';
import { useQdbStore } from '@/stores/autocare/qdb.store';

// Stores
const vcdbStore = useVCdbStore();
const pcdbStore = usePCdbStore();
const padbStore = usePAdbStore();
const qdbStore = useQdbStore();

// State
const loading = ref(false);
const error = ref('');
const activeTab = ref('vehicles');

// Database versions
const vcdbVersion = computed(() => vcdbStore.version);
const pcdbVersion = computed(() => pcdbStore.version);
const padbVersion = computed(() => padbStore.version);
const qdbVersion = computed(() => qdbStore.version);

// Dynamic stats computed properties
const vcdbStats = computed(() => [
  { label: 'Total Vehicles', value: vcdbStore.stats?.totalVehicles.toLocaleString(), icon: 'mdi-car' },
  { label: 'Makes', value: vcdbStore.stats?.makeCount.toLocaleString(), icon: 'mdi-car-info' },
  { label: 'Models', value: vcdbStore.stats?.modelCount.toLocaleString(), icon: 'mdi-car-side' },
  { label: 'Year Range', value: vcdbStore.stats?.yearRange, icon: 'mdi-calendar-range' },
]);

const pcdbStats = computed(() => [
  // { label: 'Total Parts', value: pcdbStore.stats?.totalParts.toLocaleString(), icon: 'mdi-wrench' },
  // { label: 'Categories', value: pcdbStore.stats?.categoryCount.toLocaleString(), icon: 'mdi-folder' },
  // { label: 'Positions', value: pcdbStore.stats?.positionCount.toLocaleString(), icon: 'mdi-format-align-left' },
  // { label: 'Supersessions', value: pcdbStore.stats?.supersessionCount.toLocaleString(), icon: 'mdi-arrow-up-down' },
]);

const padbStats = computed(() => [
  // { label: 'Total Attributes', value: padbStore.stats?.totalAttributes.toLocaleString(), icon: 'mdi-format-list-bulleted' },
  // { label: 'Measurement Groups', value: padbStore.stats?.measurementGroupCount.toLocaleString(), icon: 'mdi-ruler' },
  // { label: 'Valid Values', value: padbStore.stats?.validValueCount.toLocaleString(), icon: 'mdi-check-circle' },
  // { label: 'UOM Codes', value: padbStore.stats?.uomCodeCount.toLocaleString(), icon: 'mdi-code-tags' },
]);

const qdbStats = computed(() => [
  // { label: 'Total Qualifiers', value: qdbStore.stats?.totalQualifiers.toLocaleString(), icon: 'mdi-text-box' },
  // { label: 'Qualifier Types', value: qdbStore.stats?.qualifierTypeCount.toLocaleString(), icon: 'mdi-format-list-text' },
  // { label: 'Languages', value: qdbStore.stats?.languageCount.toLocaleString(), icon: 'mdi-translate' },
  // { label: 'Groups', value: qdbStore.stats?.groupCount.toLocaleString(), icon: 'mdi-folder-multiple' },
]);

// Quick search state - keep unchanged
const quickSearch = ref({
  vehicles: {
    year: null,
    make: null,
    model: null,
  },
  parts: {
    term: '',
  },
  attributes: {
    term: '',
  },
  qualifiers: {
    term: '',
  },
});

// Computed properties - keep unchanged
const isVehicleSearchValid = computed(() => {
  return (
    quickSearch.value.vehicles.year !== null ||
    quickSearch.value.vehicles.make !== null ||
    quickSearch.value.vehicles.model !== null
  );
});

// Vehicle search reference data - keep unchanged
const years = computed(() => vcdbStore.years);
const makes = computed(() => vcdbStore.makes);
const models = computed(() => vcdbStore.models);

// Methods
const loadData = async () => {
  try {
    loading.value = true;

    // Load database versions
    await Promise.all([
      vcdbStore.fetchVersion(),
      pcdbStore.fetchVersion(),
      padbStore.fetchVersion(),
      qdbStore.fetchVersion(),
    ]);

    // Load stats data
    await Promise.all([
      vcdbStore.fetchStats(),
      // pcdbStore.fetchStats(),
      // padbStore.fetchStats(),
      // qdbStore.fetchStats(),
    ]);

    // Load reference data for quick search
    await Promise.all([
      vcdbStore.fetchYears(),
      vcdbStore.fetchMakes(),
    ]);

  } catch (err) {
    console.error('Error loading dashboard data:', err);
    error.value = 'Failed to load some dashboard data';
  } finally {
    loading.value = false;
  }
};

const refreshDashboard = () => {
  loadData();
};

// Load initial data
onMounted(() => {
  loadData();
});
</script>

<style scoped>
.dashboard {
  width: 100%;
}
</style>
