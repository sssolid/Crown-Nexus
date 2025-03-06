<!-- frontend/src/views/FitmentCatalog.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Fitment Catalog</h1>
          <p class="text-subtitle-1">Browse and manage vehicle compatibility</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            :to="{ name: 'FitmentCreate' }"
            v-if="isAdmin"
          >
            Add Fitment
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search and Filters -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row>
            <!-- Year Filter -->
            <v-col cols="12" md="3">
              <v-text-field
                v-model="filters.year"
                label="Year"
                type="number"
                variant="outlined"
                density="comfortable"
                hide-details
                clearable
              ></v-text-field>
            </v-col>

            <!-- Make Filter -->
            <v-col cols="12" md="3">
              <v-autocomplete
                v-model="filters.make"
                label="Make"
                :items="makeOptions"
                variant="outlined"
                density="comfortable"
                hide-details
                clearable
              ></v-autocomplete>
            </v-col>

            <!-- Model Filter -->
            <v-col cols="12" md="3">
              <v-autocomplete
                v-model="filters.model"
                label="Model"
                :items="modelOptions"
                variant="outlined"
                density="comfortable"
                hide-details
                clearable
              ></v-autocomplete>
            </v-col>

            <!-- Engine Filter -->
            <v-col cols="12" md="3">
              <v-autocomplete
                v-model="filters.engine"
                label="Engine"
                :items="engineOptions"
                variant="outlined"
                density="comfortable"
                hide-details
                clearable
              ></v-autocomplete>
            </v-col>
          </v-row>

          <!-- Transmission Filter -->
          <v-row class="mt-2">
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="filters.transmission"
                label="Transmission"
                :items="transmissionOptions"
                variant="outlined"
                density="comfortable"
                hide-details
                clearable
              ></v-autocomplete>
            </v-col>

            <!-- Filter Actions -->
            <v-col cols="12" md="6" class="d-flex justify-end align-center">
              <v-btn
                variant="text"
                color="secondary"
                class="mx-2"
                @click="resetFilters"
              >
                Reset Filters
              </v-btn>
              <v-btn
                color="primary"
                variant="tonal"
                @click="fetchFitments"
              >
                Apply Filters
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <!-- Fitments Data Table -->
      <v-card v-else>
        <v-data-table
          v-model:items-per-page="itemsPerPage"
          :headers="headers"
          :items="fitments"
          :loading="loading"
          class="elevation-1"
          loading-text="Loading fitments..."
          no-data-text="No fitments found"
        >
          <!-- Year Column -->
          <template v-slot:item.year="{ item }">
            <div class="font-weight-medium">{{ item.raw.year }}</div>
          </template>

          <!-- Make Column -->
          <template v-slot:item.make="{ item }">
            <div>
              <router-link
                :to="{ name: 'FitmentDetail', params: { id: item.raw.id }}"
                class="text-decoration-none text-primary font-weight-medium"
              >
                {{ item.raw.make }}
              </router-link>
            </div>
          </template>

          <!-- Model Column -->
          <template v-slot:item.model="{ item }">
            <div>{{ item.raw.model }}</div>
          </template>

          <!-- Engine Column -->
          <template v-slot:item.engine="{ item }">
            <div>{{ item.raw.engine || 'N/A' }}</div>
          </template>

          <!-- Transmission Column -->
          <template v-slot:item.transmission="{ item }">
            <div>{{ item.raw.transmission || 'N/A' }}</div>
          </template>

          <!-- Product Count Column -->
          <template v-slot:item.productCount="{ item }">
            <v-chip
              size="small"
              :color="item.raw.products?.length ? 'primary' : 'grey'"
              variant="tonal"
            >
              {{ item.raw.products?.length || 0 }}
            </v-chip>
          </template>

          <!-- Actions Column -->
          <template v-slot:item.actions="{ item }">
            <div class="d-flex">
              <v-tooltip text="View Details">
                <template v-slot:activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    v-bind="props"
                    :to="{ name: 'FitmentDetail', params: { id: item.raw.id }}"
                  >
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Edit Fitment" v-if="isAdmin">
                <template v-slot:activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    color="primary"
                    v-bind="props"
                    :to="{ name: 'FitmentEdit', params: { id: item.raw.id }}"
                    class="mx-1"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Delete Fitment" v-if="isAdmin">
                <template v-slot:activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    color="error"
                    v-bind="props"
                    @click="confirmDelete(item.raw)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-data-table>

        <!-- Pagination -->
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-pagination
            v-model="page"
            :length="totalPages"
            @update:modelValue="fetchFitments"
            rounded="circle"
          ></v-pagination>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-card>

      <!-- Delete Confirmation Dialog -->
      <v-dialog v-model="deleteDialog" max-width="500">
        <v-card>
          <v-card-title class="text-h5 bg-error text-white pa-4">
            Confirm Delete
          </v-card-title>
          <v-card-text class="pa-4 pt-6">
            <p>Are you sure you want to delete the fitment <strong>{{ fitmentToDelete?.year }} {{ fitmentToDelete?.make }} {{ fitmentToDelete?.model }}</strong>?</p>
            <p class="text-medium-emphasis mt-2">This action cannot be undone.</p>
            <v-alert
              v-if="fitmentToDelete?.products?.length"
              type="warning"
              variant="tonal"
              class="mt-4"
            >
              This fitment is associated with {{ fitmentToDelete?.products?.length }} products. Deleting it will remove these associations.
            </v-alert>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              variant="tonal"
              @click="deleteDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
              color="error"
              @click="deleteFitment"
              :loading="deleteLoading"
            >
              Delete
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Fitment, FitmentFilters } from '@/types/fitment';

