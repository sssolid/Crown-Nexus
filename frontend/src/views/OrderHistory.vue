<!-- frontend/src/views/OrderHistory.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Order History</h1>
          <p class="text-subtitle-1">View, track, and manage your orders</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
            color="primary"
            prepend-icon="mdi-cart-plus"
            to="/products"
          >
            Place New Order
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search and Filters -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row>
            <!-- Search Bar -->
            <v-col cols="12" md="4">
              <v-text-field
                v-model="search"
                label="Search Orders"
                variant="outlined"
                density="comfortable"
                append-inner-icon="mdi-magnify"
                hide-details
                placeholder="Order #, PO #, or product name"
                @keyup.enter="applyFilters"
                @click:append-inner="applyFilters"
              ></v-text-field>
            </v-col>

            <!-- Date Range -->
            <v-col cols="12" md="5">
              <div class="d-flex gap-2">
                <v-text-field
                  v-model="dateRange.from"
                  label="From Date"
                  variant="outlined"
                  density="comfortable"
                  type="date"
                  hide-details
                ></v-text-field>

                <v-text-field
                  v-model="dateRange.to"
                  label="To Date"
                  variant="outlined"
                  density="comfortable"
                  type="date"
                  hide-details
                ></v-text-field>
              </div>
            </v-col>

            <!-- Status Filter -->
            <v-col cols="12" md="3">
              <v-select
                v-model="selectedStatus"
                label="Order Status"
                :items="orderStatuses"
                variant="outlined"
                density="comfortable"
                hide-details
                clearable
              ></v-select>
            </v-col>
          </v-row>

          <!-- Advanced Filters Toggle -->
          <v-row class="mt-2">
            <v-col cols="12" class="d-flex justify-end">
              <v-btn
                variant="text"
                size="small"
                color="primary"
                prepend-icon="mdi-filter-variant"
                @click="showAdvancedFilters = !showAdvancedFilters"
              >
                {{ showAdvancedFilters ? 'Hide' : 'Show' }} Advanced Filters
              </v-btn>

              <v-btn
                variant="text"
                size="small"
                color="secondary"
                class="ml-2"
                @click="resetFilters"
              >
                Reset Filters
              </v-btn>

              <v-btn
                color="primary"
                variant="tonal"
                size="small"
                class="ml-2"
                @click="applyFilters"
              >
                Apply Filters
              </v-btn>
            </v-col>
          </v-row>

          <!-- Advanced Filters Panel -->
          <v-expand-transition>
            <div v-if="showAdvancedFilters" class="mt-4">
              <v-divider class="mb-4"></v-divider>
              <v-row>
                <!-- Payment Method -->
                <v-col cols="12" md="4">
                  <v-select
                    v-model="advancedFilters.paymentMethod"
                    label="Payment Method"
                    :items="paymentMethods"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    clearable
                  ></v-select>
                </v-col>

                <!-- Order Type -->
                <v-col cols="12" md="4">
                  <v-select
                    v-model="advancedFilters.orderType"
                    label="Order Type"
                    :items="orderTypes"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    clearable
                  ></v-select>
                </v-col>

                <!-- Amount Range -->
                <v-col cols="12" md="4">
                  <div class="d-flex gap-2">
                    <v-text-field
                      v-model="advancedFilters.minAmount"
                      label="Min Amount"
                      variant="outlined"
                      density="comfortable"
                      type="number"
                      prefix="$"
                      hide-details
                    ></v-text-field>

                    <v-text-field
                      v-model="advancedFilters.maxAmount"
                      label="Max Amount"
                      variant="outlined"
                      density="comfortable"
                      type="number"
                      prefix="$"
                      hide-details
                    ></v-text-field>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-expand-transition>
        </v-card-text>
      </v-card>

      <!-- Orders List -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <template v-else>
        <div v-if="filteredOrders.length === 0" class="text-center my-12">
          <v-icon
            icon="mdi-package-variant"
            size="64"
            color="grey-lighten-2"
          ></v-icon>
          <h2 class="text-h5 mt-4">No Orders Found</h2>
          <p class="text-body-1 mt-2">No orders match your current filters.</p>
          <v-btn
            color="primary"
            class="mt-4"
            @click="resetFilters"
          >
            Clear Filters
          </v-btn>
        </div>

        <template v-else>
          <!-- Orders Table for Desktop -->
          <v-card class="d-none d-md-block mb-6">
            <v-data-table
              :headers="tableHeaders"
              :items="filteredOrders"
              :items-per-page="itemsPerPage"
              :page="page"
              @update:page="page = $event"
              :total-visible="5"
              class="elevation-1"
            >
              <!-- Order Number Column -->
              <template v-slot:item.order_number="{ item }">
                <router-link
                  :to="`/account/orders/${item.id}`"
                  class="text-decoration-none font-weight-medium text-primary"
                >
                  {{ item.order_number }}
                </router-link>
                <div class="text-caption">
                  {{ item.po_number ? `PO: ${item.po_number}` : '' }}
                </div>
              </template>

              <!-- Date Column -->
              <template v-slot:item.order_date="{ item }">
                {{ formatDate(item.order_date) }}
                <div class="text-caption">
                  {{ formatDateTime(item.order_date) }}
                </div>
              </template>

              <!-- Total Column -->
              <template v-slot:item.total="{ item }">
                {{ formatCurrency(item.total) }}
              </template>

              <!-- Status Column -->
              <template v-slot:item.status="{ item }">
                <v-chip
                  size="small"
                  :color="getStatusColor(item.status)"
                  variant="tonal"
                >
                  {{ item.status }}
                </v-chip>
              </template>

              <!-- Shipping Column -->
              <template v-slot:item.shipping="{ item }">
                <div v-if="item.tracking_number">
                  <span class="text-caption">{{ item.shipping_carrier }}</span>
                  <div>
                    <v-btn
                      size="x-small"
                      variant="text"
                      color="primary"
                      :href="getTrackingUrl(item.shipping_carrier, item.tracking_number)"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Track
                      <v-icon end icon="mdi-open-in-new" size="small"></v-icon>
                    </v-btn>
                  </div>
                </div>
                <span v-else class="text-caption">Not shipped yet</span>
              </template>

              <!-- Actions Column -->
              <template v-slot:item.actions="{ item }">
                <v-menu>
                  <template v-slot:activator="{ props }">
                    <v-btn
                      icon
                      variant="text"
                      v-bind="props"
                    >
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list density="compact">
                    <v-list-item
                      :to="`/account/orders/${item.id}`"
                      prepend-icon="mdi-eye"
                      title="View Details"
                    ></v-list-item>

                    <v-list-item
                      prepend-icon="mdi-file-pdf-box"
                      title="Download Invoice"
                      @click="downloadInvoice(item.id)"
                    ></v-list-item>

                    <v-list-item
                      prepend-icon="mdi-refresh"
                      title="Reorder"
                      @click="reorder(item.id)"
                    ></v-list-item>

                    <v-list-item
                      v-if="canCancel(item.status)"
                      prepend-icon="mdi-cancel"
                      title="Cancel Order"
                      @click="cancelOrder(item.id)"
                    ></v-list-item>

                    <v-list-item
                      v-if="canReturn(item.status)"
                      prepend-icon="mdi-keyboard-return"
                      title="Return Items"
                      :to="`/account/returns/new?order=${item.id}`"
                    ></v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>

          <!-- Order Cards for Mobile -->
          <div class="d-block d-md-none">
            <v-card
              v-for="order in paginatedMobileOrders"
              :key="order.id"
              class="mb-4"
              :to="`/account/orders/${order.id}`"
            >
              <v-card-item>
                <template v-slot:prepend>
                  <v-icon
                    size="24"
                    :color="getStatusColor(order.status)"
                    icon="mdi-package-variant"
                  ></v-icon>
                </template>
                <v-card-title>
                  Order #{{ order.order_number }}
                </v-card-title>
                <v-card-subtitle>
                  {{ formatDate(order.order_date) }}
                </v-card-subtitle>

                <template v-slot:append>
                  <v-chip
                    size="small"
                    :color="getStatusColor(order.status)"
                    variant="tonal"
                  >
                    {{ order.status }}
                  </v-chip>
                </template>
              </v-card-item>

              <v-divider></v-divider>

              <v-card-text>
                <div class="d-flex justify-space-between mb-2">
                  <span class="text-subtitle-2">Total:</span>
                  <span class="font-weight-medium">{{ formatCurrency(order.total) }}</span>
                </div>

                <div class="d-flex justify-space-between mb-2">
                  <span class="text-subtitle-2">Items:</span>
                  <span>{{ order.item_count }}</span>
                </div>

                <div class="d-flex justify-space-between" v-if="order.tracking_number">
                  <span class="text-subtitle-2">Shipping:</span>
                  <v-btn
                    size="x-small"
                    variant="text"
                    color="primary"
                    :href="getTrackingUrl(order.shipping_carrier, order.tracking_number)"
                    target="_blank"
                    rel="noopener noreferrer"
                    @click.stop
                  >
                    Track Order
                    <v-icon end icon="mdi-open-in-new" size="small"></v-icon>
                  </v-btn>
                </div>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                  variant="text"
                  color="primary"
                  size="small"
                  prepend-icon="mdi-refresh"
                  @click.stop="reorder(order.id)"
                >
                  Reorder
                </v-btn>

                <v-btn
                  v-if="canReturn(order.status)"
                  variant="text"
                  color="warning"
                  size="small"
                  prepend-icon="mdi-keyboard-return"
                  :to="`/account/returns/new?order=${order.id}`"
                  @click.stop
                >
                  Return
                </v-btn>
              </v-card-actions>
            </v-card>

            <!-- Mobile Pagination -->
            <div class="text-center mt-4">
              <v-pagination
                v-model="page"
                :length="Math.ceil(filteredOrders.length / itemsPerPage)"
                :total-visible="3"
                density="comfortable"
                variant="elevated"
                rounded="circle"
              ></v-pagination>
            </div>
          </div>
        </template>
      </template>

      <!-- Export and Print Options -->
      <v-card class="mt-6">
        <v-card-title>Export Options</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <p class="mb-4">Export your order history or print invoices in bulk:</p>
          <v-row>
            <v-col cols="12" sm="4">
              <v-btn
                prepend-icon="mdi-microsoft-excel"
                variant="outlined"
                color="success"
                block
                @click="exportToExcel"
              >
                Export to Excel
              </v-btn>
            </v-col>
            <v-col cols="12" sm="4">
              <v-btn
                prepend-icon="mdi-file-pdf-box"
                variant="outlined"
                color="error"
                block
                @click="exportToPdf"
              >
                Export to PDF
              </v-btn>
            </v-col>
            <v-col cols="12" sm="4">
              <v-btn
                prepend-icon="mdi-printer"
                variant="outlined"
                color="info"
                block
                @click="printOrders"
              >
                Print Orders
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Cancel Order Dialog -->
      <v-dialog v-model="cancelDialog.show" max-width="500">
        <v-card>
          <v-card-title class="text-h5 bg-error text-white pa-4">
            Cancel Order
          </v-card-title>
          <v-card-text class="pa-4 pt-6">
            <p>Are you sure you want to cancel this order? This action cannot be undone.</p>
            <v-select
              v-model="cancelDialog.reason"
              label="Cancellation Reason"
              :items="cancellationReasons"
              variant="outlined"
              density="comfortable"
              class="mt-4"
              required
            ></v-select>
            <v-textarea
              v-model="cancelDialog.comments"
              label="Additional Comments"
              variant="outlined"
              rows="3"
              class="mt-4"
            ></v-textarea>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-spacer></v-spacer>
            <v-btn
              color="secondary"
              variant="text"
              @click="cancelDialog.show = false"
            >
              Cancel
            </v-btn>
            <v-btn
              color="error"
              @click="confirmCancelOrder"
              :loading="cancelDialog.loading"
            >
              Confirm Cancellation
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { formatDate, formatDateTime, formatCurrency } from '@/utils/formatters';
import { notificationService } from '@/utils/notification';

