<template>
  <div class="makes-list-page">
    <PageHeader
      title="Vehicle Makes"
      subtitle="Browse all vehicle makes in the database"
      icon="mdi-car-info"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search Makes"
          hide-details
          single-line
          density="compact"
          class="search-field"
        ></v-text-field>
      </template>
    </PageHeader>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredMakes"
        :loading="loading"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:item.logo="{ item }">
          <v-avatar size="32">
            <v-img
              :src="`https://via.placeholder.com/32?text=${item.name.charAt(0)}`"
              :alt="item.name"
            ></v-img>
          </v-avatar>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            :to="{ name: 'vcdb-vehicle-search', query: { make: item.name } }"
          >
            <v-icon>mdi-magnify</v-icon>
            <v-tooltip activator="parent" location="bottom">Search Vehicles</v-tooltip>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useVCdbStore } from '@/stores/autocare/vcdb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import { Make } from '@/types';

// Store
const vcdbStore = useVCdbStore();

// State
const loading = ref(false);
const error = ref('');
const search = ref('');

// Table headers
const headers = [
  { title: 'Logo', key: 'logo', sortable: false },
  { title: 'Make ID', key: 'make_id', sortable: true },
  { title: 'Name', key: 'name', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

// Computed
const makes = computed(() => vcdbStore.makes);

const filteredMakes = computed(() => {
  return makes.value;
});

// Methods
const loadMakes = async () => {
  try {
    loading.value = true;
    error.value = '';
    await vcdbStore.fetchMakes();
  } catch (err) {
    console.error('Error loading makes:', err);
    error.value = 'Failed to load makes';
  } finally {
    loading.value = false;
  }
};

// Load initial data
onMounted(() => {
  loadMakes();
});
</script>

<style scoped>
.makes-list-page {
  width: 100%;
}

.search-field {
  max-width: 300px;
}
</style>
