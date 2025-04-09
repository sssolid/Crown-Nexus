<template>
  <div class="attribute-search-page">
    <PageHeader
      title="Part Attribute Search"
      subtitle="Search for part attributes by name or description"
      icon="mdi-format-list-bulleted"
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

    <AttributeSearch />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { usePAdbStore } from '@/stores/autocare/padb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import AttributeSearch from '@/components/autocare/padb/AttributeSearch.vue';

// Store
const padbStore = usePAdbStore();

// State
const loading = ref(false);

// Methods
const refreshData = async () => {
  loading.value = true;
  // Refresh any data needed for the attribute search
  // For example, measurement groups if you had them in your store
  loading.value = false;
};

// No initial data loading needed here, handled by the AttributeSearch component
</script>

<style scoped>
.attribute-search-page {
  width: 100%;
}
</style>
