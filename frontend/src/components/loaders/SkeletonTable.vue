<!-- src/components/loaders/SkeletonTable.vue (continued) -->
<template>
  <div class="skeleton-table" :class="containerClass">
    <v-card :elevation="elevation">
      <v-card-title v-if="showHeader">
        <v-skeleton-loader
          type="heading"
          :loading="true"
          width="60%"
        ></v-skeleton-loader>
        <v-spacer></v-spacer>
        <v-skeleton-loader
          type="button"
          :loading="true"
          width="120"
        ></v-skeleton-loader>
      </v-card-title>

      <v-divider v-if="showHeader"></v-divider>

      <div class="table-skeleton pa-4">
        <!-- Table header -->
        <div class="d-flex mb-4">
          <template v-for="(col, i) in columns" :key="i">
            <div :style="{ width: `${col.width || 100/columns.length}%` }" class="px-2">
              <v-skeleton-loader
                type="text"
                :loading="true"
              ></v-skeleton-loader>
            </div>
          </template>
        </div>

        <!-- Table rows -->
        <template v-for="row in rows" :key="row">
          <div class="d-flex mb-4">
            <template v-for="(col, i) in columns" :key="i">
              <div :style="{ width: `${col.width || 100/columns.length}%` }" class="px-2">
                <v-skeleton-loader
                  :type="col.type || 'text'"
                  :loading="true"
                ></v-skeleton-loader>
              </div>
            </template>
          </div>
        </template>
      </div>

      <!-- Pagination footer -->
      <v-divider v-if="showFooter"></v-divider>
      <v-card-actions v-if="showFooter" class="py-3">
        <v-skeleton-loader
          type="text"
          :loading="true"
          width="120"
        ></v-skeleton-loader>
        <v-spacer></v-spacer>
        <v-skeleton-loader
          type="button, button, button, button, button"
          :loading="true"
          class="d-flex"
        ></v-skeleton-loader>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script setup lang="ts">
interface Column {
  width?: number;
  type?: string;
}

const props = defineProps({
  columns: {
    type: Array as PropType<Column[]>,
    default: () => Array(4).fill({})
  },
  rows: {
    type: Number,
    default: 5,
  },
  showHeader: {
    type: Boolean,
    default: true,
  },
  showFooter: {
    type: Boolean,
    default: true,
  },
  elevation: {
    type: [Number, String],
    default: 1,
  },
  containerClass: {
    type: String,
    default: '',
  },
})
</script>

<style scoped>
.skeleton-table {
  width: 100%;
}
</style>
