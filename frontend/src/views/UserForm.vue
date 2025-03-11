<!-- frontend/src/views/UserForm.vue -->
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
                  {{ isEditMode ? 'Edit User' : 'Create User' }}
                </h1>
                <p class="text-subtitle-1">
                  {{ isEditMode ? `Editing ${form.full_name || 'user'}` : 'Add a new user to the system' }}
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
                <v-card-title>User Information</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row>
                    <!-- Full Name -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="form.full_name"
                        label="Full Name"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="errors.full_name"
                        :disabled="loading"
                        @input="clearError('full_name')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Email -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="form.email"
                        label="Email Address"
                        type="email"
                        variant="outlined"
                        :rules="[rules.required, rules.email]"
                        :error-messages="errors.email"
                        :disabled="loading || (isEditMode && form.email === currentUser?.email)"
                        @input="clearError('email')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Password (only for create mode or when changing password) -->
                    <v-col cols="12" v-if="!isEditMode || showPasswordFields">
                      <v-text-field
                        v-model="form.password"
                        label="Password"
                        :type="showPassword ? 'text' : 'password'"
                        :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="showPassword = !showPassword"
                        variant="outlined"
                        :rules="passwordRules"
                        :error-messages="errors.password"
                        :disabled="loading"
                        @input="clearError('password')"
                        :required="!isEditMode"
                      ></v-text-field>
                    </v-col>

                    <!-- Confirm Password (only for create mode or when changing password) -->
                    <v-col cols="12" v-if="!isEditMode || showPasswordFields">
                      <v-text-field
                        v-model="confirmPassword"
                        label="Confirm Password"
                        :type="showPassword ? 'text' : 'password'"
                        variant="outlined"
                        :rules="[rules.passwordMatch]"
                        :error-messages="errors.confirm_password"
                        :disabled="loading"
                        :required="!isEditMode"
                      ></v-text-field>
                    </v-col>

                    <!-- Password Change Toggle (only for edit mode) -->
                    <v-col cols="12" v-if="isEditMode && !showPasswordFields">
                      <v-btn
                        variant="outlined"
                        color="primary"
                        @click="showPasswordFields = true"
                        :disabled="loading"
                      >
                        Change Password
                      </v-btn>
                    </v-col>

                    <!-- Role Selection -->
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="form.role"
                        label="Role"
                        :items="roleOptions"
                        item-title="title"
                        item-value="value"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="errors.role"
                        :disabled="loading || (isEditMode && form.id === currentUser?.id)"
                        @update:modelValue="clearError('role')"
                        required
                      ></v-select>
                    </v-col>

                    <!-- Status -->
                    <v-col cols="12" md="6">
                      <v-switch
                        v-model="form.is_active"
                        label="User is active"
                        color="success"
                        :disabled="loading || (isEditMode && form.id === currentUser?.id)"
                        inset
                      ></v-switch>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>

              <!-- Company Association (Optional) -->
              <v-card class="mb-6">
                <v-card-title class="d-flex align-center">
                  Company Association
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row>
                    <v-col cols="12">
                      <v-autocomplete
                        v-model="form.company_id"
                        label="Associate with Company"
                        :items="companies"
                        item-title="name"
                        item-value="id"
                        variant="outlined"
                        :error-messages="errors.company_id"
                        :disabled="loading"
                        @update:modelValue="clearError('company_id')"
                        clearable
                        hint="Optional company association"
                        persistent-hint
                      ></v-autocomplete>
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
                    ? 'Update this user with your changes.'
                    : 'Create a new user in the system.'
                    }}
                  </p>

                  <v-alert
                    v-if="isEditMode && form.id === currentUser?.id"
                    type="warning"
                    variant="tonal"
                    class="mb-4"
                  >
                    You are editing your own account. Some fields are restricted.
                  </v-alert>

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
                    {{ isEditMode ? 'Update User' : 'Create User' }}
                  </v-btn>
                </v-card-actions>
              </v-card>

              <!-- Role Information Card -->
              <v-card>
                <v-card-title>Role Information</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="mb-4">Selected role permissions:</p>

                  <v-list density="compact" class="bg-grey-lighten-4 rounded">
                    <v-list-item v-for="(permission, index) in selectedRolePermissions" :key="index">
                      <template v-slot:prepend>
                        <v-icon color="primary" size="small">mdi-check-circle</v-icon>
                      </template>
                      <v-list-item-title>{{ permission }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-card-text>
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
import userService from '@/services/user';
import { User, UserRole } from '@/types/user';
import { notificationService } from '@/utils/notification';
import { parseValidationErrors } from '@/utils/error-handler';

interface UserForm {
  id?: string;
  email: string;
  full_name: string;
  password?: string;
  role: UserRole;
  is_active: boolean;
  company_id?: string | null;
}

// Company interface for dropdown (simplified)
interface Company {
  id: string;
  name: string;
  account_type: string;
}

export default defineComponent({
  name: 'UserForm',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    // Current authenticated user
    const currentUser = computed(() => authStore.user);

    // Form references
    const formRef = ref<any>(null);
    const isFormValid = ref(false);

    // Loading states
    const initialLoading = ref(false);
    const loading = ref(false);

    // Form errors
    const formError = ref('');
    const errors = ref<Record<string, string>>({});

    // Password fields
    const showPassword = ref(false);
    const showPasswordFields = ref(false);
    const confirmPassword = ref('');

    // Form data
    const form = ref<UserForm>({
      email: '',
      full_name: '',
      password: '',
      role: UserRole.READ_ONLY,
      is_active: true,
      company_id: null
    });

    // Form state tracking
    const formDirty = ref(false);
    const showUnsavedDialog = ref(false);
    const pendingNavigation = ref<any>(null);

    // Companies for dropdown
    const companies = ref<Company[]>([]);

    // Role dropdown options
    const roleOptions = [
      { title: 'Administrator', value: UserRole.ADMIN },
      { title: 'Manager', value: UserRole.MANAGER },
      { title: 'Client', value: UserRole.CLIENT },
      { title: 'Distributor', value: UserRole.DISTRIBUTOR },
      { title: 'Read Only', value: UserRole.READ_ONLY },
    ];

    // Role permissions info
    const rolePermissions = {
      [UserRole.ADMIN]: [
        'Full system access',
        'Manage all users',
        'Manage all products',
        'Manage all fitments',
        'Access admin dashboard',
        'Configure system settings'
      ],
      [UserRole.MANAGER]: [
        'Manage products',
        'Manage fitments',
        'View all users',
        'Access reporting',
        'Moderate content'
      ],
      [UserRole.CLIENT]: [
        'View products',
        'View fitments',
        'Place orders',
        'View order history',
        'Update profile'
      ],
      [UserRole.DISTRIBUTOR]: [
        'View products',
        'View and update inventory',
        'Manage distributor pricing',
        'View orders',
        'Update profile'
      ],
      [UserRole.READ_ONLY]: [
        'View products',
        'View fitments',
        'Update profile'
      ]
    };

    // Get permissions for selected role
    const selectedRolePermissions = computed(() => {
      return rolePermissions[form.value.role] || [];
    });

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
      return route.name === 'UserEdit';
    });

    // User ID from route
    const userId = computed(() => {
      return route.params.id as string;
    });

    // Form validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required',
      email: (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      passwordMatch: (v: string) => v === form.value.password || 'Passwords do not match',
      passwordLength: (v: string) => !v || v.length >= 8 || 'Password must be at least 8 characters',
      passwordComplexity: (v: string) => {
        if (!v) return true;

        // At least one uppercase, one lowercase, one number
        const hasUppercase = /[A-Z]/.test(v);
        const hasLowercase = /[a-z]/.test(v);
        const hasNumber = /[0-9]/.test(v);

        return (hasUppercase && hasLowercase && hasNumber) || 'Password must include uppercase, lowercase, and numbers';
      }
    };

    // Password validation rules - conditional based on mode
    const passwordRules = computed(() => {
      if (isEditMode.value && !form.value.password) {
        // In edit mode, password is optional (can be empty)
        return [];
      }

      // For create mode or when password is being changed
      return [
        rules.passwordLength,
        rules.passwordComplexity,
        ...(isEditMode.value ? [] : [rules.required])
      ];
    });

    // Clear a specific field error
    const clearError = (field: string) => {
      if (errors.value[field]) {
        delete errors.value[field];
      }
      formDirty.value = true;
    };

    // Fetch user data for edit mode
    const fetchUser = async () => {
      if (!isEditMode.value) return;

      initialLoading.value = true;

      try {
        const user = await userService.getUser(userId.value);

        // Populate form with user data
        form.value.id = user.id;
        form.value.email = user.email;
        form.value.full_name = user.full_name;
        form.value.role = user.role;
        form.value.is_active = user.is_active;

        // Set company ID if user has a company association
        if (user.company) {
          form.value.company_id = user.company.id;
        }

        // Reset form dirty state after loading data
        formDirty.value = false;
      } catch (error) {
        console.error('Error fetching user:', error);
        notificationService.error('Failed to load user data');
        router.push({ name: 'UserManagement' });
      } finally {
        initialLoading.value = false;
      }
    };

    // Fetch companies for dropdown
    const fetchCompanies = async () => {
      try {
        companies.value = await userService.getCompanies();
      } catch (error) {
        console.error('Error fetching companies:', error);
        notificationService.error('Failed to load companies');
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
        // Prepare form data
        const userData = { ...form.value };

        // Only include password if it's provided (for edit mode)
        if (isEditMode.value && !userData.password) {
          delete userData.password;
        }

        let result: User;
        if (isEditMode.value) {
          // Update existing user
          result = await userService.updateUser(userId.value, userData);
          notificationService.success('User updated successfully');
        } else {
          // Create new user
          result = await userService.createUser(userData);
          notificationService.success('User created successfully');
        }

        // Reset form dirty state
        formDirty.value = false;

        // Redirect to user detail
        router.push({ name: 'UserDetail', params: { id: result.id } });
      } catch (error: any) {
        console.error('Error submitting user:', error);

        // Handle validation errors
        if (error.response?.status === 422) {
          errors.value = parseValidationErrors(error);
          formError.value = 'Please correct the validation errors';
        } else {
          formError.value = error.response?.data?.detail || 'Failed to save user';
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
        fetchUser(),
        fetchCompanies()
      ]);
    });

    return {
      router,
      currentUser,
      formRef,
      isFormValid,
      initialLoading,
      loading,
      formError,
      errors,
      form,
      showPassword,
      showPasswordFields,
      confirmPassword,
      companies,
      roleOptions,
      selectedRolePermissions,
      showUnsavedDialog,
      pendingNavigation,
      isEditMode,
      rules,
      passwordRules,
      clearError,
      submitForm,
      discardChanges
    };
  }
});
</script>
