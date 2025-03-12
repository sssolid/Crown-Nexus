<!-- frontend/src/views/AccountDashboard.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <h1 class="text-h3 font-weight-bold">Account Dashboard</h1>
          <p class="text-subtitle-1">Welcome back, {{ user?.full_name }}</p>
        </v-col>
      </v-row>

      <!-- Main Dashboard Content -->
      <v-row>
        <!-- Account Navigation Sidebar -->
        <v-col cols="12" md="3" class="mb-6">
          <v-card>
            <v-list>
              <v-list-subheader>ACCOUNT MANAGEMENT</v-list-subheader>
              
              <v-list-item
                v-for="(item, index) in accountMenu"
                :key="index"
                :to="item.to"
                :prepend-icon="item.icon"
                :title="item.title"
                :value="item.title"
                :active="isActiveRoute(item.to)"
                rounded="lg"
              ></v-list-item>
              
              <v-divider class="my-2"></v-divider>
              <v-list-subheader>ORDERS & INVENTORY</v-list-subheader>
              
              <v-list-item
                v-for="(item, index) in orderMenu"
                :key="index"
                :to="item.to"
                :prepend-icon="item.icon"
                :title="item.title"
                :value="item.title"
                :active="isActiveRoute(item.to)"
                rounded="lg"
              ></v-list-item>
              
              <v-divider class="my-2"></v-divider>
              <v-list-subheader>SUPPORT</v-list-subheader>
              
              <v-list-item
                v-for="(item, index) in supportMenu"
                :key="index"
                :to="item.to"
                :prepend-icon="item.icon"
                :title="item.title"
                :value="item.title"
                :active="isActiveRoute(item.to)"
                rounded="lg"
              ></v-list-item>
              
              <v-divider class="my-2"></v-divider>
              
              <v-list-item
                prepend-icon="mdi-logout"
                title="Logout"
                @click="logout"
                color="error"
                rounded="lg"
              ></v-list-item>
            </v-list>
          </v-card>
          
          <!-- Account Status Card -->
          <v-card class="mt-6">
            <v-card-item>
              <template v-slot:prepend>
                <v-avatar
                  color="primary"
                  size="44"
                  class="mr-4"
                >
                  <span class="text-h6 font-weight-bold">{{ getUserInitials() }}</span>
                </v-avatar>
              </template>
              <v-card-title>{{ user?.full_name }}</v-card-title>
              <v-card-subtitle>{{ accountDetails?.company_name }}</v-card-subtitle>
            </v-card-item>
            <v-list density="compact">
              <v-list-item prepend-icon="mdi-account-check" density="compact">
                <v-list-item-title>Account Type</v-list-item-title>
                <v-list-item-subtitle>
                  <v-chip size="small" color="primary" variant="tonal">
                    {{ accountDetails?.account_type }}
                  </v-chip>
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-timer-outline" density="compact">
                <v-list-item-title>Member Since</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(user?.created_at) }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-credit-card-outline" density="compact">
                <v-list-item-title>Payment Terms</v-list-item-title>
                <v-list-item-subtitle>{{ accountDetails?.payment_terms }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
        
        <!-- Dashboard Main Content -->
        <v-col cols="12" md="9">
          <!-- Quick Stats Cards -->
          <v-row>
            <v-col 
              v-for="(stat, index) in quickStats" 
              :key="index"
              cols="12" 
              sm="6" 
              md="3"
            >
              <v-card 
                height="120"
                :color="stat.color"
                variant="flat"
                class="d-flex flex-column"
              >
                <v-card-item>
                  <template v-slot:prepend>
                    <v-icon size="36" :icon="stat.icon" class="mr-2"></v-icon>
                  </template>
                  <v-card-title>{{ stat.title }}</v-card-title>
                </v-card-item>
                <v-card-text class="d-flex align-center justify-center flex-grow-1">
                  <span class="text-h4 font-weight-bold">{{ stat.value }}</span>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          
          <!-- Recent Orders & Actions -->
          <v-row class="mt-6">
            <!-- Recent Orders -->
            <v-col cols="12" md="7">
              <v-card height="100%">
                <v-card-title class="d-flex align-center">
                  Recent Orders
                  <v-spacer></v-spacer>
                  <v-btn
                    variant="text"
                    color="primary"
                    size="small"
                    to="/account/orders"
                  >
                    View All
                  </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                
                <v-card-text v-if="loading" class="d-flex justify-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </v-card-text>
                
                <template v-else>
                  <v-table v-if="recentOrders.length > 0">
                    <thead>
                      <tr>
                        <th class="text-left">Order #</th>
                        <th class="text-left">Date</th>
                        <th class="text-left">Total</th>
                        <th class="text-left">Status</th>
                        <th class="text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in recentOrders" :key="order.id">
                        <td>{{ order.order_number }}</td>
                        <td>{{ formatDate(order.order_date) }}</td>
                        <td>{{ formatCurrency(order.total) }}</td>
                        <td>
                          <v-chip
                            size="small"
                            :color="getOrderStatusColor(order.status)"
                            variant="tonal"
                          >
                            {{ order.status }}
                          </v-chip>
                        </td>
                        <td class="text-right">
                          <v-btn
                            size="small"
                            variant="text"
                            color="primary"
                            :to="`/account/orders/${order.id}`"
                          >
                            Details
                          </v-btn>
                        </td>
                      </tr>
                    </tbody>
                  </v-table>
                  
                  <v-card-text v-else class="text-center pa-6">
                    <v-icon icon="mdi-package-variant" size="64" color="grey-lighten-1"></v-icon>
                    <h3 class="text-h6 mt-4">No Recent Orders</h3>
                    <p class="text-body-2 mt-2">You haven't placed any orders recently.</p>
                    <v-btn
                      color="primary"
                      class="mt-4"
                      to="/products"
                    >
                      Browse Products
                    </v-btn>
                  </v-card-text>
                </template>
              </v-card>
            </v-col>
            
            <!-- Quick Actions -->
            <v-col cols="12" md="5">
              <v-card height="100%">
                <v-card-title>Quick Actions</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row>
                    <v-col
                      v-for="(action, index) in quickActions"
                      :key="index"
                      cols="6"
                    >
                      <v-btn
                        block
                        height="80"
                        variant="tonal"
                        :color="action.color"
                        :to="action.to"
                        class="d-flex flex-column justify-center"
                      >
                        <v-icon :icon="action.icon" size="24" class="mb-1"></v-icon>
                        <span>{{ action.title }}</span>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          
          <!-- Saved Lists & Notifications -->
          <v-row class="mt-6">
            <!-- Saved Lists -->
            <v-col cols="12" md="7">
              <v-card>
                <v-card-title class="d-flex align-center">
                  Saved Lists
                  <v-spacer></v-spacer>
                  <v-btn
                    variant="text"
                    color="primary"
                    size="small"
                    to="/account/saved-lists"
                  >
                    View All
                  </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                
                <v-list v-if="savedLists.length > 0" class="py-0">
                  <v-list-item
                    v-for="list in savedLists"
                    :key="list.id"
                    :title="list.name"
                    :subtitle="`${list.item_count} items · Last updated ${formatDate(list.updated_at)}`"
                  >
                    <template v-slot:append>
                      <v-btn
                        variant="text"
                        color="primary"
                        size="small"
                        :to="`/account/saved-lists/${list.id}`"
                      >
                        View
                      </v-btn>
                    </template>
                  </v-list-item>
                </v-list>
                
                <v-card-text v-else class="text-center pa-6">
                  <v-icon icon="mdi-format-list-bulleted" size="64" color="grey-lighten-1"></v-icon>
                  <h3 class="text-h6 mt-4">No Saved Lists</h3>
                  <p class="text-body-2 mt-2">Create lists to save products for future orders.</p>
                  <v-btn
                    color="primary"
                    class="mt-4"
                    to="/account/saved-lists/new"
                  >
                    Create List
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-col>
            
            <!-- Notifications -->
            <v-col cols="12" md="5">
              <v-card>
                <v-card-title class="d-flex align-center">
                  Notifications
                  <v-spacer></v-spacer>
                  <v-btn
                    variant="text"
                    color="primary"
                    size="small"
                    to="/account/notifications"
                  >
                    View All
                  </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                
                <v-list v-if="notifications.length > 0" class="py-0">
                  <v-list-item
                    v-for="notification in notifications"
                    :key="notification.id"
                    :title="notification.title"
                    :subtitle="formatDate(notification.date)"
                    :prepend-icon="notification.icon"
                    :prepend-icon-color="notification.color"
                    lines="two"
                  >
                    <template v-slot:append>
                      <v-btn
                        icon
                        variant="text"
                        size="small"
                        @click="markAsRead(notification.id)"
                      >
                        <v-icon size="small" icon="mdi-check"></v-icon>
                      </v-btn>
                    </template>
                  </v-list-item>
                </v-list>
                
                <v-card-text v-else class="text-center pa-6">
                  <v-icon icon="mdi-bell-outline" size="64" color="grey-lighten-1"></v-icon>
                  <h3 class="text-h6 mt-4">No Notifications</h3>
                  <p class="text-body-2 mt-2">You're all caught up!</p>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          
          <!-- Recent Activity Timeline -->
          <v-row class="mt-6">
            <v-col cols="12">
              <v-card>
                <v-card-title>Recent Activity</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-timeline side="end" density="compact" align="start">
                    <v-timeline-item
                      v-for="(activity, index) in recentActivity"
                      :key="index"
                      :dot-color="activity.color"
                      size="small"
                    >
                      <div class="d-flex align-center mb-1">
                        <div class="text-subtitle-2 font-weight-medium">{{ activity.title }}</div>
                        <v-spacer></v-spacer>
                        <div class="text-caption text-medium-emphasis">{{ formatDateTime(activity.timestamp) }}</div>
                      </div>
                      <div class="text-body-2">{{ activity.description }}</div>
                    </v-timeline-item>
                  </v-timeline>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { formatDate, formatDateTime, formatCurrency } from '@/utils/formatters';

// Interface for the account details
interface AccountDetails {
  company_name: string;
  account_type: string;
  payment_terms: string;
  credit_limit: number;
  account_number: string;
  account_manager: string;
}

// Interface for order
interface Order {
  id: string;
  order_number: string;
  order_date: string;
  total: number;
  status: string;
}

// Interface for saved list
interface SavedList {
  id: string;
  name: string;
  item_count: number;
  updated_at: string;
}

// Interface for notification
interface Notification {
  id: string;
  title: string;
  message: string;
  date: string;
  read: boolean;
  icon: string;
  color: string;
}

// Interface for recent activity
interface Activity {
  title: string;
  description: string;
  timestamp: string;
  color: string;
}

export default defineComponent({
  name: 'AccountDashboard',

  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();
    
    // Get current user from auth store
    const user = computed(() => authStore.user);
    
    // Loading state
    const loading = ref(true);
    
    // Account details
    const accountDetails = ref<AccountDetails | null>(null);
    
    // Navigation menus
    const accountMenu = ref([
      { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/account/dashboard' },
      { title: 'Profile', icon: 'mdi-account', to: '/account/profile' },
      { title: 'Company Information', icon: 'mdi-domain', to: '/account/company' },
      { title: 'Payment Methods', icon: 'mdi-credit-card', to: '/account/payment-methods' },
      { title: 'Shipping Addresses', icon: 'mdi-map-marker', to: '/account/shipping-addresses' },
      { title: 'Team Members', icon: 'mdi-account-group', to: '/account/team' }
    ]);
    
    const orderMenu = ref([
      { title: 'Order History', icon: 'mdi-history', to: '/account/orders' },
      { title: 'Saved Lists', icon: 'mdi-format-list-bulleted', to: '/account/saved-lists' },
      { title: 'Quick Order', icon: 'mdi-flash', to: '/account/quick-order' },
      { title: 'Quotes & Estimates', icon: 'mdi-file-document-outline', to: '/account/quotes' },
      { title: 'Returns', icon: 'mdi-keyboard-return', to: '/account/returns' }
    ]);
    
    const supportMenu = ref([
      { title: 'Support Tickets', icon: 'mdi-lifebuoy', to: '/account/support-tickets' },
      { title: 'Downloads', icon: 'mdi-download', to: '/account/downloads' },
      { title: 'Settings', icon: 'mdi-cog', to: '/account/settings' }
    ]);
    
    // Dashboard data
    const quickStats = ref([
      { title: 'Orders', value: '24', icon: 'mdi-package-variant', color: 'primary-lighten-5' },
      { title: 'Pending', value: '3', icon: 'mdi-clock-outline', color: 'warning-lighten-5' },
      { title: 'Returns', value: '1', icon: 'mdi-keyboard-return', color: 'error-lighten-5' },
      { title: 'Lists', value: '5', icon: 'mdi-format-list-bulleted', color: 'success-lighten-5' }
    ]);
    
    // Recent orders
    const recentOrders = ref<Order[]>([
      {
        id: 'order-001',
        order_number: 'ORD-10042',
        order_date: '2023-02-15T10:30:00Z',
        total: 1295.67,
        status: 'Shipped'
      },
      {
        id: 'order-002',
        order_number: 'ORD-10039',
        order_date: '2023-02-10T14:45:00Z',
        total: 879.99,
        status: 'Delivered'
      },
      {
        id: 'order-003',
        order_number: 'ORD-10035',
        order_date: '2023-02-05T09:15:00Z',
        total: 2456.88,
        status: 'Processing'
      }
    ]);
    
    // Quick actions
    const quickActions = ref([
      { title: 'New Order', icon: 'mdi-cart-plus', to: '/products', color: 'primary' },
      { title: 'Quick Order', icon: 'mdi-flash', to: '/account/quick-order', color: 'secondary' },
      { title: 'Track Orders', icon: 'mdi-truck-delivery', to: '/account/orders', color: 'info' },
      { title: 'Support', icon: 'mdi-lifebuoy', to: '/account/support-tickets', color: 'error' },
      { title: 'Reorder', icon: 'mdi-refresh', to: '/account/orders?filter=reorder', color: 'success' },
      { title: 'Returns', icon: 'mdi-keyboard-return', to: '/account/returns', color: 'warning' }
    ]);
    
    // Saved lists
    const savedLists = ref<SavedList[]>([
      {
        id: 'list-001',
        name: 'Regular Service Items',
        item_count: 12,
        updated_at: '2023-02-18T08:30:00Z'
      },
      {
        id: 'list-002',
        name: 'Monthly Restock',
        item_count: 25,
        updated_at: '2023-02-10T11:45:00Z'
      },
      {
        id: 'list-003',
        name: 'Workshop Supplies',
        item_count: 8,
        updated_at: '2023-01-25T14:20:00Z'
      }
    ]);
    
    // Notifications
    const notifications = ref<Notification[]>([
      {
        id: 'notif-001',
        title: 'Your order ORD-10042 has shipped',
        message: 'Your order has been shipped via FedEx. Tracking number: 9876543210',
        date: '2023-02-15T14:30:00Z',
        read: false,
        icon: 'mdi-truck-delivery',
        color: 'primary'
      },
      {
        id: 'notif-002',
        title: 'Price drop on 5 items in your saved lists',
        message: 'Items in your "Regular Service Items" list have decreased in price',
        date: '2023-02-14T09:15:00Z',
        read: false,
        icon: 'mdi-sale',
        color: 'success'
      },
      {
        id: 'notif-003',
        title: 'New catalog update available',
        message: 'The latest product catalog has been updated with 200+ new items',
        date: '2023-02-12T11:45:00Z',
        read: false,
        icon: 'mdi-book-open-variant',
        color: 'info'
      }
    ]);
    
    // Recent activity
    const recentActivity = ref<Activity[]>([
      {
        title: 'Order Shipped',
        description: 'Your order ORD-10042 has shipped via FedEx',
        timestamp: '2023-02-15T14:30:00Z',
        color: 'primary'
      },
      {
        title: 'Support Ticket Updated',
        description: 'Support agent James responded to your ticket #ST-2589',
        timestamp: '2023-02-14T16:45:00Z',
        color: 'info'
      },
      {
        title: 'New Order Placed',
        description: 'You placed a new order ORD-10042 for $1,295.67',
        timestamp: '2023-02-15T10:30:00Z',
        color: 'success'
      },
      {
        title: 'Saved List Updated',
        description: 'You added 3 items to your "Monthly Restock" list',
        timestamp: '2023-02-10T11:45:00Z',
        color: 'secondary'
      },
      {
        title: 'Order Delivered',
        description: 'Your order ORD-10039 was delivered',
        timestamp: '2023-02-12T15:20:00Z',
        color: 'success'
      }
    ]);
    
    // Check if the current route matches a given route
    const isActiveRoute = (routePath: string) => {
      return route.path === routePath;
    };
    
    // Get user initials for avatar
    const getUserInitials = () => {
      if (!user.value || !user.value.full_name) return 'UN';
      
      const nameParts = user.value.full_name.split(' ');
      if (nameParts.length > 1) {
        return (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase();
      }
      
      return nameParts[0].substring(0, 2).toUpperCase();
    };
    
    // Get color for order status
    const getOrderStatusColor = (status: string) => {
      switch (status.toLowerCase()) {
        case 'pending':
          return 'warning';
        case 'processing':
          return 'info';
        case 'shipped':
          return 'primary';
        case 'delivered':
          return 'success';
        case 'cancelled':
          return 'error';
        default:
          return 'grey';
      }
    };
    
    // Mark notification as read
    const markAsRead = (id: string) => {
      const index = notifications.value.findIndex(n => n.id === id);
      if (index !== -1) {
        notifications.value.splice(index, 1);
      }
    };
    
    // Logout function
    const logout = () => {
      authStore.logout();
    };
    
    // Fetch account data
    const fetchAccountData = async () => {
      loading.value = true;
      
      try {
        // In a real implementation, this would be an API call
        // const response = await api.get('/account/details');
        
        // Mock data for demonstration
        await new Promise(resolve => setTimeout(resolve, 500));
        
        accountDetails.value = {
          company_name: 'AutoTech Solutions, Inc.',
          account_type: 'Distributor',
          payment_terms: 'Net 30',
          credit_limit: 25000,
          account_number: 'ACCT-10456',
          account_manager: 'Sarah Johnson'
        };
      } catch (error) {
        console.error('Error fetching account data:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Initialize component
    onMounted(() => {
      fetchAccountData();
    });
    
    return {
      user,
      accountDetails,
      loading,
      accountMenu,
      orderMenu,
      supportMenu,
      quickStats,
      recentOrders,
      quickActions,
      savedLists,
      notifications,
      recentActivity,
      isActiveRoute,
      getUserInitials,
      getOrderStatusColor,
      markAsRead,
      logout,
      formatDate,
      formatDateTime,
      formatCurrency
    };
  }
});
</script>

<style scoped>
/* Custom scrolling for timeline on small screens */
@media (max-width: 600px) {
  .v-timeline {
    max-height: 300px;
    overflow-y: auto;
  }
}

/* Style for unread notifications */
.notification-unread {
  background-color: rgba(var(--v-theme-primary), 0.05);
}
</style>
