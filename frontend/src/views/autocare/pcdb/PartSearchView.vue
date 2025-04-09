<template>
  <div class="part-search-page">
    <PageHeader
      title="Part Search"
      subtitle="Search for parts by name, category, or description"
      icon="mdi-wrench"
    >
      <template v-slot:actions>
        <v-btn
          color="primary"
          prepend-icon="mdi-refresh"
          @click="refreshData"
          :loading="loading"
        >
          Refresh
        </v-btn>
      </template>
    </PageHeader>

    <PartSearch />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePCdbStore } from '@/stores/autocare/pcdb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import PartSearch from '@/components/autocare/pcdb/PartSearch.vue';

// Store
const pcdbStore = usePCdbStore();

// State
const loading = ref(false);

// Methods
const refreshData = async () => {
  loading.value = true;
  await pcdbStore.fetchCategories();
  loading.value = false;
};

// Load initial data
onMounted(() => {
  // Data is loaded in the PartSearch component
});
</script>

<style scoped>
.part-search-page {
  width: 100%;
}
</style>
