<!-- frontend/src/views/UserManagement.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">User Management</h1>
          <p class="text-subtitle-1">Manage system users and permissions</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
            color="primary"
            prepend-icon="mdi-account-plus"
            :to="{ name: 'UserCreate' }"
          >
            Add User
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
                label="Search Users"
                variant="outlined"
                density="comfortable"
                append-inner-icon="mdi-magnify"
                hide-details
                @keyup.enter="fetchUsers"
                @click:append-inner="fetchUsers"
              ></v-text-field>
            </v-col>

            <!-- Role Filter -->
            <v-col cols="12" md="3">
              <v-select
                v-model="filters.role"
                label="Role"
                :items="roleOptions"
                variant="outlined"
                density="comfortable"
                clearable
                hide-details
              ></v-select>
            </v-col>

            <!-- Status Filter -->
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

          <!-- Filter Actions -->
          <v-row class="mt-2">
            <v-col cols="12" class="d-flex justify-end">
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
                @click="fetchUsers"
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

      <!-- Users Data Table -->
      <v-card v-else>
        <v-data-table
          v-model:items-per-page="itemsPerPage"
          :headers="headers"
          :items="users"
          :loading="loading"
          class="elevation-1"
          loading-text="Loading users..."
          no-data-text="No users found"
        >
          <!-- Email/Name Column -->
          <template v-slot:item.userInfo="{ item }">
            <div>
              <router-link
                :to="{ name: 'UserDetail', params: { id: item.raw.id }}"
                class="text-decoration-none text-primary font-weight-medium"
              >
                {{ item.raw.full_name }}
              </router-link>
              <div class="text-caption text-medium-emphasis">
                {{ item.raw.email }}
              </div>
            </div>
          </template>

          <!-- Role Column -->
          <template v-slot:item.role="{ item }">
            <v-chip
              :color="getRoleColor(item.raw.role)"
              size="small"
              variant="tonal"
            >
              {{ item.raw.role }}
            </v-chip>
          </template>

          <!-- Status Column -->
          <template v-slot:item.is_active="{ item }">
            <v-chip
              :color="item.raw.is_active ? 'success' : 'error'"
              size="small"
              variant="tonal"
            >
              {{ item.raw.is_active ? 'Active' : 'Inactive' }}
            </v-chip>
          </template>

          <!-- Company Column -->
          <template v-slot:item.company="{ item }">
            <div v-if="item.raw.company">
              {{ item.raw.company.name }}
              <div class="text-caption text-medium-emphasis">
                {{ item.raw.company.account_type }}
              </div>
            </div>
            <span v-else class="text-medium-emphasis">None</span>
          </template>

          <!-- Created At Column -->
          <template v-slot:item.created_at="{ item }">
            <div>{{ formatDate(item.raw.created_at) }}</div>
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
                    :to="{ name: 'UserDetail', params: { id: item.raw.id }}"
                  >
                    <v-icon>mdi-eye</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Edit User">
                <template v-slot:activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    color="primary"
                    v-bind="props"
                    :to="{ name: 'UserEdit', params: { id: item.raw.id }}"
                    class="mx-1"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>

              <v-tooltip text="Delete User">
                <template v-slot:activator="{ props }">
                  <v-btn
                    icon
                    size="small"
                    color="error"
                    v-bind="props"
                    @click="confirmDelete(item.raw)"
                    :disabled="item.raw.id === currentUserId"
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
            @update:modelValue="fetchUsers"
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
            <p>Are you sure you want to delete the user <strong>{{ userToDelete?.full_name }}</strong>?</p>
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
              @click="deleteUser"
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
import { formatDate } from '@/utils/formatters';
import { notificationService } from '@/utils/notification';
import { User, UserRole } from '@/types/user';

// User filter interface
interface UserFilters {
  search?: string;
  role?: UserRole;
  is_active?: boolean;
  page?: number;
  page_size?: number;
}

