<template>
  <div class="part-details-page">
    <PageHeader
      :title="pageTitle"
      :subtitle="pageSubtitle"
      icon="mdi-wrench"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-btn color="primary" prepend-icon="mdi-arrow-left" to="/pcdb/parts">
          Back to Search
        </v-btn>
      </template>
    </PageHeader>

    <PartDetails :part-id="partId" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { usePCdbStore } from '@/stores/autocare/pcdb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import PartDetails from '@/components/autocare/pcdb/PartDetails.vue';

// Route
const route = useRoute();

// Store
const pcdbStore = usePCdbStore();

// State
const loading = ref(false);
const error = ref('');

// Computed
const partId = computed(() => route.params.id as string);

const pageTitle = computed(() => {
  if (pcdbStore.currentPart) {
    return pcdbStore.currentPart.part_terminology_name;
  }
  return 'Part Details';
});

const pageSubtitle = computed(() => {
  if (pcdbStore.currentPart) {
    return `Part ID: ${pcdbStore.currentPart.part_terminology_id}`;
  }
  return 'Loading part information...';
});

// Methods
const clearPart = () => {
  pcdbStore.clearPart();
};

// Lifecycle hooks
onMounted(() => {
  clearPart();
});

// Watch for changes to part ID
watch(() => route.params.id, () => {
  clearPart();
});
</script>

<style scoped>
.part-details-page {
  width: 100%;
}
</style>
