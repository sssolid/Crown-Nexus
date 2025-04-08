<!-- frontend/src/views/ProductDetail.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
      </div>

      <template v-else-if="product">
        <!-- Page Header with Actions -->
        <v-row class="mb-6">
          <v-col cols="12" md="8">
            <div class="d-flex align-center">
              <v-btn icon variant="text" @click="router.back()" class="mr-4">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <div>
                <h1 class="text-h3 font-weight-bold">{{ product.part_number }}</h1>
                <p class="text-subtitle-1">Product Details</p>
              </div>
            </div>
          </v-col>

          <v-col cols="12" md="4" class="d-flex justify-end align-center">
            <v-btn
              v-if="isAdmin"
              color="primary"
              prepend-icon="mdi-pencil"
              :to="{ name: 'ProductEdit', params: { id: product.id }}"
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

        <!-- Product Details -->
        <v-row>
          <!-- Main Product Info -->
          <v-col cols="12" md="8">
            <v-card class="mb-6">
              <v-card-title>Product Details</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <!-- Basic Info -->
                  <v-col cols="12" md="6">
                    <v-list>
                      <v-list-item>
                        <template #prepend>
                          <v-icon icon="mdi-pound" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Part Number</v-list-item-title>
                        <v-list-item-subtitle>{{ product.part_number }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template #prepend>
                          <v-icon icon="mdi-circle" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Status</v-list-item-title>
                        <v-list-item-subtitle>
                          <v-chip
                            :color="product.is_active ? 'success' : 'error'"
                            size="small"
                            variant="tonal"
                          >
                            {{ product.is_active ? 'Active' : 'Inactive' }}
                          </v-chip>
                        </v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template #prepend>
                          <v-icon icon="mdi-tag" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Category</v-list-item-title>
                        <v-list-item-subtitle>{{ category }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>

                  <!-- Dates and System Info -->
                  <v-col cols="12" md="6">
                    <v-list>
                      <v-list-item>
                        <template #prepend>
                          <v-icon icon="mdi-calendar-plus" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Created</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(product.created_at) }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template #prepend>
                          <v-icon icon="mdi-calendar-edit" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Last Updated</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(product.updated_at) }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>
                </v-row>

                <!-- Description -->
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-2">Description</h3>
                <p v-if="getDescription(product.descriptions, 'Standard')" class="text-body-1">
                  {{ getDescription(product.descriptions, 'Standard') }}
                </p>
                <p v-else class="text-medium-emphasis">No description available</p>

                <!-- Attributes -->
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-2">Attributes</h3>
                <v-row v-if="Object.keys(attributes).length > 0">
                  <v-col
                    v-for="(value, key) in attributes"
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
                <p v-else class="text-medium-emphasis">No attributes available</p>
              </v-card-text>
            </v-card>

            <!-- Fitments -->
            <v-card class="mb-6">
              <v-card-title class="d-flex align-center">
                Fitments
                <v-spacer></v-spacer>
                <v-btn
                  v-if="isAdmin"
                  color="primary"
                  size="small"
                  variant="tonal"
                  prepend-icon="mdi-plus"
                  :to="{ name: 'ProductFitments', params: { id: product.id }}"
                >
                  Manage Fitments
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>

              <!-- Fitments Table -->
              <v-table v-if="fitments.length > 0">
                <thead>
                <tr>
                  <th>Year</th>
                  <th>Make</th>
                  <th>Model</th>
                  <th>Engine</th>
                  <th>Transmission</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="fitment in fitments" :key="fitment.id">
                  <td>{{ fitment.year }}</td>
                  <td>{{ fitment.make }}</td>
                  <td>{{ fitment.model }}</td>
                  <td>{{ fitment.engine || 'N/A' }}</td>
                  <td>{{ fitment.transmission || 'N/A' }}</td>
                </tr>
                </tbody>
              </v-table>

              <!-- No Fitments Message -->
              <v-card-text v-else class="text-center pa-6">
                <v-icon icon="mdi-car-off" size="large" class="mb-2"></v-icon>
                <p>No fitments available for this product</p>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" md="4">
            <!-- Media Gallery -->
            <v-card class="mb-6">
              <v-card-title class="d-flex align-center">
                Media
                <v-spacer></v-spacer>
                <v-btn
                  v-if="isAdmin"
                  color="primary"
                  size="small"
                  variant="tonal"
                  prepend-icon="mdi-upload"
                  :to="{ name: 'ProductMedia', params: { id: product.id }}"
                >
                  Manage Media
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>

              <!-- Media Content -->
              <v-card-text v-if="media.length > 0" class="pa-2">
                <v-row>
                  <v-col
                    v-for="(item, index) in media"
                    :key="item.id"
                    cols="12"
                    sm="6"
                  >
                    <v-img
                      :src="item.url"
                      height="150"
                      contain
                      class="rounded"
                      @click="openMediaDialog(index)"
                    >
                      <template #placeholder>
                        <v-row class="fill-height ma-0" align="center" justify="center">
                          <v-progress-circular indeterminate color="primary"></v-progress-circular>
                        </v-row>
                      </template>
                    </v-img>
                  </v-col>
                </v-row>
              </v-card-text>

              <!-- No Media Message -->
              <v-card-text v-else class="text-center pa-6">
                <v-icon icon="mdi-image-off" size="large" class="mb-2"></v-icon>
                <p>No media available for this product</p>
              </v-card-text>
            </v-card>

            <!-- Related Products (Placeholder) -->
            <v-card>
              <v-card-title>Related Products</v-card-title>
              <v-divider></v-divider>
              <v-card-text class="text-center pa-6">
                <v-icon icon="mdi-package-variant-closed" size="large" class="mb-2"></v-icon>
                <p>Feature coming soon</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Media Viewer Dialog -->
        <v-dialog v-model="mediaDialog" max-width="800">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>{{ currentMedia?.filename || 'Media Viewer' }}</span>
              <v-btn icon @click="mediaDialog = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
              <v-img
                v-if="currentMedia"
                :src="currentMedia.url"
                height="500"
                class="mx-auto"
                contain
              ></v-img>
            </v-card-text>
            <v-card-actions>
              <v-btn
                variant="text"
                prepend-icon="mdi-arrow-left"
                :disabled="currentMediaIndex <= 0"
                @click="currentMediaIndex--"
              >
                Previous
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                append-icon="mdi-arrow-right"
                :disabled="currentMediaIndex >= media.length - 1"
                @click="currentMediaIndex++"
              >
                Next
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
              <p>Are you sure you want to delete the product <strong>{{ product.part_number }}</strong>?</p>
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

