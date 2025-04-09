<template>
  <div class="page-header mb-4">
    <v-row align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold">
          <v-icon v-if="icon" :icon="icon" class="me-2"></v-icon>
          {{ title }}
        </h1>
        <div v-if="subtitle" class="text-subtitle-1 text-medium-emphasis">
          {{ subtitle }}
        </div>
      </v-col>
      <v-col cols="auto">
        <slot name="actions"></slot>
      </v-col>
    </v-row>
    <v-divider class="mt-2"></v-divider>

    <div v-if="loading" class="text-center my-4">
      <v-progress-linear indeterminate color="primary"></v-progress-linear>
    </div>

    <v-alert v-if="error" type="error" :text="error" variant="tonal" class="mt-4"></v-alert>
  </div>
</template>

<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '',
  },
  loading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.page-header {
  width: 100%;
}
</style>
