<template>
  <div class="vehicle-details">
    <template v-if="vehicle">
      <v-row>
        <v-col cols="12">
          <DetailCard
            title="Vehicle Information"
            icon="mdi-car"
            :loading="loading"
            :error="error"
          >
            <v-row>
              <v-col cols="12" md="6">
                <InfoList :items="vehicleInfo" />
              </v-col>
              <v-col cols="12" md="6">
                <InfoList :items="additionalInfo" />
              </v-col>
            </v-row>
          </DetailCard>
        </v-col>
      </v-row>

      <v-row v-if="vehicleConfigurations">
        <v-col cols="12" md="6" v-if="vehicleConfigurations.engines.length > 0">
          <DetailCard title="Engine Options" icon="mdi-engine">
            <v-list density="compact">
              <v-list-item v-for="engine in vehicleConfigurations.engines" :key="engine.id">
                <v-list-item-title>
                  {{ formatEngineDescription(engine.liter, engine.cylinders, engine.aspiration, engine.fuel_type) }}
                </v-list-item-title>
                <v-list-item-subtitle v-if="engine.power">
                  {{ engine.power.horsepower }} HP / {{ engine.power.kilowatt }} kW
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </DetailCard>
        </v-col>

        <v-col cols="12" md="6" v-if="vehicleConfigurations.transmissions.length > 0">
          <DetailCard title="Transmission Options" icon="mdi-cog-transfer">
            <v-list density="compact">
              <v-list-item v-for="transmission in vehicleConfigurations.transmissions" :key="transmission.id">
                <v-list-item-title>
                  {{ formatTransmissionDescription(transmission.type, transmission.speeds, transmission.control_type) }}
                </v-list-item-title>
                <v-list-item-subtitle v-if="transmission.manufacturer">
                  {{ transmission.manufacturer }} {{ transmission.code ? `(${transmission.code})` : '' }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </DetailCard>
        </v-col>
      </v-row>

      <v-row v-if="vehicleConfigurations">
        <v-col cols="12" md="4" v-if="vehicleConfigurations.drive_types.length > 0">
          <DetailCard title="Drive Types" icon="mdi-car-shift-pattern">
            <v-chip-group class="ma-2">
              <v-chip
                v-for="driveType in vehicleConfigurations.drive_types"
                :key="driveType.id"
                color="primary"
                variant="outlined"
                class="ma-1"
              >
                {{ driveType.name }}
              </v-chip>
            </v-chip-group>
          </DetailCard>
        </v-col>

        <v-col cols="12" md="4" v-if="vehicleConfigurations.body_styles.length > 0">
          <DetailCard title="Body Styles" icon="mdi-car-side">
            <v-list density="compact">
              <v-list-item v-for="bodyStyle in vehicleConfigurations.body_styles" :key="bodyStyle.id">
                <v-list-item-title>{{ bodyStyle.type }}</v-list-item-title>
                <v-list-item-subtitle v-if="bodyStyle.doors">
                  {{ bodyStyle.doors }} Doors
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </DetailCard>
        </v-col>

        <v-col cols="12" md="4" v-if="vehicleConfigurations.wheel_bases.length > 0">
          <DetailCard title="Wheel Bases" icon="mdi-ruler">
            <v-list density="compact">
              <v-list-item v-for="wheelBase in vehicleConfigurations.wheel_bases" :key="wheelBase.id">
                <v-list-item-title>{{ wheelBase.wheel_base }} in</v-list-item-title>
                <v-list-item-subtitle v-if="wheelBase.wheel_base_metric">
                  {{ wheelBase.wheel_base_metric }} mm
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </DetailCard>
        </v-col>
      </v-row>

      <v-row v-if="vehicleConfigurations && vehicleConfigurations.brake_configs.length > 0">
        <v-col cols="12">
          <DetailCard title="Brake Configurations" icon="mdi-car-brake-abs">
            <v-table>
              <thead>
                <tr>
                  <th>Front</th>
                  <th>Rear</th>
                  <th>System</th>
                  <th>ABS</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="brake in vehicleConfigurations.brake_configs" :key="brake.id">
                  <td>{{ brake.front_type }}</td>
                  <td>{{ brake.rear_type }}</td>
                  <td>{{ brake.system }}</td>
                  <td>{{ brake.abs }}</td>
                </tr>
              </tbody>
            </v-table>
          </DetailCard>
        </v-col>
      </v-row>
    </template>

    <div v-else-if="loading" class="text-center my-8">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      <h3 class="mt-4">Loading vehicle details...</h3>
    </div>

    <v-alert v-else-if="error" type="error" :text="error" variant="tonal" class="my-4"></v-alert>

    <div v-else class="text-center my-8">
      <v-icon icon="mdi-car-off" size="64" color="grey"></v-icon>
      <h3 class="mt-4">Vehicle not found</h3>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import DetailCard from '@/components/common/DetailCard.vue';
import InfoList from '@/components/common/InfoList.vue';
import { useVCdbStore } from '@/stores/autocare/vcdb.store.ts';
import { VehicleDetail, VehicleConfigurationResponse } from '@/types';
import { formatEngineDescription, formatTransmissionDescription } from '@/utils/formatters.ts';

const props = defineProps({
  vehicleId: {
    type: [Number, String],
    required: true,
  },
});

const vcdbStore = useVCdbStore();

// State
const loading = ref(false);
const error = ref('');

// Computed
const vehicle = computed(() => vcdbStore.currentVehicle);
const vehicleConfigurations = computed(() => vcdbStore.vehicleConfigurations);

const vehicleInfo = computed(() => {
  if (!vehicle.value) return [];

  return [
    { key: 'year', label: 'Year', value: vehicle.value.year },
    { key: 'make', label: 'Make', value: vehicle.value.make },
    { key: 'model', label: 'Model', value: vehicle.value.model },
    { key: 'submodel', label: 'Submodel', value: vehicle.value.submodel },
  ];
});

const additionalInfo = computed(() => {
  if (!vehicle.value) return [];

  return [
    { key: 'vehicle_id', label: 'Vehicle ID', value: vehicle.value.vehicle_id },
    { key: 'base_vehicle_id', label: 'Base Vehicle ID', value: vehicle.value.base_vehicle_id },
    { key: 'region', label: 'Region', value: vehicle.value.region },
  ];
});

// Methods
const loadVehicle = async () => {
  try {
    loading.value = true;
    error.value = '';

    await vcdbStore.fetchVehicleDetails(Number(props.vehicleId));
    await vcdbStore.fetchVehicleConfigurations(Number(props.vehicleId));
  } catch (err) {
    console.error('Error loading vehicle details:', err);
    error.value = 'Failed to load vehicle details';
  } finally {
    loading.value = false;
  }
};

// Lifecycle hooks
onMounted(() => {
  loadVehicle();
});

// Watch for changes to vehicleId
watch(() => props.vehicleId, () => {
  loadVehicle();
});
</script>

<style scoped>
.vehicle-details {
  width: 100%;
}
</style>
