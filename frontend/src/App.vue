<!-- src/App.vue (improved) -->
<template>
  <component :is="layout">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </component>

  <!-- Global notification system -->
  <notification-system />
</template>

<script setup lang="ts">
import { computed, markRaw, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PublicLayout from '@/layouts/PublicLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import BlankLayout from '@/layouts/BlankLayout.vue'
import AppLayout from '@/layouts/AppLayout.vue'
import NotificationSystem from '@/components/notifications/NotificationSystem.vue'

const route = useRoute()
const authStore = useAuthStore()

// Determine layout based on route meta
const layout = computed(() => {
  if (route.meta.layout === 'blank') {
    return markRaw(BlankLayout)
  }

  if (route.meta.layout === 'app') {
    return markRaw(AppLayout)
  }

  if (route.meta.requiresAuth && authStore.isLoggedIn) {
    return markRaw(DashboardLayout)
  }

  return markRaw(PublicLayout)
})

// Initialize auth if user is logged in
onMounted(() => {
  if (authStore.isLoggedIn && !authStore.user) {
    authStore.fetchUserProfile()
  }
})
</script>

<style>
/* Global styles */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Remove outline on focused elements except for keyboard users */
:focus:not(:focus-visible) {
  outline: none;
}

.no-hover:hover {
  background-color: transparent !important;
}

.no-outline {
  outline: none !important;
}
</style>
