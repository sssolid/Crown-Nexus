<!-- frontend/src/views/LandingPage.vue -->
<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <v-parallax
        :src="homePageHeroBanner"
        :height="600"
      >
        <div class="hero-overlay"></div>
        <v-container class="hero-content" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" md="8" lg="6" class="text-center text-white">
              <h1 class="text-h2 font-weight-bold mb-4">Crown Nexus</h1>
              <h2 class="text-h5 mb-6">The Premier B2B Platform for Automotive Aftermarket Parts</h2>
              <p class="text-body-1 mb-8">
                Streamline your inventory management, discover new products, and grow your business with our comprehensive catalog and inventory system.
              </p>
              <div>
                <v-btn
                  to="/login"
                  color="primary"
                  size="large"
                  class="me-4"
                  variant="elevated"
                >
                  Sign In
                  <v-icon end icon="mdi-login"></v-icon>
                </v-btn>
                <v-btn
                  to="/products"
                  color="white"
                  size="large"
                  variant="outlined"
                  class="text-white"
                >
                  Browse Catalog
                  <v-icon end icon="mdi-arrow-right"></v-icon>
                </v-btn>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-parallax>
    </section>

    <!-- Features Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold mb-2">Why Choose Crown Nexus</h2>
            <p class="text-subtitle-1">Designed specifically for the automotive aftermarket industry</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                height="100%"
                class="d-flex flex-column"
              >
                <v-card-item>
                  <template v-slot:prepend>
                    <v-avatar color="primary" size="48" class="me-4">
                      <v-icon size="24" icon="mdi-package-variant-closed" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title class="text-h5">Extensive Product Catalog</v-card-title>
                </v-card-item>
                <v-card-text class="text-body-1 flex-grow-1">
                  Access thousands of high-quality aftermarket parts with detailed specifications, fitment data, and pricing information all in one place.
                </v-card-text>
                <v-card-actions>
                  <v-btn variant="text" color="primary" to="/products">
                    Explore Products
                    <v-icon end icon="mdi-arrow-right"></v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>

          <v-col cols="12" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                height="100%"
                class="d-flex flex-column"
              >
                <v-card-item>
                  <template v-slot:prepend>
                    <v-avatar color="success" size="48" class="me-4">
                      <v-icon size="24" icon="mdi-car" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title class="text-h5">Advanced Fitment Search</v-card-title>
                </v-card-item>
                <v-card-text class="text-body-1 flex-grow-1">
                  Find the exact parts you need with our comprehensive vehicle compatibility database. Filter by year, make, model, engine, and more.
                </v-card-text>
                <v-card-actions>
                  <v-btn variant="text" color="success" to="/fitments">
                    Browse Fitments
                    <v-icon end icon="mdi-arrow-right"></v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>

          <v-col cols="12" md="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                height="100%"
                class="d-flex flex-column"
              >
                <v-card-item>
                  <template v-slot:prepend>
                    <v-avatar color="info" size="48" class="me-4">
                      <v-icon size="24" icon="mdi-account-group" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title class="text-h5">B2B Account Management</v-card-title>
                </v-card-item>
                <v-card-text class="text-body-1 flex-grow-1">
                  Manage your team's access with custom permissions, view order history, and maintain your business profile all in one secure platform.
                </v-card-text>
                <v-card-actions>
                  <v-btn variant="text" color="info">
                    Learn More
                    <v-icon end icon="mdi-arrow-right"></v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Metrics Section -->
    <section class="py-12 bg-primary">
      <v-container>
        <v-row>
          <v-col cols="12" sm="6" md="3">
            <div class="text-center text-white">
              <div class="text-h2 font-weight-bold mb-2">10,000+</div>
              <div class="text-h6">Products</div>
            </div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-center text-white">
              <div class="text-h2 font-weight-bold mb-2">5,000+</div>
              <div class="text-h6">Fitments</div>
            </div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-center text-white">
              <div class="text-h2 font-weight-bold mb-2">500+</div>
              <div class="text-h6">B2B Customers</div>
            </div>
          </v-col>
          <v-col cols="12" sm="6" md="3">
            <div class="text-center text-white">
              <div class="text-h2 font-weight-bold mb-2">99.9%</div>
              <div class="text-h6">Uptime</div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Featured Categories -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold mb-2">Featured Categories</h2>
            <p class="text-subtitle-1">Browse our most popular product lines</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="category in featuredCategories" :key="category.id" cols="12" sm="6" md="4" lg="3">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                :class="{ 'on-hover': isHovering }"
                @click="goToCategory(category.id)"
                class="category-card"
              >
                <v-img
                  :src="category.image"
                  height="200"
                  cover
                  class="align-end"
                  gradient="to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%"
                >
                  <v-card-title class="text-white">{{ category.name }}</v-card-title>
                </v-img>
                <v-card-text>
                  <div class="d-flex align-center justify-space-between">
                    <span>{{ category.productCount }} Products</span>
                    <v-btn
                      variant="text"
                      icon="mdi-arrow-right"
                      color="primary"
                      @click.stop="goToCategory(category.id)"
                    ></v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>

        <v-row class="mt-6">
          <v-col cols="12" class="text-center">
            <v-btn
              color="primary"
              size="large"
              variant="tonal"
              to="/products"
              prepend-icon="mdi-view-grid"
            >
              View All Categories
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Testimonials -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold mb-2">Trusted by Industry Leaders</h2>
            <p class="text-subtitle-1">See what our customers have to say</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-carousel
              hide-delimiters
              show-arrows="hover"
              height="auto"
              :continuous="false"
            >
              <v-carousel-item v-for="(testimonial, i) in testimonials" :key="i">
                <v-sheet class="px-6 py-12 d-flex align-center justify-center">
                  <v-row>
                    <v-col cols="12" md="8" offset-md="2">
                      <v-card elevation="2" class="pa-6 testimonial-card">
                        <div class="d-flex flex-column align-center mb-6">
                          <v-avatar size="96" class="mb-4">
                            <v-img :src="testimonial.avatar"></v-img>
                          </v-avatar>
                          <v-rating
                            :model-value="testimonial.rating"
                            color="amber"
                            density="compact"
                            size="small"
                            readonly
                          ></v-rating>
                        </div>
                        <blockquote class="text-body-1 text-center mb-6">
                          "{{ testimonial.quote }}"
                        </blockquote>
                        <div class="text-center">
                          <div class="text-h6 font-weight-bold mb-1">{{ testimonial.name }}</div>
                          <div class="text-caption">{{ testimonial.position }}, {{ testimonial.company }}</div>
                        </div>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-sheet>
              </v-carousel-item>
            </v-carousel>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="py-12 bg-primary">
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" md="8" lg="6" class="text-center text-white">
            <h2 class="text-h4 font-weight-bold mb-4">Ready to streamline your parts ordering?</h2>
            <p class="text-body-1 mb-6">
              Join thousands of automotive businesses that trust Crown Nexus for their aftermarket parts needs.
            </p>
            <v-btn
              color="white"
              size="large"
              to="/login"
              variant="elevated"
              class="mx-2"
            >
              Get Started
              <v-icon end icon="mdi-arrow-right"></v-icon>
            </v-btn>
            <v-btn
              color="white"
              size="large"
              variant="outlined"
              class="text-white mx-2"
              href="mailto:sales@crownnexus.com"
            >
              Contact Sales
              <v-icon end icon="mdi-email"></v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Footer is now handled by the layout system -->
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import homePageHeroBanner from '@/assets/marketing_landing/home_page_hero_banner.png';
import productCatalogBrakeSystem from '@/assets/product_catalog/brake_systems.png';
import productCatalogSuspensionSystem from '@/assets/product_catalog/suspension_parts.png';
import productCatalogEngineComponents from '@/assets/product_catalog/engine_components.png';
import productCatalogElectricalSystems from '@/assets/product_catalog/electrical_systems.png';
import productCatalogInteriorAccessories from '@/assets/product_catalog/interior_accessories.png';
import productCatalogExteriorAccessories from '@/assets/product_catalog/exterior_accessories.png';
import productCatalogMaintenanceItems from '@/assets/product_catalog/maintenance_items.png';
import productCatalogPerformanceParts from '@/assets/product_catalog/performance_parts.png';

