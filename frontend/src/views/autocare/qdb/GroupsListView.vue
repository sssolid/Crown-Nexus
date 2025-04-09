<template>
  <div class="groups-list-page">
    <PageHeader
      title="Qualifier Groups"
      subtitle="Browse all qualifier groups in the database"
      icon="mdi-folder-multiple"
      :loading="loading"
      :error="error"
    >
      <template v-slot:actions>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search Groups"
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
        :items="filteredGroups"
        :loading="loading"
        class="elevation-1"
        :search="search"
      >
        <template v-slot:item.icon="{ item }">
          <v-icon color="primary">mdi-folder-multiple</v-icon>
        </template>

        <template v-slot:item.qualifier_count="{ item }">
          <v-chip color="info" size="small">
            {{ getQualifierCount(item.group_number_id) }} qualifiers
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            @click="viewQualifiers(item.group_number_id)"
          >
            <v-icon>mdi-magnify</v-icon>
            <v-tooltip activator="parent" location="bottom">View Qualifiers</v-tooltip>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Qualifiers Dialog -->
    <v-dialog v-model="qualifiersDialog" max-width="800">
      <v-card>
        <v-card-title>
          <span v-if="selectedGroup">Qualifiers in {{ selectedGroup.group_description }}</span>
          <span v-else>Qualifiers</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="qualifiersDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-data-table
            :headers="qualifiersHeaders"
            :items="qualifiers"
            :loading="qualifiersLoading"
            class="elevation-1"
          >
            <template v-slot:item.qualifier_text="{ item }">
              <div>{{ item.qualifier_text }}</div>
              <div v-if="item.example_text" class="text-caption">Example: {{ item.example_text }}</div>
            </template>

            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                variant="text"
                size="small"
                color="primary"
                :to="{ name: 'qdb-qualifier-details', params: { id: item.qualifier_id } }"
              >
                <v-icon>mdi-eye</v-icon>
                <v-tooltip activator="parent" location="bottom">View Details</v-tooltip>
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
import { useQdbStore } from '@/stores/autocare/qdb.store.ts';
import PageHeader from '@/components/common/PageHeader.vue';
import { GroupNumber, Qualifier } from '@/types';

// Store
const qdbStore = useQdbStore();

// State
const loading = ref(false);
const error = ref('');
const search = ref('');
const qualifiersDialog = ref(false);
const qualifiersLoading = ref(false);
const qualifiers = ref<Qualifier[]>([]);
const selectedGroupId = ref<number | null>(null);
const qualifierCounts = ref<Map<number, number>>(new Map());

// Table headers
const headers = [
  { title: '', key: 'icon', sortable: false, width: '48px' },
  { title: 'Group ID', key: 'group_number_id', sortable: true },
  { title: 'Description', key: 'group_description', sortable: true },
  { title: 'Qualifiers', key: 'qualifier_count', sortable: false },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

const qualifiersHeaders = [
  { title: 'Qualifier ID', key: 'qualifier_id', sortable: true },
  { title: 'Text', key: 'qualifier_text', sortable: true },
  { title: 'Type', key: 'type', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false, align: 'end' },
];

// Computed
const groups = computed(() => qdbStore.groupNumbers);

const filteredGroups = computed(() => {
  return groups.value;
});

const selectedGroup = computed(() => {
  if (!selectedGroupId.value) return null;
  return groups.value.find(group => group.group_number_id === selectedGroupId.value) || null;
});

// Methods
const loadGroups = async () => {
  try {
    loading.value = true;
    error.value = '';
    await qdbStore.fetchGroupNumbers();

    // In a real app, you'd fetch qualifier counts for each group
    // For now, we'll simulate it with random numbers
    const counts = new Map<number, number>();
    for (const group of qdbStore.groupNumbers) {
      counts.set(group.group_number_id, Math.floor(Math.random() * 20) + 5);
    }
    qualifierCounts.value = counts;

  } catch (err) {
    console.error('Error loading groups:', err);
    error.value = 'Failed to load groups';
  } finally {
    loading.value = false;
  }
};

const getQualifierCount = (groupId: number): number => {
  return qualifierCounts.value.get(groupId) || 0;
};

const viewQualifiers = async (groupId: number) => {
  try {
    selectedGroupId.value = groupId;
    qualifiersDialog.value = true;
    qualifiersLoading.value = true;

    // In a real app, you would fetch qualifiers for the selected group
    // For now, we'll simulate it with a delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Create some sample qualifiers
    const sampleQualifiers: Qualifier[] = [];
    const count = qualifierCounts.value.get(groupId) || 0;

    for (let i = 1; i <= count; i++) {
      sampleQualifiers.push({
        id: `qualifier-${groupId}-${i}`,
        qualifier_id: 1000 + i,
        qualifier_text: `Sample qualifier text ${i} in group ${groupId}`,
        example_text: i % 3 === 0 ? `Example for qualifier ${i}` : undefined,
        qualifier_type_id: 1,
        type: 'General'
      });
    }

    qualifiers.value = sampleQualifiers;
  } catch (err) {
    console.error('Error loading qualifiers:', err);
  } finally {
    qualifiersLoading.value = false;
  }
};

// Load initial data
onMounted(() => {
  loadGroups();
});
</script>

<style scoped>
.groups-list-page {
  width: 100%;
}

.search-field {
  max-width: 300px;
}
</style>
