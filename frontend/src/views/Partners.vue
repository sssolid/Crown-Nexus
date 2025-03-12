<!-- frontend/src/views/Partners.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Hero Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card class="bg-primary" elevation="0">
            <v-img
              src="https://via.placeholder.com/1600x500?text=Our+Partners+and+Integrations"
              height="350"
              cover
              gradient="to bottom, rgba(0,0,0,.4), rgba(0,0,0,.7)"
            >
              <v-container class="fill-height">
                <v-row align="center" justify="center">
                  <v-col cols="12" md="8" class="text-center">
                    <h1 class="text-h2 font-weight-bold text-white mb-4">Our Partners</h1>
                    <p class="text-h6 text-white mb-6">
                      Collaborating with industry leaders to provide the best solutions for the automotive aftermarket
                    </p>
                    <v-btn
                      color="white"
                      variant="elevated"
                      size="large"
                      to="/contact?inquiry=partnership"
                    >
                      Become a Partner
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-img>
          </v-card>
        </v-col>
      </v-row>

      <!-- Partner Types Tabs -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card>
            <v-tabs
              v-model="activeTab"
              color="primary"
              align-tabs="center"
              grow
            >
              <v-tab value="manufacturers">Manufacturers</v-tab>
              <v-tab value="distributors">Distributors</v-tab>
              <v-tab value="technology">Technology Partners</v-tab>
              <v-tab value="industry">Industry Affiliations</v-tab>
            </v-tabs>

            <v-window v-model="activeTab">
              <!-- Manufacturers Tab -->
              <v-window-item value="manufacturers">
                <v-container>
                  <v-row class="mb-6">
                    <v-col cols="12">
                      <h2 class="text-h4 font-weight-bold mb-2">Manufacturing Partners</h2>
                      <p class="text-subtitle-1 mb-6">
                        Crown Nexus collaborates with leading automotive parts manufacturers to provide comprehensive catalog data and streamline supply chain operations.
                      </p>
                    </v-col>
                  </v-row>
                  
                  <!-- Featured Manufacturing Partners -->
                  <v-row>
                    <v-col
                      v-for="partner in featuredManufacturers"
                      :key="partner.id"
                      cols="12"
                      md="6"
                    >
                      <v-card class="mb-4 partner-card h-100">
                        <v-row no-gutters>
                          <v-col cols="4">
                            <v-img
                              :src="partner.logo || 'https://via.placeholder.com/200x200'"
                              height="100%"
                              cover
                              class="bg-grey-lighten-3 h-100"
                              contain
                            ></v-img>
                          </v-col>
                          <v-col cols="8">
                            <v-card-item>
                              <v-card-title>{{ partner.name }}</v-card-title>
                              <v-card-subtitle>{{ partner.category }}</v-card-subtitle>
                            </v-card-item>
                            <v-card-text>
                              <p>{{ partner.description }}</p>
                            </v-card-text>
                            <v-card-actions>
                              <v-btn
                                variant="text"
                                color="primary"
                                :href="partner.website"
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                Visit Website
                                <v-icon end icon="mdi-open-in-new"></v-icon>
                              </v-btn>
                            </v-card-actions>
                          </v-col>
                        </v-row>
                      </v-card>
                    </v-col>
                  </v-row>
                  
                  <!-- All Manufacturing Partners Grid -->
                  <v-row class="mt-8">
                    <v-col cols="12">
                      <h3 class="text-h5 font-weight-bold mb-4">All Manufacturing Partners</h3>
                    </v-col>
                  </v-row>
                  
                  <v-row>
                    <v-col
                      v-for="partner in manufacturingPartners"
                      :key="partner.id"
                      cols="6"
                      sm="4"
                      md="3"
                      lg="2"
                    >
                      <v-card class="pa-2 partner-logo-card">
                        <v-img
                          :src="partner.logo || 'https://via.placeholder.com/200x200'"
                          height="100"
                          contain
                          class="mb-2"
                        ></v-img>
                        <v-card-text class="text-center pa-1">
                          <div class="text-subtitle-2 font-weight-medium">{{ partner.name }}</div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-container>
              </v-window-item>

              <!-- Distributors Tab -->
              <v-window-item value="distributors">
                <v-container>
                  <v-row class="mb-6">
                    <v-col cols="12">
                      <h2 class="text-h4 font-weight-bold mb-2">Distributor Network</h2>
                      <p class="text-subtitle-1 mb-6">
                        Our extensive network of distributor partners helps deliver parts efficiently across North America and beyond.
                      </p>
                    </v-col>
                  </v-row>
                  
                  <!-- Map of Distributor Network -->
                  <v-row class="mb-8">
                    <v-col cols="12">
                      <v-card class="pa-4">
                        <v-card-text class="text-center">
                          <img 
                            src="https://via.placeholder.com/1200x600?text=Distributor+Network+Map" 
                            alt="Distributor Network Map"
                            style="max-width: 100%; height: auto;"
                            class="rounded"
                          />
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  
                  <!-- Distributor Categories -->
                  <v-row>
                    <v-col
                      v-for="category in distributorCategories"
                      :key="category.id"
                      cols="12"
                      md="4"
                    >
                      <v-card class="h-100" :color="category.color" variant="outlined">
                        <v-card-item>
                          <template v-slot:prepend>
                            <v-avatar :color="category.color" size="48">
                              <v-icon color="white" size="24" :icon="category.icon"></v-icon>
                            </v-avatar>
                          </template>
                          <v-card-title>{{ category.name }}</v-card-title>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ category.description }}</p>
                          <v-list density="compact" :bg-color="category.color + '-lighten-5'">
                            <v-list-subheader>Top Partners</v-list-subheader>
                            <v-list-item
                              v-for="partner in category.topPartners"
                              :key="partner.id"
                              :title="partner.name"
                              :subtitle="partner.location"
                            ></v-list-item>
                          </v-list>
                        </v-card-text>
                        <v-card-actions>
                          <v-btn
                            variant="tonal"
                            :color="category.color"
                            :to="`/distributors/${category.id}`"
                          >
                            View All {{ category.name }}
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-container>
              </v-window-item>

              <!-- Technology Partners Tab -->
              <v-window-item value="technology">
                <v-container>
                  <v-row class="mb-6">
                    <v-col cols="12">
                      <h2 class="text-h4 font-weight-bold mb-2">Technology Partners & Integrations</h2>
                      <p class="text-subtitle-1 mb-6">
                        Crown Nexus integrates with leading technology providers to offer a comprehensive ecosystem for the automotive aftermarket industry.
                      </p>
                    </v-col>
                  </v-row>
                  
                  <!-- Integration Categories -->
                  <v-row>
                    <v-col cols="12">
                      <v-tabs
                        v-model="techTab"
                        color="primary"
                        align-tabs="start"
                        slider-color="primary"
                      >
                        <v-tab value="all">All</v-tab>
                        <v-tab value="erp">ERP Systems</v-tab>
                        <v-tab value="ecommerce">E-commerce</v-tab>
                        <v-tab value="shipping">Shipping & Logistics</v-tab>
                        <v-tab value="payment">Payment Processors</v-tab>
                        <v-tab value="shop">Shop Management</v-tab>
                      </v-tabs>
                      
                      <v-divider></v-divider>
                      
                      <v-window v-model="techTab">
                        <v-window-item
                          v-for="category in ['all', 'erp', 'ecommerce', 'shipping', 'payment', 'shop']"
                          :key="category"
                          :value="category"
                        >
                          <v-row class="mt-4">
                            <v-col
                              v-for="partner in filteredTechPartners(category)"
                              :key="partner.id"
                              cols="12"
                              sm="6"
                              md="4"
                            >
                              <v-card class="h-100 tech-partner-card">
                                <v-img
                                  :src="partner.logo || 'https://via.placeholder.com/400x200'"
                                  height="140"
                                  contain
                                  class="bg-grey-lighten-3 pa-4"
                                ></v-img>
                                <v-card-item>
                                  <v-card-title>{{ partner.name }}</v-card-title>
                                  <v-card-subtitle>{{ partner.category }}</v-card-subtitle>
                                </v-card-item>
                                <v-card-text>
                                  <p>{{ partner.description }}</p>
                                  <v-chip
                                    v-if="partner.certified"
                                    color="success"
                                    size="small"
                                    variant="outlined"
                                    class="mt-2"
                                  >
                                    Certified Integration
                                  </v-chip>
                                </v-card-text>
                                <v-card-actions>
                                  <v-btn
                                    variant="text"
                                    color="primary"
                                    :to="`/integrations/${partner.id}`"
                                  >
                                    Integration Details
                                  </v-btn>
                                </v-card-actions>
                              </v-card>
                            </v-col>
                          </v-row>
                        </v-window-item>
                      </v-window>
                    </v-col>
                  </v-row>
                </v-container>
              </v-window-item>

              <!-- Industry Affiliations Tab -->
              <v-window-item value="industry">
                <v-container>
                  <v-row class="mb-6">
                    <v-col cols="12">
                      <h2 class="text-h4 font-weight-bold mb-2">Industry Affiliations</h2>
                      <p class="text-subtitle-1 mb-6">
                        Crown Nexus is proud to be an active member of these automotive aftermarket industry organizations.
                      </p>
                    </v-col>
                  </v-row>
                  
                  <!-- Industry Organizations -->
                  <v-row>
                    <v-col
                      v-for="org in industryOrganizations"
                      :key="org.id"
                      cols="12"
                      md="6"
                    >
                      <v-card class="mb-4 partner-card h-100">
                        <v-row no-gutters>
                          <v-col cols="4">
                            <v-img
                              :src="org.logo || 'https://via.placeholder.com/200x200'"
                              height="100%"
                              cover
                              class="bg-grey-lighten-3 h-100"
                              contain
                            ></v-img>
                          </v-col>
                          <v-col cols="8">
                            <v-card-item>
                              <v-card-title>{{ org.name }}</v-card-title>
                              <v-card-subtitle>{{ org.acronym }}</v-card-subtitle>
                            </v-card-item>
                            <v-card-text>
                              <p>{{ org.description }}</p>
                              <div class="mt-2">
                                <v-chip
                                  v-if="org.memberSince"
                                  size="small"
                                  variant="outlined"
                                  class="mr-2"
                                >
                                  Member since {{ org.memberSince }}
                                </v-chip>
                                <v-chip
                                  v-if="org.boardMember"
                                  size="small"
                                  color="primary"
                                  variant="outlined"
                                >
                                  Board Member
                                </v-chip>
                              </div>
                            </v-card-text>
                            <v-card-actions>
                              <v-btn
                                variant="text"
                                color="primary"
                                :href="org.website"
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                Visit Website
                                <v-icon end icon="mdi-open-in-new"></v-icon>
                              </v-btn>
                            </v-card-actions>
                          </v-col>
                        </v-row>
                      </v-card>
                    </v-col>
                  </v-row>
                  
                  <!-- Standards & Certifications -->
                  <v-row class="mt-8">
                    <v-col cols="12">
                      <h3 class="text-h5 font-weight-bold mb-4">Standards & Certifications</h3>
                      <p class="text-subtitle-2 mb-6">
                        Crown Nexus adheres to and supports these industry standards and certifications.
                      </p>
                    </v-col>
                    
                    <v-col
                      v-for="standard in industryStandards"
                      :key="standard.id"
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-card variant="outlined" class="h-100">
                        <v-card-item>
                          <template v-slot:prepend>
                            <v-avatar :color="standard.color" size="48">
                              <v-icon color="white" size="24" :icon="standard.icon"></v-icon>
                            </v-avatar>
                          </template>
                          <v-card-title>{{ standard.name }}</v-card-title>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ standard.description }}</p>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-container>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>

      <!-- Become a Partner Section -->
      <v-row class="mb-8">
        <v-col cols="12">
          <v-card color="primary" class="text-center pa-8">
            <v-card-title class="text-h4 text-white mb-4">Become a Partner</v-card-title>
            <v-card-text class="text-white text-subtitle-1 mb-6">
              Interested in partnering with Crown Nexus? We're always looking for new partners to expand our ecosystem and provide better solutions for the automotive aftermarket industry.
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn
                color="white"
                variant="elevated"
                size="large"
                to="/partner-program"
                class="mr-4"
              >
                Partner Program Details
              </v-btn>
              <v-btn
                color="primary"
                variant="outlined"
                size="large"
                to="/contact?inquiry=partnership"
                class="bg-white"
              >
                Contact Us
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <!-- Recent Partner News Section -->
      <v-row>
        <v-col cols="12">
          <h2 class="text-h4 font-weight-bold mb-6">Recent Partner News</h2>
          <v-row>
            <v-col
              v-for="(news, index) in partnerNews"
              :key="index"
              cols="12"
              md="4"
            >
              <v-card class="h-100">
                <v-img
                  :src="news.image || 'https://via.placeholder.com/600x300'"
                  height="200"
                  cover
                ></v-img>
                <v-card-item>
                  <v-card-title>{{ news.title }}</v-card-title>
                  <v-card-subtitle>{{ news.date }} | {{ news.partner }}</v-card-subtitle>
                </v-card-item>
                <v-card-text>
                  <p>{{ news.summary }}</p>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    variant="text"
                    color="primary"
                    :to="`/blog/${news.slug}`"
                  >
                    Read More
                    <v-icon end icon="mdi-arrow-right"></v-icon>
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          
          <div class="text-center mt-6">
            <v-btn
              color="primary"
              variant="tonal"
              to="/blog?category=partner-news"
            >
              View All Partner News
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';

