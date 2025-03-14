<!-- frontend/src/views/ProductForm.vue -->
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

      <template v-else>
        <!-- Page Header with Back Button -->
        <v-row class="mb-6">
          <v-col cols="12">
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
                  {{ isEditMode ? 'Edit Product' : 'Create Product' }}
                </h1>
                <p class="text-subtitle-1">
                  {{ isEditMode ? `Editing ${form.name || 'product'}` : 'Add a new product to the catalog' }}
                </p>
              </div>
            </div>
          </v-col>
        </v-row>

        <!-- Form -->
        <v-form ref="formRef" @submit.prevent="submitForm" v-model="isFormValid">
          <v-row>
            <!-- Main Form Column -->
            <v-col cols="12" md="8">
              <v-card class="mb-6">
                <v-card-title>Product Information</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row>
                    <!-- SKU -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="form.sku"
                        label="SKU"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="errors.sku"
                        :disabled="loading"
                        @input="clearError('sku')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Part Number -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="form.part_number"
                        label="Part Number"
                        variant="outlined"
                        :error-messages="errors.part_number"
                        :disabled="loading"
                        @input="clearError('part_number')"
                        hint="Optional manufacturer part number"
                        persistent-hint
                      ></v-text-field>
                    </v-col>

                    <!-- Name -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="form.name"
                        label="Product Name"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="errors.name"
                        :disabled="loading"
                        @input="clearError('name')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Description -->
                    <v-col cols="12">
                      <v-textarea
                        v-model="form.description"
                        label="Description"
                        variant="outlined"
                        :error-messages="errors.description"
                        :disabled="loading"
                        @input="clearError('description')"
                        rows="4"
                        auto-grow
                      ></v-textarea>
                    </v-col>

                    <!-- Status -->
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="form.is_active"
                        label="Product is active"
                        color="success"
                        :disabled="loading"
                        inset
                      ></v-switch>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>

              <!-- Product Attributes Card -->
              <v-card class="mb-6">
                <v-card-title class="d-flex align-center">
                  Product Attributes
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    size="small"
                    variant="text"
                    prepend-icon="mdi-plus"
                    @click="addAttribute"
                    :disabled="loading"
                  >
                    Add Attribute
                  </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <div v-if="attributes.length === 0" class="text-center py-4">
                    <v-icon icon="mdi-tag-off" size="large" class="mb-2"></v-icon>
                    <p>No attributes added yet. Click "Add Attribute" to add product specifications.</p>
                  </div>

                  <v-row v-for="(attr, index) in attributes" :key="index" class="align-center">
                    <v-col cols="5">
                      <v-text-field
                        v-model="attr.key"
                        label="Attribute Name"
                        variant="outlined"
                        density="comfortable"
                        :disabled="loading"
                        placeholder="e.g. Color, Weight, Material"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="5">
                      <v-text-field
                        v-model="attr.value"
                        label="Value"
                        variant="outlined"
                        density="comfortable"
                        :disabled="loading"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2" class="d-flex justify-end">
                      <v-btn
                        icon
                        color="error"
                        variant="text"
                        @click="removeAttribute(index)"
                        :disabled="loading"
                      >
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Sidebar Column -->
            <v-col cols="12" md="4">
              <!-- Save Card -->
              <v-card class="mb-6">
                <v-card-title>Save Changes</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="mb-4">
                    {{ isEditMode
                    ? 'Update this product with your changes.'
                    : 'Create a new product in the catalog.'
                    }}
                  </p>

                  <!-- Form-level error message -->
                  <v-alert
                    v-if="formError"
                    type="error"
                    variant="tonal"
                    class="mb-4"
                    closable
                    @click:close="formError = ''"
                  >
                    {{ formError }}
                  </v-alert>
                </v-card-text>
                <v-card-actions class="pa-4">
                  <v-spacer></v-spacer>
                  <v-btn
                    variant="text"
                    color="secondary"
                    @click="router.back()"
                    :disabled="loading"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    color="primary"
                    type="submit"
                    :loading="loading"
                    :disabled="!isFormValid"
                    @click="submitForm"
                  >
                    {{ isEditMode ? 'Update Product' : 'Create Product' }}
                  </v-btn>
                </v-card-actions>
              </v-card>

              <!-- Additional Resources Card (Placeholder) -->
              <v-card>
                <v-card-title>After Saving</v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pb-0">
                  <p class="mb-4">
                    {{ isEditMode
                    ? 'What would you like to do after updating this product?'
                    : 'What would you like to do after creating this product?'
                    }}
                  </p>
                </v-card-text>
                <v-card-actions class="px-4 pb-4 pt-0">
                  <v-row>
                    <v-col cols="12">
                      <v-btn
                        block
                        color="secondary"
                        variant="outlined"
                        prepend-icon="mdi-image-plus"
                        :disabled="!isEditMode || loading"
                      >
                        Add Media
                      </v-btn>
                    </v-col>
                    <v-col cols="12">
                      <v-btn
                        block
                        color="secondary"
                        variant="outlined"
                        prepend-icon="mdi-car-connected"
                        :disabled="!isEditMode || loading"
                      >
                        Manage Fitments
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </v-form>

        <!-- Unsaved Changes Dialog -->
        <v-dialog v-model="showUnsavedDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-warning pa-4">
              Unsaved Changes
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>You have unsaved changes. Are you sure you want to leave this page?</p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="tonal"
                @click="showUnsavedDialog = false"
              >
                Stay on Page
              </v-btn>
              <v-btn
                color="error"
                @click="discardChanges"
              >
                Discard Changes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import productService from '@/services/product';
import { Product } from '@/types/product';
import { notificationService } from '@/utils/notification';
import { parseValidationErrors } from '@/utils/error-handler';

