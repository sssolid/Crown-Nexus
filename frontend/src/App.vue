// frontend/src/App.vue
<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script lang="ts">
import { defineComponent, computed, markRaw, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Import layouts
import PublicLayout from '@/components/layout/PublicLayout.vue';
import DashboardLayout from '@/components/layout/DashboardLayout.vue';
import BlankLayout from '@/components/layout/BlankLayout.vue';

export default defineComponent({
  name: 'App',
  components: {
    PublicLayout,
    DashboardLayout,
    BlankLayout
  },
  setup() {
    const route = useRoute();
    const authStore = useAuthStore();

    // Determine which layout to use based on route meta and auth state
    const layout = computed(() => {
      // If route specifies 'blank' layout
      if (route.meta.layout === 'blank') {
        return markRaw(BlankLayout);
      }

      // For authenticated routes, use dashboard layout
      if (route.meta.requiresAuth && authStore.isLoggedIn) {
        return markRaw(DashboardLayout);
      }

      // Default to public layout for non-authenticated routes
      return markRaw(PublicLayout);
    });

    // Initialize user profile if token exists
    onMounted(() => {
      if (authStore.isLoggedIn && !authStore.user) {
        authStore.fetchUserProfile();
      }
    });

    return {
      layout
    };
  }
});
</script>
