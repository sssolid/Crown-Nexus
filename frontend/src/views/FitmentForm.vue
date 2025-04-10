<!-- frontend/src/views/FitmentForm.vue -->
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
                  {{ isEditMode ? 'Edit Fitment' : 'Create Fitment' }}
                </h1>
                <p class="text-subtitle-1">
                  {{ isEditMode
                  ? `Editing ${form.year} ${form.make} ${form.model}`
                  : 'Add a new vehicle fitment'
                  }}
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
                <v-card-title>Vehicle Information</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row>
                    <!-- Year -->
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model.number="form.year"
                        label="Year"
                        type="number"
                        variant="outlined"
                        :rules="[rules.required, rules.yearValid]"
                        :error-messages="errors.year"
                        :disabled="loading"
                        @input="clearError('year')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Make -->
                    <v-col cols="12" md="4">
                      <v-autocomplete
                        v-model="form.make"
                        label="Make"
                        :items="makeOptions"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="errors.make"
                        :disabled="loading"
                        @input="clearError('make')"
                        required
                        clearable
                      ></v-autocomplete>
                    </v-col>

                    <!-- Model -->
                    <v-col cols="12" md="4">
                      <v-autocomplete
                        v-model="form.model"
                        label="Model"
                        :items="modelOptions"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="errors.model"
                        :disabled="loading"
                        @input="clearError('model')"
                        required
                        clearable
                      ></v-autocomplete>
                    </v-col>

                    <!-- Engine -->
                    <v-col cols="12" md="6">
                      <v-autocomplete
                        v-model="form.engine"
                        label="Engine"
                        :items="engineOptions"
                        variant="outlined"
                        :error-messages="errors.engine"
                        :disabled="loading"
                        @input="clearError('engine')"
                        clearable
                        hint="Optional engine specification"
                        persistent-hint
                      ></v-autocomplete>
                    </v-col>

                    <!-- Transmission -->
                    <v-col cols="12" md="6">
                      <v-autocomplete
                        v-model="form.transmission"
                        label="Transmission"
                        :items="transmissionOptions"
                        variant="outlined"
                        :error-messages="errors.transmission"
                        :disabled="loading"
                        @input="clearError('transmission')"
                        clearable
                        hint="Optional transmission specification"
                        persistent-hint
                      ></v-autocomplete>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>

              <!-- Additional Attributes Card -->
              <v-card class="mb-6">
                <v-card-title class="d-flex align-center">
                  Additional Attributes
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
                    <v-icon icon="mdi-car-off" size="large" class="mb-2"></v-icon>
                    <p>No additional attributes added yet. Click "Add Attribute" to add vehicle specifications.</p>
                  </div>

                  <v-row v-for="(attr, index) in attributes" :key="index" class="align-center">
                    <v-col cols="5">
                      <v-text-field
                        v-model="attr.key"
                        label="Attribute Name"
                        variant="outlined"
                        density="comfortable"
                        :disabled="loading"
                        placeholder="e.g. Trim, Body Style, Drivetrain"
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

              !-- Part Application Processing -->
              <v-card class="mb-6">
                <v-card-title class="d-flex align-center">
                  Process Part Application
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    size="small"
                    variant="tonal"
                    @click="showProcessingInfo = !showProcessingInfo"
                  >
                    {{ showProcessingInfo ? 'Hide Info' : 'Show Info' }}
                  </v-btn>
                </v-card-title>
                <v-divider></v-divider>

                <v-expand-transition>
                  <div v-if="showProcessingInfo">
                    <v-card-text class="bg-grey-lighten-4">
                      <h3 class="text-subtitle-1 font-weight-bold mb-2">Part Application Format</h3>
                      <p class="mb-2">Enter part applications in the format: <code>YYYY-YYYY Vehicle Model (Position);</code></p>
                      <v-alert type="info" variant="tonal" density="compact">
                        Example: <code>2005-2010 WK Grand Cherokee (Left or Right Front Upper Ball Joint);</code>
                      </v-alert>
                      <p class="mt-4 mb-2">Each application should be on a new line. The system will process each line and create the appropriate fitments.</p>
                    </v-card-text>
                  </div>
                </v-expand-transition>

                <v-card-text>
                  <v-textarea
                    v-model="partApplications"
                    label="Part Applications"
                    placeholder="Enter part applications, one per line"
                    variant="outlined"
                    rows="5"
                    counter
                    :disabled="loading || processingApplications"
                  ></v-textarea>

                  <v-text-field
                    v-model.number="partTerminologyId"
                    label="Part Terminology ID"
                    type="number"
                    variant="outlined"
                    placeholder="Enter PCDB Part Terminology ID"
                    :disabled="loading || processingApplications"
                    class="mt-2"
                  ></v-text-field>

                  <v-text-field
                    v-model="productId"
                    label="Product ID (Optional)"
                    variant="outlined"
                    placeholder="Enter Product ID to associate with fitments"
                    :disabled="loading || processingApplications"
                    class="mt-2"
                    hint="If provided, successful fitments will be associated with this product"
                    persistent-hint
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    :loading="processingApplications"
                    :disabled="!partApplications || !partTerminologyId || loading"
                    @click="processPartApplications"
                  >
                    Process Applications
                  </v-btn>
                </v-card-actions>
              </v-card>

              <!-- Processing Results -->
              <v-card v-if="processingResults" class="mb-6">
                <v-card-title>Processing Results</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-alert type="success" variant="tonal" class="mb-4">
                    <div class="d-flex justify-space-between">
                      <span>Successfully processed {{ processingResults.valid_count + processingResults.warning_count }} out of {{ processingResults.valid_count + processingResults.warning_count + processingResults.error_count }} applications</span>
                      <div>
                        <v-chip color="success" size="small" class="ml-2">{{ processingResults.valid_count }} Valid</v-chip>
                        <v-chip color="warning" size="small" class="ml-2">{{ processingResults.warning_count }} Warnings</v-chip>
                        <v-chip color="error" size="small" class="ml-2">{{ processingResults.error_count }} Errors</v-chip>
                      </div>
                    </div>
                  </v-alert>

                  <v-expansion-panels variant="accordion">
                    <v-expansion-panel
                      v-for="(results, appText) in processingResults.results"
                      :key="appText"
                    >
                      <v-expansion-panel-title>
                        <div class="d-flex align-center">
                          <v-icon
                            :color="getApplicationResultColor(results)"
                            :icon="getApplicationResultIcon(results)"
                            class="mr-2"
                          ></v-icon>
                          <div>{{ appText }}</div>
                        </div>
                      </v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <v-list>
                          <v-list-item
                            v-for="(result, index) in results"
                            :key="index"
                            :title="result.message"
                            :subtitle="result.original_text"
                            :prepend-icon="getResultStatusIcon(result.status)"
                            :color="getResultStatusColor(result.status)"
                            class="mb-2"
                          >
                            <template v-if="result.fitment" v-slot:append>
                              <v-chip
                                v-if="result.fitment.vcdb_vehicle_id"
                                size="small"
                                color="info"
                                class="mr-1"
                              >
                                VCDB ID: {{ result.fitment.vcdb_vehicle_id }}
                              </v-chip>
                              <v-chip
                                v-if="result.fitment.pcdb_position_ids && result.fitment.pcdb_position_ids.length"
                                size="small"
                                color="success"
                              >
                                PCDB Positions: {{ result.fitment.pcdb_position_ids.length }}
                              </v-chip>
                            </template>
                          </v-list-item>
                        </v-list>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
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
                    ? 'Update this fitment with your changes.'
                    : 'Create a new vehicle fitment.'
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
                    {{ isEditMode ? 'Update Fitment' : 'Create Fitment' }}
                  </v-btn>
                </v-card-actions>
              </v-card>

              <!-- Additional Resources Card -->
              <v-card v-if="isEditMode">
                <v-card-title>Associated Products</v-card-title>
                <v-divider></v-divider>
                <v-card-text v-if="associatedProducts.length > 0">
                  <v-list lines="two">
                    <v-list-item
                      v-for="product in associatedProducts"
                      :key="product.id"
                      :to="{ name: 'ProductDetail', params: { id: product.id } }"
                    >
                      <template v-slot:prepend>
                        <v-avatar color="primary" variant="tonal">
                          <v-icon>mdi-package-variant-closed</v-icon>
                        </v-avatar>
                      </template>
                      <v-list-item-title>{{ product.name }}</v-list-item-title>
                      <v-list-item-subtitle>SKU: {{ product.sku }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card-text>
                <v-card-text v-else class="text-center py-4">
                  <v-icon icon="mdi-package-variant-closed-remove" size="large" class="mb-2"></v-icon>
                  <p>No products associated with this fitment yet.</p>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions class="pa-4">
                  <v-btn
                    block
                    color="primary"
                    variant="outlined"
                    prepend-icon="mdi-link"
                    :disabled="loading"
                  >
                    Manage Product Associations
                  </v-btn>
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
import fitmentService from '@/services/fitment';
import fitmentProcessingService, { ProcessFitmentResponse } from '@/services/fitmentProcessing';
import { Fitment } from '@/types/fitment';
import { notificationService } from '@/utils/notification';
import { parseValidationErrors } from '@/utils/error-handler';
import { Product } from '@/types/product';

interface FitmentForm {
  year: number;
  make: string;
  model: string;
  engine?: string;
  transmission?: string;
  attributes: Record<string, any>;
}

interface AttributeItem {
  key: string;
  value: string;
}

export default defineComponent({
  name: 'FitmentForm',

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
    const form = ref<FitmentForm>({
      year: new Date().getFullYear(),
      make: '',
      model: '',
      engine: undefined,
      transmission: undefined,
      attributes: {}
    });

    // Form state tracking
    const formDirty = ref(false);
    const showUnsavedDialog = ref(false);
    const pendingNavigation = ref<any>(null);

    // Part Application Processing
    const showProcessingInfo = ref(false);
    const partApplications = ref('');
    const partTerminologyId = ref<number | null>(null);
    const productId = ref('');
    const processingApplications = ref(false);
    const processingResults = ref<ProcessFitmentResponse | null>(null);

    // Fitment attributes
    const attributes = ref<AttributeItem[]>([]);

    // Associated products (for edit mode)
    const associatedProducts = ref<Product[]>([]);

    // Dropdown options
    const makeOptions = ref<string[]>([
      'Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan', 'BMW', 'Mercedes-Benz',
      'Audi', 'Subaru', 'Mazda', 'Lexus', 'Volkswagen', 'Jeep', 'Hyundai', 'Kia'
    ]);

    const modelOptions = ref<string[]>([
      'Camry', 'Accord', 'F-150', 'Silverado', 'Altima', '3 Series', 'C-Class',
      'A4', 'Outback', 'CX-5', 'RX', 'Golf', 'Wrangler', 'Elantra', 'Sportage'
    ]);

    const engineOptions = ref<string[]>([
      '2.0L I4', '2.5L I4', '3.0L V6', '3.5L V6', '4.0L V6', '5.0L V8', '5.7L V8',
      '2.0L Turbo', '3.0L Turbo', '1.5L I4', '1.8L I4', '2.4L I4', '6.2L V8'
    ]);

    const transmissionOptions = ref<string[]>([
      'Automatic', 'Manual', 'CVT', 'Dual-Clutch', '6-Speed Automatic',
      '8-Speed Automatic', '10-Speed Automatic', '9-Speed Automatic', '5-Speed Manual'
    ]);

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
      return route.name === 'FitmentEdit';
    });

    // Fitment ID from route
    const fitmentId = computed(() => {
      return route.params.id as string;
    });

    // Form validation rules
    const rules = {
      required: (v: any) => !!v || 'This field is required',
      yearValid: (v: number) => {
        const currentYear = new Date().getFullYear();
        return (v >= 1900 && v <= currentYear + 1) || 'Year must be between 1900 and ' + (currentYear + 1);
      }
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

    // Fetch fitment data for edit mode
    const fetchFitment = async () => {
      if (!isEditMode.value) return;

      initialLoading.value = true;

      try {
        const fitment = await fitmentService.getFitment(fitmentId.value);

        // Populate form with fitment data
        form.value.year = fitment.year;
        form.value.make = fitment.make;
        form.value.model = fitment.model;
        form.value.engine = fitment.engine;
        form.value.transmission = fitment.transmission;

        // Convert fitment attributes to form format
        if (fitment.attributes && Object.keys(fitment.attributes).length > 0) {
          attributes.value = objectToAttributes(fitment.attributes);
        }

        // Reset form dirty state after loading data
        formDirty.value = false;

        // Fetch associated products
        fetchAssociatedProducts();
      } catch (error) {
        console.error('Error fetching fitment:', error);
        notificationService.error('Failed to load fitment data');
        router.push({ name: 'FitmentCatalog' });
      } finally {
        initialLoading.value = false;
      }
    };

    // Fetch products associated with this fitment
    const fetchAssociatedProducts = async () => {
      if (!isEditMode.value) return;

      try {
        const products = await fitmentService.getFitmentProducts(fitmentId.value);
        associatedProducts.value = products;
      } catch (error) {
        console.error('Error fetching associated products:', error);
      }
    };

    // Process part applications
    const processPartApplications = async () => {
      if (!partApplications.value || !partTerminologyId.value) {
        notificationService.error('Please enter part applications and a part terminology ID');
        return;
      }

      processingApplications.value = true;

      try {
        // Split by lines and filter out empty lines
        const applicationTexts = partApplications.value
          .split('\n')
          .map(line => line.trim())
          .filter(line => line.length > 0);

        if (applicationTexts.length === 0) {
          notificationService.error('Please enter at least one part application');
          processingApplications.value = false;
          return;
        }

        // Process applications
        const results = await fitmentProcessingService.processApplications(
          applicationTexts,
          partTerminologyId.value,
          productId.value || undefined
        );

        // Store results
        processingResults.value = results;

        // Show notification
        const successCount = results.valid_count + results.warning_count;
        const totalCount = successCount + results.error_count;

        if (successCount === totalCount) {
          notificationService.success(`Successfully processed all ${totalCount} part applications`);
        } else if (successCount > 0) {
          notificationService.warning(`Processed ${successCount} out of ${totalCount} part applications with some issues`);
        } else {
          notificationService.error(`Failed to process ${totalCount} part applications`);
        }
      } catch (error) {
        console.error('Error processing part applications:', error);
        notificationService.error('Failed to process part applications');
      } finally {
        processingApplications.value = false;
      }
    };

    // Helper methods for displaying processing results
    const getApplicationResultColor = (results: any[]): string => {
      if (results.every(r => r.status === 'VALID')) {
        return 'success';
      } else if (results.some(r => r.status === 'ERROR')) {
        return 'error';
      } else {
        return 'warning';
      }
    };

    const getApplicationResultIcon = (results: any[]): string => {
      if (results.every(r => r.status === 'VALID')) {
        return 'mdi-check-circle';
      } else if (results.some(r => r.status === 'ERROR')) {
        return 'mdi-alert-circle';
      } else {
        return 'mdi-alert';
      }
    };

    const getResultStatusIcon = (status: string): string => {
      switch (status) {
        case 'VALID':
          return 'mdi-check-circle';
        case 'WARNING':
          return 'mdi-alert';
        case 'ERROR':
          return 'mdi-alert-circle';
        default:
          return 'mdi-help-circle';
      }
    };

    const getResultStatusColor = (status: string): string => {
      switch (status) {
        case 'VALID':
          return 'success';
        case 'WARNING':
          return 'warning';
        case 'ERROR':
          return 'error';
        default:
          return '';
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

        let result: Fitment;
        if (isEditMode.value) {
          // Update existing fitment
          result = await fitmentService.updateFitment(fitmentId.value, form.value);
          notificationService.success('Fitment updated successfully');
        } else {
          // Create new fitment
          result = await fitmentService.createFitment(form.value);
          notificationService.success('Fitment created successfully');
        }

        // Reset form dirty state
        formDirty.value = false;

        // Redirect to fitment detail
        router.push({ name: 'FitmentDetail', params: { id: result.id } });
      } catch (error: any) {
        console.error('Error submitting fitment:', error);

        // Handle validation errors
        if (error.response?.status === 422) {
          errors.value = parseValidationErrors(error);
          formError.value = 'Please correct the validation errors';
        } else {
          formError.value = error.response?.data?.detail || 'Failed to save fitment';
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
      fetchFitment();
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
      associatedProducts,
      makeOptions,
      modelOptions,
      engineOptions,
      transmissionOptions,
      showUnsavedDialog,
      pendingNavigation,
      isEditMode,
      rules,
      showProcessingInfo,
      partApplications,
      partTerminologyId,
      productId,
      processingApplications,
      processingResults,
      clearError,
      addAttribute,
      removeAttribute,
      submitForm,
      discardChanges,
      processPartApplications,
      getApplicationResultColor,
      getApplicationResultIcon,
      getResultStatusIcon,
      getResultStatusColor
    };
  }
});
</script>
