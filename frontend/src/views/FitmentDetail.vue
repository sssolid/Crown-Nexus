<!-- frontend/src/views/FitmentDetail.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <template v-else-if="fitment">
        <!-- Page Header with Actions -->
        <v-row class="mb-6">
          <v-col cols="12" md="8">
            <div class="d-flex align-center">
              <v-btn
                icon
                variant="text"
                @click="router.back()"
                class="mr-4"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>

              <div>
                <h1 class="text-h3 font-weight-bold">
                  {{ fitment.year }} {{ fitment.make }} {{ fitment.model }}
                </h1>
                <p class="text-subtitle-1">
                  {{ fitment.engine || '' }} {{ fitment.transmission || '' }}
                </p>
              </div>
            </div>
          </v-col>

          <v-col cols="12" md="4" class="d-flex justify-end align-center">
            <v-btn
              v-if="isAdmin"
              color="primary"
              prepend-icon="mdi-pencil"
              :to="{ name: 'FitmentEdit', params: { id: fitment.id }}"
              class="mr-2"
            >
              Edit
            </v-btn>

            <v-btn
              v-if="isAdmin"
              color="error"
              variant="outlined"
              prepend-icon="mdi-delete"
              @click="confirmDelete"
            >
              Delete
            </v-btn>
          </v-col>
        </v-row>

        <!-- Fitment Details -->
        <v-row>
          <!-- Main Fitment Info -->
          <v-col cols="12" md="8">
            <v-card class="mb-6">
              <v-card-title>Fitment Details</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <!-- Vehicle Info -->
                  <v-col cols="12" md="6">
                    <v-list>
                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-calendar" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Year</v-list-item-title>
                        <v-list-item-subtitle>{{ fitment.year }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-car-estate" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Make</v-list-item-title>
                        <v-list-item-subtitle>{{ fitment.make }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-car-side" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Model</v-list-item-title>
                        <v-list-item-subtitle>{{ fitment.model }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>

                  <!-- Additional Info -->
                  <v-col cols="12" md="6">
                    <v-list>
                      <v-list-item v-if="fitment.engine">
                        <template v-slot:prepend>
                          <v-icon icon="mdi-engine" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Engine</v-list-item-title>
                        <v-list-item-subtitle>{{ fitment.engine }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item v-if="fitment.transmission">
                        <template v-slot:prepend>
                          <v-icon icon="mdi-car-clutch" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Transmission</v-list-item-title>
                        <v-list-item-subtitle>{{ fitment.transmission }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-calendar-plus" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Created</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(fitment.created_at) }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-calendar-edit" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Last Updated</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(fitment.updated_at) }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>
                </v-row>

                <!-- Attributes -->
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-2">Additional Attributes</h3>
                <v-row v-if="Object.keys(fitment.attributes || {}).length > 0">
                  <v-col
                    v-for="(value, key) in fitment.attributes"
                    :key="key"
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-card variant="outlined" class="mb-2">
                      <v-card-item>
                        <v-card-title class="text-caption text-uppercase">{{ key }}</v-card-title>
                        <v-card-text class="pt-2">{{ value }}</v-card-text>
                      </v-card-item>
                    </v-card>
                  </v-col>
                </v-row>
                <p v-else class="text-medium-emphasis">No additional attributes available</p>
              </v-card-text>
            </v-card>

            <!-- Compatible Products -->
            <v-card>
              <v-card-title class="d-flex align-center">
                Compatible Products
                <v-spacer></v-spacer>
                <v-btn
                  v-if="isAdmin"
                  color="primary"
                  size="small"
                  variant="tonal"
                  prepend-icon="mdi-link"
                >
                  Manage Associations
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>

              <!-- Products Table -->
              <v-table v-if="products.length > 0">
                <thead>
                <tr>
                  <th>SKU</th>
                  <th>Name</th>
                  <th>Part Number</th>
                  <th>Actions</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="product in products" :key="product.id">
                  <td>{{ product.sku }}</td>
                  <td>
                    <router-link
                      :to="{ name: 'ProductDetail', params: { id: product.id }}"
                      class="text-decoration-none text-primary"
                    >
                      {{ product.name }}
                    </router-link>
                  </td>
                  <td>{{ product.part_number || 'N/A' }}</td>
                  <td>
                    <div class="d-flex">
                      <v-tooltip text="View Product">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            icon
                            size="small"
                            v-bind="props"
                            :to="{ name: 'ProductDetail', params: { id: product.id }}"
                          >
                            <v-icon>mdi-eye</v-icon>
                          </v-btn>
                        </template>
                      </v-tooltip>

                      <v-tooltip v-if="isAdmin" text="Remove Association">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            icon
                            size="small"
                            color="error"
                            v-bind="props"
                            @click="confirmRemoveProduct(product)"
                            class="ml-2"
                          >
                            <v-icon>mdi-link-off</v-icon>
                          </v-btn>
                        </template>
                      </v-tooltip>
                    </div>
                  </td>
                </tr>
                </tbody>
              </v-table>

              <!-- No Products Message -->
              <v-card-text v-else class="text-center pa-6">
                <v-icon icon="mdi-package-variant-closed-remove" size="large" class="mb-2"></v-icon>
                <p>No compatible products are associated with this fitment</p>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" md="4">
            <!-- Actions Card -->
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
                      prepend-icon="mdi-magnify"
                      :to="{ name: 'FitmentCatalog', query: { year: fitment.year, make: fitment.make } }"
                    >
                      Find Similar Fitments
                    </v-btn>
                  </v-col>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="secondary"
                      variant="outlined"
                      prepend-icon="mdi-link-plus"
                      :disabled="!isAdmin"
                      @click="showAddProductDialog = true"
                    >
                      Add Compatible Product
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Similar Fitments Card -->
            <v-card>
              <v-card-title>Related Fitments</v-card-title>
              <v-divider></v-divider>
              <v-list v-if="similarFitments.length > 0" lines="two">
                <v-list-item
                  v-for="item in similarFitments"
                  :key="item.id"
                  :to="{ name: 'FitmentDetail', params: { id: item.id } }"
                >
                  <v-list-item-title>
                    {{ item.year }} {{ item.make }} {{ item.model }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ item.engine || '' }} {{ item.transmission || '' }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <v-card-text v-else class="text-center pa-6">
                <v-icon icon="mdi-car-off" size="large" class="mb-2"></v-icon>
                <p>No related fitments found</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Add Product Dialog -->
        <v-dialog v-model="showAddProductDialog" max-width="600">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Add Compatible Product
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <v-autocomplete
                v-model="selectedProduct"
                label="Select Product"
                :items="availableProducts"
                item-title="name"
                item-value="id"
                return-object
                variant="outlined"
                :disabled="addProductLoading"
                :loading="productsLoading"
                no-data-text="No products available"
                :rules="[v => !!v || 'Please select a product']"
              >
                <template v-slot:item="{ item, props }">
                  <v-list-item v-bind="props">
                    <template v-slot:prepend>
                      <v-avatar color="primary" variant="tonal">
                        <v-icon>mdi-package-variant-closed</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>{{ item.raw.name }}</v-list-item-title>
                    <v-list-item-subtitle>SKU: {{ item.raw.sku }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-autocomplete>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                color="secondary"
                @click="showAddProductDialog = false"
                :disabled="addProductLoading"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="addProduct"
                :loading="addProductLoading"
                :disabled="!selectedProduct"
              >
                Add Product
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Delete Confirmation Dialog -->
        <v-dialog v-model="deleteDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-error text-white pa-4">
              Confirm Delete
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>Are you sure you want to delete the fitment <strong>{{ fitment.year }} {{ fitment.make }} {{ fitment.model }}</strong>?</p>
              <p class="text-medium-emphasis mt-2">This action cannot be undone.</p>
              <v-alert
                v-if="products.length > 0"
                type="warning"
                variant="tonal"
                class="mt-4"
              >
                This fitment is associated with {{ products.length }} products. Deleting it will remove these associations.
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

        <!-- Remove Product Association Dialog -->
        <v-dialog v-model="removeProductDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-warning pa-4">
              Remove Product Association
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>Are you sure you want to remove the association between this fitment and the product <strong>{{ productToRemove?.name }}</strong>?</p>
              <p class="text-medium-emphasis mt-2">This will not delete the product, only remove the compatibility link.</p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="tonal"
                @click="removeProductDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="warning"
                @click="removeProductAssociation"
                :loading="removeProductLoading"
              >
                Remove Association
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <!-- Not Found State -->
      <div v-else class="text-center my-12">
        <v-icon icon="mdi-alert-circle" color="warning" size="64"></v-icon>
        <h2 class="text-h4 mt-4">Fitment Not Found</h2>
        <p class="text-body-1 mt-2">The fitment you're looking for doesn't exist or has been removed.</p>
        <v-btn
          color="primary"
          class="mt-4"
          @click="router.push({ name: 'FitmentCatalog' })"
        >
          Back to Fitments
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import fitmentService from '@/services/fitment';
import productService from '@/services/product';
import { Fitment } from '@/types/fitment';
import { Product } from '@/types/product';
import { formatDateTime } from '@/utils/formatters';
import { notificationService } from '@/utils/notification';

export default defineComponent({
  name: 'FitmentDetail',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    // User permissions
    const isAdmin = computed(() => authStore.isAdmin);

    // Data loading state
    const loading = ref(true);
    const fitment = ref<Fitment | null>(null);
    const products = ref<Product[]>([]);
    const similarFitments = ref<Fitment[]>([]);

    // Delete functionality
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);

    // Remove product functionality
    const removeProductDialog = ref(false);
    const removeProductLoading = ref(false);
    const productToRemove = ref<Product | null>(null);

    // Add product functionality
    const showAddProductDialog = ref(false);
    const productsLoading = ref(false);
    const addProductLoading = ref(false);
    const availableProducts = ref<Product[]>([]);
    const selectedProduct = ref<Product | null>(null);

    // Get fitment ID from route
    const fitmentId = computed(() => route.params.id as string);

    // Fetch fitment data
    const fetchFitment = async () => {
      loading.value = true;

      try {
        fitment.value = await fitmentService.getFitment(fitmentId.value);

        // Fetch related data
        await Promise.all([
          fetchProducts(),
          fetchSimilarFitments(),
        ]);
      } catch (error) {
        console.error('Error fetching fitment:', error);
        fitment.value = null;
        notificationService.error('Failed to load fitment details');
      } finally {
        loading.value = false;
      }
    };

    // Fetch products associated with this fitment
    const fetchProducts = async () => {
      try {
        products.value = await fitmentService.getFitmentProducts(fitmentId.value);
      } catch (error) {
        console.error('Error fetching products:', error);
        products.value = [];
      }
    };

    // Fetch similar fitments
    const fetchSimilarFitments = async () => {
      if (!fitment.value) return;

      try {
        // Find fitments with same make and model but different year
        const response = await fitmentService.getFitments({
          make: fitment.value.make,
          model: fitment.value.model
        });

        // Filter out the current fitment
        similarFitments.value = response.items.filter(f => f.id !== fitment.value?.id);
      } catch (error) {
        console.error('Error fetching similar fitments:', error);
        similarFitments.value = [];
      }
    };

    // Fetch available products for association
    const fetchAvailableProducts = async () => {
      productsLoading.value = true;

      try {
        // In a real implementation, you might want to fetch only products not already associated
        const response = await productService.getProducts({
          page_size: 50 // Limit to 50 products
        });

        // Filter out already associated products
        const associatedProductIds = products.value.map(p => p.id);
        availableProducts.value = response.items.filter(p => !associatedProductIds.includes(p.id));
      } catch (error) {
        console.error('Error fetching available products:', error);
        notificationService.error('Failed to load available products');
      } finally {
        productsLoading.value = false;
      }
    };

    // Show delete confirmation dialog
    const confirmDelete = () => {
      deleteDialog.value = true;
    };

    // Delete fitment
    const deleteFitment = async () => {
      deleteLoading.value = true;

      try {
        await fitmentService.deleteFitment(fitmentId.value);
        deleteDialog.value = false;

        notificationService.success('Fitment deleted successfully');

        // Redirect to fitment catalog
        router.push({ name: 'FitmentCatalog' });
      } catch (error) {
        console.error('Error deleting fitment:', error);
        notificationService.error('Failed to delete fitment');
      } finally {
        deleteLoading.value = false;
      }
    };

    // Show remove product confirmation dialog
    const confirmRemoveProduct = (product: Product) => {
      productToRemove.value = product;
      removeProductDialog.value = true;
    };

    // Remove product association
    const removeProductAssociation = async () => {
      if (!productToRemove.value) return;

      removeProductLoading.value = true;

      try {
        await fitmentService.removeProductAssociation(fitmentId.value, productToRemove.value.id);
        removeProductDialog.value = false;

        // Refresh product list
        await fetchProducts();

        notificationService.success('Product association removed successfully');
      } catch (error) {
        console.error('Error removing product association:', error);
        notificationService.error('Failed to remove product association');
      } finally {
        removeProductLoading.value = false;
        productToRemove.value = null;
      }
    };

    // Add product association
    const addProduct = async () => {
      if (!selectedProduct.value) return;

      addProductLoading.value = true;

      try {
        await fitmentService.associateProduct(fitmentId.value, selectedProduct.value.id);
        showAddProductDialog.value = false;

        // Refresh product list
        await fetchProducts();

        notificationService.success('Product association added successfully');
      } catch (error) {
        console.error('Error adding product association:', error);
        notificationService.error('Failed to add product association');
      } finally {
        addProductLoading.value = false;
        selectedProduct.value = null;
      }
    };

    // Initialize component
    onMounted(() => {
      fetchFitment();
    });

    // When add product dialog is shown, fetch available products
    watch(showAddProductDialog, (isOpen) => {
      if (isOpen) {
        fetchAvailableProducts();
      }
    });

    return {
      router,
      isAdmin,
      loading,
      fitment,
      products,
      similarFitments,
      deleteDialog,
      deleteLoading,
      removeProductDialog,
      removeProductLoading,
      productToRemove,
      showAddProductDialog,
      productsLoading,
      addProductLoading,
      availableProducts,
      selectedProduct,
      formatDateTime,
      confirmDelete,
      deleteFitment,
      confirmRemoveProduct,
      removeProductAssociation,
      addProduct
    };
  }
});
</script>
