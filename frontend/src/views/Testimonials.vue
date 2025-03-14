<!-- frontend/src/views/Testimonials.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Success Stories</h1>
          <p class="text-subtitle-1">
            See how businesses in the automotive aftermarket are succeeding with Crown Nexus
          </p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center" v-if="isAdmin">
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            to="/testimonials/new"
          >
            Add Case Study
          </v-btn>
        </v-col>
      </v-row>

      <!-- Featured Case Study -->
      <v-card v-if="featuredTestimonial" class="mb-8" elevation="3">
        <v-row no-gutters>
          <v-col cols="12" md="6">
            <v-img
              :src="featuredTestimonial.image_url || 'https://via.placeholder.com/800x600?text=Case+Study'"
              height="400"
              cover
            ></v-img>
          </v-col>
          <v-col cols="12" md="6">
            <v-card-item class="pa-6 h-100 d-flex flex-column">
              <v-chip color="primary" variant="flat" size="small" class="mb-2">
                Featured Success Story
              </v-chip>
              <v-card-title class="text-h4 font-weight-bold mb-2">
                {{ featuredTestimonial.title }}
              </v-card-title>
              <v-card-subtitle class="text-subtitle-1 mb-4">
                {{ featuredTestimonial.company }} | {{ featuredTestimonial.industry }}
              </v-card-subtitle>
              <v-card-text class="text-body-1 flex-grow-1">
                <p class="mb-4">{{ featuredTestimonial.summary }}</p>
                <v-rating
                  :model-value="featuredTestimonial.rating"
                  color="amber"
                  density="compact"
                  size="small"
                  readonly
                  class="mb-2"
                ></v-rating>
                <blockquote class="text-h6 font-italic">
                  "{{ featuredTestimonial.quote }}"
                </blockquote>
                <p class="text-subtitle-2 mt-2">— {{ featuredTestimonial.contact_name }}, {{ featuredTestimonial.contact_title }}</p>
              </v-card-text>
              <div class="px-4 pb-4">
                <v-btn
                  color="primary"
                  variant="tonal"
                  :to="`/testimonials/${featuredTestimonial.id}`"
                >
                  Read Full Case Study
                </v-btn>
              </div>
            </v-card-item>
          </v-col>
        </v-row>
      </v-card>

      <!-- Industry Filter -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="4">
              <v-select
                v-model="selectedIndustry"
                label="Filter by Industry"
                :items="industryOptions"
                variant="outlined"
                density="comfortable"
                clearable
                hide-details
                @update:model-value="filterTestimonials"
              ></v-select>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="selectedRating"
                label="Filter by Rating"
                :items="ratingOptions"
                variant="outlined"
                density="comfortable"
                clearable
                hide-details
                @update:model-value="filterTestimonials"
              ></v-select>
            </v-col>
            <v-col cols="12" md="4" class="d-flex align-center justify-end">
              <v-btn
                variant="text"
                color="primary"
                @click="resetFilters"
                class="ml-2"
              >
                Reset Filters
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Loading State -->
      <div v-if="loading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <!-- Testimonials Grid -->
      <v-row v-else-if="filteredTestimonials.length > 0">
        <v-col
          v-for="testimonial in filteredTestimonials"
          :key="testimonial.id"
          cols="12"
          md="6"
          lg="4"
        >
          <v-card height="100%" class="d-flex flex-column">
            <v-img
              :src="testimonial.image_url || 'https://via.placeholder.com/400x200?text=Case+Study'"
              height="200"
              cover
              class="align-end"
            >
              <v-chip
                color="primary"
                variant="elevated"
                class="ma-2"
              >
                {{ testimonial.industry }}
              </v-chip>
            </v-img>
            <v-card-item>
              <v-card-title>{{ testimonial.title }}</v-card-title>
              <v-card-subtitle>{{ testimonial.company }}</v-card-subtitle>
            </v-card-item>
            <v-card-text class="flex-grow-1">
              <v-rating
                :model-value="testimonial.rating"
                color="amber"
                density="compact"
                size="small"
                readonly
                class="mb-2"
              ></v-rating>
              <p class="text-truncate-3-lines">{{ testimonial.summary }}</p>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                color="primary"
                :to="`/testimonials/${testimonial.id}`"
              >
                Read More
              </v-btn>
              <v-btn
                v-if="isAdmin"
                icon
                variant="text"
                color="primary"
                :to="`/testimonials/${testimonial.id}/edit`"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Empty State -->
      <v-card v-else class="text-center pa-8">
        <v-icon icon="mdi-emoticon-sad-outline" size="64" color="grey-lighten-1"></v-icon>
        <h3 class="text-h5 mt-4 mb-2">No Case Studies Found</h3>
        <p class="text-body-1 mb-4">
          No case studies match your selected filters. Please try different criteria.
        </p>
        <v-btn color="primary" variant="tonal" @click="resetFilters">Reset Filters</v-btn>
      </v-card>

      <!-- Pagination -->
      <div class="d-flex justify-center mt-6">
        <v-pagination
          v-if="totalPages > 1"
          v-model="page"
          :length="totalPages"
          rounded="circle"
          @update:model-value="fetchTestimonials"
        ></v-pagination>
      </div>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import testimonialsAutoRepairShop from '@/assets/testimonials/auto_repair.jpg';
