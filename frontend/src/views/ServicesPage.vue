<!-- frontend/src/views/ServicesPage.vue -->
<template>
  <div class="services-page">
    <!-- Hero Section -->
    <section class="services-hero">
      <v-parallax
        src="https://images.unsplash.com/photo-1591439657848-9f4b9ce3c977?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
        :height="400"
      >
        <div class="hero-overlay"></div>
        <v-container class="hero-content" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" md="10" lg="8" class="text-center text-white">
              <h1 class="text-h2 font-weight-bold mb-4">Our Services</h1>
              <h2 class="text-h5 mb-6">Comprehensive solutions for the automotive aftermarket industry</h2>
            </v-col>
          </v-row>
        </v-container>
      </v-parallax>
    </section>

    <!-- Services Overview -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" md="8" lg="7">
            <h2 class="text-h4 font-weight-bold mb-4">Elevate Your Business</h2>
            <p class="text-body-1 mb-4">
              At Crown Nexus, we go beyond simply supplying aftermarket parts. Our comprehensive service offerings
              are designed to streamline your operations, boost sales, and enhance customer satisfaction.
            </p>
            <p class="text-body-1 mb-4">
              From advanced inventory management to technical support and warranty programs, we provide the tools,
              resources, and expertise you need to thrive in today's competitive market.
            </p>
            <v-btn
              color="primary"
              size="large"
              variant="tonal"
              prepend-icon="mdi-account-tie"
              to="/contact"
              class="mt-2"
            >
              Speak With a Specialist
            </v-btn>
          </v-col>
          <v-col cols="12" md="4" lg="5" class="d-flex align-center justify-center">
            <v-img
              src="https://images.unsplash.com/photo-1553877522-43269d4ea984?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
              max-width="400"
              class="rounded-lg"
            ></v-img>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Main Services Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Core Services</h2>
            <p class="text-subtitle-1">Comprehensive solutions tailored to your business needs</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(service, i) in coreServices" :key="i" cols="12" md="6">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                height="100%"
                class="d-flex flex-column"
              >
                <v-img
                  :src="service.image"
                  height="200"
                  cover
                  class="align-end"
                  gradient="to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.6) 100%"
                >
                  <v-card-title class="text-white">
                    <v-icon :icon="service.icon" start class="me-2"></v-icon>
                    {{ service.title }}
                  </v-card-title>
                </v-img>
                <v-card-text class="text-body-1 flex-grow-1 pa-4">
                  <p class="mb-4">{{ service.description }}</p>
                  <v-list density="compact" class="pa-0 bg-transparent">
                    <v-list-item v-for="(feature, j) in service.features" :key="j" :title="feature">
                      <template v-slot:prepend>
                        <v-icon icon="mdi-check-circle" color="success" size="small"></v-icon>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card-text>
                <v-card-actions class="pa-4 pt-0">
                  <v-btn
                    variant="text"
                    :color="service.color"
                    :to="service.link"
                  >
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

    <!-- Specialized Services -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Specialized Services</h2>
            <p class="text-subtitle-1">Additional offerings to enhance your business operations</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(service, i) in specializedServices" :key="i" cols="12" sm="6" lg="4">
            <v-card height="100%" class="d-flex flex-column">
              <v-card-item>
                <template v-slot:prepend>
                  <v-avatar :color="service.color" size="48" class="me-4">
                    <v-icon size="24" :icon="service.icon" color="white"></v-icon>
                  </v-avatar>
                </template>
                <v-card-title>{{ service.title }}</v-card-title>
              </v-card-item>
              <v-card-text class="text-body-1 flex-grow-1">
                {{ service.description }}
              </v-card-text>
              <v-card-actions>
                <v-btn
                  variant="text"
                  :color="service.color"
                  :to="service.link"
                >
                  Details
                  <v-icon end icon="mdi-arrow-right"></v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Technology Platform Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Our Technology Platform</h2>
            <p class="text-subtitle-1">Streamlining your business with advanced digital solutions</p>
          </v-col>
        </v-row>

        <v-row align="center">
          <v-col cols="12" md="6" class="mb-8 mb-md-0">
            <v-img
              src="https://images.unsplash.com/photo-1573164713619-24c711fe7878?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
              class="rounded-xl"
              max-width="500"
              max-height="400"
            ></v-img>
          </v-col>
          <v-col cols="12" md="6">
            <h3 class="text-h5 font-weight-bold mb-4">Digital Transformation for Aftermarket Businesses</h3>
            <p class="text-body-1 mb-4">
              Our proprietary B2B platform is designed specifically for the automotive aftermarket industry,
              integrating seamlessly with your existing systems and workflows.
            </p>
            <v-list>
              <v-list-item
                v-for="(feature, i) in technologyFeatures"
                :key="i"
                :title="feature.title"
                :subtitle="feature.description"
              >
                <template v-slot:prepend>
                  <v-avatar :color="feature.color" size="36">
                    <v-icon size="20" :icon="feature.icon" color="white"></v-icon>
                  </v-avatar>
                </template>
              </v-list-item>
            </v-list>
            <v-btn
              color="primary"
              size="large"
              variant="tonal"
              prepend-icon="mdi-monitor-dashboard"
              class="mt-6"
              to="/demo"
            >
              Request a Platform Demo
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Warranty Section -->
    <section class="py-12 bg-primary">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="7" class="text-white">
            <h2 class="text-h4 font-weight-bold mb-4">Crown Nexus Warranty Program</h2>
            <p class="text-body-1 mb-4">
              Our industry-leading warranty program provides peace of mind for you and your customers.
              We stand behind the quality of our products with comprehensive coverage and hassle-free claims processing.
            </p>
            <v-row class="mt-6">
              <v-col v-for="(feature, i) in warrantyFeatures" :key="i" cols="12" sm="6">
                <div class="d-flex mb-4">
                  <v-icon :icon="feature.icon" color="white" size="24" class="me-3 mt-1"></v-icon>
                  <div>
                    <h4 class="text-h6 font-weight-bold mb-1">{{ feature.title }}</h4>
                    <p>{{ feature.description }}</p>
                  </div>
                </div>
              </v-col>
            </v-row>
            <v-btn
              color="white"
              variant="outlined"
              size="large"
              class="mt-4 text-white"
              to="/warranty"
            >
              View Warranty Details
            </v-btn>
          </v-col>
          <v-col cols="12" md="5" class="text-center">
            <v-sheet color="white" class="pa-6 rounded-lg">
              <v-icon icon="mdi-shield-check" color="primary" size="64" class="mb-4"></v-icon>
              <h3 class="text-h5 font-weight-bold mb-3">Premium Protection</h3>
              <v-list density="compact" lines="two">
                <v-list-item
                  v-for="(item, i) in warrantyItems"
                  :key="i"
                  :title="item.category"
                  :subtitle="item.coverage"
                >
                  <template v-slot:prepend>
                    <v-icon icon="mdi-check" color="success"></v-icon>
                  </template>
                </v-list-item>
              </v-list>
              <v-btn
                color="primary"
                variant="tonal"
                class="mt-4"
                to="/warranty-registration"
              >
                Register Warranty
              </v-btn>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Training & Support Section -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Training & Technical Support</h2>
            <p class="text-subtitle-1">Expert resources to empower your team</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(training, i) in trainingOptions" :key="i" cols="12" md="6" class="mb-6">
            <v-card>
              <v-img
                :src="training.image"
                height="200"
                cover
              ></v-img>
              <v-card-title class="text-h5">{{ training.title }}</v-card-title>
              <v-card-text class="text-body-1">
                <p>{{ training.description }}</p>
                <v-chip-group class="mt-4">
                  <v-chip
                    v-for="(tag, j) in training.tags"
                    :key="j"
                    color="primary"
                    variant="outlined"
                    size="small"
                  >
                    {{ tag }}
                  </v-chip>
                </v-chip-group>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="primary"
                  variant="tonal"
                  :to="training.link"
                >
                  Learn More
                </v-btn>
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-row class="mt-6">
          <v-col cols="12" class="text-center">
            <v-btn
              color="primary"
              size="large"
              to="/resources"
              prepend-icon="mdi-book-open-variant"
            >
              View All Resources
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Business Programs Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-8">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">Business Programs</h2>
            <p class="text-subtitle-1">Specialized partnership opportunities to grow your business</p>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col v-for="(program, i) in businessPrograms" :key="i" cols="12" sm="6" lg="4">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                height="100%"
                class="d-flex flex-column"
                :class="isHovering ? 'on-hover' : ''"
              >
                <v-card-item :class="`bg-${program.color}`">
                  <template v-slot:prepend>
                    <v-avatar :color="program.color" size="48" class="me-4" variant="tonal">
                      <v-icon size="24" :icon="program.icon" color="white"></v-icon>
                    </v-avatar>
                  </template>
                  <v-card-title class="text-white">{{ program.title }}</v-card-title>
                </v-card-item>
                <v-card-text class="text-body-1 flex-grow-1 pa-4">
                  <p class="mb-4">{{ program.description }}</p>
                  <div class="mt-4">
                    <div class="d-flex align-center mb-2" v-for="(benefit, j) in program.benefits" :key="j">
                      <v-icon icon="mdi-check-circle" color="success" size="small" class="me-2"></v-icon>
                      <span>{{ benefit }}</span>
                    </div>
                  </div>
                </v-card-text>
                <v-card-actions class="pa-4">
                  <v-spacer></v-spacer>
                  <v-btn
                    :color="program.color"
                    variant="tonal"
                    :to="program.link"
                  >
                    Program Details
                  </v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Testimonials -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold">What Our Partners Say</h2>
            <p class="text-subtitle-1">Hear from businesses using our services</p>
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
                <v-sheet class="px-6 py-6 d-flex align-center justify-center">
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

        <v-row class="mt-6">
          <v-col cols="12" class="text-center">
            <v-btn
              color="primary"
              variant="tonal"
              to="/testimonials"
              prepend-icon="mdi-account-voice"
            >
              View All Testimonials
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="py-12 bg-primary">
      <v-container>
        <v-row align="center" justify="center">
          <v-col cols="12" md="8" lg="6" class="text-center text-white">
            <h2 class="text-h4 font-weight-bold mb-4">Ready to enhance your business?</h2>
            <p class="text-body-1 mb-6">
              Speak with a Crown Nexus specialist to discover how our services can benefit your company.
            </p>
            <v-btn
              color="white"
              size="large"
              to="/contact"
              variant="elevated"
              class="mx-2"
            >
              Contact Us
              <v-icon end icon="mdi-arrow-right"></v-icon>
            </v-btn>
            <v-btn
              color="white"
              size="large"
              variant="outlined"
              class="text-white mx-2"
              to="/demo"
            >
              Request a Demo
              <v-icon end icon="mdi-presentation"></v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

