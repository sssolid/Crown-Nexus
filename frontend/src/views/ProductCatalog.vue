<!-- frontend/src/views/ProductCatalog.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Product Catalog</h1>
          <p class="text-subtitle-1">Browse and manage products</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            :to="{ name: 'ProductCreate' }"
            v-if="isAdmin"
          >
            Add Product
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search and Filters -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="searchInput"
                label="Search Products"
                variant="outlined"
                density="comfortable"
                append-inner-icon="mdi-magnify"
                hide-details
                @keyup.enter="applyFilters"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="statusFilter"
                label="Status"
                :items="statusOptions"
                variant="outlined"
                density="comfortable"
                clearable
                hide-details
              ></v-select>
            </v-col>
          </v-row>
          <v-row class="mt-2">
            <v-col cols="12" class="d-flex justify-end">
              <v-btn variant="text" color="primary" @click="showAdvancedFilters = !showAdvancedFilters">
                <v-icon :icon="showAdvancedFilters ? 'mdi-chevron-up' : 'mdi-chevron-down'" class="mr-1"></v-icon>
                Advanced Filters
              </v-btn>
              <v-btn variant="text" color="secondary" class="ml-2" @click="resetFilters">
                Reset Filters
              </v-btn>
            </v-col>
          </v-row>
          <v-expand-transition>
            <div v-if="showAdvancedFilters">
              <v-divider class="mt-2 mb-4"></v-divider>
              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="partNumberFilter"
                    label="Part Number"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="attributeFilter"
                    label="Attribute Filter"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    placeholder="material:steel"
                    hint="Format: key:value"
                    persistent-hint
                  ></v-text-field>
                </v-col>
              </v-row>
            </div>
          </v-expand-transition>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="tonal" @click="applyFilters" :loading="loading">
            Apply Filters
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- Loading State -->
      <div v-if="loading && products.length === 0" class="d-flex justify-center my-6">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </div>

      <!-- Products Data Table -->
      <v-card v-if="!loading || products.length > 0">
        <v-data-table-server
          v-model:options="tableOptions"
          :headers="headers"
          :items="products"
          :items-length="totalItems"
          :loading="loading"
          :items-per-page-options="itemsPerPageOptions"
          class="elevation-1"
          loading-text="Loading products..."
          no-data-text="No products found"
          @update:options="onTableOptionsChange"
        >
          <template #item.part_number="{ item }">
            <div>
              <router-link
                :to="{ name: 'ProductDetail', params: { id: item.id }}"
                class="text-decoration-none text-primary font-weight-medium"
              >
                {{ item.part_number }}
              </router-link>
              <div class="text-caption text-medium-emphasis">
                {{ getDescription(item.descriptions, 'Standard') }}
              </div>
            </div>
          </template>

          <template #item.description="{ item }">
            <div style="white-space: normal; word-break: break-word; overflow-wrap: break-word;">
              {{ getDescription(item.descriptions, 'Long_AllModels') }}
            </div>
          </template>

          <template #item.is_active="{ item }">
            <v-chip
              :color="item.is_active ? 'success' : 'error'"
              size="small"
              variant="tonal"
            >
              {{ item.is_active ? 'Active' : 'Inactive' }}
            </v-chip>
          </template>

          <template #item.actions="{ item }">
            <div class="d-flex">
              <v-tooltip text="View Details">
                <template #activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    v-bind="props"
                    :to="{ name: 'ProductDetail', params: { id: item.id }}"
                  >
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              <v-tooltip text="Edit Product" v-if="isAdmin">
                <template #activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    color="primary"
                    v-bind="props"
                    :to="{ name: 'ProductEdit', params: { id: item.id }}"
                    class="mx-1"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              <v-tooltip text="Delete Product" v-if="isAdmin">
                <template #activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    color="error"
                    v-bind="props"
                    @click="confirmDelete(item)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-data-table-server>
      </v-card>

      <!-- No Results Message -->
      <v-card v-if="!loading && products.length === 0" class="text-center py-8">
        <v-icon icon="mdi-alert-circle-outline" size="64" color="grey-lighten-1" class="mb-4"></v-icon>
        <h3 class="text-h5 font-weight-medium mb-2">No Products Found</h3>
        <p class="text-body-1 text-medium-emphasis mb-4">
          Try adjusting your search or filter criteria
        </p>
        <v-btn color="primary" @click="resetFilters">Clear Filters</v-btn>
      </v-card>
    </v-container>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-error text-white pa-4">
          Confirm Delete
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p>Are you sure you want to delete the product?</p>
          <p class="font-weight-bold mt-2">{{ productToDelete?.part_number }}</p>
          <p class="text-caption text-medium-emphasis mt-4">
            This action cannot be undone. This will permanently delete the product and all associated data.
          </p>
        </v-card-text>
        <v-card-actions class="pa-4 pt-0">
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="deleteDialog = false" :disabled="deleteLoading">Cancel</v-btn>
          <v-btn
            color="error"
            variant="elevated"
            @click="deleteProduct"
            :loading="deleteLoading"
          >
            Delete Product
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar for notifications -->
    <v-snackbar v-model="snackbar.show" :timeout="5000" :color="snackbar.color">
      {{ snackbar.text }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.show = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import productService from '@/services/product';
import { Product, ProductFilters, ProductDescription } from '@/types/product';

const router = useRouter();
const authStore = useAuthStore();
const isAdmin = computed(() => authStore.isAdmin);

// Table configuration
const itemsPerPageOptions = [
  { title: '10', value: 10 },
  { title: '25', value: 25 },
  { title: '50', value: 50 },
  { title: '100', value: 100 }
];

const tableOptions = ref({
  page: 1,
  itemsPerPage: 10,
  sortBy: [{ key: 'part_number', order: 'asc' }],
  groupBy: [],
  multiSort: false
});

// State variables
const loading = ref(false);
const products = ref<Product[]>([]);
const totalItems = ref(0);
const searchInput = ref('');
const partNumberFilter = ref('');
const attributeFilter = ref('');
const statusFilter = ref<boolean | null>(null);
const showAdvancedFilters = ref(false);

// Filters that will be sent to the API
const currentFilters = ref<ProductFilters>({
  page: 1,
  page_size: 10,
  sort_by: 'part_number',
  sort_desc: false,
});

// Snackbar notification
const snackbar = reactive({
  show: false,
  text: '',
  color: 'success'
});

// Table headers
const headers = [
  { key: 'part_number', title: 'Name', sortable: true, align: 'start' },
  { key: 'description', title: 'Description', sortable: false },
  { key: 'is_active', title: 'Status', sortable: true, align: 'center', width: '120px' },
  { key: 'actions', title: 'Actions', sortable: false, align: 'end', width: '120px' }
];

const statusOptions = [
  { title: 'Active', value: true },
  { title: 'Inactive', value: false }
];

// Delete dialog state
const deleteDialog = ref(false);
const deleteLoading = ref(false);
const productToDelete = ref<Product | null>(null);

// Build filters from UI state
const buildFilters = () => {
  const filters: ProductFilters = {
    page: tableOptions.value.page,
    page_size: tableOptions.value.itemsPerPage,
    sort_by: tableOptions.value.sortBy[0]?.key || 'part_number',
    sort_desc: tableOptions.value.sortBy[0]?.order === 'desc'
  };

  if (searchInput.value) filters.search = searchInput.value;
  if (statusFilter.value !== null) filters.is_active = statusFilter.value;
  if (partNumberFilter.value) filters.part_number = partNumberFilter.value;
  if (attributeFilter.value?.includes(':')) {
    const [key, value] = attributeFilter.value.split(':');
    if (key && value) filters.attributes = { [key.trim()]: value.trim() };
  }

  return filters;
};

// Fetch products from the API
const fetchProducts = async () => {
  loading.value = true;
  try {
    const filters = buildFilters();
    currentFilters.value = { ...filters }; // Ensure deep copy to avoid reactivity issues

    const response = await productService.getProducts(filters);
    products.value = response.items;
    totalItems.value = response.total;
  } catch (err) {
    showErrorMessage('Failed to load products. Please try again.');
    console.error('Fetch failed:', err);
  } finally {
    loading.value = false;
  }
};

// Handle table options changes (sorting, pagination)
const onTableOptionsChange = () => {
  fetchProducts(); // Simply fetch products with updated options
};

// Watch tableOptions for changes
watch(tableOptions, () => {
  onTableOptionsChange();
}, { deep: true });

// Extract description by type from product descriptions
const getDescription = (descriptions: ProductDescription[] | undefined, type: string): string => {
  if (!descriptions || !Array.isArray(descriptions)) return 'N/A';
  const description = descriptions.find(d => d.description_type === type);
  return description?.description || 'N/A';
};

// Reset all filters and reload products
const resetFilters = () => {
  searchInput.value = '';
  partNumberFilter.value = '';
  attributeFilter.value = '';
  statusFilter.value = null;
  showAdvancedFilters.value = false;

  tableOptions.value = {
    page: 1,
    itemsPerPage: 10,
    sortBy: [{ key: 'part_number', order: 'asc' }],
    groupBy: [],
    multiSort: false
  };

  fetchProducts();
};

// Apply filters and fetch products
const applyFilters = () => {
  tableOptions.value.page = 1; // Reset to first page on filter apply
  fetchProducts();
};

// Confirm product deletion
const confirmDelete = (product: Product) => {
  productToDelete.value = product;
  deleteDialog.value = true;
};

// Delete the product
const deleteProduct = async () => {
  if (!productToDelete.value) return;

  deleteLoading.value = true;
  try {
    await productService.deleteProduct(productToDelete.value.id);
    showSuccessMessage(`Product ${productToDelete.value.part_number} deleted successfully`);
    deleteDialog.value = false;

    if (products.value.length === 1 && tableOptions.value.page > 1) {
      tableOptions.value.page--;
    }
    fetchProducts();
  } catch (error) {
    showErrorMessage('Failed to delete product. Please try again.');
    console.error('Delete failed:', error);
  } finally {
    deleteLoading.value = false;
    productToDelete.value = null;
  }
};

// Show success message
const showSuccessMessage = (text: string) => {
  snackbar.text = text;
  snackbar.color = 'success';
  snackbar.show = true;
};

// Show error message
const showErrorMessage = (text: string) => {
  snackbar.text = text;
  snackbar.color = 'error';
  snackbar.show = true;
};

// Initialize component
onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const searchParam = urlParams.get('search');
  if (searchParam) {
    searchInput.value = searchParam;
  }
  fetchProducts();
});
</script>
