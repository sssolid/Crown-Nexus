<!-- frontend/src/views/NotFound.vue -->
<template>
  <div class="d-flex align-center justify-center" style="height: 80vh">
    <v-card class="text-center pa-6" max-width="500" elevation="3">
      <v-card-title class="text-h3 font-weight-bold mb-4">404</v-card-title>
      <v-card-subtitle class="text-h5 mb-4">Page Not Found</v-card-subtitle>

      <v-card-text>
        <v-img
          :src=notFound
          alt="Page not found"
          height="200"
          class="mb-4"
        ></v-img>

        <p class="text-body-1 mb-6">
          The page you are looking for might have been removed, had its name changed,
          or is temporarily unavailable.
        </p>

        <v-btn
          color="primary"
          size="large"
          variant="elevated"
          @click="goBack"
          class="mr-4"
        >
          <v-icon icon="mdi-arrow-left" start></v-icon>
          Go Back
        </v-btn>

        <v-btn
          color="secondary"
          size="large"
          to="/"
          variant="tonal"
        >
          <v-icon icon="mdi-home" start></v-icon>
          Home
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import notFound from '@/assets/status_notification/no_search_results.png';

const router = useRouter();

const goBack = () => {
  router.back();
};
</script>

<style scoped>
/* You could add custom styles here if needed */
</style>
