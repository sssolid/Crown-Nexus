<template>
  <div class="vehicle-details-page">
    <PageHeader
      :title="pageTitle"
      :subtitle="pageSubtitle"
      icon="mdi-car"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-btn color="primary" prepend-icon="mdi-arrow-left" to="/vcdb/vehicles">
          Back to Search
        </v-btn>
      </template>
    </PageHeader>

    <VehicleDetails :vehicle-id="vehicleId" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useVCdbStore } from '@/stores/autocare/vcdb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import VehicleDetails from '@/components/autocare/vcdb/VehicleDetails.vue';

// Route
const route = useRoute();

// Store
const vcdbStore = useVCdbStore();

// State
const loading = ref(false);
const error = ref('');

// Computed
const vehicleId = computed(() => route.params.id as string);

const pageTitle = computed(() => {
  if (vcdbStore.currentVehicle) {
    const { year, make, model, submodel } = vcdbStore.currentVehicle;
    let title = `${year} ${make} ${model}`;
    if (submodel) {
      title += ` ${submodel}`;
    }
    return title;
  }
  return 'Vehicle Details';
});

const pageSubtitle = computed(() => {
  if (vcdbStore.currentVehicle) {
    return `Vehicle ID: ${vcdbStore.currentVehicle.vehicle_id}`;
  }
  return 'Loading vehicle information...';
});

// Methods
const clearVehicle = () => {
  vcdbStore.clearVehicle();
};

// Lifecycle hooks
onMounted(() => {
  clearVehicle();
});

// Watch for changes to vehicle ID
watch(() => route.params.id, () => {
  clearVehicle();
});
</script>

<style scoped>
.vehicle-details-page {
  width: 100%;
}
</style>
