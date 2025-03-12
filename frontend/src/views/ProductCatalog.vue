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
            <!-- Search Bar -->
            <v-col cols="12" md="6">
              <v-text-field
                v-model="search"
                label="Search Products"
                variant="outlined"
                density="comfortable"
                append-inner-icon="mdi-magnify"
                hide-details
                @keyup.enter="fetchProducts"
                @click:append-inner="fetchProducts"
              ></v-text-field>
            </v-col>

            <!-- Category Filter -->
            <v-col cols="12" md="3">
              <v-select
                v-model="filters.category_id"
                label="Category"
                :items="categories"
                item-title="name"
                item-value="id"
                variant="outlined"
                density="comfortable"
                clearable
                hide-details
                return-object
              ></v-select>
            </v-col>

            <!-- Active Filter -->
            <v-col cols="12" md="3">
              <v-select
                v-model="filters.is_active"
                label="Status"
                :items="statusOptions"
                variant="outlined"
                density="comfortable"
                clearable
                hide-details
              ></v-select>
            </v-col>
          </v-row>

          <!-- Advanced Filters Button -->
          <v-row class="mt-2">
            <v-col cols="12" class="d-flex justify-end">
              <v-btn
                variant="text"
                color="primary"
                @click="showAdvancedFilters = !showAdvancedFilters"
              >
                <v-icon :icon="showAdvancedFilters ? 'mdi-chevron-up' : 'mdi-chevron-down'" class="mr-1"></v-icon>
                Advanced Filters
              </v-btn>
              <v-btn
                variant="text"
                color="secondary"
                class="ml-2"
                @click="resetFilters"
              >
                Reset Filters
              </v-btn>
            </v-col>
          </v-row>

          <!-- Advanced Filters -->
          <v-expand-transition>
            <div v-if="showAdvancedFilters">
              <v-divider class="mt-2 mb-4"></v-divider>
              <v-row>
                <!-- Part Number -->
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="filters.part_number"
                    label="Part Number"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                  ></v-text-field>
                </v-col>

                <!-- SKU -->
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="filters.sku"
                    label="SKU"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                  ></v-text-field>
                </v-col>

                <!-- Attribute Filter (example) -->
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
          <v-btn
            color="primary"
            variant="tonal"
            @click="fetchProducts"
          >
            Apply Filters
          </v-btn>
        </v-card-actions>
      </v-card>

      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <!-- Products Data Table -->
      <v-card v-else>
        <v-data-table
          v-model:items-per-page="itemsPerPage"
          :headers="headers"
          :items="products"
          :loading="loading"
          class="elevation-1"
          loading-text="Loading products..."
          no-data-text="No products found"
        >
          <!-- SKU Column -->
          <template v-slot:item.sku="{ item }">
            <div class="font-weight-medium">{{ item.sku }}</div>
          </template>

          <!-- Name Column -->
          <template v-slot:item.name="{ item }">
            <div>
              <router-link
                :to="{ name: 'ProductDetail', params: { id: item.id }}"
                class="text-decoration-none text-primary font-weight-medium"
              >
                {{ item.name }}
              </router-link>
              <div class="text-caption text-medium-emphasis">
                {{ item.part_number }}
              </div>
            </div>
          </template>

          <!-- Description Column -->
          <template v-slot:item.description="{ item }">
            <div class="text-truncate" style="max-width: 250px">
              {{ item.description || 'No description' }}
            </div>
          </template>

          <!-- Category Column -->
          <template v-slot:item.category="{ item }">
            <v-chip
              v-if="item.category"
              size="small"
              color="primary"
              variant="tonal"
            >
              {{ item.category.name }}
            </v-chip>
            <span v-else class="text-medium-emphasis">None</span>
          </template>

          <!-- Status Column -->
          <template v-slot:item.is_active="{ item }">
            <v-chip
              :color="item.is_active ? 'success' : 'error'"
              size="small"
              variant="tonal"
            >
              {{ item.is_active ? 'Active' : 'Inactive' }}
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
                    :to="{ name: 'ProductDetail', params: { id: item.id }}"
                  >
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Edit Product" v-if="isAdmin">
                <template v-slot:activator="{ props }">
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
            @update:modelValue="fetchProducts"
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
            <p>Are you sure you want to delete the product <strong>{{ productToDelete?.name }}</strong>?</p>
            <p class="text-medium-emphasis mt-2">This action cannot be undone.</p>
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
              @click="deleteProduct"
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
import productService from '@/services/product';
import { Product, ProductFilters } from '@/types/product';
import { Category } from '@/types/category';

