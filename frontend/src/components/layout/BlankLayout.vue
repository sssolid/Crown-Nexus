// frontend/src/components/layout/BlankLayout.vue
<template>
  <v-app>
    <!-- Minimal navigation -->
    <div class="position-absolute top-0 start-0 mt-6 ms-6">
      <v-btn to="/" icon variant="text" size="large">
        <v-icon icon="mdi-arrow-left" size="large"></v-icon>
      </v-btn>
    </div>

    <v-main>
      <slot></slot>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'BlankLayout'
});
</script>
