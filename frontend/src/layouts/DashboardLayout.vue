<!-- src/layouts/DashboardLayout.vue (enhanced) -->
<template>
  <app-layout
    title="Crown Nexus"
    :has-navigation-drawer="true"
    app-bar-color="primary"
    drawer-color="surface"
  >
    <!-- App Bar -->
    <template #app-bar-prepend>
      <v-app-bar-nav-icon
        v-if="isMobile"
        @click="drawerOpen = !drawerOpen"
      ></v-app-bar-nav-icon>
      <v-btn
        to="/"
        variant="plain"
        class="text-h5 font-weight-bold text-white no-hover no-outline"
      >
        Crown Nexus
      </v-btn>
    </template>

    <template #app-bar-append>
      <v-btn to="/dashboard" text>Dashboard</v-btn>
      <v-btn to="/products" text>Products</v-btn>
      <v-btn to="/fitment/model-mappings" text>Mapper</v-btn>
      <v-btn to="/fitments" text>Fitments</v-btn>
      <v-btn to="/media" text>Media</v-btn>
      <v-btn to="/autocare/dashboard" text>Autocare</v-btn>

      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar size="36">
              <v-icon icon="mdi-account-circle"></v-icon>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/profile">
            <template v-slot:prepend>
              <v-icon icon="mdi-account"></v-icon>
            </template>
            <v-list-item-title>Profile</v-list-item-title>
          </v-list-item>
          <v-list-item to="/settings">
            <template v-slot:prepend>
              <v-icon icon="mdi-cog"></v-icon>
            </template>
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="logout">
            <template v-slot:prepend>
              <v-icon icon="mdi-logout"></v-icon>
            </template>
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>

    <!-- Navigation Drawer -->
    <template #navigation-drawer>
      <v-list>
        <v-list-item title="Dashboard" to="/dashboard" prepend-icon="mdi-view-dashboard"></v-list-item>

        <v-list-group value="products">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              title="Products"
              prepend-icon="mdi-package-variant-closed"
            ></v-list-item>
          </template>
          <v-list-item title="Browse Products" to="/products" prepend-icon="mdi-view-list"></v-list-item>
          <v-list-item title="Add Product" to="/products/new" prepend-icon="mdi-plus"></v-list-item>
        </v-list-group>

        <v-list-group value="fitments">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              title="Fitments"
              prepend-icon="mdi-car"
            ></v-list-item>
          </template>
          <v-list-item title="Browse Fitments" to="/fitments" prepend-icon="mdi-view-list"></v-list-item>
          <v-list-item title="Add Fitment" to="/fitments/new" prepend-icon="mdi-plus"></v-list-item>
          <v-list-item title="Model Mappings" to="/fitment/model-mappings" prepend-icon="mdi-map"></v-list-item>
        </v-list-group>

        <v-list-item title="Media Library" to="/media" prepend-icon="mdi-image-multiple"></v-list-item>

        <v-list-group value="autocare">
          <template v-slot:activator="{ props }">
            <v-list-item
              v-bind="props"
              title="Autocare"
              prepend-icon="mdi-car-cog"
            ></v-list-item>
          </template>
          <v-list-item title="Dashboard" to="/autocare/dashboard" prepend-icon="mdi-view-dashboard"></v-list-item>
          <v-list-item title="Vehicle Search" to="/vcdb/vehicles" prepend-icon="mdi-car-search"></v-list-item>
          <v-list-item title="Part Search" to="/pcdb/parts" prepend-icon="mdi-wrench"></v-list-item>
          <v-list-item title="Attribute Search" to="/padb/attributes" prepend-icon="mdi-format-list-bulleted"></v-list-item>
          <v-list-item title="Qualifier Search" to="/qdb/qualifiers" prepend-icon="mdi-filter"></v-list-item>
        </v-list-group>

        <v-divider class="my-3"></v-divider>

        <v-list-item title="User Management" to="/users" prepend-icon="mdi-account-group"></v-list-item>
        <v-list-item title="Settings" to="/settings" prepend-icon="mdi-cog"></v-list-item>
      </v-list>
    </template>

    <!-- Footer -->
    <template #footer>
      <dashboard-footer />
    </template>

    <!-- Main Content (default slot) -->
    <slot></slot>
  </app-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppLayout from '@/layouts/AppLayout.vue'
import DashboardFooter from './DashboardFooter.vue'

const authStore = useAuthStore()
const drawerOpen = ref(true)
const isMobile = ref(false)

// Handle window resize
const checkScreenSize = () => {
  isMobile.value = window.innerWidth < 960
  drawerOpen.value = !isMobile.value
}

// Initialize auth
const initializeAuth = async () => {
  if (authStore.isLoggedIn && !authStore.user) {
    await authStore.fetchUserProfile()
  }
}

// Logout function
const logout = () => {
  authStore.logout()
}

onMounted(() => {
  initializeAuth()
  checkScreenSize()
  window.addEventListener('resize', checkScreenSize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkScreenSize)
})
</script>