export default defineComponent({
  name: 'ProductCatalog',

  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    // User permissions
    const isAdmin = computed(() => authStore.isAdmin);

    // Data loading state
    const loading = ref(false);
    const products = ref<Product[]>([]);
    const categories = ref<Category[]>([]);

    // Pagination
    const page = ref(1);
    const itemsPerPage = ref(10);
    const totalItems = ref(0);
    const totalPages = ref(1);

    // Filters
    const search = ref('');
    const attributeFilter = ref('');
    const showAdvancedFilters = ref(false);
    const filters = ref<ProductFilters>({
      page: 1,
      page_size: 10,
    });

    // Delete functionality
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);
    const productToDelete = ref<Product | null>(null);

    // Table headers
    const headers = [
      { title: 'SKU', key: 'sku', sortable: true },
      { title: 'Name', key: 'name', sortable: true },
      { title: 'Description', key: 'description', sortable: false },
      { title: 'Category', key: 'category', sortable: false },
      { title: 'Status', key: 'is_active', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
    ];

    // Status filter options
    const statusOptions = [
      { title: 'Active', value: true },
      { title: 'Inactive', value: false },
    ];

    // Update filters when search changes
    watch(search, (newValue) => {
      filters.value.search = newValue || undefined;
    });

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

    // Process attribute filter
    watch(attributeFilter, (newValue) => {
      if (newValue && newValue.includes(':')) {
        const [key, value] = newValue.split(':');
        if (key && value) {
          filters.value.attributes = filters.value.attributes || {};
          filters.value.attributes[key.trim()] = value.trim();
        }
      } else {
        filters.value.attributes = undefined;
      }
    });

    // Fetch products with current filters
    const fetchProducts = async () => {
      loading.value = true;

      try {
        const response = await productService.getProducts({
          ...filters.value,
          page: page.value,
          page_size: itemsPerPage.value,
        });

        products.value = response.items;
        totalItems.value = response.total;
        totalPages.value = response.pages;
        page.value = response.page;
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        loading.value = false;
      }
    };

    // Fetch categories for filter dropdown
    const fetchCategories = async () => {
      try {
        categories.value = await productService.getCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    // Reset all filters
    const resetFilters = () => {
      search.value = '';
      attributeFilter.value = '';
      filters.value = {
        page: 1,
        page_size: itemsPerPage.value,
      };
      page.value = 1;
      fetchProducts();
    };

    // Delete confirmation dialog
    const confirmDelete = (product: Product) => {
      productToDelete.value = product;
      deleteDialog.value = true;
    };

    // Delete product
    const deleteProduct = async () => {
      if (!productToDelete.value) return;

      deleteLoading.value = true;

      try {
        await productService.deleteProduct(productToDelete.value.id);
        deleteDialog.value = false;

        // Remove from local list or refetch
        fetchProducts();
      } catch (error) {
        console.error('Error deleting product:', error);
      } finally {
        deleteLoading.value = false;
      }
    };

    // Initialize component
    onMounted(() => {
      fetchProducts();
      fetchCategories();
    });

    return {
      authStore,
      isAdmin,
      loading,
      products,
      categories,
      page,
      itemsPerPage,
      totalItems,
      totalPages,
      search,
      attributeFilter,
      showAdvancedFilters,
      filters,
      headers,
      statusOptions,
      deleteDialog,
      deleteLoading,
      productToDelete,
      fetchProducts,
      resetFilters,
      confirmDelete,
      deleteProduct,
    };
  }
});
</script>
