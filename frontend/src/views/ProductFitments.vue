<!-- frontend/src/views/ProductFitments.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Loading State -->
      <div v-if="initialLoading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <template v-else-if="product">
        <!-- Page Header with Back Button -->
        <v-row class="mb-6">
          <v-col cols="12">
            <div class="d-flex align-center">
              <v-btn
                icon
                variant="text"
                :to="{ name: 'ProductDetail', params: { id: productId } }"
                class="mr-4"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>

              <div>
                <h1 class="text-h3 font-weight-bold">Manage Fitments</h1>
                <p class="text-subtitle-1">
                  <v-chip
                    color="primary"
                    variant="flat"
                    class="mr-2"
                    size="small"
                    :to="{ name: 'ProductDetail', params: { id: productId } }"
                  >
                    {{ product.sku }}
                  </v-chip>
                  {{ product.name }}
                </p>
              </div>
            </div>
          </v-col>
        </v-row>

        <!-- Main Content -->
        <v-row>
          <!-- Fitments List -->
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="d-flex align-center">
                Compatible Vehicles
                <v-spacer></v-spacer>

                <!-- Batch Actions Button -->
                <v-menu v-if="selected.length > 0">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      color="primary"
                      variant="tonal"
                      v-bind="props"
                      class="mr-2"
                    >
                      Batch Actions ({{ selected.length }})
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item @click="confirmRemoveSelected">
                      <template v-slot:prepend>
                        <v-icon color="error">mdi-link-off</v-icon>
                      </template>
                      <v-list-item-title>Remove Selected</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>

                <!-- Add Existing Fitment Button -->
                <v-btn
                  color="primary"
                  prepend-icon="mdi-link-plus"
                  @click="showAddDialog = true"
                >
                  Add Fitment
                </v-btn>
              </v-card-title>

              <!-- Search and Filter Section -->
              <v-card-text>
                <v-row>
                  <v-col cols="12" sm="8">
                    <v-text-field
                      v-model="search"
                      label="Search Fitments"
                      variant="outlined"
                      density="comfortable"
                      append-inner-icon="mdi-magnify"
                      hide-details
                      @input="filterFitments"
                      clearable
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <v-select
                      v-model="yearFilter"
                      label="Filter by Year"
                      variant="outlined"
                      density="comfortable"
                      :items="availableYears"
                      hide-details
                      @update:modelValue="filterFitments"
                      clearable
                    ></v-select>
                  </v-col>
                </v-row>
              </v-card-text>

              <v-divider></v-divider>

              <!-- Fitments Data Table -->
              <div v-if="loading" class="d-flex justify-center py-4">
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </div>

              <template v-else>
                <v-data-table
                  v-model="selected"
                  :headers="headers"
                  :items="filteredFitments"
                  :loading="loading"
                  item-value="id"
                  show-select
                  class="elevation-0"
                  density="comfortable"
                >
                  <!-- Year Column -->
                  <template v-slot:item.year="{ item }">
                    <div class="font-weight-medium">{{ item.raw.year }}</div>
                  </template>

                  <!-- Make/Model Column -->
                  <template v-slot:item.makeModel="{ item }">
                    <div>
                      <router-link
                        :to="{ name: 'FitmentDetail', params: { id: item.raw.id }}"
                        class="text-decoration-none text-primary font-weight-medium"
                      >
                        {{ item.raw.make }} {{ item.raw.model }}
                      </router-link>
                    </div>
                  </template>

                  <!-- Engine Column -->
                  <template v-slot:item.engine="{ item }">
                    <span>{{ item.raw.engine || 'N/A' }}</span>
                  </template>

                  <!-- Transmission Column -->
                  <template v-slot:item.transmission="{ item }">
                    <span>{{ item.raw.transmission || 'N/A' }}</span>
                  </template>

                  <!-- Actions Column -->
                  <template v-slot:item.actions="{ item }">
                    <div class="d-flex">
                      <v-tooltip text="View Fitment">
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

                      <v-tooltip text="Remove Association">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            icon
                            size="small"
                            color="error"
                            v-bind="props"
                            @click="confirmRemoveSingle(item.raw)"
                            class="ml-2"
                          >
                            <v-icon>mdi-link-off</v-icon>
                          </v-btn>
                        </template>
                      </v-tooltip>
                    </div>
                  </template>

                  <!-- No Data Display -->
                  <template v-slot:no-data>
                    <div class="text-center py-4">
                      <v-icon icon="mdi-car-off" size="large" class="mb-2"></v-icon>
                      <p>No fitments found for this product</p>
                    </div>
                  </template>
                </v-data-table>

                <!-- Pagination -->
                <v-divider v-if="totalPages > 1"></v-divider>
                <v-card-actions v-if="totalPages > 1">
                  <v-spacer></v-spacer>
                  <v-pagination
                    v-model="page"
                    :length="totalPages"
                    @update:modelValue="paginate"
                    rounded="circle"
                  ></v-pagination>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </template>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" md="4">
            <!-- Quick Actions Card -->
            <v-card class="mb-6">
              <v-card-title>Quick Actions</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="primary"
                      variant="outlined"
                      prepend-icon="mdi-car-connected"
                      @click="showBulkDialog = true"
                    >
                      Bulk Add Fitments
                    </v-btn>
                  </v-col>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="secondary"
                      variant="outlined"
                      prepend-icon="mdi-plus-circle"
                      :to="{ name: 'FitmentCreate' }"
                    >
                      Create New Fitment
                    </v-btn>
                  </v-col>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="secondary"
                      variant="outlined"
                      prepend-icon="mdi-view-list"
                      :to="{ name: 'ProductDetail', params: { id: productId } }"
                    >
                      Back to Product
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Statistics Card -->
            <v-card>
              <v-card-title>Fitment Statistics</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="primary" variant="tonal">
                        <v-icon>mdi-car-multiple</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Total Fitments</v-list-item-title>
                    <v-list-item-subtitle>{{ totalFitments }}</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="info" variant="tonal">
                        <v-icon>mdi-car-estate</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Makes</v-list-item-title>
                    <v-list-item-subtitle>{{ uniqueMakes.length }}</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="success" variant="tonal">
                        <v-icon>mdi-car-side</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Models</v-list-item-title>
                    <v-list-item-subtitle>{{ uniqueModels.length }}</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="warning" variant="tonal">
                        <v-icon>mdi-calendar-range</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Year Range</v-list-item-title>
                    <v-list-item-subtitle>{{ yearRange }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Add Fitment Dialog -->
        <v-dialog v-model="showAddDialog" max-width="700">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Add Existing Fitment
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <p class="mb-4">
                Search for and select fitments to associate with this product.
              </p>

              <!-- Fitment Search Filters -->
              <v-row>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="addFilters.year"
                    label="Year"
                    variant="outlined"
                    density="comfortable"
                    :items="availableYearsToAdd"
                    @update:modelValue="searchFitments"
                    clearable
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="addFilters.make"
                    label="Make"
                    variant="outlined"
                    density="comfortable"
                    :items="availableMakesToAdd"
                    @update:modelValue="searchFitments"
                    clearable
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="addFilters.model"
                    label="Model"
                    variant="outlined"
                    density="comfortable"
                    :items="availableModelsToAdd"
                    @update:modelValue="searchFitments"
                    clearable
                    :disabled="!addFilters.make"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    v-model="addFilters.search"
                    label="Search"
                    variant="outlined"
                    density="comfortable"
                    append-inner-icon="mdi-magnify"
                    @click:append-inner="searchFitments"
                    @keyup.enter="searchFitments"
                    clearable
                  ></v-text-field>
                </v-col>
              </v-row>

              <!-- Search Results Table -->
              <div v-if="searchLoading" class="d-flex justify-center py-4">
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </div>

              <v-table v-else-if="searchResults.length > 0">
                <thead>
                <tr>
                  <th class="text-left">Year</th>
                  <th class="text-left">Make</th>
                  <th class="text-left">Model</th>
                  <th class="text-left">Engine</th>
                  <th class="text-center">Add</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="fitment in searchResults" :key="fitment.id">
                  <td>{{ fitment.year }}</td>
                  <td>{{ fitment.make }}</td>
                  <td>{{ fitment.model }}</td>
                  <td>{{ fitment.engine || 'N/A' }}</td>
                  <td class="text-center">
                    <v-btn
                      icon
                      size="small"
                      color="success"
                      @click="addFitment(fitment)"
                      :loading="fitment.adding"
                      :disabled="fitment.added"
                    >
                      <v-icon v-if="fitment.added">mdi-check</v-icon>
                      <v-icon v-else>mdi-plus</v-icon>
                    </v-btn>
                  </td>
                </tr>
                </tbody>
              </v-table>

              <div v-else-if="searchPerformed" class="text-center py-4">
                <v-icon icon="mdi-car-off" size="large" class="mb-2"></v-icon>
                <p>No fitments found matching your search criteria</p>
              </div>

              <div v-else class="text-center py-4">
                <v-icon icon="mdi-magnify" size="large" class="mb-2"></v-icon>
                <p>Use the filters above to search for fitments</p>
              </div>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="tonal"
                @click="showAddDialog = false"
              >
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Bulk Add Dialog -->
        <v-dialog v-model="showBulkDialog" max-width="700">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Bulk Add Fitments
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <p class="mb-4">
                Select multiple years, makes, and models to add in bulk.
              </p>

              <!-- Bulk Filters -->
              <v-row>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="bulkFilters.years"
                    label="Years"
                    variant="outlined"
                    density="comfortable"
                    :items="availableYearsToAdd"
                    multiple
                    chips
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    v-model="bulkFilters.makes"
                    label="Makes"
                    variant="outlined"
                    density="comfortable"
                    :items="availableMakesToAdd"
                    multiple
                    chips
                  ></v-select>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="bulkFilters.models"
                    label="Models"
                    variant="outlined"
                    density="comfortable"
                    :items="availableModelsToAdd"
                    multiple
                    chips
                    :disabled="bulkFilters.makes.length === 0"
                  ></v-select>
                </v-col>
              </v-row>

              <v-alert
                v-if="estimatedBulkCount > 0"
                type="info"
                variant="tonal"
                class="mt-2"
              >
                This will add approximately {{ estimatedBulkCount }} fitments.
              </v-alert>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showBulkDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="bulkAddFitments"
                :loading="bulkLoading"
                :disabled="!canBulkAdd"
              >
                Add Fitments
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Remove Single Fitment Dialog -->
        <v-dialog v-model="showRemoveDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-warning pa-4">
              Remove Fitment Association
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>
                Are you sure you want to remove the association between this product and the fitment
                <strong>{{ fitmentToRemove?.year }} {{ fitmentToRemove?.make }} {{ fitmentToRemove?.model }}</strong>?
              </p>
              <p class="text-medium-emphasis mt-2">
                This will not delete the fitment, only remove the compatibility link.
              </p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showRemoveDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="warning"
                @click="removeFitment"
                :loading="removeLoading"
              >
                Remove
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Remove Multiple Fitments Dialog -->
        <v-dialog v-model="showRemoveMultipleDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-warning pa-4">
              Remove Multiple Fitments
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>
                Are you sure you want to remove the association between this product and
                <strong>{{ selected.length }}</strong> selected fitments?
              </p>
              <p class="text-medium-emphasis mt-2">
                This will not delete the fitments, only remove the compatibility links.
              </p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showRemoveMultipleDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="warning"
                @click="removeSelectedFitments"
                :loading="removeMultipleLoading"
              >
                Remove Selected
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <!-- Not Found State -->
      <div v-else class="text-center my-12">
        <v-icon icon="mdi-alert-circle" color="warning" size="64"></v-icon>
        <h2 class="text-h4 mt-4">Product Not Found</h2>
        <p class="text-body-1 mt-2">The product you're looking for doesn't exist or has been removed.</p>
        <v-btn
          color="primary"
          class="mt-4"
          @click="router.push({ name: 'ProductCatalog' })"
        >
          Back to Products
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import productService from '@/services/product';
import fitmentService from '@/services/fitment';
import { Product } from '@/types/product';
import { Fitment } from '@/types/fitment';
import { notificationService } from '@/utils/notifications';

// Search result with loading state
interface FitmentSearchResult extends Fitment {
  adding?: boolean;
  added?: boolean;
}

// Bulk add filters
interface BulkFilters {
  years: number[];
  makes: string[];
  models: string[];
}

export default defineComponent({
  name: 'ProductFitments',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    // Data loading states
    const initialLoading = ref(true);
    const loading = ref(false);
    const searchLoading = ref(false);
    const bulkLoading = ref(false);
    const removeLoading = ref(false);
    const removeMultipleLoading = ref(false);

    // Product data
    const product = ref<Product | null>(null);
    const fitments = ref<Fitment[]>([]);
    const filteredFitments = ref<Fitment[]>([]);
    const selected = ref<Fitment[]>([]);

    // Dialog states
    const showAddDialog = ref(false);
    const showBulkDialog = ref(false);
    const showRemoveDialog = ref(false);
    const showRemoveMultipleDialog = ref(false);

    // Fitment to remove
    const fitmentToRemove = ref<Fitment | null>(null);

    // Search state
    const search = ref('');
    const yearFilter = ref<number | null>(null);
    const page = ref(1);
    const pageSize = ref(10);
    const totalPages = ref(1);

    // Search results
    const searchResults = ref<FitmentSearchResult[]>([]);
    const searchPerformed = ref(false);

    // Add fitment filters
    const addFilters = ref({
      year: null as number | null,
      make: null as string | null,
      model: null as string | null,
      search: ''
    });

    // Bulk add filters
    const bulkFilters = ref<BulkFilters>({
      years: [],
      makes: [],
      models: []
    });

    // Available options for filters
    const availableMakesToAdd = ref<string[]>([]);
    const availableModelsToAdd = ref<string[]>([]);
    const availableYearsToAdd = ref<number[]>([]);

    // Get product ID from route
    const productId = computed(() => route.params.id as string);

    // Table headers
    const headers = [
      { title: 'Year', key: 'year', sortable: true },
      { title: 'Make/Model', key: 'makeModel', sortable: true },
      { title: 'Engine', key: 'engine', sortable: true },
      { title: 'Transmission', key: 'transmission', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
    ];

    // Computed values for statistics
    const totalFitments = computed(() => fitments.value.length);

    const uniqueMakes = computed(() => {
      const makes = new Set<string>();
      fitments.value.forEach(f => makes.add(f.make));
      return Array.from(makes);
    });

    const uniqueModels = computed(() => {
      const models = new Set<string>();
      fitments.value.forEach(f => models.add(f.model));
      return Array.from(models);
    });

    const yearRange = computed(() => {
      if (fitments.value.length === 0) return 'N/A';

      const years = fitments.value.map(f => f.year);
      const minYear = Math.min(...years);
      const maxYear = Math.max(...years);

      return minYear === maxYear ? minYear.toString() : `${minYear} - ${maxYear}`;
    });

    const availableYears = computed(() => {
      const years = new Set<number>();
      fitments.value.forEach(f => years.add(f.year));
      return Array.from(years).sort((a, b) => b - a); // Sort descending
    });

    // Estimated bulk count
    const estimatedBulkCount = computed(() => {
      if (bulkFilters.value.years.length === 0 || bulkFilters.value.makes.length === 0) {
        return 0;
      }

      // Simple estimation: years × makes × models (or 1 if no models selected)
      const modelCount = bulkFilters.value.models.length || 1;
      return bulkFilters.value.years.length * bulkFilters.value.makes.length * modelCount;
    });

    // Can bulk add
    const canBulkAdd = computed(() => {
      return bulkFilters.value.years.length > 0 && bulkFilters.value.makes.length > 0;
    });

    // Fetch product data
    const fetchProduct = async () => {
      initialLoading.value = true;

      try {
        product.value = await productService.getProduct(productId.value);

        // Fetch fitments after product is loaded
        await fetchFitments();

        // Fetch available options for filters
        await Promise.all([
          fetchAvailableMakes(),
          fetchAvailableYears()
        ]);
      } catch (error) {
        console.error('Error fetching product:', error);
        product.value = null;
        notificationService.error('Failed to load product details');
      } finally {
        initialLoading.value = false;
      }
    };

    // Fetch fitments for the product
    const fetchFitments = async () => {
      loading.value = true;

      try {
        fitments.value = await productService.getProductFitments(productId.value);

        // Apply initial filtering
        filterFitments();

        // Calculate total pages
        totalPages.value = Math.ceil(filteredFitments.value.length / pageSize.value);

        // Reset selected items
        selected.value = [];
      } catch (error) {
        console.error('Error fetching fitments:', error);
        notificationService.error('Failed to load product fitments');
        fitments.value = [];
        filteredFitments.value = [];
      } finally {
        loading.value = false;
      }
    };

    // Fetch available makes
    const fetchAvailableMakes = async () => {
      try {
        availableMakesToAdd.value = await fitmentService.getDistinctValues('make');
      } catch (error) {
        console.error('Error fetching makes:', error);
        availableMakesToAdd.value = [];
      }
    };

    // Fetch available models based on selected make
    const fetchAvailableModels = async () => {
      if (!addFilters.value.make) {
        availableModelsToAdd.value = [];
        return;
      }

      try {
        // In a real implementation, this would call a specific API endpoint
        // For now, simulating with a mock response
        await new Promise(resolve => setTimeout(resolve, 300));

        // Example models for each make
        const modelsByMake: Record<string, string[]> = {
          'Toyota': ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Tacoma'],
          'Honda': ['Accord', 'Civic', 'CR-V', 'Pilot', 'Odyssey'],
          'Ford': ['F-150', 'Mustang', 'Explorer', 'Escape', 'Edge'],
          'Chevrolet': ['Silverado', 'Equinox', 'Tahoe', 'Malibu', 'Camaro'],
          'Nissan': ['Altima', 'Rogue', 'Sentra', 'Pathfinder', 'Frontier']
        };

        // Get models for selected make or empty array if not found
        availableModelsToAdd.value = modelsByMake[addFilters.value.make] || [];
      } catch (error) {
        console.error('Error fetching models:', error);
        availableModelsToAdd.value = [];
      }
    };

    // Fetch available years
    const fetchAvailableYears = async () => {
      try {
        // In a real implementation, this would call a specific API endpoint
        // For now, using a range of years
        const currentYear = new Date().getFullYear();
        const years = [];

        for (let year = currentYear + 1; year >= currentYear - 20; year--) {
          years.push(year);
        }

        availableYearsToAdd.value = years;
      } catch (error) {
        console.error('Error fetching years:', error);
        availableYearsToAdd.value = [];
      }
    };

    // Filter fitments based on search and year filter
    const filterFitments = () => {
      if (!search.value && !yearFilter.value) {
        filteredFitments.value = [...fitments.value];
      } else {
        filteredFitments.value = fitments.value.filter(fitment => {
          // Apply year filter if set
          if (yearFilter.value && fitment.year !== yearFilter.value) {
            return false;
          }

          // Apply search filter if set
          if (search.value) {
            const searchLower = search.value.toLowerCase();
            return (
              fitment.make.toLowerCase().includes(searchLower) ||
              fitment.model.toLowerCase().includes(searchLower) ||
              (fitment.engine && fitment.engine.toLowerCase().includes(searchLower)) ||
              (fitment.transmission && fitment.transmission.toLowerCase().includes(searchLower))
            );
          }

          return true;
        });
      }

      // Reset to first page when filtering
      page.value = 1;

      // Calculate total pages
      totalPages.value = Math.ceil(filteredFitments.value.length / pageSize.value);

      // Apply pagination
      paginate();
    };

    // Apply pagination
    const paginate = () => {
      const start = (page.value - 1) * pageSize.value;
      const end = start + pageSize.value;

      // Slice the filtered fitments for current page
      // (In a real implementation, this would be handled by the backend)
      filteredFitments.value = fitments.value.slice(start, end);
    };

    // Search for fitments to add
    const searchFitments = async () => {
      searchLoading.value = true;
      searchPerformed.value = true;

      try {
        // In a real implementation, this would call an API endpoint
        // For now, simulating with a mock response
        await new Promise(resolve => setTimeout(resolve, 500));

        // Build filter object
        const filters = {
          year: addFilters.value.year,
          make: addFilters.value.make,
          model: addFilters.value.model,
          search: addFilters.value.search
        };

        // Remove null/empty values
        Object.keys(filters).forEach(key => {
          const typedKey = key as keyof typeof filters;
          if (!filters[typedKey]) {
            delete filters[typedKey];
          }
        });

        // Mock response - generate some fitments
        const results: FitmentSearchResult[] = [];

        // Generate 5-10 mock results
        const count = Math.floor(Math.random() * 5) + 5;

        for (let i = 0; i < count; i++) {
          const year = filters.year || (Math.floor(Math.random() * 5) + 2019);
          const make = filters.make || availableMakesToAdd.value[Math.floor(Math.random() * availableMakesToAdd.value.length)];

          let modelOptions = availableModelsToAdd.value;
          if (modelOptions.length === 0) {
            modelOptions = ['Model A', 'Model B', 'Model C', 'Model D', 'Model E'];
          }

          const model = filters.model || modelOptions[Math.floor(Math.random() * modelOptions.length)];
          const engines = ['2.0L I4', '2.4L I4', '3.0L V6', '3.5L V6', '5.0L V8', ''];
          const transmissions = ['Automatic', 'Manual', 'CVT', 'Dual-Clutch', ''];

          // Create fitment
          results.push({
            id: `fitment-${Math.random().toString(36).substr(2, 9)}`,
            year,
            make,
            model,
            engine: engines[Math.floor(Math.random() * engines.length)],
            transmission: transmissions[Math.floor(Math.random() * transmissions.length)],
            attributes: {},
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            adding: false,
            added: false
          });
        }

        // Filter out fitments already associated with the product
        const existingIds = fitments.value.map(f => f.id);
        searchResults.value = results.filter(r => !existingIds.includes(r.id));

      } catch (error) {
        console.error('Error searching fitments:', error);
        notificationService.error('Failed to search fitments');
        searchResults.value = [];
      } finally {
        searchLoading.value = false;
      }
    };

    // Add a fitment to the product
    const addFitment = async (fitment: FitmentSearchResult) => {
      // Update state to show loading
      const index = searchResults.value.findIndex(f => f.id === fitment.id);
      if (index === -1) return;

      searchResults.value[index].adding = true;

      try {
        // In a real implementation, this would call an API endpoint
        await fitmentService.associateProduct(fitment.id, productId.value);

        // Mark as added
        searchResults.value[index].adding = false;
        searchResults.value[index].added = true;

        // Add to fitments list
        fitments.value.push(fitment);

        // Reapply filters
        filterFitments();

        notificationService.success('Fitment added successfully');
      } catch (error) {
        console.error('Error adding fitment:', error);
        notificationService.error('Failed to add fitment');

        // Reset loading state
        searchResults.value[index].adding = false;
      }
    };

    // Show dialog to confirm removing a single fitment
    const confirmRemoveSingle = (fitment: Fitment) => {
      fitmentToRemove.value = fitment;
      showRemoveDialog.value = true;
    };

    // Remove a single fitment from product
    const removeFitment = async () => {
      if (!fitmentToRemove.value) return;

      removeLoading.value = true;

      try {
        await fitmentService.removeProductAssociation(fitmentToRemove.value.id, productId.value);

        // Remove from fitments list
        const index = fitments.value.findIndex(f => f.id === fitmentToRemove.value?.id);
        if (index !== -1) {
          fitments.value.splice(index, 1);
        }

        // Reapply filters
        filterFitments();

        showRemoveDialog.value = false;
        fitmentToRemove.value = null;

        notificationService.success('Fitment removed successfully');
      } catch (error) {
        console.error('Error removing fitment:', error);
        notificationService.error('Failed to remove fitment');
      } finally {
        removeLoading.value = false;
      }
    };

    // Show dialog to confirm removing multiple fitments
    const confirmRemoveSelected = () => {
      if (selected.value.length === 0) return;
      showRemoveMultipleDialog.value = true;
    };

    // Remove selected fitments from product
    const removeSelectedFitments = async () => {
      if (selected.value.length === 0) return;

      removeMultipleLoading.value = true;

      try {
        // Create promises for all removals
        const promises = selected.value.map(fitment =>
          fitmentService.removeProductAssociation(fitment.id, productId.value)
        );

        // Wait for all promises to resolve
        await Promise.all(promises);

        // Remove from fitments list
        const selectedIds = selected.value.map(f => f.id);
        fitments.value = fitments.value.filter(f => !selectedIds.includes(f.id));

        // Reapply filters
        filterFitments();

        showRemoveMultipleDialog.value = false;
        selected.value = [];

        notificationService.success(`${selectedIds.length} fitments removed successfully`);
      } catch (error) {
        console.error('Error removing fitments:', error);
        notificationService.error('Failed to remove fitments');
      } finally {
        removeMultipleLoading.value = false;
      }
    };

    // Bulk add fitments
    const bulkAddFitments = async () => {
      if (!canBulkAdd.value) return;

      bulkLoading.value = true;

      try {
        // In a real implementation, this would call a bulk API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Mock success
        showBulkDialog.value = false;

        // Reset bulk filters
        bulkFilters.value = {
          years: [],
          makes: [],
          models: []
        };

        // Refresh fitments
        await fetchFitments();

        notificationService.success(`${estimatedBulkCount.value} fitments added successfully`);
      } catch (error) {
        console.error('Error bulk adding fitments:', error);
        notificationService.error('Failed to bulk add fitments');
      } finally {
        bulkLoading.value = false;
      }
    };

    // Watch for make change to fetch models
    watch(() => addFilters.value.make, (newMake) => {
      if (newMake) {
        fetchAvailableModels();
      } else {
        availableModelsToAdd.value = [];
        addFilters.value.model = null;
      }
    });

    // Initialize component
    onMounted(() => {
      fetchProduct();
    });

    return {
      router,
      product,
      productId,
      initialLoading,
      loading,
      fitments,
      filteredFitments,
      headers,
      search,
      yearFilter,
      availableYears,
      page,
      pageSize,
      totalPages,
      selected,
      showAddDialog,
      showBulkDialog,
      showRemoveDialog,
      showRemoveMultipleDialog,
      fitmentToRemove,
      searchResults,
      searchPerformed,
      searchLoading,
      addFilters,
      availableMakesToAdd,
      availableModelsToAdd,
      availableYearsToAdd,
      bulkFilters,
      estimatedBulkCount,
      canBulkAdd,
      bulkLoading,
      removeLoading,
      removeMultipleLoading,
      totalFitments,
      uniqueMakes,
      uniqueModels,
      yearRange,
      filterFitments,
      paginate,
      searchFitments,
      addFitment,
      confirmRemoveSingle,
      removeFitment,
      confirmRemoveSelected,
      removeSelectedFitments,
      bulkAddFitments
    };
  }
});
</script>