interface FeaturedCategory {
  id: string;
  name: string;
  image: string;
  productCount: number;
}

interface Testimonial {
  quote: string;
  name: string;
  position: string;
  company: string;
  avatar: string;
  rating: number;
}

// Setup router
const router = useRouter();

// Featured categories data
const featuredCategories = ref<FeaturedCategory[]>([
  {
    id: 'brakes',
    name: 'Brake Systems',
    image: productCatalogBrakeSystem,
    productCount: 423
  },
  {
    id: 'suspension',
    name: 'Suspension',
    image: productCatalogSuspensionSystem,
    productCount: 358
  },
  {
    id: 'engine',
    name: 'Engine Components',
    image: productCatalogEngineComponents,
    productCount: 621
  },
  {
    id: 'electrical',
    name: 'Electrical Systems',
    image: productCatalogElectricalSystems,
    productCount: 287
  },
  {
    id: 'interior',
    name: 'Interior Accessories',
    image: productCatalogInteriorAccessories,
    productCount: 514
  },
  {
    id: 'exterior',
    name: 'Body & Exterior',
    image: productCatalogExteriorAccessories,
    productCount: 389
  },
  {
    id: 'maintenance',
    name: 'Maintenance Items',
    image: productCatalogMaintenanceItems,
    productCount: 276
  },
  {
    id: 'performance',
    name: 'Performance Parts',
    image: productCatalogPerformanceParts,
    productCount: 193
  },
]);

// Testimonials data
const testimonials = ref<Testimonial[]>([
  {
    quote: "Crown Nexus has revolutionized how we manage our aftermarket parts inventory. The platform's ease of use and comprehensive database have saved us countless hours and increased our sales by 30%.",
    name: "Michael Johnson",
    position: "Operations Manager",
    company: "AutoPro Distributors",
    avatar: "https://randomuser.me/api/portraits/men/32.jpg",
    rating: 5
  },
  {
    quote: "The fitment search functionality is a game-changer. We can quickly find the exact parts needed for specific vehicles, eliminating guesswork and reducing returns dramatically.",
    name: "Sarah Williams",
    position: "Purchasing Director",
    company: "Elite Auto Parts",
    avatar: "https://randomuser.me/api/portraits/women/44.jpg",
    rating: 5
  },
  {
    quote: "As a growing chain of auto repair shops, Crown Nexus gives us the ability to centralize our parts ordering across all locations. The platform's reliability and customer support are unmatched.",
    name: "David Chen",
    position: "CEO",
    company: "FastFix Auto Centers",
    avatar: "https://randomuser.me/api/portraits/men/67.jpg",
    rating: 4
  },
]);

// Navigation function
const goToCategory = (categoryId: string) => {
  router.push(`/products?category=${categoryId}`);
};
</script>

<style scoped>
.hero-section {
  position: relative;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
}

.hero-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  align-items: center;
}

.on-hover {
  transition: all 0.3s ease;
}

.category-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.category-card:hover {
  transform: translateY(-5px);
}

.testimonial-card {
  border-radius: 16px;
}
</style>
