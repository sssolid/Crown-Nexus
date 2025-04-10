<!-- frontend/src/views/UserProfile.vue -->
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

      <template v-else>
        <!-- Page Header -->
        <v-row class="mb-6">
          <v-col cols="12">
            <h1 class="text-h3 font-weight-bold">User Profile</h1>
            <p class="text-subtitle-1">Manage your account settings and preferences</p>
          </v-col>
        </v-row>

        <!-- Profile Content -->
        <v-row>
          <!-- Main Content Column -->
          <v-col cols="12" md="8">
            <!-- Personal Information Card -->
            <v-card class="mb-6">
              <v-card-title class="d-flex align-center">
                Personal Information
                <v-spacer></v-spacer>
                <v-btn
                  v-if="!editingProfile"
                  color="primary"
                  variant="text"
                  prepend-icon="mdi-pencil"
                  @click="startEditingProfile"
                >
                  Edit
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>

              <!-- View Mode -->
              <v-card-text v-if="!editingProfile">
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

                  <v-list-item v-if="user.last_login">
                    <template v-slot:prepend>
                      <v-icon icon="mdi-login" class="mr-2"></v-icon>
                    </template>
                    <v-list-item-title>Last Login</v-list-item-title>
                    <v-list-item-subtitle>{{ formatDateTime(user.last_login) }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>

              <!-- Edit Mode -->
              <v-card-text v-else>
                <v-form ref="profileFormRef" @submit.prevent="updateProfile" v-model="isProfileFormValid">
                  <v-row>
                    <!-- Full Name -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="profileForm.full_name"
                        label="Full Name"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="profileErrors.full_name"
                        @input="clearProfileError('full_name')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Email -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="profileForm.email"
                        label="Email Address"
                        type="email"
                        variant="outlined"
                        :rules="[rules.required, rules.email]"
                        :error-messages="profileErrors.email"
                        @input="clearProfileError('email')"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <!-- Error Message -->
                  <v-alert
                    v-if="profileFormError"
                    type="error"
                    variant="tonal"
                    class="mt-4 mb-4"
                    closable
                    @click:close="profileFormError = ''"
                  >
                    {{ profileFormError }}
                  </v-alert>
                </v-form>
              </v-card-text>

              <!-- Edit Mode Actions -->
              <v-card-actions v-if="editingProfile" class="pa-4">
                <v-spacer></v-spacer>
                <v-btn
                  variant="text"
                  color="secondary"
                  @click="cancelEditingProfile"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="primary"
                  @click="updateProfile"
                  :loading="updatingProfile"
                  :disabled="!isProfileFormValid"
                >
                  Save Changes
                </v-btn>
              </v-card-actions>
            </v-card>

            <!-- Change Password Card -->
            <v-card class="mb-6">
              <v-card-title class="d-flex align-center">
                Change Password
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-form ref="passwordFormRef" @submit.prevent="changePassword" v-model="isPasswordFormValid">
                  <v-row>
                    <!-- Current Password -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="passwordForm.current_password"
                        label="Current Password"
                        :type="showCurrentPassword ? 'text' : 'password'"
                        :append-inner-icon="showCurrentPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="showCurrentPassword = !showCurrentPassword"
                        variant="outlined"
                        :rules="[rules.required]"
                        :error-messages="passwordErrors.current_password"
                        @input="clearPasswordError('current_password')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- New Password -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="passwordForm.new_password"
                        label="New Password"
                        :type="showNewPassword ? 'text' : 'password'"
                        :append-inner-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="showNewPassword = !showNewPassword"
                        variant="outlined"
                        :rules="[rules.required, rules.passwordLength, rules.passwordComplexity]"
                        :error-messages="passwordErrors.new_password"
                        @input="clearPasswordError('new_password')"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Confirm New Password -->
                    <v-col cols="12">
                      <v-text-field
                        v-model="passwordForm.confirm_password"
                        label="Confirm New Password"
                        :type="showNewPassword ? 'text' : 'password'"
                        variant="outlined"
                        :rules="[rules.required, rules.passwordMatch]"
                        :error-messages="passwordErrors.confirm_password"
                        @input="clearPasswordError('confirm_password')"
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>

                  <!-- Error Message -->
                  <v-alert
                    v-if="passwordFormError"
                    type="error"
                    variant="tonal"
                    class="mt-4 mb-4"
                    closable
                    @click:close="passwordFormError = ''"
                  >
                    {{ passwordFormError }}
                  </v-alert>
                </v-form>
              </v-card-text>
              <v-card-actions class="pa-4">
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  @click="changePassword"
                  :loading="updatingPassword"
                  :disabled="!isPasswordFormValid"
                >
                  Change Password
                </v-btn>
              </v-card-actions>
            </v-card>

            <!-- Preferences Card -->
            <v-card>
              <v-card-title class="d-flex align-center">
                Application Preferences
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <!-- Theme Preference -->
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="preferences.theme"
                      label="Theme"
                      variant="outlined"
                      :items="[
                        { title: 'Light', value: 'light' },
                        { title: 'Dark', value: 'dark' },
                        { title: 'System Default', value: 'system' }
                      ]"
                      item-title="title"
                      item-value="value"
                      @update:modelValue="updatePreferences"
                    ></v-select>
                  </v-col>

                  <!-- Language Preference -->
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="preferences.language"
                      label="Language"
                      variant="outlined"
                      :items="[
                        { title: 'English', value: 'en' },
                        { title: 'Spanish', value: 'es' },
                        { title: 'French', value: 'fr' }
                      ]"
                      item-title="title"
                      item-value="value"
                      @update:modelValue="updatePreferences"
                    ></v-select>
                  </v-col>

                  <!-- Timezone Preference -->
                  <v-col cols="12" sm="6">
                    <v-select
                      v-model="preferences.timezone"
                      label="Timezone"
                      variant="outlined"
                      :items="timezoneOptions"
                      @update:modelValue="updatePreferences"
                    ></v-select>
                  </v-col>

                  <!-- Notification Preference -->
                  <v-col cols="12" sm="6">
                    <v-switch
                      v-model="preferences.notifications_enabled"
                      label="Enable Notifications"
                      color="primary"
                      inset
                      @update:modelValue="updatePreferences"
                    ></v-switch>
                  </v-col>

                  <!-- Dashboard Widgets -->
                  <v-col cols="12">
                    <p class="text-subtitle-1 mb-2">Dashboard Widgets</p>
                    <v-chip-group
                      v-model="preferences.dashboard_widgets"
                      column
                      multiple
                      @update:modelValue="updatePreferences"
                    >
                      <v-chip filter value="recent_activity">Recent Activity</v-chip>
                      <v-chip filter value="product_stats">Product Statistics</v-chip>
                      <v-chip filter value="fitment_stats">Fitment Statistics</v-chip>
                      <v-chip filter value="quick_actions">Quick Actions</v-chip>
                    </v-chip-group>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Sidebar Column -->
          <v-col cols="12" md="4">
            <!-- Account Security Card -->
            <v-card class="mb-6">
              <v-card-title>Account Security</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list>
                  <v-list-item prepend-icon="mdi-shield-account">
                    <v-list-item-title>Two-Factor Authentication</v-list-item-title>
                    <v-list-item-subtitle>
                      <div class="d-flex align-center">
                        <v-chip
                          :color="twoFactorEnabled ? 'success' : 'error'"
                          size="small"
                          variant="tonal"
                          class="mr-2"
                        >
                          {{ twoFactorEnabled ? 'Enabled' : 'Disabled' }}
                        </v-chip>
                        <v-btn
                          variant="text"
                          size="small"
                          color="primary"
                          @click="showTwoFactorDialog = true"
                        >
                          {{ twoFactorEnabled ? 'Manage' : 'Enable' }}
                        </v-btn>
                      </div>
                    </v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item prepend-icon="mdi-lock-check">
                    <v-list-item-title>Password Last Changed</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ formatDate(passwordLastChanged) }}
                    </v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item prepend-icon="mdi-history">
                    <v-list-item-title>Recent Login Activity</v-list-item-title>
                    <v-list-item-subtitle>
                      <v-btn
                        variant="text"
                        size="small"
                        color="primary"
                        @click="showActivityDialog = true"
                      >
                        View Activity
                      </v-btn>
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <!-- API Access Card -->
            <v-card>
              <v-card-title class="d-flex align-center">
                API Access
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  variant="text"
                  size="small"
                  prepend-icon="mdi-key-plus"
                  @click="showApiKeyDialog = true"
                >
                  Generate Key
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <div v-if="apiKeys.length > 0">
                  <v-list>
                    <v-list-item
                      v-for="key in apiKeys"
                      :key="key.id"
                    >
                      <template v-slot:prepend>
                        <v-icon :color="key.active ? 'success' : 'error'">mdi-key</v-icon>
                      </template>
                      <v-list-item-title>{{ key.name }}</v-list-item-title>
                      <v-list-item-subtitle>
                        Created: {{ formatDate(key.created_at) }}
                      </v-list-item-subtitle>
                      <template v-slot:append>
                        <v-btn
                          icon
                          variant="text"
                          size="small"
                          color="error"
                          @click="confirmRevokeKey(key)"
                        >
                          <v-icon>mdi-delete</v-icon>
                        </v-btn>
                      </template>
                    </v-list-item>
                  </v-list>
                </div>
                <div v-else class="text-center py-4">
                  <v-icon icon="mdi-key-remove" size="large" class="mb-2"></v-icon>
                  <p>No API keys found. Generate a key to access the API.</p>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Two-Factor Authentication Dialog -->
        <v-dialog v-model="showTwoFactorDialog" max-width="600">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              {{ twoFactorEnabled ? 'Manage Two-Factor Authentication' : 'Enable Two-Factor Authentication' }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <div v-if="!twoFactorEnabled">
                <p class="mb-4">
                  Two-factor authentication adds an extra layer of security to your account. In addition to your password,
                  you'll need to enter a code from your mobile device when logging in.
                </p>

                <v-row>
                  <v-col cols="12" md="6">
                    <v-card variant="outlined" class="pa-4 text-center mb-4">
                      <v-img
                        src="https://via.placeholder.com/200x200?text=QR+Code"
                        width="200"
                        height="200"
                        class="mx-auto mb-2"
                      ></v-img>
                      <p class="text-caption">Scan with authenticator app</p>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6">
                    <p class="mb-2">Or enter the code manually:</p>
                    <v-text-field
                      value="ABCD-EFGH-IJKL-MNOP"
                      variant="outlined"
                      readonly
                      class="mb-4"
                    ></v-text-field>

                    <p class="mb-2">Enter verification code from your authenticator app:</p>
                    <v-text-field
                      v-model="twoFactorCode"
                      variant="outlined"
                      placeholder="123456"
                      type="number"
                      :rules="[rules.required, rules.sixDigits]"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </div>

              <div v-else>
                <p class="mb-4">
                  Two-factor authentication is currently enabled for your account.
                </p>

                <v-alert
                  type="info"
                  variant="tonal"
                  class="mb-4"
                >
                  If you disable two-factor authentication, your account will be less secure.
                </v-alert>

                <v-card variant="outlined" class="pa-4 mb-4">
                  <p class="font-weight-bold mb-2">Recovery Codes</p>
                  <p class="text-caption mb-2">
                    Save these recovery codes in a secure location. You can use these codes to access your account if
                    you lose your device.
                  </p>
                  <v-textarea
                    value="ABCD-1234-EFGH-5678\nIJKL-9012-MNOP-3456"
                    variant="outlined"
                    readonly
                    rows="2"
                    class="mb-2"
                  ></v-textarea>
                  <div class="d-flex justify-end">
                    <v-btn
                      variant="text"
                      color="primary"
                      size="small"
                      prepend-icon="mdi-content-copy"
                    >
                      Copy
                    </v-btn>
                    <v-btn
                      variant="text"
                      color="primary"
                      size="small"
                      prepend-icon="mdi-refresh"
                    >
                      Regenerate
                    </v-btn>
                  </div>
                </v-card>

                <div>
                  <p class="mb-2">To disable two-factor authentication, enter your password:</p>
                  <v-text-field
                    v-model="disableTwoFactorPassword"
                    variant="outlined"
                    type="password"
                    :rules="[rules.required]"
                  ></v-text-field>
                </div>
              </div>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showTwoFactorDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                v-if="!twoFactorEnabled"
                color="primary"
                @click="enableTwoFactor"
                :loading="twoFactorLoading"
                :disabled="!twoFactorCode"
              >
                Enable
              </v-btn>
              <v-btn
                v-else
                color="error"
                @click="disableTwoFactor"
                :loading="twoFactorLoading"
                :disabled="!disableTwoFactorPassword"
              >
                Disable
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Login Activity Dialog -->
        <v-dialog v-model="showActivityDialog" max-width="700">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Recent Login Activity
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
              <v-table>
                <thead>
                <tr>
                  <th class="text-left">Date & Time</th>
                  <th class="text-left">IP Address</th>
                  <th class="text-left">Device / Browser</th>
                  <th class="text-left">Status</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(activity, index) in loginActivity" :key="index">
                  <td>{{ formatDateTime(activity.timestamp) }}</td>
                  <td>{{ activity.ip_address }}</td>
                  <td>{{ activity.user_agent }}</td>
                  <td>
                    <v-chip
                      :color="activity.status === 'success' ? 'success' : 'error'"
                      size="small"
                      variant="tonal"
                    >
                      {{ activity.status === 'success' ? 'Success' : 'Failed' }}
                    </v-chip>
                  </td>
                </tr>
                </tbody>
              </v-table>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="tonal"
                @click="showActivityDialog = false"
              >
                Close
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- API Key Dialog -->
        <v-dialog v-model="showApiKeyDialog" max-width="600">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Generate New API Key
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <p class="mb-4">
                API keys allow programmatic access to the Crown Nexus API. Please store your API key securely - it will
                only be shown once after generation.
              </p>

              <v-form ref="apiKeyFormRef" @submit.prevent="generateApiKey" v-model="isApiKeyFormValid">
                <v-text-field
                  v-model="apiKeyForm.name"
                  label="API Key Name"
                  variant="outlined"
                  :rules="[rules.required]"
                  placeholder="My Application"
                  hint="A descriptive name for this API key"
                  persistent-hint
                ></v-text-field>

                <v-select
                  v-model="apiKeyForm.expiration"
                  label="Expiration"
                  variant="outlined"
                  :items="[
                    { title: 'Never', value: 'never' },
                    { title: '30 days', value: '30d' },
                    { title: '90 days', value: '90d' },
                    { title: '1 year', value: '1y' }
                  ]"
                  item-title="title"
                  item-value="value"
                  class="mt-4"
                ></v-select>
              </v-form>

              <v-alert
                v-if="newApiKey"
                type="success"
                variant="tonal"
                class="mt-4"
              >
                <p class="font-weight-bold">Your API key has been generated:</p>
                <v-text-field
                  :value="newApiKey"
                  variant="outlined"
                  readonly
                  class="mt-2"
                  append-inner-icon="mdi-content-copy"
                  @click:append-inner="copyApiKey"
                ></v-text-field>
                <p class="text-caption">This key will only be shown once. Make sure to copy it now.</p>
              </v-alert>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="cancelApiKeyDialog"
              >
                {{ newApiKey ? 'Close' : 'Cancel' }}
              </v-btn>
              <v-btn
                v-if="!newApiKey"
                color="primary"
                @click="generateApiKey"
                :loading="apiKeyLoading"
                :disabled="!isApiKeyFormValid"
              >
                Generate Key
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Revoke API Key Dialog -->
        <v-dialog v-model="showRevokeKeyDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-error text-white pa-4">
              Revoke API Key
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>
                Are you sure you want to revoke the API key <strong>{{ keyToRevoke?.name }}</strong>?
              </p>
              <p class="text-medium-emphasis mt-2">
                This action cannot be undone. Any applications using this key will no longer be able to access
                the API.
              </p>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showRevokeKeyDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="error"
                @click="revokeApiKey"
                :loading="revokeKeyLoading"
              >
                Revoke Key
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import userService from '@/services/user';
import { User, UserRole } from '@/types/user';
import { formatDate, formatDateTime } from '@/utils/formatters';
import { notificationService } from '@/utils/notifications';
import { parseValidationErrors } from '@/utils/error-handler';