import testimonialsGTPerformance from '@/assets/testimonials/gt_performance.jpg';
import testimonialsPacificAuto from '@/assets/testimonials/pacific_auto.jpg';
import testimonialsMidwestAuto from '@/assets/testimonials/midwest_auto.jpg';
import testimonialsCityWide from '@/assets/testimonials/citywide.jpg';
import testimonialsVelocityPerformance from '@/assets/testimonials/velocity_performance.jpg';

// Testimonial interface - would be imported from types in a real app
interface Testimonial {
  id: string;
  title: string;
  company: string;
  industry: string;
  contact_name: string;
  contact_title: string;
  quote: string;
  summary: string;
  content: string;
  rating: number;
  image_url?: string;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

const authStore = useAuthStore();
const isAdmin = computed(() => authStore.isAdmin);

// Data loading state
const loading = ref(true);
const testimonials = ref<Testimonial[]>([]);
const featuredTestimonial = ref<Testimonial | null>(null);

// Pagination
const page = ref(1);
const itemsPerPage = ref(9);
const totalItems = ref(0);
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value));

// Filters
const selectedIndustry = ref<string | null>(null);
const selectedRating = ref<number | null>(null);
const filteredTestimonials = ref<Testimonial[]>([]);

// Filter options
const industryOptions = ref([
  'Auto Repair Shop',
  'Parts Retailer',
  'Distributor',
  'Dealership',
  'Fleet Service',
  'Performance Shop'
]);

const ratingOptions = ref([
  { title: '5 Stars', value: 5 },
  { title: '4+ Stars', value: 4 },
  { title: '3+ Stars', value: 3 }
]);

