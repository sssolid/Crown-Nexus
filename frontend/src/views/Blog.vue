<!-- frontend/src/views/Blog.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Blog & News</h1>
          <p class="text-subtitle-1">Industry insights, product updates, and automotive aftermarket trends</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center" v-if="isAdmin">
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            to="/blog/new"
          >
            Create Post
          </v-btn>
        </v-col>
      </v-row>

      <!-- Featured Article -->
      <v-card v-if="featuredPost" class="mb-8" elevation="3">
        <v-row no-gutters>
          <v-col cols="12" md="6">
            <v-img
              :src="featuredPost.image_url || 'https://via.placeholder.com/800x600?text=Featured+Article'"
              height="400"
              cover
            ></v-img>
          </v-col>
          <v-col cols="12" md="6">
            <v-card-item class="pa-6 h-100 d-flex flex-column">
              <v-chip color="primary" variant="flat" size="small" class="mb-2">
                Featured Article
              </v-chip>
              <v-card-title class="text-h4 font-weight-bold mb-2">
                {{ featuredPost.title }}
              </v-card-title>
              <v-card-subtitle class="text-subtitle-1 mb-4">
                <span class="text-primary font-weight-medium">{{ featuredPost.category }}</span> |
                {{ formatDate(featuredPost.published_at) }} |
                By {{ featuredPost.author }}
              </v-card-subtitle>
              <v-card-text class="text-body-1 flex-grow-1">
                {{ featuredPost.excerpt }}
              </v-card-text>
              <div class="px-4 pb-4">
                <v-btn
                  color="primary"
                  variant="tonal"
                  :to="`/blog/${featuredPost.slug}`"
                >
                  Read Article
                </v-btn>
              </div>
            </v-card-item>
          </v-col>
        </v-row>
      </v-card>

      <!-- Blog Filters -->
      <v-row class="mb-6">
        <v-col cols="12" lg="10" class="mx-auto">
          <v-card>
            <v-card-text>
              <v-row>
                <!-- Search -->
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="searchQuery"
                    label="Search Articles"
                    variant="outlined"
                    density="comfortable"
                    prepend-inner-icon="mdi-magnify"
                    hide-details
                    clearable
                    @keyup.enter="searchPosts"
                    @click:clear="clearSearch"
                  ></v-text-field>
                </v-col>

                <!-- Category Filter -->
                <v-col cols="12" md="3">
                  <v-select
                    v-model="selectedCategory"
                    label="Category"
                    :items="categories"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    clearable
                    @update:model-value="filterPosts"
                  ></v-select>
                </v-col>

                <!-- Sort Order -->
                <v-col cols="12" md="3">
                  <v-select
                    v-model="sortOrder"
                    label="Sort By"
                    :items="sortOptions"
                    variant="outlined"
                    density="comfortable"
                    hide-details
                    @update:model-value="filterPosts"
                  ></v-select>
                </v-col>
              </v-row>
            </v-card-text>
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

      <!-- Blog Grid -->
      <v-row v-else>
        <!-- Blog Main Content -->
        <v-col cols="12" lg="8">
          <!-- Blog Post Cards -->
          <div v-if="filteredPosts.length > 0">
            <v-card
              v-for="post in filteredPosts"
              :key="post.id"
              class="mb-6"
              variant="outlined"
            >
              <v-row no-gutters>
                <v-col cols="12" sm="4">
                  <v-img
                    :src="post.image_url || 'https://via.placeholder.com/400x300?text=Blog+Post'"
                    height="100%"
                    min-height="200"
                    cover
                  ></v-img>
                </v-col>
                <v-col cols="12" sm="8">
                  <v-card-item class="pa-4">
                    <v-card-title class="text-h5 font-weight-bold mb-2">
                      <router-link
                        :to="`/blog/${post.slug}`"
                        class="text-decoration-none text-inherit hover-primary"
                      >
                        {{ post.title }}
                      </router-link>
                    </v-card-title>
                    <v-card-subtitle class="pb-0">
                      <span class="text-primary font-weight-medium">{{ post.category }}</span> |
                      {{ formatDate(post.published_at) }} |
                      By {{ post.author }}
                    </v-card-subtitle>
                    <v-card-text class="text-body-1 pt-3">
                      <p>{{ post.excerpt }}</p>
                      <div class="d-flex justify-space-between align-center mt-4">
                        <v-btn
                          variant="text"
                          color="primary"
                          :to="`/blog/${post.slug}`"
                        >
                          Read More
                          <v-icon end icon="mdi-arrow-right"></v-icon>
                        </v-btn>
                        <div v-if="isAdmin" class="d-flex">
                          <v-btn
                            icon
                            variant="text"
                            color="primary"
                            :to="`/blog/${post.slug}/edit`"
                            class="mr-1"
                          >
                            <v-icon>mdi-pencil</v-icon>
                          </v-btn>
                          <v-btn
                            icon
                            variant="text"
                            color="error"
                            @click="confirmDelete(post)"
                          >
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                        </div>
                      </div>
                    </v-card-text>
                  </v-card-item>
                </v-col>
              </v-row>
            </v-card>

            <!-- Pagination -->
            <div class="d-flex justify-center mt-6">
              <v-pagination
                v-if="totalPages > 1"
                v-model="page"
                :length="totalPages"
                rounded="circle"
                @update:model-value="fetchPosts"
              ></v-pagination>
            </div>
          </div>

          <!-- No Results -->
          <v-card v-else class="text-center pa-8">
            <v-icon icon="mdi-newspaper-variant-outline" size="64" color="grey-lighten-1"></v-icon>
            <h3 class="text-h5 mt-4 mb-2">No Articles Found</h3>
            <p class="text-body-1 mb-4">
              {{ searchQuery ? `No articles match your search for "${searchQuery}"` : 'No articles found in this category' }}
            </p>
            <v-btn color="primary" variant="tonal" @click="resetFilters">Reset Filters</v-btn>
          </v-card>
        </v-col>

        <!-- Sidebar -->
        <v-col cols="12" lg="4">
          <!-- Categories Card -->
          <v-card class="mb-6">
            <v-card-title class="font-weight-bold">
              Categories
            </v-card-title>
            <v-divider></v-divider>
            <v-list>
              <v-list-item
                v-for="category in categories"
                :key="category"
                :title="category"
                link
                @click="selectedCategory = category; filterPosts()"
              >
                <template v-slot:prepend>
                  <v-icon icon="mdi-tag"></v-icon>
                </template>
                <template v-slot:append>
                  <v-chip size="small" color="primary" variant="tonal">
                    {{ getCategoryCount(category) }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card>

          <!-- Popular Posts Card -->
          <v-card class="mb-6">
            <v-card-title class="font-weight-bold">
              Popular Articles
            </v-card-title>
            <v-divider></v-divider>
            <v-list lines="two">
              <v-list-item
                v-for="post in popularPosts"
                :key="post.id"
                :title="post.title"
                :subtitle="`${formatDate(post.published_at)} | ${post.view_count} views`"
                link
                :to="`/blog/${post.slug}`"
              >
                <template v-slot:prepend>
                  <v-avatar size="48">
                    <v-img
                      :src="post.image_url || 'https://via.placeholder.com/48x48'"
                      cover
                    ></v-img>
                  </v-avatar>
                </template>
              </v-list-item>
            </v-list>
          </v-card>

          <!-- Newsletter Card -->
          <v-card>
            <v-card-title class="font-weight-bold">
              Subscribe to Newsletter
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <p class="mb-4">Stay up to date with the latest industry news and product updates.</p>
              <v-form @submit.prevent="subscribeNewsletter">
                <v-text-field
                  v-model="email"
                  label="Email Address"
                  variant="outlined"
                  density="comfortable"
                  :rules="[rules.required, rules.email]"
                  hide-details="auto"
                  class="mb-3"
                ></v-text-field>
                <v-checkbox
                  v-model="privacyConsent"
                  :rules="[rules.required]"
                  hide-details="auto"
                  class="mb-3"
                >
                  <template v-slot:label>
                    <div>
                      I agree to the <router-link to="/privacy-policy" class="text-primary">Privacy Policy</router-link>
                    </div>
                  </template>
                </v-checkbox>
                <v-btn
                  type="submit"
                  color="primary"
                  variant="elevated"
                  block
                  :loading="subscribing"
                >
                  Subscribe
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-error text-white pa-4">
          Confirm Delete
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p>Are you sure you want to delete the article:</p>
          <p class="text-subtitle-1 font-weight-medium mt-2">
            "{{ postToDelete?.title }}"
          </p>
          <p class="text-medium-emphasis mt-2">This action cannot be undone.</p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="tonal"
            @click="deleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            @click="deletePost"
            :loading="deleteLoading"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Newsletter Success Dialog -->
    <v-dialog v-model="subscribeDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5 bg-success text-white pa-4">
          Subscription Successful
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p>Thank you for subscribing to our newsletter!</p>
          <p class="text-medium-emphasis mt-2">You'll receive the latest updates and industry news directly to your inbox.</p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            @click="subscribeDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { formatDate } from '@/utils/formatters';

// Blog post interface - would be imported from types in a real app
interface BlogPost {
  id: string;
  title: string;
  slug: string;
  author: string;
  author_id?: string;
  category: string;
  tags?: string[];
  excerpt: string;
  content: string;
  image_url?: string;
  published_at: string;
  is_published: boolean;
  is_featured: boolean;
  view_count: number;
  created_at: string;
  updated_at: string;
}

export default defineComponent({
  name: 'Blog',

  setup() {
    const authStore = useAuthStore();
    const isAdmin = computed(() => authStore.isAdmin);

    // Data loading state
    const loading = ref(true);
    const posts = ref<BlogPost[]>([]);
    const featuredPost = ref<BlogPost | null>(null);
    const popularPosts = ref<BlogPost[]>([]);

    // Pagination
    const page = ref(1);
    const itemsPerPage = ref(5);
    const totalItems = ref(0);
    const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value));

    // Filters and search
    const searchQuery = ref('');
    const selectedCategory = ref<string | null>(null);
    const sortOrder = ref('newest');
    const filteredPosts = ref<BlogPost[]>([]);

    // Newsletter subscription
    const email = ref('');
    const privacyConsent = ref(false);
    const subscribing = ref(false);
    const subscribeDialog = ref(false);

    // Form validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required',
      email: (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    };

    // Delete functionality
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);
    const postToDelete = ref<BlogPost | null>(null);

    // Category and sort options
    const categories = ref([
      'Industry News',
      'Product Updates',
      'Technical Tips',
      'Case Studies',
      'Market Trends',
      'Company News'
    ]);

    const sortOptions = ref([
      { title: 'Newest First', value: 'newest' },
      { title: 'Oldest First', value: 'oldest' },
      { title: 'Most Popular', value: 'popular' },
      { title: 'Alphabetical', value: 'alphabetical' }
    ]);

    // Fetch blog posts from API
    const fetchPosts = async () => {
      loading.value = true;

      try {
        // In a real implementation, this would be an API call
        // const response = await api.get('/blog/posts', {
        //   params: {
        //     page: page.value,
        //     per_page: itemsPerPage.value,
        //     category: selectedCategory.value,
        //     search: searchQuery.value,
        //     sort: sortOrder.value
        //   }
        // });

        // Mock data for demonstration
        await new Promise(resolve => setTimeout(resolve, 500));

        // Sample blog posts
        const mockPosts: BlogPost[] = [
          {
            id: '1',
            title: 'The Future of Electric Vehicle Parts Distribution',
            slug: 'future-of-ev-parts-distribution',
            author: 'Michael Johnson',
            author_id: 'user-1',
            category: 'Market Trends',
            tags: ['Electric Vehicles', 'Distribution', 'Future Trends'],
            excerpt: 'As electric vehicles continue to gain market share, the aftermarket industry faces new challenges and opportunities in parts distribution and inventory management.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=EV+Parts+Distribution',
            published_at: '2023-05-15T09:30:00Z',
            is_published: true,
            is_featured: true,
            view_count: 1245,
            created_at: '2023-05-10T14:20:00Z',
            updated_at: '2023-05-15T09:30:00Z'
          },
          {
            id: '2',
            title: 'Crown Nexus Releases New Inventory Management Features',
            slug: 'crown-nexus-new-inventory-features',
            author: 'Sarah Williams',
            author_id: 'user-2',
            category: 'Product Updates',
            tags: ['Product Update', 'Inventory Management', 'Software'],
            excerpt: 'Our latest platform update introduces advanced inventory forecasting, multi-location management, and integrated supplier ordering capabilities.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=Inventory+Features',
            published_at: '2023-04-28T13:45:00Z',
            is_published: true,
            is_featured: false,
            view_count: 876,
            created_at: '2023-04-25T11:30:00Z',
            updated_at: '2023-04-28T13:45:00Z'
          },
          {
            id: '3',
            title: 'How to Optimize Your Parts Catalog for Maximum Visibility',
            slug: 'optimize-parts-catalog-visibility',
            author: 'James Rodriguez',
            author_id: 'user-3',
            category: 'Technical Tips',
            tags: ['Catalog Management', 'SEO', 'Digital Marketing'],
            excerpt: 'Learn proven strategies to enhance your parts catalog\'s visibility, improve search rankings, and drive more qualified traffic to your products.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=Catalog+Optimization',
            published_at: '2023-04-12T10:15:00Z',
            is_published: true,
            is_featured: false,
            view_count: 1032,
            created_at: '2023-04-10T09:20:00Z',
            updated_at: '2023-04-12T10:15:00Z'
          },
          {
            id: '4',
            title: 'Automotive Aftermarket Forecast: Growth Trends for 2023-2024',
            slug: 'aftermarket-growth-forecast-2023-2024',
            author: 'Emily Chen',
            author_id: 'user-4',
            category: 'Industry News',
            tags: ['Market Analysis', 'Growth', 'Trends', 'Forecast'],
            excerpt: 'Our latest market analysis reveals key growth areas in the automotive aftermarket industry and provides actionable insights for distributors and retailers.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=Market+Forecast',
            published_at: '2023-03-22T14:30:00Z',
            is_published: true,
            is_featured: false,
            view_count: 1587,
            created_at: '2023-03-20T11:45:00Z',
            updated_at: '2023-03-22T14:30:00Z'
          },
          {
            id: '5',
            title: 'Case Study: How AutoPro Increased Sales by 35% with Digital Catalog Integration',
            slug: 'autopro-sales-increase-case-study',
            author: 'David Thompson',
            author_id: 'user-5',
            category: 'Case Studies',
            tags: ['Case Study', 'Success Story', 'Digital Transformation'],
            excerpt: 'Learn how AutoPro Distributors transformed their business by implementing Crown Nexus\'s digital catalog and streamlining their ordering process.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=AutoPro+Case+Study',
            published_at: '2023-03-08T09:15:00Z',
            is_published: true,
            is_featured: false,
            view_count: 923,
            created_at: '2023-03-05T16:20:00Z',
            updated_at: '2023-03-08T09:15:00Z'
          },
          {
            id: '6',
            title: 'Crown Nexus Expands Integration Partnerships with Leading Shop Management Systems',
            slug: 'crown-nexus-integration-partnerships',
            author: 'Lisa Anderson',
            author_id: 'user-6',
            category: 'Company News',
            tags: ['Integration', 'Partnerships', 'Shop Management'],
            excerpt: 'We\'re excited to announce new integration partnerships with five leading shop management systems, providing seamless workflow for automotive repair shops.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=Integration+Partnerships',
            published_at: '2023-02-20T11:45:00Z',
            is_published: true,
            is_featured: false,
            view_count: 768,
            created_at: '2023-02-18T10:30:00Z',
            updated_at: '2023-02-20T11:45:00Z'
          },
          {
            id: '7',
            title: 'Supply Chain Resilience: Strategies for Automotive Parts Distributors',
            slug: 'supply-chain-resilience-strategies',
            author: 'Michael Johnson',
            author_id: 'user-1',
            category: 'Market Trends',
            tags: ['Supply Chain', 'Resilience', 'Strategy'],
            excerpt: 'Discover proven strategies to build supply chain resilience and mitigate disruption risks in the automotive parts distribution business.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=Supply+Chain+Resilience',
            published_at: '2023-02-05T13:20:00Z',
            is_published: true,
            is_featured: false,
            view_count: 1142,
            created_at: '2023-02-03T09:45:00Z',
            updated_at: '2023-02-05T13:20:00Z'
          },
          {
            id: '8',
            title: 'The Growing Importance of Data Quality in Parts Catalogs',
            slug: 'data-quality-importance-parts-catalogs',
            author: 'Sarah Williams',
            author_id: 'user-2',
            category: 'Technical Tips',
            tags: ['Data Quality', 'Catalog Management', 'Best Practices'],
            excerpt: 'High-quality data is essential for effective parts catalogs. Learn why data quality matters and how to implement a data governance strategy.',
            content: 'Full article content would go here...',
            image_url: 'https://via.placeholder.com/800x600?text=Data+Quality',
            published_at: '2023-01-18T10:30:00Z',
            is_published: true,
            is_featured: false,
            view_count: 895,
            created_at: '2023-01-15T14:40:00Z',
            updated_at: '2023-01-18T10:30:00Z'
          }
        ];

        // Set featured post
        featuredPost.value = mockPosts.find(p => p.is_featured) || null;

        // Filter out featured post from main list
        posts.value = mockPosts.filter(p => !p.is_featured);

        // Set popular posts (top 3 by view count)
        popularPosts.value = [...mockPosts]
          .sort((a, b) => b.view_count - a.view_count)
          .slice(0, 3);

        // Apply filters
        applyFilters();

        totalItems.value = posts.value.length;
      } catch (error) {
        console.error('Error fetching blog posts:', error);
      } finally {
        loading.value = false;
      }
    };

    // Apply filters to posts
    const applyFilters = () => {
      // Start with all posts
      let filtered = [...posts.value];

      // Apply category filter
      if (selectedCategory.value) {
        filtered = filtered.filter(post => post.category === selectedCategory.value);
      }

      // Apply search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase();
        filtered = filtered.filter(post =>
          post.title.toLowerCase().includes(query) ||
          post.excerpt.toLowerCase().includes(query) ||
          post.category.toLowerCase().includes(query)
        );
      }

      // Apply sort order
      switch (sortOrder.value) {
        case 'newest':
          filtered.sort((a, b) => new Date(b.published_at).getTime() - new Date(a.published_at).getTime());
          break;
        case 'oldest':
          filtered.sort((a, b) => new Date(a.published_at).getTime() - new Date(b.published_at).getTime());
          break;
        case 'popular':
          filtered.sort((a, b) => b.view_count - a.view_count);
          break;
        case 'alphabetical':
          filtered.sort((a, b) => a.title.localeCompare(b.title));
          break;
      }

      filteredPosts.value = filtered;
    };

    // Filter posts based on current filters
    const filterPosts = () => {
      applyFilters();
    };

    // Search posts
    const searchPosts = () => {
      applyFilters();
    };

    // Clear search
    const clearSearch = () => {
      searchQuery.value = '';
      applyFilters();
    };

    // Reset all filters
    const resetFilters = () => {
      searchQuery.value = '';
      selectedCategory.value = null;
      sortOrder.value = 'newest';
      applyFilters();
    };

    // Get count of posts in a category
    const getCategoryCount = (category: string) => {
      return posts.value.filter(post => post.category === category).length;
    };

    // Subscribe to newsletter
    const subscribeNewsletter = async () => {
      subscribing.value = true;

      try {
        // In a real implementation, this would be an API call
        // await api.post('/newsletter/subscribe', { email: email.value });

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Show success dialog
        subscribeDialog.value = true;

        // Reset form
        email.value = '';
        privacyConsent.value = false;
      } catch (error) {
        console.error('Error subscribing to newsletter:', error);
      } finally {
        subscribing.value = false;
      }
    };

    // Delete confirmation
    const confirmDelete = (post: BlogPost) => {
      postToDelete.value = post;
      deleteDialog.value = true;
    };

    // Delete post
    const deletePost = async () => {
      if (!postToDelete.value) return;

      deleteLoading.value = true;

      try {
        // In a real implementation, this would be an API call
        // await api.delete(`/blog/posts/${postToDelete.value.id}`);

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));

        // Remove post from list
        posts.value = posts.value.filter(p => p.id !== postToDelete.value?.id);

        // Re-apply filters
        applyFilters();

        // Close dialog
        deleteDialog.value = false;
      } catch (error) {
        console.error('Error deleting post:', error);
      } finally {
        deleteLoading.value = false;
      }
    };

    // Watch for filter changes
    watch([selectedCategory, sortOrder], () => {
      applyFilters();
    });

    // Initialize component
    onMounted(() => {
      fetchPosts();
    });

    return {
      isAdmin,
      loading,
      posts,
      featuredPost,
      popularPosts,
      filteredPosts,
      page,
      totalPages,
      searchQuery,
      selectedCategory,
      sortOrder,
      categories,
      sortOptions,
      email,
      privacyConsent,
      subscribing,
      subscribeDialog,
      rules,
      deleteDialog,
      deleteLoading,
      postToDelete,
      formatDate,
      fetchPosts,
      filterPosts,
      searchPosts,
      clearSearch,
      resetFilters,
      getCategoryCount,
      subscribeNewsletter,
      confirmDelete,
      deletePost
    };
  }
});
</script>

<style scoped>
.text-inherit {
  color: inherit;
}

.hover-primary:hover {
  color: rgb(var(--v-theme-primary));
}
</style>