<script setup lang="ts">
import {ref, computed, onMounted} from 'vue';
import {useRouter, useRoute} from 'vue-router';
import {useAuthStore} from '@/stores/auth';
import productService from '@/services/product';
import {Product, ProductDescription} from '@/types/product';
import {Fitment} from '@/types/fitment';
import {formatDateTime} from '@/utils/formatters';
import image1 from '@/assets/mock_product_images/image-1.jpg';
import image2 from '@/assets/mock_product_images/image-2.jpg';
import mediaService from "@/services/media.ts";

// Router and route
const router = useRouter();
const route = useRoute();

// Auth store
const authStore = useAuthStore();
const isAdmin = computed(() => authStore.isAdmin);

// Data loading state
const loading = ref(true);
const product = ref<Product | null>(null);
const fitments = ref<Fitment[]>([]);
const media = ref<Media[]>([]);

// Placeholder data
const category = ref('Uncategorized'); // Placeholder for category
const attributes = ref<Record<string, string>>({
  Material: 'Steel',
  Color: 'Silver',
  Weight: '2.5 lbs',
}); // Placeholder for attributes

// Delete functionality
const deleteDialog = ref(false);
const deleteLoading = ref(false);

// Media viewer
const mediaDialog = ref(false);
const currentMediaIndex = ref(0);
const currentMedia = computed(() =>
  media.value.length > 0 && currentMediaIndex.value >= 0 ? media.value[currentMediaIndex.value] : null
);

// Get product ID from route
const productId = computed(() => route.params.id as string);

// Placeholder type for media
interface Media {
  id: string;
  filename: string;
  url: string;
  thumbnail_url?: string;
}

// Fetch product data
const fetchProduct = async () => {
  loading.value = true;
  try {
    product.value = await productService.getProduct(productId.value);
    await Promise.all([fetchFitments(), fetchMedia()]);
  } catch (error) {
    console.error('Error fetching product:', error);
    product.value = null;
  } finally {
    loading.value = false;
  }
};

// Fetch product fitments (placeholder)
const fetchFitments = async () => {
  try {
    // Placeholder data until fitments are implemented in the database
    fitments.value = [
      {id: '1', year: '2020', make: 'Toyota', model: 'Camry', engine: '2.5L', transmission: 'Auto'},
      {id: '2', year: '2021', make: 'Honda', model: 'Civic', engine: '1.5L', transmission: 'Manual'},
    ];
  } catch (error) {
    console.error('Error fetching fitments:', error);
    fitments.value = [];
  }
};

// Fetch product media (placeholder)
const fetchMedia = async () => {
  try {
    media.value = await mediaService.getProductMedia(productId.value);
  } catch (error) {
    console.error('Error fetching media:', error);
    media.value = [];
  }
};

// Open media viewer dialog
const openMediaDialog = (index: number) => {
  currentMediaIndex.value = index;
  mediaDialog.value = true;
};

// Show delete confirmation dialog
const confirmDelete = () => {
  deleteDialog.value = true;
};

// Delete product
const deleteProduct = async () => {
  deleteLoading.value = true;
  try {
    await productService.deleteProduct(productId.value);
    deleteDialog.value = false;
    router.push({name: 'ProductCatalog'});
  } catch (error) {
    console.error('Error deleting product:', error);
  } finally {
    deleteLoading.value = false;
  }
};

// Extract description by type from product descriptions
const getDescription = (descriptions: ProductDescription[] | undefined, type: string): string => {
  if (!descriptions || !Array.isArray(descriptions)) return 'N/A';
  const description = descriptions.find(d => d.description_type === type);
  return description?.description || 'N/A';
};

// Initialize component
onMounted(() => {
  fetchProduct();
});
</script>