// Fetch testimonials from API
const fetchTestimonials = async () => {
  loading.value = true;

  try {
    // In a real implementation, this would be an API call
    // api.get('/testimonials', { params: { page: page.value, per_page: itemsPerPage.value } })

    // Mock data for demonstration
    await new Promise(resolve => setTimeout(resolve, 500));

    // Sample testimonials
    const mockTestimonials: Testimonial[] = [
      {
        id: '1',
        title: 'Streamlined Our Parts Ordering Process',
        company: 'AutoPro Repair Center',
        industry: 'Auto Repair Shop',
        contact_name: 'James Wilson',
        contact_title: 'Service Manager',
        quote: 'Crown Nexus completely transformed how we order parts. We\'ve reduced our ordering time by 75% and virtually eliminated ordering errors.',
        summary: 'AutoPro Repair Center struggled with an inefficient parts ordering system that led to frequent errors. After implementing Crown Nexus, they reduced order processing time by 75% and eliminated most ordering errors.',
        content: 'AutoPro Repair Center, a busy 10-bay shop servicing over 500 vehicles per month, struggled with their parts ordering process. Their previous manual system resulted in frequent errors, delayed repairs, and frustrated customers. After implementing Crown Nexus, they saw immediate improvements in their workflow. The intuitive fitment tool ensured technicians ordered the right parts every time, while the automated inventory management system helped them optimize their stock levels. Within three months, AutoPro reduced their parts ordering time by 75%, virtually eliminated ordering errors, and improved their customer satisfaction scores by 35%.',
        rating: 5,
        image_url: testimonialsAutoRepairShop,
        is_featured: true,
        created_at: '2023-04-15T10:30:00Z',
        updated_at: '2023-04-15T10:30:00Z'
      },
      {
        id: '2',
        title: 'Doubled Our Online Parts Sales',
        company: 'GT Performance Parts',
        industry: 'Parts Retailer',
        contact_name: 'Sarah Johnson',
        contact_title: 'E-Commerce Director',
        quote: 'The integration with our online store was seamless. We\'ve doubled our online sales since implementing Crown Nexus.',
        summary: 'GT Performance Parts needed a better way to manage their online inventory and ensure customers found the right parts. Crown Nexus provided a solution that increased sales and reduced returns.',
        content: 'GT Performance Parts had a growing online presence but struggled with customer confusion about fitment and compatibility. This led to numerous returns and negative reviews. After implementing Crown Nexus and integrating it with their e-commerce platform, they saw an immediate impact. The platform\'s comprehensive fitment database allowed customers to easily find parts compatible with their vehicles, while the detailed product information reduced questions and confusion. Within six months, GT Performance doubled their online sales, reduced returns by 60%, and improved their customer review ratings significantly.',
        rating: 5,
        image_url: testimonialsGTPerformance,
        is_featured: false,
        created_at: '2023-05-20T14:45:00Z',
        updated_at: '2023-05-20T14:45:00Z'
      },
      {
        id: '3',
        title: 'Revolutionized Our Inventory Management',
        company: 'Pacific Auto Distributors',
        industry: 'Distributor',
        contact_name: 'Michael Chen',
        contact_title: 'Operations Manager',
        quote: 'Crown Nexus gave us visibility into our inventory we never had before. We\'ve reduced our carrying costs by 20% while improving our fill rates.',
        summary: 'Pacific Auto Distributors needed better inventory visibility across multiple warehouses. Crown Nexus provided the tools to optimize stock levels and improve fill rates.',
        content: 'Pacific Auto Distributors operates three warehouses serving hundreds of repair shops and retailers. Their legacy inventory system couldn\'t provide the visibility they needed across locations, resulting in overstock in some locations and stockouts in others. Crown Nexus implemented a centralized inventory management system with real-time tracking across all locations. The platform\'s analytics tools helped identify slow-moving items and optimize reorder points based on actual demand patterns. Within a year, Pacific reduced their carrying costs by 20%, improved their fill rates from 85% to 97%, and significantly enhanced their service levels to customers.',
        rating: 4,
        image_url: testimonialsPacificAuto,
        is_featured: false,
        created_at: '2023-06-12T09:15:00Z',
        updated_at: '2023-06-12T09:15:00Z'
      },
      {
        id: '4',
        title: 'Improved Customer Satisfaction Scores',
        company: 'Midwest Automotive Group',
        industry: 'Dealership',
        contact_name: 'Robert Taylor',
        contact_title: 'Parts Department Manager',
        quote: 'Our customers appreciate the faster service and accurate parts ordering. Our CSI scores have never been higher.',
        summary: 'Midwest Automotive Group dealerships were facing customer satisfaction challenges due to parts-related delays. Crown Nexus helped streamline their parts department operations.',
        content: 'Midwest Automotive Group operates five dealership locations across three states. Their service departments were struggling with parts-related delays and errors that impacted customer satisfaction. After implementing Crown Nexus, they were able to streamline parts ordering for service repairs, reduce wait times, and improve communications with customers. The platform\'s integration with their DMS system eliminated double-entry and reduced administrative overhead. Within four months, Midwest saw their Customer Satisfaction Index (CSI) scores increase by 15 points, while reducing the average repair completion time by a full day.',
        rating: 5,
        image_url: testimonialsMidwestAuto,
        is_featured: false,
        created_at: '2023-07-05T11:30:00Z',
        updated_at: '2023-07-05T11:30:00Z'
      },
      {
        id: '5',
        title: 'Optimized Our Fleet Maintenance Operations',
        company: 'CityWide Transport',
        industry: 'Fleet Service',
        contact_name: 'Lisa Rodriguez',
        contact_title: 'Fleet Maintenance Supervisor',
        quote: 'Crown Nexus has helped us extend our fleet lifecycle and reduce our maintenance costs. It\'s paid for itself many times over.',
        summary: 'CityWide Transport needed a better system to manage maintenance for their 200+ vehicle fleet. Crown Nexus provided tools to optimize maintenance schedules and parts ordering.',
        content: 'CityWide Transport maintains a fleet of over 200 vehicles that are essential to their daily operations. Their previous maintenance tracking system was falling short, resulting in excessive downtime and unplanned maintenance costs. Crown Nexus implemented a comprehensive fleet maintenance module that integrated vehicle history, maintenance schedules, and parts inventory. The platform\'s predictive maintenance tools helped identify potential failures before they happened, while the streamlined parts ordering process ensured technicians had what they needed when scheduled maintenance was due. Within the first year, CityWide reduced their fleet downtime by 30%, extended their average vehicle lifecycle by 15%, and decreased their overall maintenance costs by 22%.',
        rating: 4,
        image_url: testimonialsCityWide,
        is_featured: false,
        created_at: '2023-08-18T13:45:00Z',
        updated_at: '2023-08-18T13:45:00Z'
      },
      {
        id: '6',
        title: 'Expanded Our Product Line with Confidence',
        company: 'Velocity Performance',
        industry: 'Performance Shop',
        contact_name: 'Alex Murphy',
        contact_title: 'Owner',
        quote: 'The fitment data in Crown Nexus gave us the confidence to expand our product offerings without fear of compatibility issues.',
        summary: 'Velocity Performance wanted to expand their product offerings but was concerned about fitment accuracy. Crown Nexus provided the data they needed to grow with confidence.',
        content: 'Velocity Performance specializes in performance upgrades for European sports cars. They wanted to expand their product offerings but were concerned about the complexity of fitment data across makes and models. Crown Nexus provided them with comprehensive, accurate fitment data that gave them confidence in adding new product lines. The platform\'s customer portal also allowed their clients to verify compatibility before purchasing, reducing support calls and returns. Since implementing Crown Nexus, Velocity has expanded their product catalog by 35%, entered three new vehicle market segments, and increased their overall revenue by 40% year-over-year.',
        rating: 5,
        image_url: testimonialsVelocityPerformance,
        is_featured: false,
        created_at: '2023-09-22T15:15:00Z',
        updated_at: '2023-09-22T15:15:00Z'
      }
    ];

    // Set featured testimonial
    featuredTestimonial.value = mockTestimonials.find(t => t.is_featured) || null;

    // Filter out featured testimonial from main list
    testimonials.value = mockTestimonials.filter(t => !t.is_featured);
    filteredTestimonials.value = [...testimonials.value];

    totalItems.value = testimonials.value.length;
  } catch (error) {
    console.error('Error fetching testimonials:', error);
  } finally {
    loading.value = false;
  }
};

// Filter testimonials based on selected options
const filterTestimonials = () => {
  filteredTestimonials.value = testimonials.value.filter(t => {
    // Apply industry filter if selected
    if (selectedIndustry.value && t.industry !== selectedIndustry.value) {
      return false;
    }

    // Apply rating filter if selected
    if (selectedRating.value && t.rating < selectedRating.value) {
      return false;
    }

    return true;
  });
};

// Reset filters
const resetFilters = () => {
  selectedIndustry.value = null;
  selectedRating.value = null;
  filteredTestimonials.value = [...testimonials.value];
};

// Initialize component
onMounted(() => {
  fetchTestimonials();
});
</script>

<style scoped>
.text-truncate-3-lines {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
