<template>
  <div class="d-flex align-center justify-center" style="height: 70vh">
    <div class="text-center">
      <h1 class="text-h1">404</h1>
      <h2 class="text-h4 mb-6">Page Not Found</h2>
      <p class="mb-6">The page you are looking for doesn't exist or has been moved.</p>
      <v-btn color="primary" to="/">Go to Dashboard</v-btn>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'NotFound',
});
</script>
