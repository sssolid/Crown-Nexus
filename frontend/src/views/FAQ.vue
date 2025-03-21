<!-- frontend/src/views/FAQ.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Frequently Asked Questions</h1>
          <p class="text-subtitle-1">Find answers to common questions about Crown Nexus</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center" v-if="isAdmin">
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            to="/faqs/new"
          >
            Add FAQ
          </v-btn>
        </v-col>
      </v-row>

      <!-- Search Bar -->
      <v-row class="mb-6">
        <v-col cols="12" lg="8" class="mx-auto">
          <v-card class="pa-2">
            <v-text-field
              v-model="searchQuery"
              label="Search FAQs"
              variant="outlined"
              density="comfortable"
              clearable
              hide-details
              prepend-inner-icon="mdi-magnify"
              @update:model-value="searchFaqs"
            ></v-text-field>
          </v-card>
        </v-col>
      </v-row>

      <!-- FAQ Categories Tabs -->
      <v-row v-if="!loading">
        <v-col cols="12">
          <v-card>
            <v-tabs
              v-model="activeTab"
              color="primary"
              align-tabs="center"
              slider-color="primary"
              show-arrows
            >
              <v-tab value="all">All FAQs</v-tab>
              <v-tab 
                v-for="category in categories" 
                :key="category.id" 
                :value="category.id"
              >
                {{ category.name }}
              </v-tab>
            </v-tabs>

            <v-divider></v-divider>

            <v-window v-model="activeTab">
              <!-- All FAQs Tab -->
              <v-window-item value="all">
                <v-container>
                  <template v-if="searchQuery && searchResults.length === 0">
                    <div class="text-center py-8">
                      <v-icon icon="mdi-help-circle-outline" size="64" color="grey-lighten-1"></v-icon>
                      <h3 class="text-h5 mt-4">No Results Found</h3>
                      <p class="text-body-1 mt-2">
                        No FAQs match your search for "{{ searchQuery }}".
                      </p>
                      <p class="text-body-2 mt-2">
                        Try different keywords or check your spelling.
                      </p>
                      <v-btn color="primary" variant="text" @click="searchQuery = ''">
                        Clear Search
                      </v-btn>
                    </div>
                  </template>
                  <template v-else>
                    <FaqAccordion 
                      :faqs="searchQuery ? searchResults : allFaqs" 
                      :is-admin="isAdmin"
                    />
                  </template>
                </v-container>
              </v-window-item>

              <!-- Category Tabs -->
              <v-window-item
                v-for="category in categories"
                :key="category.id"
                :value="category.id"
              >
                <v-container>
                  <FaqAccordion 
                    :faqs="getFaqsByCategory(category.id)"
                    :is-admin="isAdmin" 
                  />
                </v-container>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>

      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <!-- Need Help Section -->
      <v-row class="mt-10">
        <v-col cols="12" lg="8" class="mx-auto">
          <v-card class="text-center pa-6">
            <v-card-title class="text-h5 font-weight-bold">Still Have Questions?</v-card-title>
            <v-card-text>
              <p class="text-body-1 mb-4">
                If you couldn't find the answer you were looking for, our support team is ready to help.
              </p>
              <v-row justify="center" class="mt-4">
                <v-col cols="12" md="4">
                  <v-card variant="outlined" class="h-100">
                    <v-card-item>
                      <template v-slot:prepend>
                        <v-icon color="primary" size="large">mdi-email-outline</v-icon>
                      </template>
                      <v-card-title>Email Support</v-card-title>
                    </v-card-item>
                    <v-card-text>
                      Send us an email and we'll respond within 24 hours.
                    </v-card-text>
                    <v-card-actions class="justify-center">
                      <v-btn variant="text" color="primary" href="mailto:support@crownnexus.com">
                        support@crownnexus.com
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col cols="12" md="4">
                  <v-card variant="outlined" class="h-100">
                    <v-card-item>
                      <template v-slot:prepend>
                        <v-icon color="primary" size="large">mdi-phone-outline</v-icon>
                      </template>
                      <v-card-title>Phone Support</v-card-title>
                    </v-card-item>
                    <v-card-text>
                      Call us during business hours (8am-6pm ET).
                    </v-card-text>
                    <v-card-actions class="justify-center">
                      <v-btn variant="text" color="primary" href="tel:+18009876543">
                        1-800-987-6543
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-col>
                <v-col cols="12" md="4">
                  <v-card variant="outlined" class="h-100">
                    <v-card-item>
                      <template v-slot:prepend>
                        <v-icon color="primary" size="large">mdi-chat-outline</v-icon>
                      </template>
                      <v-card-title>Live Chat</v-card-title>
                    </v-card-item>
                    <v-card-text>
                      Chat with a support agent in real-time.
                    </v-card-text>
                    <v-card-actions class="justify-center">
                      <v-btn variant="text" color="primary" @click="openLiveChat">
                        Start Chat
                      </v-btn>
                    </v-card-actions>
                  </v-card>
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
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import FaqAccordion from '@/components/faq/FaqAccordion.vue';

