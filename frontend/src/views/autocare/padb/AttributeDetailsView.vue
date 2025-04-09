<template>
  <div class="attribute-details-page">
    <PageHeader
      :title="pageTitle"
      :subtitle="pageSubtitle"
      icon="mdi-format-list-bulleted"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-btn color="primary" prepend-icon="mdi-arrow-left" to="/padb/attributes">
          Back to Search
        </v-btn>
      </template>
    </PageHeader>

    <AttributeDetails :attribute-id="attributeId" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { usePAdbStore } from '@/stores/autocare/padb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import AttributeDetails from '@/components/autocare/padb/AttributeDetails.vue';

// Route
const route = useRoute();

// Store
const padbStore = usePAdbStore();

// State
const loading = ref(false);
const error = ref('');

// Computed
const attributeId = computed(() => route.params.id as string);

const pageTitle = computed(() => {
  if (padbStore.currentAttribute) {
    return padbStore.currentAttribute.name || `Attribute ID: ${padbStore.currentAttribute.pa_id}`;
  }
  return 'Attribute Details';
});

const pageSubtitle = computed(() => {
  if (padbStore.currentAttribute) {
    return padbStore.currentAttribute.description || 'No description available';
  }
  return 'Loading attribute information...';
});

// Methods
const clearAttribute = () => {
  padbStore.clearAttribute();
};

// Lifecycle hooks
onMounted(() => {
  clearAttribute();
});

// Watch for changes to attribute ID
watch(() => route.params.id, () => {
  clearAttribute();
});
</script>

<style scoped>
.attribute-details-page {
  width: 100%;
}
</style>
