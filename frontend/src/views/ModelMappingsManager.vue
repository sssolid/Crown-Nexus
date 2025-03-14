<!-- frontend/src/views/ModelMappingsManager.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Model Mappings Manager</h1>
          <p class="text-subtitle-1">Manage vehicle model mappings for fitment processing</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
              color="primary"
              prepend-icon="mdi-refresh"
              @click="refreshMappings"
              class="mr-2"
          >
            Refresh Cache
          </v-btn>
          <v-btn
              color="success"
              prepend-icon="mdi-plus"
              @click="showAddMappingDialog"
          >
            Add Mapping
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search and Upload -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="8">
              <v-text-field
                  v-model="filters.pattern"
                  label="Search by Pattern"
                  variant="outlined"
                  density="comfortable"
                  clearable
                  append-inner-icon="mdi-magnify"
                  hide-details
                  @click:append-inner="applyFilter"
                  @keyup.enter="applyFilter"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="4" class="d-flex align-center">
              <v-file-input
                  v-model="uploadFile"
                  label="Import JSON Mappings"
                  variant="outlined"
                  density="comfortable"
                  accept=".json"
                  :rules="[v => !v || v.size < 1000000 || 'File size should be less than 1MB']"
                  hide-details
                  class="mr-2"
              ></v-file-input>
              <v-btn
                  color="primary"
                  @click="uploadMappings"
                  :disabled="!uploadFile"
                  :loading="uploading"
              >
                Upload
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Loading State -->
      <div v-if="initialLoading" class="d-flex justify-center my-6">
        <v-progress-circular
            indeterminate
            color="primary"
            size="64"
        ></v-progress-circular>
      </div>

      <!-- Mappings Data Table -->
      <v-card v-else>
        <v-data-table-server
            v-model:items-per-page="itemsPerPage"
            :headers="headers"
            :items="mappings"
            :loading="loading"
            :items-length="totalMappings"
            @update:options="loadMappings"
            class="elevation-1"
            loading-text="Loading model mappings..."
            no-data-text="No model mappings found"
        >
          <!-- Pattern Column -->
          <template v-slot:item.pattern="{ item }">
            <div class="font-weight-medium">{{ item.pattern }}</div>
          </template>

          <!-- Mapping Column -->
          <template v-slot:item.mapping="{ item }">
            <div class="d-flex align-center">
              <v-chip color="primary" size="small" class="mr-2">
                {{ getMake(item.mapping) }}
              </v-chip>
              <v-chip color="secondary" size="small" class="mr-2">
                {{ getVehicleCode(item.mapping) }}
              </v-chip>
              <span>{{ getModel(item.mapping) }}</span>
            </div>
          </template>

          <!-- Priority Column -->
          <template v-slot:item.priority="{ item }">
            <v-chip
                :color="item.priority > 0 ? 'success' : 'grey'"
                size="small"
                variant="tonal"
            >
              {{ item.priority }}
            </v-chip>
          </template>

          <!-- Active Column -->
          <template v-slot:item.active="{ item }">
            <v-icon
                :color="item.active ? 'success' : 'error'"
                :icon="item.active ? 'mdi-check-circle' : 'mdi-close-circle'"
            ></v-icon>
          </template>

          <!-- Actions Column -->
          <template v-slot:item.actions="{ item }">
            <div class="d-flex">
              <v-tooltip text="Edit Mapping">
                <template v-slot:activator="{ props }">
                  <v-btn
                      icon
                      size="small"
                      color="primary"
                      v-bind="props"
                      @click="editMapping(item)"
                      class="mr-1"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Toggle Active">
                <template v-slot:activator="{ props }">
                  <v-btn
                      icon
                      size="small"
                      :color="item.active ? 'warning' : 'success'"
                      v-bind="props"
                      @click="toggleActive(item)"
                      class="mr-1"
                  >
                    <v-icon>{{ item.active ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Delete Mapping">
                <template v-slot:activator="{ props }">
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

      <!-- Debug Info -->
      <v-card v-if="debug" class="mt-4">
        <v-card-text class="text-caption">
          <p>Debug Info:</p>
          <ul>
            <li>Current Page: {{ currentPage }}</li>
            <li>Items Per Page: {{ itemsPerPage }}</li>
            <li>Total Mappings: {{ totalMappings }}</li>
            <li>Items Count: {{ mappings.length }}</li>
            <li>Sort By: {{ currentSort?.key }}</li>
            <li>Sort Order: {{ currentSort?.order }}</li>
          </ul>
        </v-card-text>
      </v-card>

      <!-- Add/Edit Mapping Dialog -->
      <v-dialog v-model="mappingDialog" max-width="600">
        <v-card>
          <v-card-title class="text-h5 pa-4">
            {{ editMode ? 'Edit Mapping' : 'Add New Mapping' }}
          </v-card-title>
          <v-card-text class="pa-4">
            <v-form ref="form" @submit.prevent="saveMappingForm">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                      v-model="mappingForm.pattern"
                      label="Pattern"
                      variant="outlined"
                      :rules="[v => !!v || 'Pattern is required']"
                      hint="Pattern to match in vehicle text (e.g., 'WK Grand Cherokee')"
                      persistent-hint
                      required
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                      v-model="mappingForm.make"
                      label="Make"
                      variant="outlined"
                      :rules="[v => !!v || 'Make is required']"
                      hint="Vehicle make (e.g., 'Jeep')"
                      persistent-hint
                      required
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                      v-model="mappingForm.vehicleCode"
                      label="Vehicle Code"
                      variant="outlined"
                      :rules="[v => !!v || 'Vehicle code is required']"
                      hint="Vehicle code (e.g., 'WK')"
                      persistent-hint
                      required
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="4">
                  <v-text-field
                      v-model="mappingForm.model"
                      label="Model"
                      variant="outlined"
                      :rules="[v => !!v || 'Model is required']"
                      hint="Vehicle model (e.g., 'Grand Cherokee')"
                      persistent-hint
                      required
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-text-field
                      v-model.number="mappingForm.priority"
                      label="Priority"
                      type="number"
                      variant="outlined"
                      hint="Higher values are processed first"
                      persistent-hint
                  ></v-text-field>
                </v-col>

                <v-col cols="12" md="6">
                  <v-switch
                      v-model="mappingForm.active"
                      label="Active"
                      color="success"
                      hide-details
                      inset
                  ></v-switch>
                </v-col>

                <v-col cols="12">
                  <v-alert
                      v-if="mappingForm.make && mappingForm.vehicleCode && mappingForm.model"
                      type="info"
                      variant="tonal"
                  >
                    Mapping: <strong>{{ mappingForm.make }}|{{ mappingForm.vehicleCode }}|{{ mappingForm.model }}</strong>
                  </v-alert>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn
                color="secondary"
                variant="text"
                @click="mappingDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
                color="primary"
                @click="saveMapping"
                :loading="savingMapping"
            >
              {{ editMode ? 'Update' : 'Create' }}
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
            <p>Are you sure you want to delete the mapping for <strong>{{ mappingToDelete?.pattern }}</strong>?</p>
            <p class="text-medium-emphasis mt-2">This action cannot be undone.</p>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                variant="text"
                @click="deleteDialog = false"
            >
              Cancel
            </v-btn>
            <v-btn
                color="error"
                @click="deleteMapping"
                :loading="deletingMapping"
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
import { defineComponent, ref, computed, onMounted } from 'vue';
import modelMappingService, { ModelMapping } from '@/services/modelMapping';
import { notificationService } from '@/utils/notification';

interface MappingForm {
  id?: number;
  pattern: string;
  make: string;
  vehicleCode: string;
  model: string;
  priority: number;
  active: boolean;
}

interface SortState {
  key: string;
  order: string;
}

export default defineComponent({
  name: 'ModelMappingsManager',

  setup() {
    // Debug mode
    const debug = ref(true);

    // Table data
    const initialLoading = ref(true);
    const loading = ref(false);
    const mappings = ref<ModelMapping[]>([]);
    const totalMappings = ref(0);
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const currentSort = ref<SortState | null>(null);

    // Filters
    const filters = ref({
      pattern: '',
    });

    // File upload
    const uploadFile = ref<File | null>(null);
    const uploading = ref(false);

    // Mapping dialog
    const mappingDialog = ref(false);
    const editMode = ref(false);
    const savingMapping = ref(false);
    const mappingForm = ref<MappingForm>({
      pattern: '',
      make: '',
      vehicleCode: '',
      model: '',
      priority: 0,
      active: true,
    });
    const form = ref<any>(null);

    // Delete dialog
    const deleteDialog = ref(false);
    const deletingMapping = ref(false);
    const mappingToDelete = ref<ModelMapping | null>(null);

    // Table headers
    const headers = [
      { title: 'Pattern', key: 'pattern', sortable: true },
      { title: 'Mapping', key: 'mapping', sortable: true },
      { title: 'Priority', key: 'priority', sortable: true, width: '100px' },
      { title: 'Active', key: 'active', sortable: true, width: '80px' },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end', width: '120px' },
    ];

    // Helper methods for mapping display
    const getMake = (mapping: string): string => {
      const parts = mapping.split('|');
      if (parts[0]) return parts[0];
      if (parts[1]) return parts[1]; // Use vehicle code as fallback
      if (parts[2]) return parts[2]; // Use model as fallback
      return 'Universal';
    };

    const getVehicleCode = (mapping: string): string => {
      const parts = mapping.split('|');
      return parts[1] || '-';  // Show dash if empty
    };

    const getModel = (mapping: string): string => {
      const parts = mapping.split('|');
      if (parts[2]) return parts[2];
      if (parts[1]) return parts[1]; // Use vehicle code as fallback
      if (parts[0]) return parts[0]; // Use make as fallback
      return 'Universal';
    };

    // Server-side data loading
    const loadMappings = async (options: any) => {
      console.log('Data table options:', options);
      loading.value = true;

      // Get current page and items per page
      currentPage.value = options.page;
      itemsPerPage.value = options.itemsPerPage;

      // Calculate skip for backend pagination
      const skip = (currentPage.value - 1) * itemsPerPage.value;

      // Handle sorting
      let sortBy = undefined;
      let sortOrder = undefined;

      if (options.sortBy && options.sortBy.length > 0) {
        sortBy = options.sortBy[0].key;
        sortOrder = options.sortBy[0].order;
        currentSort.value = { key: sortBy, order: sortOrder };
      } else {
        currentSort.value = null;
      }

      try {
        console.log(`Loading mappings with skip=${skip}, limit=${itemsPerPage.value}, pattern=${filters.value.pattern || 'none'}, sortBy=${sortBy || 'none'}, sortOrder=${sortOrder || 'none'}`);

        const result = await modelMappingService.getModelMappings(
            skip,
            itemsPerPage.value,
            filters.value.pattern,
            sortBy,
            sortOrder
        );

        mappings.value = result.items;
        totalMappings.value = result.total;

        console.log(`Loaded ${result.items.length} items out of ${result.total} total`);
      } catch (error) {
        console.error('Error loading mappings:', error);
        notificationService.error('Failed to load model mappings');
      } finally {
        loading.value = false;
        initialLoading.value = false;
      }
    };

    // Apply filter and reload data
    const applyFilter = () => {
      // Reset to first page when applying a filter
      currentPage.value = 1;

      // Trigger data reload
      loadMappings({
        page: currentPage.value,
        itemsPerPage: itemsPerPage.value,
        sortBy: currentSort.value ? [currentSort.value] : []
      });
    };

    // Refresh mappings cache
    const refreshMappings = async () => {
      try {
        await modelMappingService.refreshMappings();
        notificationService.success('Mapping cache refreshed successfully');

        // Reload data
        loadMappings({
          page: currentPage.value,
          itemsPerPage: itemsPerPage.value,
          sortBy: currentSort.value ? [currentSort.value] : []
        });
      } catch (error) {
        console.error('Error refreshing mappings:', error);
        notificationService.error('Failed to refresh mapping cache');
      }
    };

    // Upload mappings
    const uploadMappings = async () => {
      if (!uploadFile.value) return;

      uploading.value = true;

      try {
        const result = await modelMappingService.uploadModelMappings(uploadFile.value);
        notificationService.success(`${result.mapping_count} mappings imported successfully`);

        // Reset upload file
        uploadFile.value = null;

        // Refresh data
        loadMappings({
          page: currentPage.value,
          itemsPerPage: itemsPerPage.value,
          sortBy: currentSort.value ? [currentSort.value] : []
        });

        // Refresh the cache
        await refreshMappings();
      } catch (error) {
        console.error('Error uploading mappings:', error);
        notificationService.error('Failed to upload mappings');
      } finally {
        uploading.value = false;
      }
    };

    // Show add mapping dialog
    const showAddMappingDialog = () => {
      editMode.value = false;
      mappingForm.value = {
        pattern: '',
        make: '',
        vehicleCode: '',
        model: '',
        priority: 0,
        active: true,
      };
      mappingDialog.value = true;
    };

    // Edit mapping
    const editMapping = (mapping: ModelMapping) => {
      editMode.value = true;

      // Parse mapping string and handle special cases
      const parts = mapping.mapping.split('|');

      mappingForm.value = {
        id: mapping.id,
        pattern: mapping.pattern,
        make: parts[0] || '',
        vehicleCode: parts[1] || '',
        model: parts[2] || '',
        priority: mapping.priority,
        active: mapping.active,
      };

      mappingDialog.value = true;
    };

    // Toggle active state
    const toggleActive = async (mapping: ModelMapping) => {
      try {
        await modelMappingService.updateModelMapping(
            mapping.id,
            {
              pattern: mapping.pattern,
              mapping: mapping.mapping,
              priority: mapping.priority,
              active: !mapping.active,
            }
        );

        // Refresh the data
        loadMappings({
          page: currentPage.value,
          itemsPerPage: itemsPerPage.value,
          sortBy: currentSort.value ? [currentSort.value] : []
        });

        // Refresh the cache
        await refreshMappings();

        notificationService.success(`Mapping ${mapping.active ? 'disabled' : 'enabled'} successfully`);
      } catch (error) {
        console.error('Error toggling mapping active state:', error);
        notificationService.error('Failed to update mapping');
      }
    };

    // Save mapping form
    const saveMappingForm = () => {
      // This is just to trigger form validation
      // Actual save logic is in saveMapping
    };

    // Save mapping
    const saveMapping = async () => {
      // Validate form
      const { valid } = await form.value.validate();

      if (!valid) {
        notificationService.error('Please fix the errors in the form');
        return;
      }

      savingMapping.value = true;

      try {
        // Create mapping string
        const mappingString = `${mappingForm.value.make}|${mappingForm.value.vehicleCode}|${mappingForm.value.model}`;

        if (editMode.value && mappingForm.value.id) {
          // Update existing mapping
          await modelMappingService.updateModelMapping(
              mappingForm.value.id,
              {
                pattern: mappingForm.value.pattern,
                mapping: mappingString,
                priority: mappingForm.value.priority,
                active: mappingForm.value.active,
              }
          );

          notificationService.success('Mapping updated successfully');
        } else {
          // Create new mapping
          await modelMappingService.createModelMapping({
            pattern: mappingForm.value.pattern,
            mapping: mappingString,
            priority: mappingForm.value.priority,
            active: mappingForm.value.active,
          });

          notificationService.success('Mapping created successfully');
        }

        // Close dialog
        mappingDialog.value = false;

        // Refresh the data
        loadMappings({
          page: currentPage.value,
          itemsPerPage: itemsPerPage.value,
          sortBy: currentSort.value ? [currentSort.value] : []
        });

        // Refresh the cache
        await refreshMappings();
      } catch (error) {
        console.error('Error saving mapping:', error);
        notificationService.error('Failed to save mapping');
      } finally {
        savingMapping.value = false;
      }
    };

    // Confirm delete
    const confirmDelete = (mapping: ModelMapping) => {
      mappingToDelete.value = mapping;
      deleteDialog.value = true;
    };

    // Delete mapping
    const deleteMapping = async () => {
      if (!mappingToDelete.value) return;

      deletingMapping.value = true;

      try {
        await modelMappingService.deleteModelMapping(mappingToDelete.value.id);

        notificationService.success('Mapping deleted successfully');

        // Close dialog
        deleteDialog.value = false;

        // Refresh the data
        loadMappings({
          page: currentPage.value,
          itemsPerPage: itemsPerPage.value,
          sortBy: currentSort.value ? [currentSort.value] : []
        });

        // Refresh the cache
        await refreshMappings();
      } catch (error) {
        console.error('Error deleting mapping:', error);
        notificationService.error('Failed to delete mapping');
      } finally {
        deletingMapping.value = false;
        mappingToDelete.value = null;
      }
    };

    // Initialize
    onMounted(() => {
      // Initial data load
      loadMappings({
        page: currentPage.value,
        itemsPerPage: itemsPerPage.value,
        sortBy: []
      });
    });

    return {
      // Data
      debug,
      initialLoading,
      loading,
      mappings,
      totalMappings,
      currentPage,
      itemsPerPage,
      currentSort,
      filters,
      uploadFile,
      uploading,
      mappingDialog,
      editMode,
      savingMapping,
      mappingForm,
      form,
      deleteDialog,
      deletingMapping,
      mappingToDelete,
      headers,

      // Methods
      getMake,
      getVehicleCode,
      getModel,
      loadMappings,
      applyFilter,
      refreshMappings,
      uploadMappings,
      showAddMappingDialog,
      editMapping,
      toggleActive,
      saveMappingForm,
      saveMapping,
      confirmDelete,
      deleteMapping,
    };
  }
});
</script>
