<template>
  <div class="categories-list-page">
    <PageHeader
      title="Part Categories"
      subtitle="Browse all part categories in the database"
      icon="mdi-folder"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search Categories"
          hide-details
          single-line
          density="compact"
          class="search-field"
        ></v-text-field>
      </template>
    </PageHeader>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="filteredCategories"
        :loading="loading"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:item.icon="{ item }">
          <v-icon color="primary">mdi-folder</v-icon>
        </template>

        <template v-slot:item.subcategories="{ item }">
          <v-chip v-if="getSubcategoryCount(item.category_id)" color="info" size="small">
            {{ getSubcategoryCount(item.category_id) }} subcategories
          </v-chip>
          <span v-else>-</span>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            :to="{ name: 'pcdb-part-search', query: { category: item.category_id } }"
          >
            <v-icon>mdi-magnify</v-icon>
            <v-tooltip activator="parent" location="bottom">Search Parts</v-tooltip>
          </v-btn>

          <v-btn
            icon
            variant="text"
            size="small"
            color="info"
            @click="showSubcategories(item.category_id)"
          >
            <v-icon>mdi-folder-open</v-icon>
            <v-tooltip activator="parent" location="bottom">View Subcategories</v-tooltip>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Subcategories Dialog -->
    <v-dialog v-model="subcategoriesDialog" max-width="800">
      <v-card>
        <v-card-title>
          <span v-if="selectedCategory">Subcategories of {{ selectedCategory.category_name }}</span>
          <span v-else>Subcategories</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="subcategoriesDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-data-table
            :headers="subcategoriesHeaders"
            :items="subcategories"
            :loading="subcategoriesLoading"
            class="elevation-1"
          >
            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                variant="text"
                size="small"
                color="primary"
                :to="{
                  name: 'pcdb-part-search',
                  query: {
                    category: selectedCategoryId,
                    subcategory: item.subcategory_id
                  }
                }"
              >
                <v-icon>mdi-magnify</v-icon>
                <v-tooltip activator="parent" location="bottom">Search Parts</v-tooltip>
              </v-btn>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { usePCdbStore } from '@/stores/autocare/pcdb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import { Category, SubCategory } from '@/types';

// Store
const pcdbStore = usePCdbStore();

// State
const loading = ref(false);
const error = ref('');
const search = ref('');
const subcategoriesDialog = ref(false);
const subcategoriesLoading = ref(false);
const subcategories = ref<SubCategory[]>([]);
const selectedCategoryId = ref<number | null>(null);
const subcategoryCounts = ref<Map<number, number>>(new Map());

// Table headers
const headers = [
  { title: '', key: 'icon', sortable: false, width: '48px' },
  { title: 'Category ID', key: 'category_id', sortable: true },
  { title: 'Name', key: 'category_name', sortable: true },
  { title: 'Subcategories', key: 'subcategories', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

const subcategoriesHeaders = [
  { title: 'Subcategory ID', key: 'subcategory_id', sortable: true },
  { title: 'Name', key: 'subcategory_name', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

// Computed
const categories = computed(() => pcdbStore.categories);

const filteredCategories = computed(() => {
  return categories.value;
});

const selectedCategory = computed(() => {
  if (!selectedCategoryId.value) return null;
  return categories.value.find(cat => cat.category_id === selectedCategoryId.value) || null;
});

// Methods
const loadCategories = async () => {
  try {
    loading.value = true;
    error.value = '';
    await pcdbStore.fetchCategories();

    // In a real app, you'd fetch subcategory counts for each category
    // For now, we'll simulate it with random numbers
    const counts = new Map<number, number>();
    for (const cat of pcdbStore.categories) {
      counts.set(cat.category_id, Math.floor(Math.random() * 10) + 1);
    }
    subcategoryCounts.value = counts;

  } catch (err) {
    console.error('Error loading categories:', err);
    error.value = 'Failed to load categories';
  } finally {
    loading.value = false;
  }
};

const getSubcategoryCount = (categoryId: number): number => {
  return subcategoryCounts.value.get(categoryId) || 0;
};

const showSubcategories = async (categoryId: number) => {
  try {
    selectedCategoryId.value = categoryId;
    subcategoriesDialog.value = true;
    subcategoriesLoading.value = true;

    // In a real app, you would fetch subcategories for the selected category
    // For now, we'll simulate it with a delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Create some sample subcategories
    const sampleSubcategories: SubCategory[] = [];
    const count = subcategoryCounts.value.get(categoryId) || 0;

    for (let i = 1; i <= count; i++) {
      sampleSubcategories.push({
        id: `subcategory-${categoryId}-${i}`,
        subcategory_id: i,
        subcategory_name: `Subcategory ${i} of ${selectedCategory.value?.category_name}`
      });
    }

    subcategories.value = sampleSubcategories;
  } catch (err) {
    console.error('Error loading subcategories:', err);
  } finally {
    subcategoriesLoading.value = false;
  }
};

// Load initial data
onMounted(() => {
  loadCategories();
});
</script>

<style scoped>
.categories-list-page {
  width: 100%;
}

.search-field {
  max-width: 300px;
}
</style>
