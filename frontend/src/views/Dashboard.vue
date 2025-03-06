<!-- frontend/src/views/Dashboard.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <h1 class="text-h3 font-weight-bold">Dashboard</h1>
          <p class="text-subtitle-1">Welcome to Crown Nexus</p>
        </v-col>
      </v-row>

      <!-- Stats Overview Cards -->
      <v-row>
        <v-col v-for="(stat, index) in stats" :key="index" cols="12" sm="6" md="3">
          <v-card class="rounded-lg" :loading="loading">
            <v-card-item>
              <template v-slot:prepend>
                <v-icon size="large" :color="stat.color" :icon="stat.icon"></v-icon>
              </template>
              <v-card-title>{{ stat.title }}</v-card-title>
              <v-card-subtitle>{{ stat.subtitle }}</v-card-subtitle>
            </v-card-item>
            <v-card-text class="text-h4 font-weight-bold text-center">
              {{ stat.value }}
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn variant="text" :to="stat.link" size="small" color="primary">
                View Details
                <v-icon icon="mdi-arrow-right" end></v-icon>
              </v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Main Dashboard Content -->
      <v-row class="mt-6">
        <!-- Recent Activity -->
        <v-col cols="12" md="6">
          <v-card class="rounded-lg" :loading="loading">
            <v-card-title class="d-flex align-center">
              Recent Activity
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                size="small"
                icon="mdi-refresh"
                @click="refreshData"
              ></v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-list v-if="activities.length > 0">
              <v-list-item
                v-for="(activity, index) in activities"
                :key="index"
                :subtitle="formatDateTime(activity.timestamp)"
                :title="activity.title"
              >
                <template v-slot:prepend>
                  <v-avatar :color="activity.color" size="36">
                    <v-icon :icon="activity.icon" color="white"></v-icon>
                  </v-avatar>
                </template>
              </v-list-item>
            </v-list>
            <v-card-text v-else class="text-center py-4">
              <v-icon icon="mdi-information-outline" color="info" size="large"></v-icon>
              <p class="mt-2">No recent activity found</p>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Quick Actions -->
        <v-col cols="12" md="6">
          <v-card class="rounded-lg">
            <v-card-title>Quick Actions</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col v-for="(action, index) in quickActions" :key="index" cols="6" sm="4">
                  <v-btn
                    block
                    height="100"
                    class="d-flex flex-column"
                    :to="action.link"
                    color="primary"
                    variant="outlined"
                  >
                    <v-icon :icon="action.icon" size="large" class="mb-2"></v-icon>
                    <span>{{ action.title }}</span>
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { formatDateTime } from '@/utils/formatters';

export default defineComponent({
  name: 'Dashboard',

  setup() {
    const authStore = useAuthStore();
    const loading = ref(false);

    // Stats data
    const stats = ref([
      {
        title: 'Products',
        subtitle: 'Total products in catalog',
        value: '0',
        icon: 'mdi-package-variant-closed',
        color: 'primary',
        link: '/products'
      },
      {
        title: 'Fitments',
        subtitle: 'Vehicle compatibility',
        value: '0',
        icon: 'mdi-car',
        color: 'success',
        link: '/fitments'
      },
      {
        title: 'Media',
        subtitle: 'Images and documents',
        value: '0',
        icon: 'mdi-image-multiple',
        color: 'info',
        link: '/media'
      },
      {
        title: 'Users',
        subtitle: 'Active accounts',
        value: '0',
        icon: 'mdi-account-group',
        color: 'warning',
        link: '/users'
      }
    ]);

    // Activities data
    const activities = ref([
      {
        title: 'New product added: Brake Pads X500',
        timestamp: new Date(Date.now() - 1000 * 60 * 30),
        icon: 'mdi-plus-circle',
        color: 'success'
      },
      {
        title: 'Updated fitment for Toyota Camry 2022',
        timestamp: new Date(Date.now() - 1000 * 60 * 120),
        icon: 'mdi-pencil',
        color: 'info'
      },
      {
        title: 'User John Doe logged in',
        timestamp: new Date(Date.now() - 1000 * 60 * 240),
        icon: 'mdi-login',
        color: 'primary'
      },
      {
        title: 'System maintenance completed',
        timestamp: new Date(Date.now() - 1000 * 60 * 360),
        icon: 'mdi-tools',
        color: 'warning'
      }
    ]);

    // Quick actions
    const quickActions = ref([
      {
        title: 'Add Product',
        icon: 'mdi-plus-circle',
        link: '/products/new'
      },
      {
        title: 'Add Fitment',
        icon: 'mdi-car-plus',
        link: '/fitments/new'
      },
      {
        title: 'Upload Media',
        icon: 'mdi-cloud-upload',
        link: '/media/upload'
      },
      {
        title: 'Search',
        icon: 'mdi-magnify',
        link: '/search'
      },
      {
        title: 'Reports',
        icon: 'mdi-chart-bar',
        link: '/reports'
      },
      {
        title: 'Settings',
        icon: 'mdi-cog',
        link: '/settings'
      }
    ]);

    // Fetch dashboard data
    const fetchDashboardData = async () => {
      loading.value = true;

      try {
        // Simulate API calls for demonstration
        // In a real application, you would make actual API calls here

        // Simulate delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Set mock data
        stats.value[0].value = '1,245';
        stats.value[1].value = '5,678';
        stats.value[2].value = '842';
        stats.value[3].value = '56';
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        loading.value = false;
      }
    };

    // Refresh data
    const refreshData = () => {
      fetchDashboardData();
    };

    // Load data on component mount
    onMounted(() => {
      fetchDashboardData();
    });

    return {
      authStore,
      loading,
      stats,
      activities,
      quickActions,
      formatDateTime,
      refreshData
    };
  }
});
</script>

<style scoped>
.dashboard-title {
  font-weight: 300;
  margin-bottom: 24px;
}
</style>