interface CoreService {
  title: string;
  description: string;
  image: string;
  icon: string;
  color: string;
  features: string[];
  link: string;
}

interface SpecializedService {
  title: string;
  description: string;
  icon: string;
  color: string;
  link: string;
}

interface TechFeature {
  title: string;
  description: string;
  icon: string;
  color: string;
}

interface WarrantyFeature {
  title: string;
  description: string;
  icon: string;
}

interface WarrantyItem {
  category: string;
  coverage: string;
}

interface TrainingOption {
  title: string;
  description: string;
  image: string;
  tags: string[];
  link: string;
}

interface BusinessProgram {
  title: string;
  description: string;
  icon: string;
  color: string;
  benefits: string[];
  link: string;
}

interface Testimonial {
  quote: string;
  name: string;
  position: string;
  company: string;
  avatar: string;
  rating: number;
}

export default defineComponent({
  name: 'ServicesPage',

  setup() {
    // Core services data
    const coreServices = ref<CoreService[]>([
      {
        title: 'Distribution & Logistics',
        description: 'Our advanced distribution network ensures fast, reliable delivery of the parts you need, when you need them.',
        image: 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        icon: 'mdi-truck-fast',
        color: 'primary',
        features: [
          'Nationwide distribution network',
          'Next-day delivery available to 85% of U.S.',
          'Real-time inventory visibility',
          'Advanced order tracking',
          'Fleet management solutions'
        ],
        link: '/services/distribution'
      },
      {
        title: 'Inventory Management',
        description: 'Optimize your parts inventory with our data-driven management tools and real-time analytics.',
        image: 'https://images.unsplash.com/photo-1566576721346-d4a3b4eaeb55?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        icon: 'mdi-package-variant-closed',
        color: 'info',
        features: [
          'Automated inventory replenishment',
          'Demand forecasting',
          'Seasonal trend analysis',
          'Stock level optimization',
          'Inventory health reports'
        ],
        link: '/services/inventory'
      },
      {
        title: 'Technical Support',
        description: 'Access expert technical assistance for product selection, installation, and troubleshooting.',
        image: 'https://images.unsplash.com/photo-1581092921461-b504ef8db5b9?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        icon: 'mdi-headset',
        color: 'success',
        features: [
          'Phone and online support',
          'Installation guidance',
          'Troubleshooting assistance',
          'Technical documentation',
          'Product training'
        ],
        link: '/services/technical-support'
      },
      {
        title: 'Marketing Support',
        description: 'Enhance your sales with customized marketing materials, promotions, and digital assets.',
        image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        icon: 'mdi-bullhorn',
        color: 'warning',
        features: [
          'Customizable marketing materials',
          'Digital asset library',
          'Seasonal promotions',
          'Point-of-sale displays',
          'Co-branded opportunities'
        ],
        link: '/services/marketing'
      }
    ]);

    // Specialized services data
    const specializedServices = ref<SpecializedService[]>([
      {
        title: 'Custom Catalog Development',
        description: 'Create customized print and digital catalogs tailored to your specific customer base and market focus.',
        icon: 'mdi-book-open-page-variant',
        color: 'primary',
        link: '/services/custom-catalogs'
      },
      {
        title: 'Business Intelligence',
        description: 'Gain valuable insights with advanced analytics and reporting on sales trends, market performance, and inventory optimization.',
        icon: 'mdi-chart-bell-curve',
        color: 'info',
        link: '/services/business-intelligence'
      },
      {
        title: 'Warranty Administration',
        description: 'Streamline your warranty process with our end-to-end warranty management system and claims processing.',
        icon: 'mdi-shield-check',
        color: 'success',
        link: '/services/warranty'
      },
      {
        title: 'E-commerce Integration',
        description: 'Seamlessly connect our catalog and inventory systems with your e-commerce platform for a unified customer experience.',
        icon: 'mdi-shopping',
        color: 'error',
        link: '/services/ecommerce'
      },
      {
        title: 'Product Training',
        description: 'Enhance your team\'s product knowledge with comprehensive training programs delivered online or at your location.',
        icon: 'mdi-school',
        color: 'warning',
        link: '/services/training'
      },
      {
        title: 'Returns Management',
        description: 'Simplify the returns process with our streamlined system for processing, evaluating, and crediting returned items.',
        icon: 'mdi-arrow-u-left-top',
        color: 'secondary',
        link: '/services/returns'
      }
    ]);

    // Technology platform features
    const technologyFeatures = ref<TechFeature[]>([
      {
        title: 'Real-Time Inventory Management',
        description: 'Access instant inventory updates across all distribution centers',
        icon: 'mdi-database-sync',
        color: 'primary'
      },
      {
        title: 'Advanced Fitment Search',
        description: 'Find the exact parts for any vehicle with our comprehensive database',
        icon: 'mdi-car-search',
        color: 'info'
      },
      {
        title: 'Order Automation',
        description: 'Set up automatic reordering based on custom triggers and thresholds',
        icon: 'mdi-refresh-auto',
        color: 'success'
      },
      {
        title: 'Business Analytics Dashboard',
        description: 'Visualize sales trends, inventory health, and business performance',
        icon: 'mdi-chart-box',
        color: 'warning'
      },
      {
        title: 'API Integration',
        description: 'Connect seamlessly with your existing business systems',
        icon: 'mdi-api',
        color: 'error'
      }
    ]);

    // Warranty features
    const warrantyFeatures = ref<WarrantyFeature[]>([
      {
        title: 'Streamlined Claims Processing',
        description: 'Submit and track warranty claims through our online portal for faster resolution',
        icon: 'mdi-clipboard-flow'
      },
      {
        title: 'Extended Coverage Options',
        description: 'Choose from various warranty plans to meet your business needs',
        icon: 'mdi-shield-plus'
      },
      {
        title: 'Transferable Warranties',
        description: 'Warranties follow the part, not the purchaser, for added customer value',
        icon: 'mdi-transfer'
      },
      {
        title: 'Online Warranty Registration',
        description: 'Register warranties digitally for instant confirmation and documentation',
        icon: 'mdi-file-document-edit'
      }
    ]);

    // Warranty items
    const warrantyItems = ref<WarrantyItem[]>([
      {
        category: 'Brake Components',
        coverage: '24 months / Unlimited miles'
      },
      {
        category: 'Suspension Parts',
        coverage: '36 months / 36,000 miles'
      },
      {
        category: 'Engine Components',
        coverage: 'Limited Lifetime Warranty'
      },
      {
        category: 'Electrical Parts',
        coverage: '12 months / 12,000 miles'
      },
      {
        category: 'Interior Accessories',
        coverage: '12 months from purchase'
      }
    ]);

    // Training options
    const trainingOptions = ref<TrainingOption[]>([
      {
        title: 'Technical Training Program',
        description: 'In-depth technical training on product installation, diagnostics, and troubleshooting, available both online and through in-person workshops.',
        image: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        tags: ['Workshop', 'Certification', 'Hands-on', 'Technical'],
        link: '/training/technical'
      },
      {
        title: 'Business Management Resources',
        description: 'Resources designed to help shop owners and managers optimize operations, improve customer service, and increase profitability.',
        image: 'https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        tags: ['Business', 'Management', 'Efficiency', 'Growth'],
        link: '/training/business'
      },
      {
        title: 'Online Learning Portal',
        description: 'Access our comprehensive library of on-demand training videos, interactive courses, and reference materials.',
        image: 'https://images.unsplash.com/photo-1610484826917-0f133e1070b7?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        tags: ['Online', 'Self-paced', 'Video', 'Interactive'],
        link: '/training/online'
      },
      {
        title: 'Customized Team Training',
        description: 'Let us create a tailored training program for your entire team, focusing on the specific products and skills relevant to your business.',
        image: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
        tags: ['Team', 'Customized', 'On-site', 'Specialized'],
        link: '/training/custom'
      }
    ]);

    // Business programs
    const businessPrograms = ref<BusinessProgram[]>([
      {
        title: 'Premium Partner Program',
        description: 'Our elite partnership program offering maximum discounts, priority service, and exclusive benefits.',
        icon: 'mdi-star',
        color: 'warning',
        benefits: [
          'Highest volume discounts',
          'Priority shipping',
          'Dedicated account manager',
          'Extended payment terms',
          'Marketing co-op funds'
        ],
        link: '/programs/premium'
      },
      {
        title: 'Professional Installer Program',
        description: 'Tailored for repair shops and service centers with installation-focused benefits and support.',
        icon: 'mdi-wrench',
        color: 'primary',
        benefits: [
          'Technical training access',
          'Installation hotline',
          'Labor reimbursement program',
          'Tool purchase incentives',
          'Customer referral program'
        ],
        link: '/programs/installer'
      },
      {
        title: 'Distributor Alliance',
        description: 'Strategic partnership program for regional distributors looking to expand their product offerings.',
        icon: 'mdi-handshake',
        color: 'success',
        benefits: [
          'Wholesale pricing structure',
          'Drop-ship capabilities',
          'White-label options',
          'Territory protection',
          'Inventory financing'
        ],
        link: '/programs/distributor'
      }
    ]);

    // Testimonials data
    const testimonials = ref<Testimonial[]>([
      {
        quote: "Crown Nexus's technical support service has been invaluable to our shop. Their experts help us diagnose complex issues and recommend the right parts, saving us time and improving customer satisfaction.",
        name: "Robert Martinez",
        position: "Owner",
        company: "Martinez Auto Repair",
        avatar: "https://randomuser.me/api/portraits/men/32.jpg",
        rating: 5
      },
      {
        quote: "The inventory management system has transformed our parts department. We've reduced our carrying costs by 23% while increasing availability. The demand forecasting feature is remarkably accurate.",
        name: "Jennifer Thompson",
        position: "Parts Manager",
        company: "Thompson Auto Group",
        avatar: "https://randomuser.me/api/portraits/women/44.jpg",
        rating: 5
      },
      {
        quote: "As a distributor, the logistics service Crown Nexus provides is a game-changer. Their nationwide network allows us to promise next-day delivery to our customers without maintaining excessive inventory.",
        name: "Michael Rogers",
        position: "Operations Director",
        company: "Pacific Parts Distributors",
        avatar: "https://randomuser.me/api/portraits/men/67.jpg",
        rating: 4
      }
    ]);

    return {
      coreServices,
      specializedServices,
      technologyFeatures,
      warrantyFeatures,
      warrantyItems,
      trainingOptions,
      businessPrograms,
      testimonials
    };
  }
});
</script>

<style scoped>
.services-hero {
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

.testimonial-card {
  border-radius: 16px;
}
</style>