interface ProductForm {
  sku: string;
  name: string;
  description: string;
  part_number: string;
  is_active: boolean;
  attributes: Record<string, any>;
}

interface AttributeItem {
  key: string;
  value: string;
}

export default defineComponent({
  name: 'ProductForm',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    // Form references
    const formRef = ref<any>(null);
    const isFormValid = ref(false);

    // Loading states
    const initialLoading = ref(false);
    const loading = ref(false);

    // Form errors
    const formError = ref('');
    const errors = ref<Record<string, string>>({});

    // Form data
    const form = ref<ProductForm>({
      sku: '',
      name: '',
      description: '',
      part_number: '',
      is_active: true,
      attributes: {}
    });

    // Form state tracking
    const formDirty = ref(false);
    const showUnsavedDialog = ref(false);
    const pendingNavigation = ref<any>(null);

    // Product attributes
    const attributes = ref<AttributeItem[]>([]);

    // Navigation guard - check for unsaved changes
    const navigationGuard = (event: BeforeUnloadEvent) => {
      if (formDirty.value) {
        event.preventDefault();
        event.returnValue = '';
      }
    };

    // Add window event listener
    onMounted(() => {
      window.addEventListener('beforeunload', navigationGuard);
    });

    // Remove window event listener
    onBeforeUnmount(() => {
      window.removeEventListener('beforeunload', navigationGuard);
    });

    // Edit mode detection
    const isEditMode = computed(() => {
      return route.name === 'ProductEdit';
    });

    // Product ID from route
    const productId = computed(() => {
      return route.params.id as string;
    });

    // Form validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required',
    };

    // Clear a specific field error
    const clearError = (field: string) => {
      if (errors.value[field]) {
        delete errors.value[field];
      }
      formDirty.value = true;
    };

    // Add a new attribute
    const addAttribute = () => {
      attributes.value.push({ key: '', value: '' });
      formDirty.value = true;
    };

    // Remove an attribute
    const removeAttribute = (index: number) => {
      attributes.value.splice(index, 1);
      formDirty.value = true;
    };

    // Convert attributes array to object format
    const attributesToObject = (): Record<string, any> => {
      const result: Record<string, any> = {};
      attributes.value.forEach(attr => {
        if (attr.key && attr.value) {
          result[attr.key] = attr.value;
        }
      });
      return result;
    };

    // Convert attributes object to array format
    const objectToAttributes = (obj: Record<string, any>) => {
      const result: AttributeItem[] = [];
      Object.entries(obj).forEach(([key, value]) => {
        result.push({ key, value: String(value) });
      });
      return result;
    };

    // Fetch product data for edit mode
    const fetchProduct = async () => {
      if (!isEditMode.value) return;

      initialLoading.value = true;

      try {
        const product = await productService.getProduct(productId.value);

        // Populate form with product data
        form.value.sku = product.sku;
        form.value.name = product.name;
        form.value.description = product.description || '';
        form.value.part_number = product.part_number || '';
        form.value.is_active = product.is_active;

        // Convert product attributes to form format
        if (product.attributes && Object.keys(product.attributes).length > 0) {
          attributes.value = objectToAttributes(product.attributes);
        }

        // Reset form dirty state after loading data
        formDirty.value = false;
      } catch (error) {
        console.error('Error fetching product:', error);
        notificationService.error('Failed to load product data');
        router.push({ name: 'ProductCatalog' });
      } finally {
        initialLoading.value = false;
      }
    };

    // Fetch categories for dropdown
    const fetchCategories = async () => {
      try {
        categories.value = await productService.getCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
        notificationService.error('Failed to load categories');
      }
    };

    // Submit the form
    const submitForm = async () => {
      // Validate form
      const validation = await formRef.value?.validate();

      if (!validation.valid) {
        formError.value = 'Please correct the errors in the form';
        return;
      }

      loading.value = true;
      formError.value = '';
      errors.value = {};

      try {
        // Convert attributes array to object
        form.value.attributes = attributesToObject();

        let result: Product;
        if (isEditMode.value) {
          // Update existing product
          result = await productService.updateProduct(productId.value, form.value);
          notificationService.success('Product updated successfully');
        } else {
          // Create new product
          result = await productService.createProduct(form.value);
          notificationService.success('Product created successfully');
        }

        // Reset form dirty state
        formDirty.value = false;

        // Redirect to product detail
        router.push({ name: 'ProductDetail', params: { id: result.id } });
      } catch (error: any) {
        console.error('Error submitting product:', error);

        // Handle validation errors
        if (error.response?.status === 422) {
          errors.value = parseValidationErrors(error);
          formError.value = 'Please correct the validation errors';
        } else {
          formError.value = error.response?.data?.detail || 'Failed to save product';
        }
      } finally {
        loading.value = false;
      }
    };

    // Discard changes and navigate away
    const discardChanges = () => {
      formDirty.value = false;
      showUnsavedDialog.value = false;

      if (pendingNavigation.value) {
        router.push(pendingNavigation.value);
      } else {
        router.back();
      }
    };

    // Watch for navigation and check for unsaved changes
    router.beforeEach((to, from, next) => {
      if (formDirty.value && from.name === route.name) {
        showUnsavedDialog.value = true;
        pendingNavigation.value = to.fullPath;
        next(false);
      } else {
        next();
      }
    });

    // Initialize component
    onMounted(() => {
      Promise.all([
        fetchProduct(),
        fetchCategories()
      ]);
    });

    return {
      router,
      formRef,
      isFormValid,
      initialLoading,
      loading,
      formError,
      errors,
      form,
      attributes,
      categories,
      showUnsavedDialog,
      pendingNavigation,
      isEditMode,
      rules,
      clearError,
      addAttribute,
      removeAttribute,
      submitForm,
      discardChanges
    };
  }
});
</script>