// FAQ interfaces - would be imported from types in a real app
interface FaqCategory {
  id: string;
  name: string;
  description?: string;
  order: number;
}

interface Faq {
  id: string;
  question: string;
  answer: string;
  category_id: string;
  order: number;
  is_popular: boolean;
  created_at: string;
  updated_at: string;
}

export default defineComponent({
  name: 'FAQ',
  
  components: {
    FaqAccordion
  },

  setup() {
    const authStore = useAuthStore();
    const isAdmin = computed(() => authStore.isAdmin);
    
    // Data loading state
    const loading = ref(true);
    const categories = ref<FaqCategory[]>([]);
    const faqs = ref<Faq[]>([]);
    
    // Tabs
    const activeTab = ref('all');
    
    // Search
    const searchQuery = ref('');
    const searchResults = ref<Faq[]>([]);
    
    // Computed properties
    const allFaqs = computed(() => {
      return [...faqs.value].sort((a, b) => a.order - b.order);
    });
    
    // Fetch FAQs and categories from API
    const fetchFaqs = async () => {
      loading.value = true;
      
      try {
        // In a real implementation, this would be API calls
        // const categoryResponse = await api.get('/faq/categories');
        // const faqResponse = await api.get('/faqs');
        
        // Mock data for demonstration
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Sample categories
        categories.value = [
          { id: 'account', name: 'Account & Access', description: 'Questions about accounts, login, and permissions', order: 1 },
          { id: 'products', name: 'Products & Catalog', description: 'Questions about managing products and the catalog', order: 2 },
          { id: 'fitments', name: 'Fitment & Compatibility', description: 'Questions about vehicle fitment and compatibility', order: 3 },
          { id: 'orders', name: 'Orders & Shipping', description: 'Questions about ordering, shipping, and returns', order: 4 },
          { id: 'billing', name: 'Billing & Pricing', description: 'Questions about pricing, billing, and payments', order: 5 },
          { id: 'technical', name: 'Technical Support', description: 'Technical questions about using the platform', order: 6 }
        ];
        
        // Sample FAQs
        faqs.value = [
          {
            id: '1',
            question: 'How do I reset my password?',
            answer: 'To reset your password, click on the "Forgot Password" link on the login page. You will receive an email with instructions to reset your password. If you don\'t receive the email within a few minutes, please check your spam folder or contact our support team.',
            category_id: 'account',
            order: 1,
            is_popular: true,
            created_at: '2023-01-15T10:30:00Z',
            updated_at: '2023-01-15T10:30:00Z'
          },
          {
            id: '2',
            question: 'How do I add a new user to my account?',
            answer: 'If you have administrator permissions, you can add new users by going to the "User Management" section in your dashboard. Click on the "Add User" button, fill in the required information, and assign appropriate roles and permissions. The new user will receive an email invitation to create their password and access the platform.',
            category_id: 'account',
            order: 2,
            is_popular: true,
            created_at: '2023-01-15T10:35:00Z',
            updated_at: '2023-01-15T10:35:00Z'
          },
          {
            id: '3',
            question: 'What do the different user roles mean?',
            answer: 'Crown Nexus offers several user roles with different permission levels: Admin - Full access to all features and settings; Manager - Can manage products, orders, and users but cannot change system settings; Client - Standard access for ordering and viewing products; Distributor - Special access for distributor partners; Read Only - Can only view information without making changes. Administrators can customize permissions for each role as needed.',
            category_id: 'account',
            order: 3,
            is_popular: false,
            created_at: '2023-01-15T10:40:00Z',
            updated_at: '2023-01-15T10:40:00Z'
          },
          {
            id: '4',
            question: 'How do I add a new product to the catalog?',
            answer: 'To add a new product, navigate to the "Products" section and click the "Add Product" button. Fill in the required fields including SKU, name, description, and price. You can also add product images, specifications, and category information. Once complete, click "Save" to add the product to your catalog. Remember to set the product status to "Active" when you want it to be visible to customers.',
            category_id: 'products',
            order: 1,
            is_popular: true,
            created_at: '2023-01-15T11:30:00Z',
            updated_at: '2023-01-15T11:30:00Z'
          },
          {
            id: '5',
            question: 'How do I update product pricing?',
            answer: 'You can update product pricing individually or in bulk. For individual updates, go to the product detail page and edit the price field. For bulk updates, use the "Bulk Edit" feature in the Products section, or import a CSV file with updated pricing information. Price changes take effect immediately, so make sure your updates are accurate before saving.',
            category_id: 'products',
            order: 2,
            is_popular: true,
            created_at: '2023-01-15T11:35:00Z',
            updated_at: '2023-01-15T11:35:00Z'
          },
          {
            id: '6',
            question: 'What is a fitment and how do I add it?',
            answer: 'A fitment defines which vehicles are compatible with a specific part. To add a fitment, go to the "Fitments" section and click "Add Fitment." Specify the year, make, model, and any other relevant attributes like engine or transmission. You can then associate this fitment with compatible products. Accurate fitment data is crucial for ensuring customers find the right parts for their vehicles.',
            category_id: 'fitments',
            order: 1,
            is_popular: true,
            created_at: '2023-01-15T12:30:00Z',
            updated_at: '2023-01-15T12:30:00Z'
          },
          {
            id: '7',
            question: 'How do I link products to specific vehicle fitments?',
            answer: 'To link products to fitments, you have two options: 1) From the product detail page, go to the "Fitments" tab and add compatible vehicles; or 2) From the fitment detail page, add compatible products. You can also use the bulk association tool for linking multiple products to multiple fitments at once. Always verify fitment accuracy before saving to ensure customers find the right parts.',
            category_id: 'fitments',
            order: 2,
            is_popular: false,
            created_at: '2023-01-15T12:35:00Z',
            updated_at: '2023-01-15T12:35:00Z'
          },
          {
            id: '8',
            question: 'How do I process a new order?',
            answer: 'When a new order is received, you\'ll see it in the "Orders" section. Click on the order to view details. Verify the order information, check inventory availability, and then click "Process." This will generate packing slips and update inventory. Once the order is shipped, enter tracking information and mark it as "Shipped." The customer will receive automatic notifications throughout this process.',
            category_id: 'orders',
            order: 1,
            is_popular: true,
            created_at: '2023-01-15T13:30:00Z',
            updated_at: '2023-01-15T13:30:00Z'
          },
          {
            id: '9',
            question: 'What shipping methods are available?',
            answer: 'Crown Nexus supports multiple shipping methods including standard ground shipping, expedited shipping, overnight delivery, and freight shipping for large orders. The available methods for each order depend on the shipping address, order weight, and your account settings. You can configure default shipping methods and rules in the Settings section under "Shipping Configuration."',
            category_id: 'orders',
            order: 2,
            is_popular: false,
            created_at: '2023-01-15T13:35:00Z',
            updated_at: '2023-01-15T13:35:00Z'
          },
          {
            id: '10',
            question: 'How do I process a return?',
            answer: 'To process a return, go to the original order in the system and click "Create Return." Select the items being returned, specify the reason, and indicate whether the customer should receive a refund or replacement. Once the return is authorized, the customer will receive return instructions and labels if applicable. When the items are received back, inspect them and complete the return process to update inventory and process any refunds.',
            category_id: 'orders',
            order: 3,
            is_popular: true,
            created_at: '2023-01-15T13:40:00Z',
            updated_at: '2023-01-15T13:40:00Z'
          },
          {
            id: '11',
            question: 'How do I set up special pricing for specific customers?',
            answer: 'Crown Nexus allows you to create custom pricing for specific customers or customer groups. Go to "Pricing Management" in the settings, and select "Customer Specific Pricing." You can create pricing rules based on customer type, volume, or individual accounts. Options include percentage discounts, flat price adjustments, or completely custom price lists. These special prices will automatically apply when the customer logs in and places orders.',
            category_id: 'billing',
            order: 1,
            is_popular: true,
            created_at: '2023-01-15T14:30:00Z',
            updated_at: '2023-01-15T14:30:00Z'
          },
          {
            id: '12',
            question: 'How do I generate an invoice?',
            answer: 'Invoices are generated automatically when an order is processed. To manually generate or modify an invoice, go to the "Billing" section and select "Invoices." Find the relevant order and click "Generate Invoice" or "Edit Invoice." You can adjust line items, add discounts, or include additional charges before finalizing. Completed invoices can be emailed directly to customers or downloaded as PDF files for printing or attachment.',
            category_id: 'billing',
            order: 2,
            is_popular: false,
            created_at: '2023-01-15T14:35:00Z',
            updated_at: '2023-01-15T14:35:00Z'
          },
          {
            id: '13',
            question: 'What payment methods do you accept?',
            answer: 'Crown Nexus supports multiple payment methods including credit cards (Visa, Mastercard, American Express), ACH/bank transfers, purchase orders (for approved accounts), and net terms (typically Net 30). Payment options available to each customer depend on their account type and credit status. To update your accepted payment methods, go to "Settings" and then "Payment Configuration."',
            category_id: 'billing',
            order: 3,
            is_popular: true,
            created_at: '2023-01-15T14:40:00Z',
            updated_at: '2023-01-15T14:40:00Z'
          },
          {
            id: '14',
            question: 'How do I export data from the system?',
            answer: 'Crown Nexus offers several export options for your data. In most sections of the platform, look for the "Export" button, which allows you to download data in CSV, Excel, or PDF formats. For more complex or scheduled exports, go to "Reports" and configure the data you need. You can also set up automated exports to be delivered to your email or integrated with your other systems via our API.',
            category_id: 'technical',
            order: 1,
            is_popular: false,
            created_at: '2023-01-15T15:30:00Z',
            updated_at: '2023-01-15T15:30:00Z'
          },
          {
            id: '15',
            question: 'Can I integrate Crown Nexus with my existing systems?',
            answer: 'Yes, Crown Nexus offers comprehensive API access and pre-built integrations with many common business systems. We support integration with accounting software (QuickBooks, Xero), e-commerce platforms (Shopify, Magento), shipping systems (UPS, FedEx), and warehouse management solutions. For custom integrations, our development team can work with you to create specific connectors. Contact our technical support team to discuss your integration needs.',
            category_id: 'technical',
            order: 2,
            is_popular: true,
            created_at: '2023-01-15T15:35:00Z',
            updated_at: '2023-01-15T15:35:00Z'
          }
        ];
      } catch (error) {
        console.error('Error fetching FAQs:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Get FAQs by category
    const getFaqsByCategory = (categoryId: string) => {
      return faqs.value
        .filter(faq => faq.category_id === categoryId)
        .sort((a, b) => a.order - b.order);
    };
    
    // Search FAQs
    const searchFaqs = () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = [];
        return;
      }
      
      const query = searchQuery.value.toLowerCase();
      searchResults.value = faqs.value.filter(faq => 
        faq.question.toLowerCase().includes(query) || 
        faq.answer.toLowerCase().includes(query)
      );
    };
    
    // Open live chat (would be implemented with a chat service in a real app)
    const openLiveChat = () => {
      alert('Live chat functionality would be integrated here');
      // In a real implementation, this would open your chat widget
    };
    
    // Initialize component
    onMounted(() => {
      fetchFaqs();
    });
    
    return {
      isAdmin,
      loading,
      categories,
      faqs,
      allFaqs,
      activeTab,
      searchQuery,
      searchResults,
      getFaqsByCategory,
      searchFaqs,
      openLiveChat
    };
  }
});
</script>
