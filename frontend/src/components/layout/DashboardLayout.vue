// frontend/src/components/layout/DashboardLayout.vue
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn
        to="/"
        variant="plain"
        class="text-h5 font-weight-bold text-white no-hover no-outline"
      >
        Crown Nexus
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn to="/dashboard" text>Dashboard</v-btn>
      <v-btn to="/products" text>Products</v-btn>
      <v-btn to="/fitment/model-mappings" text>Mapper</v-btn>
      <v-btn to="/fitments" text>Fitments</v-btn>
      <v-btn to="/media" text>Media</v-btn>
      <v-btn to="/settings" text>Settings</v-btn>
      <v-btn to="/profile" text>Profile</v-btn>
      <v-btn @click="logout" text>Logout</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <slot></slot>
      </v-container>
    </v-main>

    <dashboard-footer />
  </v-app>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import DashboardFooter from './DashboardFooter.vue';

export default defineComponent({
  name: 'DashboardLayout',
  components: {
    DashboardFooter
  },
  setup() {
    const authStore = useAuthStore();

    const logout = () => {
      authStore.logout();
    };

    // Add initialization for user profile
    const initializeAuth = async () => {
      if (authStore.isLoggedIn && !authStore.user) {
        await authStore.fetchUserProfile();
      }
    };

    // Call initialization when component is mounted
    onMounted(initializeAuth);

    return {
      logout
    };
  },
});
</script>
