<!-- frontend/src/views/UserDetail.vue -->
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

      <template v-else-if="user">
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
                <h1 class="text-h3 font-weight-bold">{{ user.full_name }}</h1>
                <p class="text-subtitle-1">{{ user.email }}</p>
              </div>
            </div>
          </v-col>

          <v-col cols="12" md="4" class="d-flex justify-end align-center">
            <v-btn
              v-if="canEdit"
              color="primary"
              prepend-icon="mdi-pencil"
              :to="{ name: 'UserEdit', params: { id: user.id }}"
              class="mr-2"
            >
              Edit
            </v-btn>

            <v-btn
              v-if="canDelete"
              color="error"
              variant="outlined"
              prepend-icon="mdi-delete"
              @click="confirmDelete"
            >
              Delete
            </v-btn>
          </v-col>
        </v-row>

        <!-- User Details -->
        <v-row>
          <!-- Main User Info -->
          <v-col cols="12" md="8">
            <v-card class="mb-6">
              <v-card-title>User Information</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <!-- Basic Info -->
                  <v-col cols="12" md="6">
                    <v-list>
                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-account" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Full Name</v-list-item-title>
                        <v-list-item-subtitle>{{ user.full_name }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-email" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Email</v-list-item-title>
                        <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-badge-account" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Role</v-list-item-title>
                        <v-list-item-subtitle>
                          <v-chip
                            :color="getRoleColor(user.role)"
                            size="small"
                            variant="tonal"
                          >
                            {{ getRoleLabel(user.role) }}
                          </v-chip>
                        </v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-circle" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Status</v-list-item-title>
                        <v-list-item-subtitle>
                          <v-chip
                            :color="user.is_active ? 'success' : 'error'"
                            size="small"
                            variant="tonal"
                          >
                            {{ user.is_active ? 'Active' : 'Inactive' }}
                          </v-chip>
                        </v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>

                  <!-- Company & Dates -->
                  <v-col cols="12" md="6">
                    <v-list>
                      <v-list-item v-if="user.company">
                        <template v-slot:prepend>
                          <v-icon icon="mdi-domain" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Company</v-list-item-title>
                        <v-list-item-subtitle>
                          <div>{{ user.company.name }}</div>
                          <div class="text-caption text-medium-emphasis">{{ user.company.account_type }}</div>
                        </v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item v-else>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-domain-off" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Company</v-list-item-title>
                        <v-list-item-subtitle>
                          <span class="text-medium-emphasis">No company association</span>
                        </v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item>
                        <template v-slot:prepend>
                          <v-icon icon="mdi-calendar-plus" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Created</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(user.created_at) }}</v-list-item-subtitle>
                      </v-list-item>

                      <v-list-item v-if="user.last_login">
                        <template v-slot:prepend>
                          <v-icon icon="mdi-login" class="mr-2"></v-icon>
                        </template>
                        <v-list-item-title>Last Login</v-list-item-title>
                        <v-list-item-subtitle>{{ formatDateTime(user.last_login) }}</v-list-item-subtitle>
                      </v-list-item>
                    </v-list>
                  </v-col>
                </v-row>

                <!-- Permissions Section -->
                <v-divider class="my-4"></v-divider>
                <h3 class="text-h6 mb-2">Role Permissions</h3>
                <v-row>
                  <v-col cols="12">
                    <v-list density="compact" class="bg-grey-lighten-4 rounded">
                      <v-list-item
                        v-for="(permission, index) in rolePermissions[user.role] || []"
                        :key="index"
                      >
                        <template v-slot:prepend>
                          <v-icon color="primary" size="small">mdi-check-circle</v-icon>
                        </template>
                        <v-list-item-title>{{ permission }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- User Activity Log -->
            <v-card>
              <v-card-title class="d-flex align-center">
                Activity Log
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  size="small"
                  variant="text"
                  prepend-icon="mdi-refresh"
                  @click="refreshActivityLog"
                  :loading="activityLoading"
                >
                  Refresh
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>

              <!-- Activity Content -->
              <div v-if="activityLoading" class="d-flex justify-center my-4">
                <v-progress-circular indeterminate color="primary"></v-progress-circular>
              </div>

              <v-list v-else-if="activityLog.length > 0" lines="two">
                <v-list-item
                  v-for="(activity, index) in activityLog"
                  :key="index"
                  :subtitle="formatDateTime(activity.timestamp)"
                >
                  <template v-slot:prepend>
                    <v-avatar :color="activity.color" size="36">
                      <v-icon :icon="activity.icon" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title>{{ activity.description }}</v-list-item-title>
                </v-list-item>
              </v-list>

              <v-card-text v-else class="text-center py-4">
                <v-icon icon="mdi-information-outline" color="info" size="large" class="mb-2"></v-icon>
                <p>No activity recorded for this user</p>
              </v-card-text>

              <!-- Pagination (if needed) -->
              <v-card-actions v-if="activityLog.length > 0">
                <v-spacer></v-spacer>
                <v-btn
                  variant="text"
                  prepend-icon="mdi-eye"
                  color="primary"
                  @click="loadMoreActivity"
                  :disabled="activityLoading || !hasMoreActivity"
                >
                  Load More
                </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-col>

          <!-- Sidebar -->
          <v-col cols="12" md="4">
            <!-- Quick Actions -->
            <v-card class="mb-6">
              <v-card-title>Quick Actions</v-card-title>
              <v-divider></v-divider>
              <v-card-text class="p-0">
                <v-list>
                  <v-list-item
                    v-if="canSendPasswordReset"
                    prepend-icon="mdi-lock-reset"
                    @click="confirmPasswordReset"
                  >
                    <v-list-item-title>Send Password Reset</v-list-item-title>
                    <v-list-item-subtitle>Email user a reset link</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item
                    v-if="canToggleUserStatus"
                    :prepend-icon="user.is_active ? 'mdi-account-cancel' : 'mdi-account-check'"
                    @click="confirmToggleStatus"
                  >
                    <v-list-item-title>{{ user.is_active ? 'Deactivate User' : 'Activate User' }}</v-list-item-title>
                    <v-list-item-subtitle>{{ user.is_active ? 'Disable account access' : 'Enable account access' }}</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item
                    v-if="canImpersonateUser"
                    prepend-icon="mdi-account-convert"
                    @click="confirmImpersonateUser"
                  >
                    <v-list-item-title>Impersonate User</v-list-item-title>
                    <v-list-item-subtitle>View system as this user</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- Associated Content Card -->
            <v-card v-if="user.company">
              <v-card-title class="d-flex align-center">
                Company Details
                <v-spacer></v-spacer>
                <v-btn
                  variant="text"
                  size="small"
                  color="primary"
                  icon="mdi-arrow-right"
                  :to="{ name: 'CompanyDetail', params: { id: user.company.id } }"
                ></v-btn>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list density="compact">
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon icon="mdi-domain" size="small"></v-icon>
                    </template>
                    <v-list-item-title>{{ user.company.name }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon icon="mdi-identifier" size="small"></v-icon>
                    </template>
                    <v-list-item-title>Account #: {{ user.company.account_number }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon icon="mdi-tag" size="small"></v-icon>
                    </template>
                    <v-list-item-title>Type: {{ user.company.account_type }}</v-list-item-title>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon icon="mdi-account-group" size="small"></v-icon>
                    </template>
                    <v-list-item-title>
                      <v-btn
                        variant="text"
                        color="primary"
                        density="compact"
                        :to="{ name: 'UserManagement', query: { company_id: user.company.id } }"
                      >
                        View All Users
                      </v-btn>
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Delete Confirmation Dialog -->
        <v-dialog v-model="deleteDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-error text-white pa-4">
              Confirm Delete
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>Are you sure you want to delete the user <strong>{{ user.full_name }}</strong>?</p>
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

        <!-- Toggle Status Confirmation Dialog -->
        <v-dialog v-model="statusDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 pa-4" :class="user.is_active ? 'bg-warning' : 'bg-success'">
              {{ user.is_active ? 'Deactivate User' : 'Activate User' }}
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>
                Are you sure you want to {{ user.is_active ? 'deactivate' : 'activate' }}
                <strong>{{ user.full_name }}</strong>?
              </p>
              <p class="text-medium-emphasis mt-2">
                {{ user.is_active
                ? 'Deactivated users cannot log in to the system.'
                : 'Activated users can log in to the system.'
                }}
              </p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="tonal"
                @click="statusDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                :color="user.is_active ? 'warning' : 'success'"
                @click="toggleUserStatus"
                :loading="statusLoading"
              >
                {{ user.is_active ? 'Deactivate' : 'Activate' }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Password Reset Confirmation Dialog -->
        <v-dialog v-model="resetDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-primary text-white pa-4">
              Send Password Reset
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>Send a password reset email to <strong>{{ user.email }}</strong>?</p>
              <p class="text-medium-emphasis mt-2">
                The user will receive an email with instructions to reset their password.
              </p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="resetDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="sendPasswordReset"
                :loading="resetLoading"
              >
                Send Reset Email
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Impersonate User Confirmation Dialog -->
        <v-dialog v-model="impersonateDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-primary text-white pa-4">
              Impersonate User
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>
                You are about to impersonate <strong>{{ user.full_name }}</strong>.
              </p>
              <p class="text-medium-emphasis mt-2">
                While impersonating, you will see and interact with the system as this user.
                This action is logged for security purposes.
              </p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="impersonateDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="impersonateUser"
                :loading="impersonateLoading"
              >
                Start Impersonation
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <!-- Not Found State -->
      <div v-else class="text-center my-12">
        <v-icon icon="mdi-alert-circle" color="warning" size="64"></v-icon>
        <h2 class="text-h4 mt-4">User Not Found</h2>
        <p class="text-body-1 mt-2">The user you're looking for doesn't exist or has been removed.</p>
        <v-btn
          color="primary"
          class="mt-4"
          @click="router.push({ name: 'UserManagement' })"
        >
          Back to Users
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import userService from '@/services/user';
import { User, UserRole } from '@/types/user';
import { formatDateTime } from '@/utils/formatters';
import { notificationService } from '@/utils/notification';

// Activity log entry interface
interface ActivityLogEntry {
  id: string;
  user_id: string;
  action: string;
  description: string;
  timestamp: string;
  metadata?: Record<string, any>;
  icon: string;
  color: string;
}

export default defineComponent({
  name: 'UserDetail',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    // Data loading state
    const loading = ref(true);
    const user = ref<User | null>(null);

    // Activity log state
    const activityLog = ref<ActivityLogEntry[]>([]);
    const activityLoading = ref(false);
    const activityPage = ref(1);
    const activityPageSize = ref(10);
    const hasMoreActivity = ref(false);

    // Dialog states
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);
    const statusDialog = ref(false);
    const statusLoading = ref(false);
    const resetDialog = ref(false);
    const resetLoading = ref(false);
    const impersonateDialog = ref(false);
    const impersonateLoading = ref(false);

    // Get user ID from route
    const userId = computed(() => route.params.id as string);

    // Current user permissions
    const currentUser = computed(() => authStore.user);
    const isCurrentUser = computed(() => user.value?.id === currentUser.value?.id);
    const isAdmin = computed(() => authStore.isAdmin);

    // Permission checks
    const canEdit = computed(() => isAdmin.value || isCurrentUser.value);
    const canDelete = computed(() => isAdmin.value && !isCurrentUser.value);
    const canToggleUserStatus = computed(() => isAdmin.value && !isCurrentUser.value);
    const canSendPasswordReset = computed(() => isAdmin.value);
    const canImpersonateUser = computed(() => isAdmin.value && !isCurrentUser.value && user.value?.is_active);

    // Role permissions map
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

    // Get formatted role label
    const getRoleLabel = (role: UserRole): string => {
      switch (role) {
        case UserRole.ADMIN: return 'Administrator';
        case UserRole.MANAGER: return 'Manager';
        case UserRole.CLIENT: return 'Client';
        case UserRole.DISTRIBUTOR: return 'Distributor';
        case UserRole.READ_ONLY: return 'Read Only';
        default: return role;
      }
    };

    // Get color for role chip
    const getRoleColor = (role: UserRole): string => {
      switch (role) {
        case UserRole.ADMIN: return 'error';
        case UserRole.MANAGER: return 'warning';
        case UserRole.CLIENT: return 'primary';
        case UserRole.DISTRIBUTOR: return 'success';
        case UserRole.READ_ONLY: return 'grey';
        default: return 'grey';
      }
    };

    // Fetch user data
    const fetchUser = async () => {
      loading.value = true;

      try {
        user.value = await userService.getUser(userId.value);

        // Fetch activity log after user is loaded
        fetchActivityLog();
      } catch (error) {
        console.error('Error fetching user:', error);
        user.value = null;
        notificationService.error('Failed to load user details');
      } finally {
        loading.value = false;
      }
    };

    // Fetch user activity log
    const fetchActivityLog = async (reset: boolean = true) => {
      if (reset) {
        activityPage.value = 1;
        activityLog.value = [];
      }

      activityLoading.value = true;

      try {
        // In a real implementation, you would fetch from the API
        // For now, using mock data
        await new Promise(resolve => setTimeout(resolve, 500));

        // Activity log entry types and their icons/colors
        const activityTypes = [
          { action: 'login', icon: 'mdi-login', color: 'primary', description: 'User logged in' },
          { action: 'logout', icon: 'mdi-logout', color: 'grey', description: 'User logged out' },
          { action: 'profile_update', icon: 'mdi-account-edit', color: 'info', description: 'Updated profile information' },
          { action: 'password_change', icon: 'mdi-lock-reset', color: 'warning', description: 'Changed password' },
          { action: 'view_product', icon: 'mdi-eye', color: 'grey', description: 'Viewed product details' },
          { action: 'create_order', icon: 'mdi-cart-plus', color: 'success', description: 'Created a new order' }
        ];

        // Generate some mock activity
        const mockActivity: ActivityLogEntry[] = [];
        const now = new Date();

        for (let i = 0; i < 10; i++) {
          const typeIndex = Math.floor(Math.random() * activityTypes.length);
          const type = activityTypes[typeIndex];
          const timestamp = new Date(now.getTime() - i * 3600000 * 24);

          mockActivity.push({
            id: `activity-${i}`,
            user_id: userId.value,
            action: type.action,
            description: type.description,
            timestamp: timestamp.toISOString(),
            icon: type.icon,
            color: type.color,
            metadata: {}
          });
        }

        // If first page, replace; otherwise append
        if (reset) {
          activityLog.value = mockActivity;
        } else {
          activityLog.value = [...activityLog.value, ...mockActivity];
        }

        // For demo, always show "load more" option
        hasMoreActivity.value = activityPage.value < 3;

      } catch (error) {
        console.error('Error fetching activity log:', error);
        notificationService.error('Failed to load activity log');
      } finally {
        activityLoading.value = false;
      }
    };

    // Load more activity log entries
    const loadMoreActivity = () => {
      activityPage.value++;
      fetchActivityLog(false);
    };

    // Refresh activity log
    const refreshActivityLog = () => {
      fetchActivityLog(true);
    };

    // Show delete confirmation dialog
    const confirmDelete = () => {
      if (!canDelete.value) return;
      deleteDialog.value = true;
    };

    // Delete user
    const deleteUser = async () => {
      deleteLoading.value = true;

      try {
        await userService.deleteUser(userId.value);
        deleteDialog.value = false;

        notificationService.success('User deleted successfully');

        // Redirect to user list
        router.push({ name: 'UserManagement' });
      } catch (error) {
        console.error('Error deleting user:', error);
        notificationService.error('Failed to delete user');
      } finally {
        deleteLoading.value = false;
      }
    };

    // Show toggle status confirmation dialog
    const confirmToggleStatus = () => {
      if (!canToggleUserStatus.value) return;
      statusDialog.value = true;
    };

    // Toggle user active status
    const toggleUserStatus = async () => {
      if (!user.value) return;

      statusLoading.value = true;

      try {
        // Update user status
        const updatedUser = await userService.updateUser(userId.value, {
          is_active: !user.value.is_active
        });

        // Update local state
        user.value = updatedUser;
        statusDialog.value = false;

        notificationService.success(
          user.value.is_active
            ? 'User activated successfully'
            : 'User deactivated successfully'
        );
      } catch (error) {
        console.error('Error updating user status:', error);
        notificationService.error('Failed to update user status');
      } finally {
        statusLoading.value = false;
      }
    };

    // Show password reset confirmation dialog
    const confirmPasswordReset = () => {
      if (!canSendPasswordReset.value) return;
      resetDialog.value = true;
    };

    // Send password reset email
    const sendPasswordReset = async () => {
      if (!user.value) return;

      resetLoading.value = true;

      try {
        await userService.sendPasswordReset(user.value.email);
        resetDialog.value = false;

        notificationService.success('Password reset email sent successfully');
      } catch (error) {
        console.error('Error sending password reset:', error);
        notificationService.error('Failed to send password reset');
      } finally {
        resetLoading.value = false;
      }
    };

    // Show impersonate user confirmation dialog
    const confirmImpersonateUser = () => {
      if (!canImpersonateUser.value) return;
      impersonateDialog.value = true;
    };

    // Impersonate user
    const impersonateUser = async () => {
      if (!user.value) return;

      impersonateLoading.value = true;

      try {
        // In a real implementation, this would call an API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        impersonateDialog.value = false;

        notificationService.success(`Now impersonating ${user.value.full_name}`);

        // Redirect to dashboard
        router.push({ name: 'Dashboard' });
      } catch (error) {
        console.error('Error impersonating user:', error);
        notificationService.error('Failed to impersonate user');
      } finally {
        impersonateLoading.value = false;
      }
    };

    // Initialize component
    onMounted(() => {
      fetchUser();
    });

    return {
      router,
      user,
      loading,
      userId,
      currentUser,
      isCurrentUser,
      isAdmin,
      canEdit,
      canDelete,
      canToggleUserStatus,
      canSendPasswordReset,
      canImpersonateUser,
      activityLog,
      activityLoading,
      hasMoreActivity,
      deleteDialog,
      deleteLoading,
      statusDialog,
      statusLoading,
      resetDialog,
      resetLoading,
      impersonateDialog,
      impersonateLoading,
      rolePermissions,
      formatDateTime,
      getRoleLabel,
      getRoleColor,
      refreshActivityLog,
      loadMoreActivity,
      confirmDelete,
      deleteUser,
      confirmToggleStatus,
      toggleUserStatus,
      confirmPasswordReset,
      sendPasswordReset,
      confirmImpersonateUser,
      impersonateUser
    };
  }
});
</script>