export default defineComponent({
  name: 'UserManagement',

  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    // Current user ID (for preventing self-deletion)
    const currentUserId = computed(() => authStore.user?.id);

    // Data loading state
    const loading = ref(false);
    const users = ref<User[]>([]);

    // Pagination
    const page = ref(1);
    const itemsPerPage = ref(10);
    const totalItems = ref(0);
    const totalPages = ref(1);

    // Filters
    const search = ref('');
    const filters = ref<UserFilters>({
      page: 1,
      page_size: 10,
    });

    // Role options
    const roleOptions = [
      { title: 'Admin', value: UserRole.ADMIN },
      { title: 'Manager', value: UserRole.MANAGER },
      { title: 'Client', value: UserRole.CLIENT },
      { title: 'Distributor', value: UserRole.DISTRIBUTOR },
      { title: 'Read Only', value: UserRole.READ_ONLY },
    ];

    // Status options
    const statusOptions = [
      { title: 'Active', value: true },
      { title: 'Inactive', value: false },
    ];

    // Delete functionality
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);
    const userToDelete = ref<User | null>(null);

    // Table headers
    const headers = [
      { title: 'User', key: 'userInfo', sortable: false },
      { title: 'Role', key: 'role', sortable: true },
      { title: 'Status', key: 'is_active', sortable: true },
      { title: 'Company', key: 'company', sortable: false },
      { title: 'Created', key: 'created_at', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
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

    // Get color for role chip
    const getRoleColor = (role: UserRole): string => {
      switch (role) {
        case UserRole.ADMIN:
          return 'error';
        case UserRole.MANAGER:
          return 'warning';
        case UserRole.CLIENT:
          return 'primary';
        case UserRole.DISTRIBUTOR:
          return 'success';
        case UserRole.READ_ONLY:
          return 'grey';
        default:
          return 'grey';
      }
    };

    // Fetch users with current filters
    const fetchUsers = async () => {
      loading.value = true;

      try {
        // In a real implementation, this would call a userService
        // For now, we'll use mock data
        await new Promise(resolve => setTimeout(resolve, 500));

        // Mock response data
        const mockUsers: User[] = [];
        for (let i = 0; i < 15; i++) {
          const roleIndex = i % roleOptions.length;
          mockUsers.push({
            id: `user-${i}`,
            email: `user${i}@example.com`,
            full_name: `Test User ${i}`,
            role: roleOptions[roleIndex].value as UserRole,
            is_active: i % 5 !== 0,
            created_at: new Date(Date.now() - i * 86400000).toISOString(),
            company: i % 3 === 0 ? {
              id: `company-${i}`,
              name: `Company ${i}`,
              account_number: `ACC-${i}`,
              account_type: 'Client',
              is_active: true,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString()
            } : undefined
          });
        }

        // Filter by search term
        let filteredUsers = [...mockUsers];
        if (filters.value.search) {
          const searchTerm = filters.value.search.toLowerCase();
          filteredUsers = filteredUsers.filter(user =>
            user.email.toLowerCase().includes(searchTerm) ||
            user.full_name.toLowerCase().includes(searchTerm)
          );
        }

        // Filter by role
        if (filters.value.role) {
          filteredUsers = filteredUsers.filter(user => user.role === filters.value.role);
        }

        // Filter by status
        if (filters.value.is_active !== undefined) {
          filteredUsers = filteredUsers.filter(user => user.is_active === filters.value.is_active);
        }

        // Apply pagination
        const startIndex = (page.value - 1) * itemsPerPage.value;
        const endIndex = startIndex + itemsPerPage.value;
        users.value = filteredUsers.slice(startIndex, endIndex);

        totalItems.value = filteredUsers.length;
        totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value);
      } catch (error) {
        console.error('Error fetching users:', error);
        notificationService.error('Failed to load users.');
      } finally {
        loading.value = false;
      }
    };

    // Reset all filters
    const resetFilters = () => {
      search.value = '';
      filters.value = {
        page: 1,
        page_size: itemsPerPage.value,
      };
      page.value = 1;
      fetchUsers();
    };

    // Delete confirmation dialog
    const confirmDelete = (user: User) => {
      // Prevent deleting self
      if (user.id === currentUserId.value) {
        notificationService.error('You cannot delete your own account.');
        return;
      }

      userToDelete.value = user;
      deleteDialog.value = true;
    };

    // Delete user
    const deleteUser = async () => {
      if (!userToDelete.value) return;

      deleteLoading.value = true;

      try {
        // In a real implementation, this would call a userService
        await new Promise(resolve => setTimeout(resolve, 500));

        deleteDialog.value = false;

        notificationService.success(`User ${userToDelete.value.full_name} deleted successfully.`);

        // Remove from local list or refetch
        fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
        notificationService.error('Failed to delete user.');
      } finally {
        deleteLoading.value = false;
      }
    };

    // Initialize component
    onMounted(() => {
      fetchUsers();
    });

    return {
      currentUserId,
      loading,
      users,
      page,
      itemsPerPage,
      totalItems,
      totalPages,
      search,
      filters,
      roleOptions,
      statusOptions,
      headers,
      deleteDialog,
      deleteLoading,
      userToDelete,
      formatDate,
      getRoleColor,
      fetchUsers,
      resetFilters,
      confirmDelete,
      deleteUser,
    };
  }
});
</script>
