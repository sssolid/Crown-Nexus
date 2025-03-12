<!-- frontend/src/views/ShippingReturns.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-8">
        <v-col cols="12" lg="8" class="mx-auto">
          <h1 class="text-h2 font-weight-bold text-center mb-3">Shipping & Returns</h1>
          <p class="text-subtitle-1 text-center mb-6">
            Crown Nexus provides flexible shipping options and streamlined returns for our B2B customers
          </p>
          
          <!-- Page Navigation Tabs -->
          <v-card class="mb-6">
            <v-tabs
              v-model="activeTab"
              color="primary"
              align-tabs="center"
              grow
            >
              <v-tab value="shipping">Shipping Options</v-tab>
              <v-tab value="policies">Policies & Procedures</v-tab>
              <v-tab value="returns">Returns & Warranties</v-tab>
              <v-tab value="international">International Shipping</v-tab>
            </v-tabs>
          </v-card>
        </v-col>
      </v-row>

      <!-- Tab Content -->
      <v-window v-model="activeTab">
        <!-- Shipping Options Tab -->
        <v-window-item value="shipping">
          <v-row>
            <v-col cols="12" lg="8" class="mx-auto">
              <v-card class="mb-8">
                <v-card-title class="text-h4 font-weight-bold pb-2">Shipping Options</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus offers a variety of shipping methods to meet your business needs. All orders are processed and shipped from our distribution centers strategically located across North America.
                  </p>
                  
                  <h3 class="text-h5 font-weight-bold mb-3 mt-6">Available Shipping Methods</h3>
                  
                  <!-- Shipping Methods Table -->
                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left">Shipping Method</th>
                        <th class="text-left">Estimated Delivery</th>
                        <th class="text-left">Availability</th>
                        <th class="text-left">Best For</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(method, index) in shippingMethods" :key="index">
                        <td class="font-weight-medium">{{ method.name }}</td>
                        <td>{{ method.delivery }}</td>
                        <td>{{ method.availability }}</td>
                        <td>{{ method.bestFor }}</td>
                      </tr>
                    </tbody>
                  </v-table>
                  
                  <h3 class="text-h5 font-weight-bold mb-3 mt-6">Carrier Partners</h3>
                  
                  <!-- Carrier Partners -->
                  <v-row>
                    <v-col 
                      v-for="(carrier, index) in carriers" 
                      :key="index"
                      cols="6" 
                      sm="4" 
                      md="3"
                    >
                      <v-card variant="outlined" class="text-center pa-4">
                        <v-img
                          :src="carrier.logo || 'https://via.placeholder.com/150x80'"
                          height="80"
                          contain
                          class="mb-2"
                        ></v-img>
                        <div class="text-subtitle-2">{{ carrier.name }}</div>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <!-- Expedited Shipping Options -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">Expedited Shipping</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Need parts faster? Crown Nexus offers several expedited shipping options to get you what you need, when you need it.
                  </p>
                  
                  <v-row>
                    <v-col 
                      v-for="(option, index) in expeditedOptions" 
                      :key="index"
                      cols="12" 
                      md="6"
                    >
                      <v-card 
                        variant="outlined" 
                        class="h-100"
                        :color="option.color + '-lighten-5'"
                      >
                        <v-card-item>
                          <template v-slot:prepend>
                            <v-avatar :color="option.color" size="48">
                              <v-icon icon="mdi-{{ option.icon }}" color="white"></v-icon>
                            </v-avatar>
                          </template>
                          <v-card-title>{{ option.title }}</v-card-title>
                          <v-card-subtitle>{{ option.timing }}</v-card-subtitle>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ option.description }}</p>
                          <v-list density="compact" :bg-color="option.color + '-lighten-5'">
                            <v-list-subheader>Details</v-list-subheader>
                            <v-list-item
                              v-for="(detail, dIndex) in option.details"
                              :key="dIndex"
                              :prepend-icon="detail.icon"
                            >
                              <v-list-item-title>{{ detail.text }}</v-list-item-title>
                            </v-list-item>
                          </v-list>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <!-- Custom Shipping Solutions -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">Custom Shipping Solutions</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus understands that different businesses have different shipping needs. We offer custom shipping solutions for our partners and high-volume customers.
                  </p>
                  
                  <v-list>
                    <v-list-item
                      v-for="(solution, index) in customSolutions"
                      :key="index"
                      :title="solution.title"
                      :subtitle="solution.subtitle"
                    >
                      <template v-slot:prepend>
                        <v-avatar color="primary" size="36">
                          <v-icon icon="mdi-{{ solution.icon }}" color="white"></v-icon>
                        </v-avatar>
                      </template>
                    </v-list-item>
                  </v-list>
                  
                  <div class="text-center mt-6">
                    <v-btn
                      color="primary"
                      variant="tonal"
                      to="/contact?inquiry=custom-shipping"
                    >
                      Contact Us for Custom Shipping
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
              
              <!-- Shipping Calculators and Tools -->
              <v-card>
                <v-card-title class="text-h5 font-weight-bold">
                  Shipping Calculators & Tools
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    As a Crown Nexus customer, you have access to these shipping tools to help plan and optimize your orders:
                  </p>
                  
                  <v-list>
                    <v-list-item
                      v-for="(tool, index) in shippingTools"
                      :key="index"
                      :title="tool.name"
                      :subtitle="tool.description"
                    >
                      <template v-slot:prepend>
                        <v-icon icon="mdi-{{ tool.icon }}" color="primary"></v-icon>
                      </template>
                      <template v-slot:append>
                        <v-btn
                          variant="text"
                          color="primary"
                          :to="tool.link"
                        >
                          Access Tool
                        </v-btn>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
        
        <!-- Policies & Procedures Tab -->
        <v-window-item value="policies">
          <v-row>
            <v-col cols="12" lg="8" class="mx-auto">
              <v-card class="mb-8">
                <v-card-title class="text-h4 font-weight-bold pb-2">Shipping Policies & Procedures</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus maintains transparent and efficient shipping policies to ensure a smooth experience for our B2B customers. Here's what you need to know about our shipping procedures:
                  </p>
                  
                  <v-expansion-panels variant="accordion" class="mt-4">
                    <v-expansion-panel
                      v-for="(policy, index) in shippingPolicies"
                      :key="index"
                      :title="policy.title"
                      class="mb-2"
                    >
                      <v-expansion-panel-text>
                        <div v-html="policy.content"></div>
                        
                        <v-list v-if="policy.bulletPoints" density="compact" class="mt-2">
                          <v-list-item
                            v-for="(point, pIndex) in policy.bulletPoints"
                            :key="pIndex"
                          >
                            <template v-slot:prepend>
                              <v-icon icon="mdi-check" size="small" color="success"></v-icon>
                            </template>
                            <v-list-item-title v-html="point"></v-list-item-title>
                          </v-list-item>
                        </v-list>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-card-text>
              </v-card>
              
              <!-- Order Processing Timeline -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">Order Processing Timeline</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-timeline align="start" direction="horizontal" density="compact">
                    <v-timeline-item
                      v-for="(step, index) in orderProcessingSteps"
                      :key="index"
                      :dot-color="step.color"
                    >
                      <template v-slot:opposite>
                        <div class="text-subtitle-2 font-weight-bold">{{ step.title }}</div>
                        <div class="text-caption">{{ step.timing }}</div>
                      </template>
                      <div>
                        <p class="text-body-2">{{ step.description }}</p>
                      </div>
                    </v-timeline-item>
                  </v-timeline>
                </v-card-text>
              </v-card>
              
              <!-- Freight & LTL Shipping -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">Freight & LTL Shipping</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    For larger orders, Crown Nexus offers freight and LTL (Less Than Truckload) shipping options. Our logistics team will help coordinate the best shipping method for your bulk orders.
                  </p>
                  
                  <v-row>
                    <v-col cols="12" md="6">
                      <h3 class="text-h6 font-weight-bold mb-2">Freight Guidelines</h3>
                      <v-list density="compact">
                        <v-list-item
                          v-for="(item, index) in freightGuidelines"
                          :key="index"
                          :title="item"
                          prepend-icon="mdi-truck"
                        ></v-list-item>
                      </v-list>
                    </v-col>
                    <v-col cols="12" md="6">
                      <h3 class="text-h6 font-weight-bold mb-2">LTL Requirements</h3>
                      <v-list density="compact">
                        <v-list-item
                          v-for="(item, index) in ltlRequirements"
                          :key="index"
                          :title="item"
                          prepend-icon="mdi-package-variant"
                        ></v-list-item>
                      </v-list>
                    </v-col>
                  </v-row>
                  
                  <div class="text-center mt-6">
                    <v-btn
                      color="primary"
                      to="/freight-quote"
                    >
                      Request Freight Quote
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
              
              <!-- Packaging & Handling -->
              <v-card>
                <v-card-title class="text-h5 font-weight-bold">Packaging & Handling</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus follows industry-best practices for packaging to ensure your products arrive in perfect condition. Our standard packaging procedures include:
                  </p>
                  
                  <v-row>
                    <v-col 
                      v-for="(practice, index) in packagingPractices" 
                      :key="index"
                      cols="12" 
                      sm="6"
                    >
                      <v-card variant="outlined" class="h-100">
                        <v-card-item>
                          <template v-slot:prepend>
                            <v-avatar color="primary-lighten-1" size="40">
                              <v-icon icon="mdi-{{ practice.icon }}" color="white"></v-icon>
                            </v-avatar>
                          </template>
                          <v-card-title>{{ practice.title }}</v-card-title>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ practice.description }}</p>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  
                  <v-alert
                    type="info"
                    variant="tonal"
                    class="mt-6"
                  >
                    <div class="text-subtitle-1 font-weight-bold">Special Packaging Requests</div>
                    <p class="mt-2 mb-0">
                      We accommodate special packaging requirements for certain products or shipping scenarios. Please contact your account manager to discuss specific packaging needs for your business.
                    </p>
                  </v-alert>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
        
        <!-- Returns & Warranties Tab -->
        <v-window-item value="returns">
          <v-row>
            <v-col cols="12" lg="8" class="mx-auto">
              <v-card class="mb-8">
                <v-card-title class="text-h4 font-weight-bold pb-2">Returns & Warranties</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-6">
                    Crown Nexus is committed to providing quality products and excellent service. Our returns and warranty processes are designed to be straightforward and efficient for our B2B customers.
                  </p>
                  
                  <!-- Returns Process Diagram -->
                  <h3 class="text-h5 font-weight-bold mb-4">Returns Process</h3>
                  
                  <v-timeline>
                    <v-timeline-item
                      v-for="(step, index) in returnsProcess"
                      :key="index"
                      :dot-color="step.color"
                      size="small"
                    >
                      <template v-slot:icon>
                        <v-avatar :color="step.color" size="36">
                          <v-icon icon="mdi-{{ step.icon }}" color="white" size="small"></v-icon>
                        </v-avatar>
                      </template>
                      <div class="d-flex flex-column">
                        <div class="text-h6 font-weight-bold">{{ step.title }}</div>
                        <div class="text-body-1 mt-1">{{ step.description }}</div>
                      </div>
                    </v-timeline-item>
                  </v-timeline>
                  
                  <v-divider class="my-6"></v-divider>
                  
                  <!-- Return Policy Details -->
                  <h3 class="text-h5 font-weight-bold mb-4">Return Policy Details</h3>
                  
                  <v-row>
                    <v-col 
                      v-for="(policy, index) in returnPolicies" 
                      :key="index"
                      cols="12" 
                      md="6"
                    >
                      <v-card variant="outlined" class="h-100">
                        <v-card-item>
                          <v-card-title>{{ policy.title }}</v-card-title>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ policy.description }}</p>
                          <v-list density="compact" class="mt-2">
                            <v-list-item
                              v-for="(point, pIndex) in policy.points"
                              :key="pIndex"
                              :title="point"
                            >
                              <template v-slot:prepend>
                                <v-icon icon="mdi-check-circle" color="success" size="small"></v-icon>
                              </template>
                            </v-list-item>
                          </v-list>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <!-- Warranty Information -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">Warranty Information</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus stands behind the quality of our products. All products come with manufacturer warranties, and many include additional coverage through our Crown Nexus Protection program.
                  </p>
                  
                  <v-expansion-panels variant="accordion" class="mt-4">
                    <v-expansion-panel
                      v-for="(warranty, index) in warrantyInformation"
                      :key="index"
                      :title="warranty.title"
                      class="mb-2"
                    >
                      <v-expansion-panel-text>
                        <p>{{ warranty.description }}</p>
                        
                        <v-table v-if="warranty.coverage" class="mt-4">
                          <thead>
                            <tr>
                              <th class="text-left">Product Category</th>
                              <th class="text-left">Standard Warranty</th>
                              <th class="text-left">Extended Warranty</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(item, cIndex) in warranty.coverage" :key="cIndex">
                              <td>{{ item.category }}</td>
                              <td>{{ item.standard }}</td>
                              <td>{{ item.extended }}</td>
                            </tr>
                          </tbody>
                        </v-table>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-card-text>
              </v-card>
              
              <!-- Returns Tools & Resources -->
              <v-card>
                <v-card-title class="text-h5 font-weight-bold">Returns Tools & Resources</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus provides several tools and resources to make the returns process as efficient as possible:
                  </p>
                  
                  <v-row>
                    <v-col 
                      v-for="(resource, index) in returnsResources" 
                      :key="index"
                      cols="12" 
                      sm="6" 
                      md="4"
                    >
                      <v-card class="h-100" variant="outlined">
                        <v-img
                          v-if="resource.image"
                          :src="resource.image"
                          height="140"
                          cover
                        ></v-img>
                        <v-card-item>
                          <template v-slot:prepend>
                            <v-icon icon="mdi-{{ resource.icon }}" color="primary"></v-icon>
                          </template>
                          <v-card-title>{{ resource.title }}</v-card-title>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ resource.description }}</p>
                        </v-card-text>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            variant="text"
                            color="primary"
                            :to="resource.link"
                          >
                            {{ resource.buttonText }}
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
        
        <!-- International Shipping Tab -->
        <v-window-item value="international">
          <v-row>
            <v-col cols="12" lg="8" class="mx-auto">
              <v-card class="mb-8">
                <v-card-title class="text-h4 font-weight-bold pb-2">International Shipping</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus serves customers internationally with dedicated shipping solutions for businesses outside the United States and Canada. Our international shipping department specializes in navigating customs requirements, documentation, and logistics for global commerce.
                  </p>
                  
                  <!-- International Map -->
                  <div class="text-center mb-6">
                    <v-img
                      src="https://via.placeholder.com/1000x500?text=International+Shipping+Map"
                      height="400"
                      cover
                      class="rounded-lg"
                    ></v-img>
                  </div>
                  
                  <!-- Regions We Serve -->
                  <h3 class="text-h5 font-weight-bold mb-4">Regions We Serve</h3>
                  
                  <v-row>
                    <v-col 
                      v-for="(region, index) in internationalRegions" 
                      :key="index"
                      cols="12" 
                      sm="6" 
                      md="4"
                    >
                      <v-card variant="outlined" class="h-100">
                        <v-card-item :title="region.name">
                          <template v-slot:prepend>
                            <v-icon icon="mdi-{{ region.icon }}" color="primary"></v-icon>
                          </template>
                        </v-card-item>
                        <v-card-text>
                          <v-list density="compact">
                            <v-list-item
                              v-for="(country, cIndex) in region.countries"
                              :key="cIndex"
                              :title="country"
                            ></v-list-item>
                          </v-list>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
              
              <!-- International Shipping Methods -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">International Shipping Methods</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus offers several shipping methods for international orders to meet your timeline and budget requirements:
                  </p>
                  
                  <v-table>
                    <thead>
                      <tr>
                        <th class="text-left">Method</th>
                        <th class="text-left">Estimated Delivery</th>
                        <th class="text-left">Best For</th>
                        <th class="text-left">Tracking</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(method, index) in internationalShippingMethods" :key="index">
                        <td class="font-weight-medium">{{ method.name }}</td>
                        <td>{{ method.delivery }}</td>
                        <td>{{ method.bestFor }}</td>
                        <td><v-icon :icon="method.tracking ? 'mdi-check' : 'mdi-close'" :color="method.tracking ? 'success' : 'error'"></v-icon></td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-card-text>
              </v-card>
              
              <!-- Customs & Documentation -->
              <v-card class="mb-8">
                <v-card-title class="text-h5 font-weight-bold">Customs & Documentation</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    International shipments require proper documentation to clear customs efficiently. Crown Nexus helps prepare and provide all necessary documents for your international orders.
                  </p>
                  
                  <h3 class="text-h6 font-weight-bold mb-3">Required Documentation</h3>
                  
                  <v-row>
                    <v-col 
                      v-for="(doc, index) in customsDocuments" 
                      :key="index"
                      cols="12" 
                      md="6"
                    >
                      <v-card variant="outlined" class="h-100">
                        <v-card-item>
                          <template v-slot:prepend>
                            <v-icon icon="mdi-file-document" color="primary"></v-icon>
                          </template>
                          <v-card-title>{{ doc.name }}</v-card-title>
                        </v-card-item>
                        <v-card-text>
                          <p>{{ doc.description }}</p>
                          <v-divider class="my-2"></v-divider>
                          <div class="text-caption">Required for: {{ doc.requiredFor }}</div>
                        </v-card-text>
                      </v-card>
                    </v-col>
                  </v-row>
                  
                  <v-alert
                    type="info"
                    variant="tonal"
                    class="mt-6"
                  >
                    <div class="text-subtitle-1 font-weight-bold">Crown Nexus Documentation Support</div>
                    <p class="mt-2 mb-0">
                      Our international shipping team helps prepare all necessary customs documentation for your orders. We can also provide guidance on harmonized tariff codes, import regulations, and other requirements specific to your destination country.
                    </p>
                  </v-alert>
                </v-card-text>
              </v-card>
              
              <!-- International Returns -->
              <v-card>
                <v-card-title class="text-h5 font-weight-bold">International Returns</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <p class="text-body-1 mb-4">
                    Crown Nexus handles international returns through our specialized returns process designed for cross-border shipments.
                  </p>
                  
                  <v-expansion-panels variant="accordion">
                    <v-expansion-panel
                      v-for="(section, index) in internationalReturns"
                      :key="index"
                      :title="section.title"
                    >
                      <v-expansion-panel-text>
                        <p class="mb-3">{{ section.description }}</p>
                        <v-list density="compact">
                          <v-list-item
                            v-for="(point, pIndex) in section.points"
                            :key="pIndex"
                          >
                            <template v-slot:prepend>
                              <v-icon icon="mdi-check" size="small" color="success"></v-icon>
                            </template>
                            <v-list-item-title>{{ point }}</v-list-item-title>
                          </v-list-item>
                        </v-list>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                  
                  <div class="text-center mt-6">
                    <v-btn
                      color="primary"
                      to="/contact?inquiry=international-returns"
                    >
                      Contact International Returns Team
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>

      <!-- Common Questions -->
      <v-row class="mt-12">
        <v-col cols="12" lg="8" class="mx-auto">
          <h2 class="text-h4 font-weight-bold text-center mb-6">Common Questions</h2>
          
          <v-expansion-panels variant="accordion">
            <v-expansion-panel
              v-for="(faq, index) in commonQuestions"
              :key="index"
              :title="faq.question"
              class="mb-2"
            >
              <v-expansion-panel-text>
                <div v-html="faq.answer"></div>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
          
          <div class="text-center mt-6">
            <v-btn
              color="primary"
              variant="text"
              to="/faq?category=shipping"
              size="large"
            >
              View All Shipping FAQs
            </v-btn>
          </div>
        </v-col>
      </v-row>

      <!-- Contact Shipping Support -->
      <v-row class="mt-12">
        <v-col cols="12" lg="8" class="mx-auto">
          <v-card color="primary" class="text-center pa-8">
            <v-card-title class="text-h4 text-white mb-4">Need Help With Shipping?</v-card-title>
            <v-card-text class="text-white text-subtitle-1 mb-6">
              Our shipping specialists are available to answer your questions and help with any shipping needs.
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn
                color="white"
                variant="elevated"
                size="large"
                prepend-icon="mdi-phone"
                class="mr-4"
                href="tel:+18009876543"
              >
                1-800-987-6543
              </v-btn>
              <v-btn
                color="white"
                variant="outlined"
                size="large"
                prepend-icon="mdi-email"
                to="/contact?department=shipping"
              >
                Email Support
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ShippingReturns',

  setup() {
    // Active tab state
    const activeTab = ref('shipping');
    
    // Shipping Methods
    const shippingMethods = ref([
      {
        name: 'Standard Ground',
        delivery: '3-5 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Regular restocking orders'
      },
      {
        name: 'Expedited Ground',
        delivery: '2-3 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Time-sensitive orders'
      },
      {
        name: 'Priority Overnight',
        delivery: 'Next business day',
        availability: 'Continental US & Canada',
        bestFor: 'Emergency parts needs'
      },
      {
        name: 'LTL Freight',
        delivery: '3-7 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Large or heavy shipments'
      },
      {
        name: 'Will Call',
        delivery: 'Same day pickup',
        availability: 'Distribution center locations',
        bestFor: 'Local customers needing immediate parts'
      }
    ]);
    
    // Carrier Partners
    const carriers = ref([
      { name: 'FedEx', logo: 'https://via.placeholder.com/150x80?text=FedEx' },
      { name: 'UPS', logo: 'https://via.placeholder.com/150x80?text=UPS' },
      { name: 'USPS', logo: 'https://via.placeholder.com/150x80?text=USPS' },
      { name: 'DHL', logo: 'https://via.placeholder.com/150x80?text=DHL' },
      { name: 'XPO Logistics', logo: 'https://via.placeholder.com/150x80?text=XPO' },
      { name: 'Old Dominion', logo: 'https://via.placeholder.com/150x80?text=Old+Dominion' },
      { name: 'R+L Carriers', logo: 'https://via.placeholder.com/150x80?text=R%2BL' },
      { name: 'YRC Freight', logo: 'https://via.placeholder.com/150x80?text=YRC' }
    ]);
    
    // Expedited Shipping Options
    const expeditedOptions = ref([
      {
        title: 'Same-Day Delivery',
        timing: 'Delivery within hours',
        color: 'error',
        icon: 'clock-fast',
        description: 'For critical parts needs, we offer same-day delivery service in select metro areas. Orders must be placed before 10 AM local time.',
        details: [
          { icon: 'mdi-map-marker', text: 'Available in major metro areas' },
          { icon: 'mdi-currency-usd', text: 'Premium pricing applies' },
          { icon: 'mdi-truck-fast', text: 'Direct courier delivery' },
          { icon: 'mdi-phone', text: 'Call for availability' }
        ]
      },
      {
        title: 'Next-Day Air',
        timing: 'Delivery by 10:30 AM next business day',
        color: 'warning',
        icon: 'airplane',
        description: 'Our premium overnight service guarantees delivery by 10:30 AM the next business day to most locations in the continental US.',
        details: [
          { icon: 'mdi-calendar-clock', text: 'Order by 4 PM EST for next-day delivery' },
          { icon: 'mdi-map', text: 'Available to most US locations' },
          { icon: 'mdi-truck-check', text: 'Full tracking and delivery confirmation' },
          { icon: 'mdi-account-check', text: 'Signature required on delivery' }
        ]
      }
    ]);
    
    // Custom Shipping Solutions
    const customSolutions = ref([
      {
        title: 'Dedicated Freight Program',
        subtitle: 'For high-volume customers with regular shipping needs',
        icon: 'truck-check'
      },
      {
        title: 'Cross-Dock Services',
        subtitle: 'Consolidate multiple shipments for more efficient delivery',
        icon: 'forklift'
      },
      {
        title: 'Just-In-Time Delivery',
        subtitle: 'Scheduled deliveries to support lean inventory management',
        icon: 'clock-time-five'
      },
      {
        title: 'Customized Packaging',
        subtitle: 'Special packaging solutions for unique product requirements',
        icon: 'package-variant'
      },
      {
        title: 'Managed Transportation',
        subtitle: 'Let our logistics team manage your entire shipping process',
        icon: 'truck-delivery'
      }
    ]);
    
    // Shipping Tools
    const shippingTools = ref([
      {
        name: 'Shipping Rate Calculator',
        description: 'Calculate shipping costs based on weight, dimensions, and destination',
        icon: 'calculator',
        link: '/tools/shipping-calculator'
      },
      {
        name: 'Transit Time Estimator',
        description: 'Get estimated delivery times for any shipping method to your location',
        icon: 'clock-outline',
        link: '/tools/transit-estimator'
      },
      {
        name: 'Order Tracking Portal',
        description: 'Track all your shipments in one place with real-time updates',
        icon: 'map-marker-path',
        link: '/account/order-tracking'
      },
      {
        name: 'Shipping Documentation Generator',
        description: 'Generate shipping labels, packing slips, and customs forms',
        icon: 'file-document-outline',
        link: '/tools/documentation'
      }
    ]);
    
    // Shipping Policies
    const shippingPolicies = ref([
      {
        title: 'Order Processing Times',
        content: 'Crown Nexus processes orders according to the following schedule:<br><br>• Orders received before 2 PM EST on business days are processed the same day<br>• Orders received after 2 PM EST are processed the next business day<br>• Processing time does not include weekends or holidays<br><br>Orders are processed in the sequence they are received, with priority given to emergency orders and expedited shipping requests.'
      },
      {
        title: 'Shipping Cutoff Times',
        content: 'To ensure your order ships on the same day, please place your order before these cutoff times:',
        bulletPoints: [
          'Standard Ground: 2 PM EST',
          'Expedited Ground: 2 PM EST',
          'Priority Overnight: 3 PM EST (may vary by location)',
          'LTL Freight: 12 PM EST',
          'Will Call: 4 PM local time at the distribution center'
        ]
      },
      {
        title: 'Shipping Costs & Calculation',
        content: 'Shipping costs are calculated based on several factors including:<br><br>• Package weight and dimensions<br>• Shipping destination<br>• Selected shipping method<br>• Order value<br><br>Volume discounts are available for qualifying accounts based on monthly shipping volume. Contact your account manager for details about shipping cost optimization.'
      },
      {
        title: 'Delivery Confirmation & Tracking',
        content: 'All shipments include tracking information that is automatically emailed to the account contact when the order ships. You can also track shipments through your Crown Nexus account dashboard.<br><br>For signature-required deliveries, the recipient must be available to sign for the package. If no one is available, the carrier will typically attempt delivery up to three times before returning the package.'
      },
      {
        title: 'Special Handling & Additional Services',
        content: 'Crown Nexus offers several special handling options and additional services for an extra fee:',
        bulletPoints: [
          'Inside delivery for large items',
          'Lift gate service for freight shipments',
          'Residential delivery (for home-based businesses)',
          'Saturday delivery (where available)',
          'Delivery appointment scheduling',
          'Address correction'
        ]
      }
    ]);
    
    // Order Processing Steps
    const orderProcessingSteps = ref([
      {
        title: 'Order Placement',
        timing: 'Day 0',
        description: 'Order is submitted through website, EDI, or phone',
        color: 'primary'
      },
      {
        title: 'Order Verification',
        timing: 'Within 30 minutes',
        description: 'Order is checked for accuracy and availability',
        color: 'primary'
      },
      {
        title: 'Payment Processing',
        timing: 'Within 1 hour',
        description: 'Payment method is verified or terms are applied',
        color: 'primary'
      },
      {
        title: 'Picking & Packing',
        timing: 'Same day for orders before 2 PM',
        description: 'Items are picked from warehouse and packaged',
        color: 'secondary'
      },
      {
        title: 'Shipping',
        timing: 'Same day for orders before cutoff',
        description: 'Order is handed off to carrier with tracking',
        color: 'info'
      },
      {
        title: 'Delivery',
        timing: 'Based on shipping method',
        description: 'Carrier delivers to specified address',
        color: 'success'
      }
    ]);
    
    // Freight Guidelines
    const freightGuidelines = ref([
      'Orders over 150 lbs typically ship via freight',
      'Standard delivery is dock-to-dock',
      'Inside delivery available for additional fee',
      'Lift gate service available for locations without loading docks',
      'Freight shipments require a delivery appointment',
      'Inspection required at time of delivery'
    ]);
    
    // LTL Requirements
    const ltlRequirements = ref([
      'Proper packaging for freight handling',
      'Items must be palletized or crated',
      'Accurate dimensions and weight required',
      'Hazardous materials must be declared',
      'Commercial address with loading dock preferred',
      'Delivery contact information required'
    ]);
    
    // Packaging Practices
    const packagingPractices = ref([
      {
        title: 'Multiple Box Sizes',
        icon: 'package-variant-closed',
        description: 'We use the appropriate box size for each order to minimize shipping costs and environmental impact while ensuring product protection.'
      },
      {
        title: 'Eco-Friendly Materials',
        icon: 'leaf',
        description: 'Whenever possible, we use recyclable and biodegradable packaging materials, including recycled cardboard and paper-based void fill.'
      },
      {
        title: 'Part-Specific Protection',
        icon: 'shield',
        description: 'Delicate parts receive additional protection with custom inserts, bubble wrap, or foam padding to prevent damage during transit.'
      },
      {
        title: 'Consolidation',
        icon: 'package-variant',
        description: 'Multiple items in a single order are consolidated whenever possible to reduce packaging materials and shipping costs.'
      }
    ]);
    
    // Returns Process
    const returnsProcess = ref([
      {
        title: 'Request Return Authorization',
        description: 'Submit a return request through your account dashboard or by contacting customer service with your order number and reason for return.',
        icon: 'file-document-edit',
        color: 'primary'
      },
      {
        title: 'Receive RMA and Instructions',
        description: 'Once approved, you\'ll receive a Return Merchandise Authorization (RMA) number and detailed instructions for returning the items.',
        icon: 'email',
        color: 'secondary'
      },
      {
        title: 'Package Items',
        description: 'Package the items securely in original packaging if possible. Include the RMA paperwork inside the box and write the RMA number on the outside.',
        icon: 'package-variant-closed',
        color: 'info'
      },
      {
        title: 'Ship Returns',
        description: 'Ship the package using the provided return label or the shipping method specified in your return instructions.',
        icon: 'truck',
        color: 'warning'
      },
      {
        title: 'Returns Processing',
        description: 'Our returns department will inspect the returned items and process your refund, exchange, or warranty claim according to your request.',
        icon: 'clipboard-check',
        color: 'success'
      }
    ]);
    
    // Return Policies
    const returnPolicies = ref([
      {
        title: 'Standard Returns',
        description: 'Our standard return policy for most products:',
        points: [
          '30-day return window from delivery date',
          'Items must be in original condition and packaging',
          'Return shipping paid by customer for non-defective items',
          'Restocking fee may apply (typically 15%)',
          'Full refund to original payment method'
        ]
      },
      {
        title: 'Warranty Returns',
        description: 'Our process for handling warranty claims:',
        points: [
          'Manufacturer warranty terms apply',
          'Defective items can be returned at any time during warranty period',
          'No restocking fee for warranty returns',
          'Return shipping covered for defective items',
          'Replacement shipped upon receipt and verification of defect'
        ]
      },
      {
        title: 'Special Order Returns',
        description: 'Policy for custom or special-order items:',
        points: [
          'Non-returnable unless defective',
          'Manufacturer defects covered under normal warranty terms',
          'Custom fabrication and modification services are non-refundable',
          'Special orders may require manufacturer approval for returns',
          'Higher restocking fees may apply (up to 25%)'
        ]
      },
      {
        title: 'Bulk Order Returns',
        description: 'Returns policy for large-volume orders:',
        points: [
          'Volume discounts remain in effect for partial returns if minimum quantity thresholds are still met',
          'Bulk returns require pre-approval and coordination with our returns department',
          'Special handling fees may apply for large returns',
          'Returns over $5,000 may be subject to extended processing time',
          'Contact your account manager for bulk return assistance'
        ]
      }
    ]);
    
    // Warranty Information
    const warrantyInformation = ref([
      {
        title: 'Manufacturer Warranties',
        description: 'All products sold through Crown Nexus come with the original manufacturer warranty. Warranty terms vary by manufacturer and product category.',
        coverage: [
          { category: 'Brake Components', standard: '12 months / 12,000 miles', extended: '24 months / 24,000 miles' },
          { category: 'Engine Parts', standard: '12 months / 12,000 miles', extended: '36 months / 36,000 miles' },
          { category: 'Suspension Components', standard: '24 months / 24,000 miles', extended: 'Lifetime (limited)' },
          { category: 'Electrical Components', standard: '12 months', extended: '24 months' },
          { category: 'Filters & Maintenance Items', standard: '90 days', extended: 'Not available' }
        ]
      },
      {
        title: 'Crown Nexus Protection Plans',
        description: 'Our optional extended protection plans provide additional coverage beyond the standard manufacturer warranty, offering peace of mind for your critical parts purchases.',
        coverage: [
          { category: 'Silver Plan', standard: 'Extends warranty by 12 months', extended: 'Available for most part categories' },
          { category: 'Gold Plan', standard: 'Doubles original warranty period', extended: 'Includes labor reimbursement' },
          { category: 'Platinum Plan', standard: 'Lifetime limited warranty', extended: 'Premium parts categories only' }
        ]
      },
      {
        title: 'Commercial Vehicle Coverage',
        description: 'Special warranty terms apply to parts used in commercial vehicles, fleet applications, or heavy-duty service.',
        coverage: [
          { category: 'Light Duty Commercial', standard: 'Standard warranty with mileage limit doubled', extended: '18 months / 36,000 miles' },
          { category: 'Medium Duty Commercial', standard: '6 months / unlimited miles', extended: '12 months / unlimited miles' },
          { category: 'Heavy Duty Commercial', standard: '3 months / unlimited miles', extended: '12 months / unlimited miles' }
        ]
      },
      {
        title: 'Labor Claims',
        description: 'Some manufacturer warranties and Crown Nexus Protection Plans include provisions for labor reimbursement when defective parts must be replaced under warranty.',
        coverage: [
          { category: 'Standard Warranty', standard: 'Labor not included', extended: 'N/A' },
          { category: 'Limited Labor Coverage', standard: 'Up to 2 hours at published labor rate', extended: 'Select manufacturers only' },
          { category: 'Gold/Platinum Plans', standard: 'Full published labor rate', extended: 'Subject to maximum reimbursement' }
        ]
      }
    ]);
    
    // Returns Resources
    const returnsResources = ref([
      {
        title: 'Returns Portal',
        icon: 'laptop',
        description: 'Manage all your returns online through our self-service returns portal. Request RMAs, print shipping labels, and track return status.',
        link: '/account/returns',
        buttonText: 'Access Portal',
        image: 'https://via.placeholder.com/400x200?text=Returns+Portal'
      },
      {
        title: 'RMA Generator',
        icon: 'note-text',
        description: 'Quickly generate return merchandise authorizations for multiple items or orders with our easy-to-use RMA tool.',
        link: '/tools/rma-generator',
        buttonText: 'Generate RMA',
        image: 'https://via.placeholder.com/400x200?text=RMA+Generator'
      },
      {
        title: 'Returns Guide',
        icon: 'book-open-variant',
        description: 'Download our comprehensive returns guide with step-by-step instructions, packaging requirements, and tips for efficient returns processing.',
        link: '/resources/returns-guide',
        buttonText: 'Download Guide',
        image: 'https://via.placeholder.com/400x200?text=Returns+Guide'
      }
    ]);
    
    // International Regions
    const internationalRegions = ref([
      {
        name: 'North America',
        icon: 'earth',
        countries: ['Canada', 'Mexico']
      },
      {
        name: 'Latin America',
        icon: 'earth',
        countries: ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Panama']
      },
      {
        name: 'Europe',
        icon: 'earth',
        countries: ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 'Sweden']
      },
      {
        name: 'Asia Pacific',
        icon: 'earth',
        countries: ['Australia', 'Japan', 'South Korea', 'Singapore', 'Thailand', 'New Zealand']
      },
      {
        name: 'Middle East',
        icon: 'earth',
        countries: ['United Arab Emirates', 'Saudi Arabia', 'Qatar']
      },
      {
        name: 'Africa',
        icon: 'earth',
        countries: ['South Africa', 'Egypt', 'Morocco']
      }
    ]);
    
    // International Shipping Methods
    const internationalShippingMethods = ref([
      {
        name: 'Economy International',
        delivery: '7-14 business days',
        bestFor: 'Non-urgent shipments and budget-conscious customers',
        tracking: true
      },
      {
        name: 'Standard International',
        delivery: '5-10 business days',
        bestFor: 'Regular international shipments with balanced cost and speed',
        tracking: true
      },
      {
        name: 'Expedited International',
        delivery: '3-5 business days',
        bestFor: 'Time-sensitive shipments needing faster delivery',
        tracking: true
      },
      {
        name: 'Priority International',
        delivery: '2-3 business days',
        bestFor: 'Urgent shipments requiring quick delivery',
        tracking: true
      },
      {
        name: 'International Air Freight',
        delivery: '5-7 business days',
        bestFor: 'Large volume shipments too heavy for standard service',
        tracking: true
      },
      {
        name: 'International Ocean Freight',
        delivery: '30-45 days',
        bestFor: 'Very large shipments where time is not critical',
        tracking: true
      }
    ]);
    
    // Customs Documents
    const customsDocuments = ref([
      {
        name: 'Commercial Invoice',
        description: 'Official document that details the sale transaction between seller and buyer, including item descriptions, quantities, and values.',
        requiredFor: 'All international shipments'
      },
      {
        name: 'Packing List',
        description: 'Detailed list of all items in the shipment, including quantities, weights, and dimensions.',
        requiredFor: 'All international shipments'
      },
      {
        name: 'Certificate of Origin',
        description: 'Document certifying the country where the goods were manufactured or produced.',
        requiredFor: 'Shipments to countries with preferential trade agreements'
      },
      {
        name: 'Shipper\'s Letter of Instruction',
        description: 'Detailed instructions from the shipper to the carrier about how to handle the shipment.',
        requiredFor: 'Most international shipments'
      },
      {
        name: 'Dangerous Goods Declaration',
        description: 'Document required for shipping hazardous materials, detailing the nature of the goods and safety precautions.',
        requiredFor: 'Shipments containing hazardous materials'
      },
      {
        name: 'Import License',
        description: 'Government-issued permit allowing the importation of specific goods into the destination country.',
        requiredFor: 'Certain restricted items in specific countries'
      }
    ]);
    
    // International Returns
    const internationalReturns = ref([
      {
        title: 'International Return Process',
        description: 'Our international returns process is designed to make cross-border returns as smooth as possible:',
        points: [
          'Standard 30-day return window applies to international orders',
          'Return shipping costs are the responsibility of the customer unless the item is defective',
          'All returns require an RMA number before shipping',
          'Return shipping method should match or be slower than the original shipping method',
          'Customer is responsible for all duties and taxes on return shipments'
        ]
      },
      {
        title: 'Customs Documentation for Returns',
        description: 'Proper documentation is crucial for international returns to clear customs efficiently:',
        points: [
          'Mark packages as "Return of Goods" or "Warranty Return" as appropriate',
          'Include commercial invoice stating "No Commercial Value - Returned Goods"',
          'Reference the original order number and RMA number on all documents',
          'Include copy of original commercial invoice if available',
          'Declare actual value for customs purposes (even for warranty returns)'
        ]
      },
      {
        title: 'International Warranty Claims',
        description: 'Process for handling international warranty claims:',
        points: [
          'All manufacturer warranties apply to international customers',
          'Local repair options may be available in some regions',
          'Return shipping for warranty items may be covered (pre-approval required)',
          'Replacement parts can be shipped before return receipt in some cases',
          'International customers should contact our International Customer Service team for warranty assistance'
        ]
      }
    ]);
    
    // Common Questions
    const commonQuestions = ref([
      {
        question: 'How can I track my shipment?',
        answer: 'You can track your shipment in several ways:<br><br>1. Log into your Crown Nexus account and go to the "Orders" section<br>2. Click on the specific order to view tracking information<br>3. Click the tracking number to be redirected to the carrier\'s tracking page<br><br>You will also receive automated email updates with tracking information when your order ships and at key points during transit.'
      },
      {
        question: 'What if my shipment is damaged or items are missing?',
        answer: 'If you receive a damaged shipment or discover missing items:<br><br>1. Document the damage with photos before unpacking further<br>2. Note any damage on the delivery receipt when signing for the package<br>3. Contact our customer service team within 24 hours at 1-800-987-6543<br>4. Keep all original packaging materials until the claim is resolved<br><br>For missing items, please verify against the packing slip and contact customer service with the order number and details of the missing items.'
      },
      {
        question: 'Can I change my shipping address after placing an order?',
        answer: 'Address changes may be possible if the order has not yet been processed for shipping:<br><br>1. Log into your account and check your order status<br>2. If the status is "Processing" or earlier, contact customer service immediately<br>3. For orders already shipped, we cannot change the destination address<br>4. In some cases, we may be able to recall a package, but additional fees will apply<br><br>To avoid delivery issues, always verify your shipping address before completing your order.'
      },
      {
        question: 'What is your policy for partial shipments?',
        answer: 'Crown Nexus may split large orders into multiple shipments to ensure you receive available items as quickly as possible:<br><br>• You will not be charged extra shipping for partial shipments<br>• Each shipment will have its own tracking number<br>• You\'ll receive notification emails for each partial shipment<br>• Backordered items will ship as they become available<br><br>If you prefer to receive all items in a single shipment, please specify "Ship Complete" in the order notes during checkout or contact customer service.'
      },
      {
        question: 'How do I request a return for an incorrect item?',
        answer: 'If you received an incorrect item:<br><br>1. Contact customer service within 5 business days of receipt<br>2. Provide your order number and details about the incorrect item<br>3. We will issue an RMA and return shipping label at no cost to you<br>4. The correct item will be shipped as soon as possible<br>5. You are not responsible for restocking fees when we ship incorrect items<br><br>Please do not return items without an RMA number as this will delay processing and resolution.'
      }
    ]);
    
    return {
      activeTab,
      shippingMethods,
      carriers,
      expeditedOptions,
      customSolutions,
      shippingTools,
      shippingPolicies,
      orderProcessingSteps,
      freightGuidelines,
      ltlRequirements,
      packagingPractices,
      returnsProcess,
      returnPolicies,
      warrantyInformation,
      returnsResources,
      internationalRegions,
      internationalShippingMethods,
      customsDocuments,
      internationalReturns,
      commonQuestions
    };
  }
});
</script>

<style scoped>
/* Responsive timeline adjustments */
@media (max-width: 600px) {
  .v-timeline {
    overflow-x: auto;
    padding-bottom: 16px;
  }
}
</style>