// Interface definitions
interface Manufacturer {
  id: string;
  name: string;
  category: string;
  description: string;
  logo?: string;
  website: string;
  featured?: boolean;
}

interface DistributorCategory {
  id: string;
  name: string;
  description: string;
  color: string;
  icon: string;
  topPartners: {
    id: string;
    name: string;
    location: string;
  }[];
}

interface TechPartner {
  id: string;
  name: string;
  category: string;
  type: string;
  description: string;
  logo?: string;
  certified: boolean;
}

interface IndustryOrganization {
  id: string;
  name: string;
  acronym: string;
  description: string;
  logo?: string;
  website: string;
  memberSince?: string;
  boardMember?: boolean;
}

interface IndustryStandard {
  id: string;
  name: string;
  description: string;
  color: string;
  icon: string;
}

interface PartnerNews {
  title: string;
  date: string;
  partner: string;
  summary: string;
  image?: string;
  slug: string;
}

export default defineComponent({
  name: 'Partners',

  setup() {
    // Active tab state
    const activeTab = ref('manufacturers');
    const techTab = ref('all');
    
    // Featured manufacturing partners
    const featuredManufacturers = ref<Manufacturer[]>([
      {
        id: 'premium-brake',
        name: 'Premium Brake Systems',
        category: 'Brake Components',
        description: 'A leading manufacturer of high-performance brake systems and components with over 30 years of industry experience.',
        logo: 'https://via.placeholder.com/400x200?text=Premium+Brake+Systems',
        website: 'https://example.com/premium-brake',
        featured: true
      },
      {
        id: 'elite-suspension',
        name: 'Elite Suspension Technologies',
        category: 'Suspension Components',
        description: 'Innovative manufacturer of advanced suspension systems for passenger vehicles, trucks, and performance applications.',
        logo: 'https://via.placeholder.com/400x200?text=Elite+Suspension',
        website: 'https://example.com/elite-suspension',
        featured: true
      }
    ]);
    
    // All manufacturing partners
    const manufacturingPartners = ref<Manufacturer[]>([
      {
        id: 'premium-brake',
        name: 'Premium Brake Systems',
        category: 'Brake Components',
        logo: 'https://via.placeholder.com/200x200?text=PBS',
        website: 'https://example.com/premium-brake',
        description: ''
      },
      {
        id: 'elite-suspension',
        name: 'Elite Suspension Technologies',
        category: 'Suspension Components',
        logo: 'https://via.placeholder.com/200x200?text=EST',
        website: 'https://example.com/elite-suspension',
        description: ''
      },
      {
        id: 'powertrain-pro',
        name: 'PowerTrain Pro',
        category: 'Engine Components',
        logo: 'https://via.placeholder.com/200x200?text=PTP',
        website: 'https://example.com/powertrain-pro',
        description: ''
      },
      {
        id: 'driveline-dynamics',
        name: 'Driveline Dynamics',
        category: 'Drivetrain Components',
        logo: 'https://via.placeholder.com/200x200?text=DD',
        website: 'https://example.com/driveline-dynamics',
        description: ''
      },
      {
        id: 'quantum-electrical',
        name: 'Quantum Electrical',
        category: 'Electrical Systems',
        logo: 'https://via.placeholder.com/200x200?text=QE',
        website: 'https://example.com/quantum-electrical',
        description: ''
      },
      {
        id: 'global-filters',
        name: 'Global Filtration Solutions',
        category: 'Filters',
        logo: 'https://via.placeholder.com/200x200?text=GFS',
        website: 'https://example.com/global-filters',
        description: ''
      },
      {
        id: 'climatemaster',
        name: 'ClimateMaster HVAC',
        category: 'Climate Control',
        logo: 'https://via.placeholder.com/200x200?text=CM',
        website: 'https://example.com/climatemaster',
        description: ''
      },
      {
        id: 'performance-exhaust',
        name: 'Performance Exhaust Systems',
        category: 'Exhaust Components',
        logo: 'https://via.placeholder.com/200x200?text=PES',
        website: 'https://example.com/performance-exhaust',
        description: ''
      },
      {
        id: 'precision-steering',
        name: 'Precision Steering & Control',
        category: 'Steering Components',
        logo: 'https://via.placeholder.com/200x200?text=PSC',
        website: 'https://example.com/precision-steering',
        description: ''
      },
      {
        id: 'ultralight-wheels',
        name: 'UltraLight Wheel Co.',
        category: 'Wheels & Accessories',
        logo: 'https://via.placeholder.com/200x200?text=UWC',
        website: 'https://example.com/ultralight-wheels',
        description: ''
      },
      {
        id: 'interstate-bearings',
        name: 'Interstate Bearings',
        category: 'Bearings & Seals',
        logo: 'https://via.placeholder.com/200x200?text=IB',
        website: 'https://example.com/interstate-bearings',
        description: ''
      },
      {
        id: 'fusion-lighting',
        name: 'Fusion Lighting Technologies',
        category: 'Lighting Systems',
        logo: 'https://via.placeholder.com/200x200?text=FLT',
        website: 'https://example.com/fusion-lighting',
        description: ''
      }
    ]);
    
    // Distributor categories
    const distributorCategories = ref<DistributorCategory[]>([
      {
        id: 'national',
        name: 'National Distributors',
        description: 'Large-scale distributors with nationwide coverage across the United States and Canada.',
        color: 'primary',
        icon: 'mdi-map',
        topPartners: [
          { id: 'nat1', name: 'Continental Auto Parts Network', location: 'Multiple Locations, USA & Canada' },
          { id: 'nat2', name: 'AllPro Distribution Group', location: 'Multiple Locations, USA' },
          { id: 'nat3', name: 'United Parts Distributors', location: 'Multiple Locations, USA & Mexico' }
        ]
      },
      {
        id: 'regional',
        name: 'Regional Distributors',
        description: 'Regional specialists providing focused coverage and expertise in specific geographic areas.',
        color: 'secondary',
        icon: 'mdi-map-marker-radius',
        topPartners: [
          { id: 'reg1', name: 'Pacific Northwest Parts Co.', location: 'Northwest USA' },
          { id: 'reg2', name: 'Southern States Distribution', location: 'Southeast USA' },
          { id: 'reg3', name: 'Midwest Auto Supply Chain', location: 'Midwest USA' }
        ]
      },
      {
        id: 'specialty',
        name: 'Specialty Distributors',
        description: 'Specialized distributors focusing on specific product categories or vehicle types.',
        color: 'info',
        icon: 'mdi-star',
        topPartners: [
          { id: 'spec1', name: 'Performance Parts Direct', location: 'Performance & Racing Specialists' },
          { id: 'spec2', name: 'Commercial Fleet Supply', location: 'Commercial & Fleet Vehicles' },
          { id: 'spec3', name: 'Classic & Vintage Auto Parts', location: 'Classic & Restoration Specialists' }
        ]
      }
    ]);
    
    // Technology partners
    const techPartners = ref<TechPartner[]>([
      {
        id: 'erp1',
        name: 'Enterprise Pro',
        category: 'ERP Systems',
        type: 'erp',
        description: 'Comprehensive ERP solution with specialized modules for inventory management and order processing.',
        logo: 'https://via.placeholder.com/400x200?text=Enterprise+Pro',
        certified: true
      },
      {
        id: 'erp2',
        name: 'GlobalSuite ERP',
        category: 'ERP Systems',
        type: 'erp',
        description: 'Cloud-based ERP system designed for multi-location businesses with complex supply chains.',
        logo: 'https://via.placeholder.com/400x200?text=GlobalSuite',
        certified: true
      },
      {
        id: 'ecom1',
        name: 'ShopifyPlus',
        category: 'E-commerce Platform',
        type: 'ecommerce',
        description: 'Enterprise e-commerce platform with B2B capabilities and advanced inventory management.',
        logo: 'https://via.placeholder.com/400x200?text=ShopifyPlus',
        certified: true
      },
      {
        id: 'ecom2',
        name: 'Magento Commerce',
        category: 'E-commerce Platform',
        type: 'ecommerce',
        description: 'Flexible e-commerce platform for businesses with complex catalogs and multiple sales channels.',
        logo: 'https://via.placeholder.com/400x200?text=Magento',
        certified: true
      },
      {
        id: 'shipping1',
        name: 'ShipStation',
        category: 'Shipping Software',
        type: 'shipping',
        description: 'Shipping software that streamlines order fulfillment across multiple sales channels and carriers.',
        logo: 'https://via.placeholder.com/400x200?text=ShipStation',
        certified: true
      },
      {
        id: 'shipping2',
        name: 'FreightWise',
        category: 'Logistics Management',
        type: 'shipping',
        description: 'End-to-end logistics management platform for optimizing freight and reducing shipping costs.',
        logo: 'https://via.placeholder.com/400x200?text=FreightWise',
        certified: false
      },
      {
        id: 'payment1',
        name: 'Stripe',
        category: 'Payment Processor',
        type: 'payment',
        description: 'Comprehensive payment processing platform with support for subscription billing and invoicing.',
        logo: 'https://via.placeholder.com/400x200?text=Stripe',
        certified: true
      },
      {
        id: 'payment2',
        name: 'Square for Business',
        category: 'Payment Processor',
        type: 'payment',
        description: 'Payment processing solution with integrated POS capabilities for in-store and online sales.',
        logo: 'https://via.placeholder.com/400x200?text=Square',
        certified: false
      },
      {
        id: 'shop1',
        name: 'AutoShop Manager',
        category: 'Shop Management System',
        type: 'shop',
        description: 'Comprehensive shop management system for automotive repair facilities of all sizes.',
        logo: 'https://via.placeholder.com/400x200?text=AutoShop+Manager',
        certified: true
      },
      {
        id: 'shop2',
        name: 'TechWorks Pro',
        category: 'Shop Management System',
        type: 'shop',
        description: 'Cloud-based shop management solution with integrated estimating and parts ordering capabilities.',
        logo: 'https://via.placeholder.com/400x200?text=TechWorks+Pro',
        certified: true
      }
    ]);
    
    // Filter tech partners by category
    const filteredTechPartners = (category: string) => {
      if (category === 'all') {
        return techPartners.value;
      }
      return techPartners.value.filter(partner => partner.type === category);
    };
    
    // Industry organizations
    const industryOrganizations = ref<IndustryOrganization[]>([
      {
        id: 'aasa',
        name: 'Automotive Aftermarket Suppliers Association',
        acronym: 'AASA',
        description: 'The voice for automotive aftermarket suppliers, providing advocacy, industry insights, and networking opportunities.',
        logo: 'https://via.placeholder.com/400x200?text=AASA',
        website: 'https://example.com/aasa',
        memberSince: '2019',
        boardMember: true
      },
      {
        id: 'sema',
        name: 'Specialty Equipment Market Association',
        acronym: 'SEMA',
        description: 'Trade association representing manufacturers of specialty automotive parts and accessories.',
        logo: 'https://via.placeholder.com/400x200?text=SEMA',
        website: 'https://example.com/sema',
        memberSince: '2018'
      },
      {
        id: 'aaia',
        name: 'Auto Care Association',
        acronym: 'ACA',
        description: 'National trade association representing the entire auto care industry supply chain.',
        logo: 'https://via.placeholder.com/400x200?text=ACA',
        website: 'https://example.com/aca',
        memberSince: '2018',
        boardMember: true
      },
      {
        id: 'hdma',
        name: 'Heavy Duty Manufacturers Association',
        acronym: 'HDMA',
        description: 'The commercial vehicle supplier division of the Motor & Equipment Manufacturers Association.',
        logo: 'https://via.placeholder.com/400x200?text=HDMA',
        website: 'https://example.com/hdma',
        memberSince: '2020'
      }
    ]);
    
    // Industry standards
    const industryStandards = ref<IndustryStandard[]>([
      {
        id: 'aces',
        name: 'ACES (Aftermarket Catalog Exchange Standard)',
        description: 'Industry standard for the management and exchange of automotive catalog information.',
        color: 'primary',
        icon: 'mdi-database'
      },
      {
        id: 'pies',
        name: 'PIES (Product Information Exchange Standard)',
        description: 'Industry standard for communicating product information throughout the supply chain.',
        color: 'secondary',
        icon: 'mdi-file-document'
      },
      {
        id: 'iso9001',
        name: 'ISO 9001:2015',
        description: 'International standard for quality management systems to ensure consistent product quality.',
        color: 'success',
        icon: 'mdi-certificate'
      },
      {
        id: 'iso27001',
        name: 'ISO 27001',
        description: 'International standard for information security management to protect customer data.',
        color: 'info',
        icon: 'mdi-shield'
      },
      {
        id: 'aapex',
        name: 'AAPEX Verified',
        description: 'Verification program for automotive aftermarket software and data providers.',
        color: 'warning',
        icon: 'mdi-check-decagram'
      },
      {
        id: 'autocare',
        name: 'Auto Care Association Certified',
        description: 'Certification program for aftermarket businesses meeting industry standards.',
        color: 'error',
        icon: 'mdi-star-check'
      }
    ]);
    
    // Partner news
    const partnerNews = ref<PartnerNews[]>([
      {
        title: 'Crown Nexus and Premium Brake Systems Announce Expanded Partnership',
        date: 'March 5, 2023',
        partner: 'Premium Brake Systems',
        summary: 'Crown Nexus and Premium Brake Systems have expanded their partnership to include enhanced catalog data and integrated inventory management.',
        image: 'https://via.placeholder.com/600x300?text=Partnership+Announcement',
        slug: 'crown-nexus-premium-brake-partnership-2023'
      },
      {
        title: 'New Integration with TechWorks Pro Shop Management System',
        date: 'February 22, 2023',
        partner: 'TechWorks Pro',
        summary: 'Crown Nexus announces a new certified integration with TechWorks Pro, enhancing parts ordering capabilities for automotive repair shops.',
        image: 'https://via.placeholder.com/600x300?text=TechWorks+Integration',
        slug: 'techworks-pro-integration-announcement'
      },
      {
        title: 'Crown Nexus Joins Automotive Aftermarket Suppliers Association Board',
        date: 'January 15, 2023',
        partner: 'AASA',
        summary: 'Crown Nexus CEO has been appointed to the board of directors of the Automotive Aftermarket Suppliers Association (AASA).',
        image: 'https://via.placeholder.com/600x300?text=AASA+Board',
        slug: 'crown-nexus-aasa-board-appointment-2023'
      }
    ]);
    
    return {
      // State
      activeTab,
      techTab,
      
      // Data
      featuredManufacturers,
      manufacturingPartners,
      distributorCategories,
      techPartners,
      industryOrganizations,
      industryStandards,
      partnerNews,
      
      // Methods
      filteredTechPartners
    };
  }
});
</script>

<style scoped>
.partner-card {
  transition: transform 0.2s;
}

.partner-card:hover {
  transform: translateY(-5px);
}

.partner-logo-card {
  transition: all 0.2s;
}

.partner-logo-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
}

.tech-partner-card {
  transition: all 0.2s;
}

.tech-partner-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