export default defineComponent({
  name: 'FitmentCatalog',

  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    // User permissions
    const isAdmin = computed(() => authStore.isAdmin);

    // Data loading state
    const loading = ref(false);
    const fitments = ref<Fitment[]>([]);

    // Pagination
    const page = ref(1);
    const itemsPerPage = ref(10);
    const totalItems = ref(0);
    const totalPages = ref(1);

    // Filters
    const filters = ref<FitmentFilters>({
      page: 1,
      page_size: 10,
    });

    // Filter options (would be populated from API in a real implementation)
    const makeOptions = ref<string[]>([
      'Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 'BMW', 'Mercedes-Benz'
    ]);

    const modelOptions = ref<string[]>([
      'Camry', 'Accord', 'F-150', 'Silverado', 'Altima', '3 Series', 'C-Class'
    ]);

    const engineOptions = ref<string[]>([
      '2.5L I4', '3.5L V6', '5.0L V8', '2.0L Turbo', '3.0L Turbo'
    ]);

    const transmissionOptions = ref<string[]>([
      'Automatic', 'Manual', 'CVT', 'Dual-Clutch', '8-Speed Automatic'
    ]);

    // Delete functionality
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);
    const fitmentToDelete = ref<Fitment | null>(null);

    // Table headers
    const headers = [
      { title: 'Year', key: 'year', sortable: true },
      { title: 'Make', key: 'make', sortable: true },
      { title: 'Model', key: 'model', sortable: true },
      { title: 'Engine', key: 'engine', sortable: true },
      { title: 'Transmission', key: 'transmission', sortable: true },
      { title: 'Products', key: 'productCount', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
    ];

    // Update filters when page changes
    watch(page, (newValue) => {
      filters.value.page = newValue;
    });

    // Update filters when items per page changes
    watch(itemsPerPage, (newValue) => {
      filters.value.page_size = newValue;
      // Reset to first page when changing page size
      page.value = 1;
      filters.value.page = 1;
    });

    // Fetch fitments with current filters
    const fetchFitments = async () => {
      loading.value = true;

      try {
        // In a real implementation, this would call a fitmentService
        // For now, we'll use mock data
        await new Promise(resolve => setTimeout(resolve, 500));

        // Mock response data
        const mockFitments: Fitment[] = [];
        for (let i = 0; i < 20; i++) {
          mockFitments.push({
            id: `fitment-${i}`,
            year: 2020 + Math.floor(i / 5),
            make: makeOptions.value[i % makeOptions.value.length],
            model: modelOptions.value[i % modelOptions.value.length],
            engine: i % 2 === 0 ? engineOptions.value[i % engineOptions.value.length] : undefined,
            transmission: i % 3 === 0 ? transmissionOptions.value[i % transmissionOptions.value.length] : undefined,
            attributes: {},
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            products: i % 4 === 0 ? [{ id: 'product-1' }] : []
          });
        }

        const startIndex = (page.value - 1) * itemsPerPage.value;
        const endIndex = startIndex + itemsPerPage.value;
        fitments.value = mockFitments.slice(startIndex, endIndex);

        totalItems.value = mockFitments.length;
        totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value);
      } catch (error) {
        console.error('Error fetching fitments:', error);
      } finally {
        loading.value = false;
      }
    };

    // Reset all filters
    const resetFilters = () => {
      filters.value = {
        page: 1,
        page_size: itemsPerPage.value,
      };
      page.value = 1;
      fetchFitments();
    };

    // Delete confirmation dialog
    const confirmDelete = (fitment: Fitment) => {
      fitmentToDelete.value = fitment;
      deleteDialog.value = true;
    };

    // Delete fitment
    const deleteFitment = async () => {
      if (!fitmentToDelete.value) return;

      deleteLoading.value = true;

      try {
        // In a real implementation, this would call a fitmentService
        await new Promise(resolve => setTimeout(resolve, 500));

        deleteDialog.value = false;

        // Remove from local list or refetch
        fetchFitments();
      } catch (error) {
        console.error('Error deleting fitment:', error);
      } finally {
        deleteLoading.value = false;
      }
    };

    // Initialize component
    onMounted(() => {
      fetchFitments();
    });

    return {
      isAdmin,
      loading,
      fitments,
      page,
      itemsPerPage,
      totalItems,
      totalPages,
      filters,
      makeOptions,
      modelOptions,
      engineOptions,
      transmissionOptions,
      headers,
      deleteDialog,
      deleteLoading,
      fitmentToDelete,
      fetchFitments,
      resetFilters,
      confirmDelete,
      deleteFitment,
    };
  }
});
</script>