// API Key interface
interface ApiKey {
  id: string;
  name: string;
  active: boolean;
  created_at: string;
  expires_at?: string;
}

// Login Activity interface
interface LoginActivity {
  timestamp: string;
  ip_address: string;
  user_agent: string;
  status: 'success' | 'failed';
}

export default defineComponent({
  name: 'UserProfile',

  setup() {
    const authStore = useAuthStore();

    // Form references
    const profileFormRef = ref<any>(null);
    const passwordFormRef = ref<any>(null);
    const apiKeyFormRef = ref<any>(null);

    // Form validation states
    const isProfileFormValid = ref(false);
    const isPasswordFormValid = ref(false);
    const isApiKeyFormValid = ref(false);

    // Loading states
    const loading = ref(true);
    const updatingProfile = ref(false);
    const updatingPassword = ref(false);
    const updatingPreferences = ref(false);
    const twoFactorLoading = ref(false);
    const apiKeyLoading = ref(false);
    const revokeKeyLoading = ref(false);

    // Dialog states
    const editingProfile = ref(false);
    const showTwoFactorDialog = ref(false);
    const showActivityDialog = ref(false);
    const showApiKeyDialog = ref(false);
    const showRevokeKeyDialog = ref(false);

    // User data
    const user = computed(() => authStore.user || {} as User);

    // Form errors
    const profileFormError = ref('');
    const profileErrors = ref<Record<string, string>>({});
    const passwordFormError = ref('');
    const passwordErrors = ref<Record<string, string>>({});

    // Profile form
    const profileForm = ref({
      full_name: '',
      email: ''
    });

    // Password form
    const passwordForm = ref({
      current_password: '',
      new_password: '',
      confirm_password: ''
    });

    // Password visibility toggles
    const showCurrentPassword = ref(false);
    const showNewPassword = ref(false);

    // Two-factor auth
    const twoFactorEnabled = ref(false);
    const twoFactorCode = ref('');
    const disableTwoFactorPassword = ref('');

    // API keys
    const apiKeys = ref<ApiKey[]>([]);
    const apiKeyForm = ref({
      name: '',
      expiration: '90d'
    });
    const newApiKey = ref('');
    const keyToRevoke = ref<ApiKey | null>(null);

    // User preferences
    const preferences = ref({
      theme: 'light' as 'light' | 'dark' | 'system',
      language: 'en',
      timezone: 'America/New_York',
      notifications_enabled: true,
      dashboard_widgets: ['recent_activity', 'product_stats', 'quick_actions']
    });

    // Mock data
    const passwordLastChanged = ref(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)); // 30 days ago

    // Login activity
    const loginActivity = ref<LoginActivity[]>([
      {
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(), // 1 hour ago
        ip_address: '192.168.1.1',
        user_agent: 'Chrome / Windows',
        status: 'success'
      },
      {
        timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
        ip_address: '192.168.1.1',
        user_agent: 'Firefox / Mac',
        status: 'success'
      },
      {
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
        ip_address: '192.168.1.100',
        user_agent: 'Unknown / Unknown',
        status: 'failed'
      }
    ]);

    // Timezone options
    const timezoneOptions = [
      'America/New_York',
      'America/Chicago',
      'America/Denver',
      'America/Los_Angeles',
      'Europe/London',
      'Europe/Paris',
      'Asia/Tokyo',
      'Asia/Singapore',
      'Australia/Sydney',
      'Pacific/Auckland'
    ];

    // Form validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required',
      email: (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      passwordMatch: (v: string) => v === passwordForm.value.new_password || 'Passwords do not match',
      passwordLength: (v: string) => v.length >= 8 || 'Password must be at least 8 characters',
      passwordComplexity: (v: string) => {
        // At least one uppercase, one lowercase, one number
        const hasUppercase = /[A-Z]/.test(v);
        const hasLowercase = /[a-z]/.test(v);
        const hasNumber = /[0-9]/.test(v);

        return (hasUppercase && hasLowercase && hasNumber) || 'Password must include uppercase, lowercase, and numbers';
      },
      sixDigits: (v: string) => /^\d{6}$/.test(v) || 'Code must be 6 digits'
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

    // Start editing profile
    const startEditingProfile = () => {
      profileForm.value.full_name = user.value.full_name;
      profileForm.value.email = user.value.email;
      editingProfile.value = true;
    };

    // Cancel editing profile
    const cancelEditingProfile = () => {
      editingProfile.value = false;
      profileFormError.value = '';
      profileErrors.value = {};
    };

    // Clear profile form error
    const clearProfileError = (field: string) => {
      if (profileErrors.value[field]) {
        delete profileErrors.value[field];
      }
    };

    // Clear password form error
    const clearPasswordError = (field: string) => {
      if (passwordErrors.value[field]) {
        delete passwordErrors.value[field];
      }
    };

    // Update profile
    const updateProfile = async () => {
      // Validate form
      const validation = await profileFormRef.value?.validate();

      if (!validation.valid) {
        profileFormError.value = 'Please correct the errors in the form';
        return;
      }

      updatingProfile.value = true;
      profileFormError.value = '';
      profileErrors.value = {};

      try {
        // Update user profile
        const updatedUser = await userService.updateUser(user.value.id, {
          full_name: profileForm.value.full_name,
          email: profileForm.value.email
        });

        // Update user in auth store
        await authStore.fetchUserProfile();

        editingProfile.value = false;

        notificationService.success('Profile updated successfully');
      } catch (error: any) {
        console.error('Error updating profile:', error);

        // Handle validation errors
        if (error.response?.status === 422) {
          profileErrors.value = parseValidationErrors(error);
          profileFormError.value = 'Please correct the validation errors';
        } else {
          profileFormError.value = error.response?.data?.detail || 'Failed to update profile';
        }
      } finally {
        updatingProfile.value = false;
      }
    };

    // Change password
    const changePassword = async () => {
      // Validate form
      const validation = await passwordFormRef.value?.validate();

      if (!validation.valid) {
        passwordFormError.value = 'Please correct the errors in the form';
        return;
      }

      updatingPassword.value = true;
      passwordFormError.value = '';
      passwordErrors.value = {};

      try {
        // Change password
        await userService.changePassword(
          user.value.id,
          passwordForm.value.current_password,
          passwordForm.value.new_password
        );

        // Reset form
        passwordForm.value = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        };

        // Update last changed date
        passwordLastChanged.value = new Date();

        notificationService.success('Password changed successfully');
      } catch (error: any) {
        console.error('Error changing password:', error);

        // Handle validation errors
        if (error.response?.status === 422) {
          passwordErrors.value = parseValidationErrors(error);
          passwordFormError.value = 'Please correct the validation errors';
        } else {
          const errorMessage = error.response?.data?.detail || 'Failed to change password';

          // Check for current password validation error
          if (errorMessage.toLowerCase().includes('current password')) {
            passwordErrors.value.current_password = errorMessage;
          } else {
            passwordFormError.value = errorMessage;
          }
        }
      } finally {
        updatingPassword.value = false;
      }
    };

    // Update preferences
    const updatePreferences = async () => {
      updatingPreferences.value = true;

      try {
        // Update user preferences
        await userService.updateUserPreferences(user.value.id, preferences.value);

        // Apply theme if changed
        if (preferences.value.theme !== 'system') {
          // This would be handled by a theme service in a real app
          document.documentElement.setAttribute('data-theme', preferences.value.theme);
        }

        notificationService.success('Preferences updated');
      } catch (error) {
        console.error('Error updating preferences:', error);
        notificationService.error('Failed to update preferences');
      } finally {
        updatingPreferences.value = false;
      }
    };

    // Enable two-factor authentication
    const enableTwoFactor = async () => {
      twoFactorLoading.value = true;

      try {
        // In a real implementation, this would call an API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        twoFactorEnabled.value = true;
        showTwoFactorDialog.value = false;
        twoFactorCode.value = '';

        notificationService.success('Two-factor authentication enabled successfully');
      } catch (error) {
        console.error('Error enabling two-factor auth:', error);
        notificationService.error('Failed to enable two-factor authentication');
      } finally {
        twoFactorLoading.value = false;
      }
    };

    // Disable two-factor authentication
    const disableTwoFactor = async () => {
      twoFactorLoading.value = true;

      try {
        // In a real implementation, this would call an API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        twoFactorEnabled.value = false;
        showTwoFactorDialog.value = false;
        disableTwoFactorPassword.value = '';

        notificationService.success('Two-factor authentication disabled');
      } catch (error) {
        console.error('Error disabling two-factor auth:', error);
        notificationService.error('Failed to disable two-factor authentication');
      } finally {
        twoFactorLoading.value = false;
      }
    };

    // Generate API key
    const generateApiKey = async () => {
      // Validate form
      const validation = await apiKeyFormRef.value?.validate();

      if (!validation.valid) {
        return;
      }

      apiKeyLoading.value = true;

      try {
        // In a real implementation, this would call an API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Generate mock API key
        const keyParts = [];
        for (let i = 0; i < 4; i++) {
          keyParts.push(Math.random().toString(36).substring(2, 10).toUpperCase());
        }
        newApiKey.value = keyParts.join('.');

        // Add key to list
        const now = new Date();
        let expiresAt: Date | undefined;

        if (apiKeyForm.value.expiration === '30d') {
          expiresAt = new Date(now.getTime() + 30 * 24 * 60 * 60 * 1000);
        } else if (apiKeyForm.value.expiration === '90d') {
          expiresAt = new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000);
        } else if (apiKeyForm.value.expiration === '1y') {
          expiresAt = new Date(now.getTime() + 365 * 24 * 60 * 60 * 1000);
        }

        apiKeys.value.push({
          id: Math.random().toString(36).substring(2, 15),
          name: apiKeyForm.value.name,
          active: true,
          created_at: now.toISOString(),
          expires_at: expiresAt?.toISOString()
        });
      } catch (error) {
        console.error('Error generating API key:', error);
        notificationService.error('Failed to generate API key');
      } finally {
        apiKeyLoading.value = false;
      }
    };

    // Cancel API key dialog
    const cancelApiKeyDialog = () => {
      showApiKeyDialog.value = false;
      newApiKey.value = '';
      apiKeyForm.value = {
        name: '',
        expiration: '90d'
      };
    };

    // Copy API key to clipboard
    const copyApiKey = () => {
      navigator.clipboard.writeText(newApiKey.value);
      notificationService.success('API key copied to clipboard');
    };

    // Confirm revoke API key
    const confirmRevokeKey = (key: ApiKey) => {
      keyToRevoke.value = key;
      showRevokeKeyDialog.value = true;
    };

    // Revoke API key
    const revokeApiKey = async () => {
      if (!keyToRevoke.value) return;

      revokeKeyLoading.value = true;

      try {
        // In a real implementation, this would call an API endpoint
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Remove key from list
        apiKeys.value = apiKeys.value.filter(key => key.id !== keyToRevoke.value?.id);

        showRevokeKeyDialog.value = false;
        keyToRevoke.value = null;

        notificationService.success('API key revoked successfully');
      } catch (error) {
        console.error('Error revoking API key:', error);
        notificationService.error('Failed to revoke API key');
      } finally {
        revokeKeyLoading.value = false;
      }
    };

    // Initialize component
    onMounted(async () => {
      loading.value = true;

      try {
        // Fetch user preferences
        const userPreferences = await userService.getUserPreferences(user.value.id);

        // Update preferences
        preferences.value = {
          ...preferences.value,
          ...userPreferences
        };

        // Fetch API keys (mock data for now)
        apiKeys.value = [
          {
            id: 'key1',
            name: 'Development API',
            active: true,
            created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days ago
            expires_at: new Date(Date.now() + 60 * 24 * 60 * 60 * 1000).toISOString() // 60 days in future
          }
        ];
      } catch (error) {
        console.error('Error loading profile data:', error);
        notificationService.error('Failed to load profile data');
      } finally {
        loading.value = false;
      }
    });

    return {
      user,
      loading,
      profileFormRef,
      passwordFormRef,
      apiKeyFormRef,
      isProfileFormValid,
      isPasswordFormValid,
      isApiKeyFormValid,
      editingProfile,
      updatingProfile,
      updatingPassword,
      updatingPreferences,
      profileFormError,
      profileErrors,
      passwordFormError,
      passwordErrors,
      profileForm,
      passwordForm,
      showCurrentPassword,
      showNewPassword,
      preferences,
      timezoneOptions,
      twoFactorEnabled,
      twoFactorCode,
      disableTwoFactorPassword,
      showTwoFactorDialog,
      twoFactorLoading,
      passwordLastChanged,
      loginActivity,
      showActivityDialog,
      apiKeys,
      apiKeyForm,
      newApiKey,
      showApiKeyDialog,
      showRevokeKeyDialog,
      keyToRevoke,
      apiKeyLoading,
      revokeKeyLoading,
      rules,
      formatDate,
      formatDateTime,
      getRoleLabel,
      getRoleColor,
      startEditingProfile,
      cancelEditingProfile,
      clearProfileError,
      clearPasswordError,
      updateProfile,
      changePassword,
      updatePreferences,
      enableTwoFactor,
      disableTwoFactor,
      generateApiKey,
      cancelApiKeyDialog,
      copyApiKey,
      confirmRevokeKey,
      revokeApiKey
    };
  }
});
</script>