// Order interface
interface Order {
  id: string;
  order_number: string;
  po_number?: string;
  order_date: string;
  total: number;
  status: string;
  shipping_carrier?: string;
  tracking_number?: string;
  item_count: number;
  payment_method: string;
  order_type: string;
}

// Advanced filters interface
interface AdvancedFilters {
  paymentMethod: string | null;
  orderType: string | null;
  minAmount: number | null;
  maxAmount: number | null;
}

// Cancel dialog interface
interface CancelDialog {
  show: boolean;
  orderId: string | null;
  reason: string | null;
  comments: string;
  loading: boolean;
}

export default defineComponent({
  name: 'OrderHistory',

  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();

    // Loading state
    const loading = ref(true);

    // Pagination
    const page = ref(1);
    const itemsPerPage = ref(10);

    // Search and filters
    const search = ref('');
    const dateRange = ref({
      from: '',
      to: ''
    });
    const selectedStatus = ref<string | null>(null);
    const showAdvancedFilters = ref(false);
    const advancedFilters = ref<AdvancedFilters>({
      paymentMethod: null,
      orderType: null,
      minAmount: null,
      maxAmount: null
    });

    // Cancel order dialog
    const cancelDialog = ref<CancelDialog>({
      show: false,
      orderId: null,
      reason: null,
      comments: '',
      loading: false
    });

    // Filter options
    const orderStatuses = ref([
      'Pending',
      'Processing',
      'Shipped',
      'Delivered',
      'Cancelled',
      'On Hold',
      'Backordered'
    ]);

    const paymentMethods = ref([
      'Credit Card',
      'Purchase Order',
      'Net 30',
      'ACH Transfer',
      'Wire Transfer'
    ]);

    const orderTypes = ref([
      'Standard',
      'Rush',
      'Dropship',
      'Backorder',
      'Will Call'
    ]);

    const cancellationReasons = ref([
      'Ordered by mistake',
      'Found better price elsewhere',
      'Taking too long to ship',
      'Changed my mind',
      'Incorrect item(s)',
      'Other'
    ]);

    // Table headers
    const tableHeaders = ref([
      { title: 'Order #', key: 'order_number', sortable: true },
      { title: 'Date', key: 'order_date', sortable: true },
      { title: 'Total', key: 'total', sortable: true },
      { title: 'Status', key: 'status', sortable: true },
      { title: 'Shipping', key: 'shipping', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]);

    // Orders data
    const orders = ref<Order[]>([]);

    // Fetch orders from API
    const fetchOrders = async () => {
      loading.value = true;

      try {
        // In a real implementation, this would be an API call
        // const response = await api.get('/account/orders');

        // Mock data for demonstration
        await new Promise(resolve => setTimeout(resolve, 500));

        // Sample orders
        orders.value = [
          {
            id: 'order-001',
            order_number: 'ORD-10054',
            po_number: 'PO-5789',
            order_date: '2023-02-20T09:15:00Z',
            total: 2456.88,
            status: 'Processing',
            shipping_carrier: undefined,
            tracking_number: undefined,
            item_count: 15,
            payment_method: 'Purchase Order',
            order_type: 'Standard'
          },
          {
            id: 'order-002',
            order_number: 'ORD-10048',
            po_number: 'PO-5745',
            order_date: '2023-02-18T14:30:00Z',
            total: 987.65,
            status: 'Shipped',
            shipping_carrier: 'FedEx',
            tracking_number: '7891234567',
            item_count: 8,
            payment_method: 'Credit Card',
            order_type: 'Rush'
          },
          {
            id: 'order-003',
            order_number: 'ORD-10042',
            po_number: 'PO-5724',
            order_date: '2023-02-15T10:30:00Z',
            total: 1295.67,
            status: 'Delivered',
            shipping_carrier: 'UPS',
            tracking_number: '1Z9876543210',
            item_count: 12,
            payment_method: 'Net 30',
            order_type: 'Standard'
          },
          {
            id: 'order-004',
            order_number: 'ORD-10039',
            po_number: 'PO-5711',
            order_date: '2023-02-10T14:45:00Z',
            total: 879.99,
            status: 'Delivered',
            shipping_carrier: 'USPS',
            tracking_number: '9400123456789012345678',
            item_count: 5,
            payment_method: 'Credit Card',
            order_type: 'Standard'
          },
          {
            id: 'order-005',
            order_number: 'ORD-10035',
            po_number: 'PO-5698',
            order_date: '2023-02-05T09:15:00Z',
            total: 3456.88,
            status: 'Cancelled',
            shipping_carrier: undefined,
            tracking_number: undefined,
            item_count: 18,
            payment_method: 'Purchase Order',
            order_type: 'Standard'
          },
          {
            id: 'order-006',
            order_number: 'ORD-10029',
            po_number: 'PO-5684',
            order_date: '2023-01-28T11:20:00Z',
            total: 567.34,
            status: 'Delivered',
            shipping_carrier: 'FedEx',
            tracking_number: '7893216549',
            item_count: 4,
            payment_method: 'Credit Card',
            order_type: 'Standard'
          },
          {
            id: 'order-007',
            order_number: 'ORD-10025',
            po_number: 'PO-5675',
            order_date: '2023-01-22T08:45:00Z',
            total: 1789.45,
            status: 'Delivered',
            shipping_carrier: 'UPS',
            tracking_number: '1Z1234567890',
            item_count: 10,
            payment_method: 'ACH Transfer',
            order_type: 'Standard'
          },
          {
            id: 'order-008',
            order_number: 'ORD-10018',
            po_number: 'PO-5650',
            order_date: '2023-01-15T13:10:00Z',
            total: 2345.67,
            status: 'Delivered',
            shipping_carrier: 'FedEx',
            tracking_number: '7894561230',
            item_count: 14,
            payment_method: 'Net 30',
            order_type: 'Standard'
          },
          {
            id: 'order-009',
            order_number: 'ORD-10012',
            po_number: 'PO-5632',
            order_date: '2023-01-10T15:30:00Z',
            total: 456.78,
            status: 'Delivered',
            shipping_carrier: 'USPS',
            tracking_number: '9400123456789012345679',
            item_count: 3,
            payment_method: 'Credit Card',
            order_type: 'Rush'
          },
          {
            id: 'order-010',
            order_number: 'ORD-10005',
            po_number: 'PO-5618',
            order_date: '2023-01-05T09:45:00Z',
            total: 3456.78,
            status: 'Delivered',
            shipping_carrier: 'UPS',
            tracking_number: '1Z9876543211',
            item_count: 20,
            payment_method: 'Wire Transfer',
            order_type: 'Standard'
          }
        ];

        // Set initial date range to last 30 days
        const today = new Date();
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(today.getDate() - 30);

        dateRange.value.to = today.toISOString().split('T')[0];
        dateRange.value.from = thirtyDaysAgo.toISOString().split('T')[0];

        // Check if there's a status filter in the URL
        const statusParam = route.query.status as string;
        if (statusParam) {
          selectedStatus.value = statusParam;
        }
      } catch (error) {
        console.error('Error fetching orders:', error);
        notificationService.error('Failed to load order history. Please try again later.');
      } finally {
        loading.value = false;
      }
    };

    // Apply filters to orders
    const filteredOrders = computed(() => {
      let filtered = [...orders.value];

      // Apply search filter
      if (search.value) {
        const searchLower = search.value.toLowerCase();
        filtered = filtered.filter(order =>
          order.order_number.toLowerCase().includes(searchLower) ||
          (order.po_number && order.po_number.toLowerCase().includes(searchLower))
        );
      }

      // Apply date range filter
      if (dateRange.value.from) {
        const fromDate = new Date(dateRange.value.from);
        filtered = filtered.filter(order => new Date(order.order_date) >= fromDate);
      }
      if (dateRange.value.to) {
        const toDate = new Date(dateRange.value.to);
        toDate.setHours(23, 59, 59); // Set to end of day
        filtered = filtered.filter(order => new Date(order.order_date) <= toDate);
      }

      // Apply status filter
      if (selectedStatus.value) {
        filtered = filtered.filter(order => order.status === selectedStatus.value);
      }

      // Apply advanced filters
      if (advancedFilters.value.paymentMethod) {
        filtered = filtered.filter(order => order.payment_method === advancedFilters.value.paymentMethod);
      }
      if (advancedFilters.value.orderType) {
        filtered = filtered.filter(order => order.order_type === advancedFilters.value.orderType);
      }
      if (advancedFilters.value.minAmount) {
        filtered = filtered.filter(order => order.total >= (advancedFilters.value.minAmount as number));
      }
      if (advancedFilters.value.maxAmount) {
        filtered = filtered.filter(order => order.total <= (advancedFilters.value.maxAmount as number));
      }

      // Sort by order date (newest first)
      return filtered.sort((a, b) => new Date(b.order_date).getTime() - new Date(a.order_date).getTime());
    });

    // Get paginated orders for mobile view
    const paginatedMobileOrders = computed(() => {
      const startIndex = (page.value - 1) * itemsPerPage.value;
      const endIndex = startIndex + itemsPerPage.value;
      return filteredOrders.value.slice(startIndex, endIndex);
    });

    // Apply filters
    const applyFilters = () => {
      page.value = 1; // Reset to first page when filtering
    };

    // Reset all filters
    const resetFilters = () => {
      search.value = '';
      selectedStatus.value = null;

      // Reset date range to last 30 days
      const today = new Date();
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(today.getDate() - 30);

      dateRange.value.to = today.toISOString().split('T')[0];
      dateRange.value.from = thirtyDaysAgo.toISOString().split('T')[0];

      // Reset advanced filters
      advancedFilters.value = {
        paymentMethod: null,
        orderType: null,
        minAmount: null,
        maxAmount: null
      };

      page.value = 1; // Reset to first page
    };

    // Get status color
    const getStatusColor = (status: string) => {
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
        case 'on hold':
          return 'grey';
        case 'backordered':
          return 'orange';
        default:
          return 'grey';
      }
    };

    // Get tracking URL
    const getTrackingUrl = (carrier: string | undefined, trackingNumber: string | undefined) => {
      if (!carrier || !trackingNumber) return '#';

      switch (carrier.toLowerCase()) {
        case 'ups':
          return `https://www.ups.com/track?tracknum=${trackingNumber}`;
        case 'fedex':
          return `https://www.fedex.com/fedextrack/?trknbr=${trackingNumber}`;
        case 'usps':
          return `https://tools.usps.com/go/TrackConfirmAction?tLabels=${trackingNumber}`;
        case 'dhl':
          return `https://www.dhl.com/en/express/tracking.html?AWB=${trackingNumber}`;
        default:
          return '#';
      }
    };

    // Check if order can be cancelled
    const canCancel = (status: string) => {
      const cancelableStatuses = ['pending', 'processing', 'on hold'];
      return cancelableStatuses.includes(status.toLowerCase());
    };

    // Check if order can be returned
    const canReturn = (status: string) => {
      const returnableStatuses = ['delivered'];
      return returnableStatuses.includes(status.toLowerCase());
    };

    // Download invoice
    const downloadInvoice = (orderId: string) => {
      // In a real implementation, this would make an API call to generate and download the invoice
      console.log(`Downloading invoice for order ${orderId}`);
      notificationService.info('Invoice download started.');
    };

    // Reorder
    const reorder = async (orderId: string) => {
      try {
        // In a real implementation, this would make an API call to create a new order with the same items
        await new Promise(resolve => setTimeout(resolve, 500));

        notificationService.success('Items added to cart. Ready to reorder!');
        router.push('/cart');
      } catch (error) {
        console.error('Error reordering:', error);
        notificationService.error('Failed to reorder. Please try again later.');
      }
    };

    // Cancel order
    const cancelOrder = (orderId: string) => {
      cancelDialog.value = {
        show: true,
        orderId,
        reason: null,
        comments: '',
        loading: false
      };
    };

    // Confirm cancel order
    const confirmCancelOrder = async () => {
      if (!cancelDialog.value.reason) {
        notificationService.warning('Please select a cancellation reason');
        return;
      }

      cancelDialog.value.loading = true;

      try {
        // In a real implementation, this would make an API call to cancel the order
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Update the order status locally
        const orderIndex = orders.value.findIndex(o => o.id === cancelDialog.value.orderId);
        if (orderIndex !== -1) {
          orders.value[orderIndex].status = 'Cancelled';
        }

        cancelDialog.value.show = false;
        notificationService.success('Order cancelled successfully');
      } catch (error) {
        console.error('Error cancelling order:', error);
        notificationService.error('Failed to cancel order. Please try again later.');
      } finally {
        cancelDialog.value.loading = false;
      }
    };

    // Export to Excel
    const exportToExcel = () => {
      // In a real implementation, this would generate and download an Excel file
      notificationService.info('Exporting orders to Excel...');
    };

    // Export to PDF
    const exportToPdf = () => {
      // In a real implementation, this would generate and download a PDF file
      notificationService.info('Exporting orders to PDF...');
    };

    // Print orders
    const printOrders = () => {
      // In a real implementation, this would open a print dialog with formatted order data
      notificationService.info('Preparing orders for printing...');
      window.print();
    };

    // Initialize component
    onMounted(() => {
      fetchOrders();
    });

    return {
      loading,
      page,
      itemsPerPage,
      search,
      dateRange,
      selectedStatus,
      showAdvancedFilters,
      advancedFilters,
      cancelDialog,
      orderStatuses,
      paymentMethods,
      orderTypes,
      cancellationReasons,
      tableHeaders,
      orders,
      filteredOrders,
      paginatedMobileOrders,
      applyFilters,
      resetFilters,
      getStatusColor,
      getTrackingUrl,
      canCancel,
      canReturn,
      downloadInvoice,
      reorder,
      cancelOrder,
      confirmCancelOrder,
      exportToExcel,
      exportToPdf,
      printOrders,
      formatDate,
      formatDateTime,
      formatCurrency
    };
  }
});
</script>

<style scoped>
/* Print styles */
@media print {
  .v-app-bar,
  .v-footer,
  .v-btn,
  .v-toolbar {
    display: none !important;
  }

  .v-table {
    width: 100%;
    border-collapse: collapse;
  }

  .v-table th,
  .v-table td {
    border: 1px solid #ddd;
  }
}

/* Mobile card hover effect */
@media (hover: hover) {
  .order-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
}
</style>
