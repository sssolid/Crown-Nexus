<!-- frontend/src/views/ContactPage.vue -->
<template>
  <div class="contact-page">
    <!-- Hero Section -->
    <section class="contact-hero">
      <v-parallax
        src="https://images.unsplash.com/photo-1560264280-88b68371db39?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
        :height="300"
      >
        <div class="hero-overlay"></div>
        <v-container class="hero-content" fluid>
          <v-row align="center" justify="center">
            <v-col cols="12" md="10" lg="8" class="text-center text-white">
              <h1 class="text-h2 font-weight-bold mb-4">Contact Us</h1>
              <h2 class="text-h5 mb-2">We're here to support your business</h2>
            </v-col>
          </v-row>
        </v-container>
      </v-parallax>
    </section>

    <!-- Contact Options -->
    <section class="py-12">
      <v-container>
        <v-row>
          <!-- Contact Cards -->
          <v-col cols="12" md="4" v-for="(contact, i) in contactOptions" :key="i" class="mb-6 mb-md-0">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 8 : 2"
                height="100%"
                class="d-flex flex-column text-center"
              >
                <v-card-item>
                  <template v-slot:prepend>
                    <v-avatar :color="contact.color" size="64" class="mx-auto mb-4">
                      <v-icon size="32" :icon="contact.icon" color="white"></v-icon>
                    </v-avatar>
                  </template>
                </v-card-item>
                <v-card-title class="text-h5 justify-center">{{ contact.title }}</v-card-title>
                <v-card-text class="text-body-1">
                  <p v-if="contact.description" class="mb-4">{{ contact.description }}</p>
                  <div v-if="contact.value" class="font-weight-medium">{{ contact.value }}</div>
                  <div v-if="contact.subvalue" class="text-grey">{{ contact.subvalue }}</div>
                </v-card-text>
                <v-spacer></v-spacer>
                <v-card-actions class="justify-center pb-4">
                  <v-btn
                    v-if="contact.action"
                    :color="contact.color"
                    variant="tonal"
                    :href="contact.actionLink"
                    :prepend-icon="contact.actionIcon"
                  >
                    {{ contact.action }}
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Contact Form and Office Locations -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row>
          <!-- Contact Form -->
          <v-col cols="12" md="7" class="mb-8 mb-md-0">
            <v-card elevation="2">
              <v-card-title class="text-h5 bg-primary text-white px-6 py-4">
                <v-icon start icon="mdi-email-outline" class="me-2"></v-icon>
                Send us a message
              </v-card-title>
              <v-card-text class="pa-6">
                <p class="text-body-1 mb-6">
                  Fill out the form below, and a Crown Nexus representative will reach out to you within 1 business day.
                </p>

                <v-form ref="contactForm" v-model="formValid" @submit.prevent="submitForm">
                  <v-row>
                    <!-- Company Name -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.company"
                        label="Company Name*"
                        variant="outlined"
                        :rules="[rules.required]"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Business Type -->
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="formData.businessType"
                        label="Business Type*"
                        :items="businessTypes"
                        variant="outlined"
                        :rules="[rules.required]"
                        required
                      ></v-select>
                    </v-col>

                    <!-- Contact Name -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.name"
                        label="Contact Name*"
                        variant="outlined"
                        :rules="[rules.required]"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Contact Title/Role -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.title"
                        label="Title/Role"
                        variant="outlined"
                      ></v-text-field>
                    </v-col>

                    <!-- Email -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.email"
                        label="Email Address*"
                        type="email"
                        variant="outlined"
                        :rules="[rules.required, rules.email]"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Phone -->
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="formData.phone"
                        label="Phone Number*"
                        variant="outlined"
                        :rules="[rules.required]"
                        required
                      ></v-text-field>
                    </v-col>

                    <!-- Inquiry Type -->
                    <v-col cols="12">
                      <v-select
                        v-model="formData.inquiryType"
                        label="Inquiry Type*"
                        :items="inquiryTypes"
                        variant="outlined"
                        :rules="[rules.required]"
                        required
                      ></v-select>
                    </v-col>

                    <!-- Message -->
                    <v-col cols="12">
                      <v-textarea
                        v-model="formData.message"
                        label="Message*"
                        variant="outlined"
                        rows="5"
                        :rules="[rules.required]"
                        required
                      ></v-textarea>
                    </v-col>

                    <!-- Submit Button -->
                    <v-col cols="12" class="d-flex justify-end">
                      <v-btn
                        type="submit"
                        color="primary"
                        size="large"
                        :loading="formSubmitting"
                        :disabled="!formValid"
                      >
                        Submit Inquiry
                        <v-icon end icon="mdi-send"></v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Office Locations -->
          <v-col cols="12" md="5">
            <h3 class="text-h5 font-weight-bold mb-6">Our Locations</h3>

            <v-expansion-panels variant="accordion">
              <v-expansion-panel
                v-for="(location, i) in locations"
                :key="i"
                :title="location.name"
                :text="location.address"
              >
                <template v-slot:title>
                  <div class="d-flex align-center">
                    <v-avatar :color="location.color" size="36" class="me-4">
                      <v-icon color="white">{{ location.icon }}</v-icon>
                    </v-avatar>
                    <div>
                      <div class="text-subtitle-1 font-weight-bold">{{ location.name }}</div>
                      <div class="text-caption">{{ location.type }}</div>
                    </div>
                  </div>
                </template>
                <v-expansion-panel-text>
                  <div class="py-2">
                    <div class="mb-4">
                      <div class="text-body-1">{{ location.address }}</div>
                      <div class="text-body-1">{{ location.city }}, {{ location.state }} {{ location.zip }}</div>
                    </div>

                    <div class="mb-4">
                      <div class="d-flex align-center mb-2">
                        <v-icon icon="mdi-phone" class="me-2"></v-icon>
                        <span>{{ location.phone }}</span>
                      </div>
                      <div class="d-flex align-center">
                        <v-icon icon="mdi-email" class="me-2"></v-icon>
                        <span>{{ location.email }}</span>
                      </div>
                    </div>

                    <v-divider class="mb-4"></v-divider>

                    <div class="mb-4">
                      <div class="text-subtitle-2 font-weight-bold mb-2">Hours of Operation:</div>
                      <div class="text-body-2">
                        Monday - Friday: {{ location.hours.weekday }}<br>
                        Saturday: {{ location.hours.saturday }}<br>
                        Sunday: {{ location.hours.sunday }}
                      </div>
                    </div>

                    <!-- Map Placeholder (in a real implementation, you'd use Google Maps or similar) -->
                    <v-card elevation="0" class="bg-grey-lighten-3 d-flex align-center justify-center" height="180">
                      <div class="text-center">
                        <v-icon icon="mdi-map" size="36" class="mb-2"></v-icon>
                        <div class="text-body-2">
                          <a :href="location.mapUrl" target="_blank" class="text-decoration-none">
                            View on Google Maps
                          </a>
                        </div>
                      </div>
                    </v-card>
                  </div>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>

            <!-- Business Hours Card -->
            <v-card class="mt-6" variant="outlined">
              <v-card-title class="text-subtitle-1 font-weight-bold">
                <v-icon start icon="mdi-clock-outline" class="me-2"></v-icon>
                General Business Hours
              </v-card-title>
              <v-card-text>
                <v-list density="compact" lines="two">
                  <v-list-item>
                    <v-list-item-title>Customer Service</v-list-item-title>
                    <v-list-item-subtitle>Monday - Friday: 8:00 AM - 6:00 PM EST<br>Saturday: 9:00 AM - 3:00 PM EST</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Order Processing</v-list-item-title>
                    <v-list-item-subtitle>Monday - Friday: 7:00 AM - 7:00 PM EST<br>Saturday: 8:00 AM - 4:00 PM EST</v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>Technical Support</v-list-item-title>
                    <v-list-item-subtitle>Monday - Friday: 8:00 AM - 8:00 PM EST<br>Saturday: 9:00 AM - 2:00 PM EST</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Department Contacts -->
    <section class="py-12">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold mb-2">Specialist Teams</h2>
            <p class="text-subtitle-1">Contact the department that can best assist you</p>
          </v-col>
        </v-row>

        <v-row>
          <v-col v-for="(dept, i) in departments" :key="i" cols="12" sm="6" lg="4" class="mb-4">
            <v-card height="100%">
              <v-card-item>
                <template v-slot:prepend>
                  <v-avatar :color="dept.color" size="42" class="me-4">
                    <v-icon :icon="dept.icon" color="white"></v-icon>
                  </v-avatar>
                </template>
                <v-card-title>{{ dept.name }}</v-card-title>
              </v-card-item>
              <v-card-text>
                <p class="text-body-2 mb-3">{{ dept.description }}</p>
                <div class="d-flex align-center mb-2">
                  <v-icon size="small" icon="mdi-email" class="me-2"></v-icon>
                  <span>{{ dept.email }}</span>
                </div>
                <div class="d-flex align-center">
                  <v-icon size="small" icon="mdi-phone" class="me-2"></v-icon>
                  <span>{{ dept.phone }}</span>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- FAQ Section -->
    <section class="py-12 bg-grey-lighten-4">
      <v-container>
        <v-row class="mb-6">
          <v-col cols="12" class="text-center">
            <h2 class="text-h4 font-weight-bold mb-2">Frequently Asked Questions</h2>
            <p class="text-subtitle-1 mb-8">Find quick answers to common questions</p>
          </v-col>
        </v-row>

        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <v-expansion-panels variant="accordion">
              <v-expansion-panel
                v-for="(faq, i) in faqs"
                :key="i"
                :title="faq.question"
                :text="faq.answer"
              >
              </v-expansion-panel>
            </v-expansion-panels>

            <div class="text-center mt-8">
              <p class="text-body-1 mb-4">Still have questions? Our customer service team is ready to help.</p>
              <v-btn
                color="primary"
                variant="tonal"
                size="large"
                prepend-icon="mdi-headset"
                href="tel:+18005551234"
              >
                Call Customer Service
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Social Media & Newsletter -->
    <section class="py-12 bg-primary">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="text-center text-md-left text-white">
            <h3 class="text-h5 font-weight-bold mb-3">Connect with Us</h3>
            <p class="text-body-1 mb-6">
              Follow Crown Nexus on social media for industry news, product updates, and special offers.
            </p>
            <div class="d-flex justify-center justify-md-start">
              <v-btn v-for="(social, i) in socialMedia" :key="i"
                variant="outlined"
                :icon="social.icon"
                color="white"
                class="mx-2"
                :href="social.link"
                target="_blank">
              </v-btn>
            </div>
          </v-col>

          <v-col cols="12" md="6" class="mt-8 mt-md-0">
            <v-card>
              <v-card-text class="pa-6">
                <h3 class="text-h6 font-weight-bold mb-3">Subscribe to Our Newsletter</h3>
                <p class="text-body-2 mb-4">
                  Get the latest product updates, industry insights, and exclusive offers delivered to your inbox.
                </p>

                <v-form @submit.prevent="subscribeNewsletter">
                  <v-row>
                    <v-col cols="12" sm="8">
                      <v-text-field
                        v-model="newsletterEmail"
                        label="Email Address"
                        variant="outlined"
                        type="email"
                        density="comfortable"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="4" class="d-flex align-center">
                      <v-btn
                        type="submit"
                        color="primary"
                        block
                        :loading="newsletterSubmitting"
                      >
                        Subscribe
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Success Dialog -->
    <v-dialog v-model="showSuccessDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-success text-white pa-4">
          <v-icon start icon="mdi-check-circle" class="me-2"></v-icon>
          Message Sent Successfully
        </v-card-title>
        <v-card-text class="pa-6">
          <p class="text-body-1 mb-4">
            Thank you for reaching out to Crown Nexus. Your message has been received and a team member will contact you within 1 business day.
          </p>
          <p class="text-body-2">
            Reference Number: <span class="font-weight-bold">{{ referenceNumber }}</span>
          </p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="tonal"
            @click="showSuccessDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue';

interface ContactOption {
  title: string;
  icon: string;
  color: string;
  description?: string;
  value?: string;
  subvalue?: string;
  action?: string;
  actionIcon?: string;
  actionLink?: string;
}

interface Location {
  name: string;
  type: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  phone: string;
  email: string;
  hours: {
    weekday: string;
    saturday: string;
    sunday: string;
  };
  mapUrl: string;
  icon: string;
  color: string;
}

interface Department {
  name: string;
  description: string;
  email: string;
  phone: string;
  icon: string;
  color: string;
}

interface FAQ {
  question: string;
  answer: string;
}

interface SocialMedia {
  name: string;
  icon: string;
  link: string;
}

export default defineComponent({
  name: 'ContactPage',

  setup() {
    // Form data and state
    const contactForm = ref<any>(null);
    const formValid = ref(false);
    const formSubmitting = ref(false);
    const formData = reactive({
      company: '',
      businessType: '',
      name: '',
      title: '',
      email: '',
      phone: '',
      inquiryType: '',
      message: ''
    });

    // Business and inquiry types
    const businessTypes = [
      'Auto Repair Shop',
      'Auto Parts Retailer',
      'Dealership',
      'Fleet Service',
      'Distributor',
      'Manufacturer',
      'Other'
    ];

    const inquiryTypes = [
      'General Information',
      'Product Inquiry',
      'Become a Partner',
      'Technical Support',
      'Order Status',
      'Returns & Warranty',
      'Bulk Ordering',
      'Media & Press'
    ];

    // Validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required',
      email: (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    };

    // Newsletter
    const newsletterEmail = ref('');
    const newsletterSubmitting = ref(false);

    // Success dialog
    const showSuccessDialog = ref(false);
    const referenceNumber = ref('');

    // Contact options data
    const contactOptions = ref<ContactOption[]>([
      {
        title: 'Call Us',
        icon: 'mdi-phone',
        color: 'primary',
        description: 'Our customer service team is available during business hours:',
        value: '1-800-555-1234',
        subvalue: 'Monday-Friday: 8am-6pm EST',
        action: 'Call Now',
        actionIcon: 'mdi-phone',
        actionLink: 'tel:+18005551234'
      },
      {
        title: 'Email Us',
        icon: 'mdi-email',
        color: 'info',
        description: 'Send us an email and we\'ll respond within 24 hours:',
        value: 'contact@crownnexus.com',
        action: 'Send Email',
        actionIcon: 'mdi-email',
        actionLink: 'mailto:contact@crownnexus.com'
      },
      {
        title: 'Schedule a Demo',
        icon: 'mdi-presentation',
        color: 'success',
        description: 'See our platform in action with a personalized demo:',
        value: 'Book a 30-minute session with a product specialist',
        action: 'Schedule Now',
        actionIcon: 'mdi-calendar',
        actionLink: '/demo'
      }
    ]);

    // Locations data
    const locations = ref<Location[]>([
      {
        name: 'Headquarters',
        type: 'Corporate Office & Distribution Center',
        address: '1500 Automotive Drive',
        city: 'Detroit',
        state: 'MI',
        zip: '48201',
        phone: '(313) 555-7000',
        email: 'info@crownnexus.com',
        hours: {
          weekday: '8:00 AM - 6:00 PM EST',
          saturday: '9:00 AM - 3:00 PM EST',
          sunday: 'Closed'
        },
        mapUrl: 'https://maps.google.com',
        icon: 'mdi-office-building',
        color: 'primary'
      },
      {
        name: 'West Coast Distribution Center',
        type: 'Distribution & Customer Service',
        address: '2300 Pacific Avenue',
        city: 'Los Angeles',
        state: 'CA',
        zip: '90058',
        phone: '(213) 555-9000',
        email: 'westcoast@crownnexus.com',
        hours: {
          weekday: '8:00 AM - 6:00 PM PST',
          saturday: '9:00 AM - 3:00 PM PST',
          sunday: 'Closed'
        },
        mapUrl: 'https://maps.google.com',
        icon: 'mdi-warehouse',
        color: 'success'
      },
      {
        name: 'Southern Distribution Center',
        type: 'Distribution & Technical Support',
        address: '850 Logistics Parkway',
        city: 'Dallas',
        state: 'TX',
        zip: '75247',
        phone: '(214) 555-6000',
        email: 'southern@crownnexus.com',
        hours: {
          weekday: '8:00 AM - 6:00 PM CST',
          saturday: '9:00 AM - 3:00 PM CST',
          sunday: 'Closed'
        },
        mapUrl: 'https://maps.google.com',
        icon: 'mdi-warehouse',
        color: 'warning'
      },
      {
        name: 'Southeast Distribution Center',
        type: 'Distribution & Returns Processing',
        address: '1200 Commerce Boulevard',
        city: 'Atlanta',
        state: 'GA',
        zip: '30318',
        phone: '(404) 555-4000',
        email: 'southeast@crownnexus.com',
        hours: {
          weekday: '8:00 AM - 6:00 PM EST',
          saturday: '9:00 AM - 3:00 PM EST',
          sunday: 'Closed'
        },
        mapUrl: 'https://maps.google.com',
        icon: 'mdi-warehouse',
        color: 'error'
      }
    ]);

    // Department contacts data
    const departments = ref<Department[]>([
      {
        name: 'Sales',
        description: 'For new accounts, product inquiries, and pricing information.',
        email: 'sales@crownnexus.com',
        phone: '(800) 555-1235',
        icon: 'mdi-cash-register',
        color: 'success'
      },
      {
        name: 'Customer Service',
        description: 'For assistance with existing orders, returns, and general inquiries.',
        email: 'support@crownnexus.com',
        phone: '(800) 555-1236',
        icon: 'mdi-account-voice',
        color: 'primary'
      },
      {
        name: 'Technical Support',
        description: 'For product specifications, fitment questions, and technical assistance.',
        email: 'tech@crownnexus.com',
        phone: '(800) 555-1237',
        icon: 'mdi-tools',
        color: 'info'
      },
      {
        name: 'Warranty Claims',
        description: 'For processing warranty claims and product replacements.',
        email: 'warranty@crownnexus.com',
        phone: '(800) 555-1238',
        icon: 'mdi-shield-check',
        color: 'warning'
      },
      {
        name: 'Accounts Receivable',
        description: 'For billing inquiries, payment processing, and account updates.',
        email: 'accounting@crownnexus.com',
        phone: '(800) 555-1239',
        icon: 'mdi-cash-multiple',
        color: 'error'
      },
      {
        name: 'Careers',
        description: 'For employment opportunities and human resources inquiries.',
        email: 'careers@crownnexus.com',
        phone: '(800) 555-1240',
        icon: 'mdi-briefcase',
        color: 'secondary'
      }
    ]);

    // FAQ data
    const faqs = ref<FAQ[]>([
      {
        question: 'How do I create a B2B account?',
        answer: 'To create a B2B account, click on the "Sign Up" button in the top-right corner of our website. You\'ll need to provide your business details, including your company name, business type, and contact information. We\'ll verify your business credentials and activate your account within 1-2 business days.'
      },
      {
        question: 'What are your shipping options and times?',
        answer: 'We offer several shipping methods including standard (3-5 business days), expedited (2-3 business days), and premium (next business day). Orders placed before 2:00 PM EST are typically processed the same day. Shipping times may vary based on your location and the availability of products in your nearest distribution center.'
      },
      {
        question: 'Do you offer volume discounts?',
        answer: 'Yes, we offer tiered volume discounts based on order value and quantity. These discounts are automatically applied to qualifying orders. For large or recurring orders, please contact our sales team to discuss custom pricing options and potential contract terms.'
      },
      {
        question: 'What is your return policy?',
        answer: 'We offer a 30-day return policy on most products. Items must be in their original packaging and in resalable condition. To initiate a return, please log into your account and visit the "Orders" section, or contact our customer service team. Some products may have special return requirements or restocking fees.'
      },
      {
        question: 'How can I check if a part is compatible with a specific vehicle?',
        answer: 'Our website features a comprehensive fitment search tool. Simply enter the year, make, model, and engine details of the vehicle to see all compatible parts. You can also contact our technical support team for assistance with complex fitment questions or specialty applications.'
      },
      {
        question: 'What forms of payment do you accept?',
        answer: 'We accept major credit cards (Visa, Mastercard, American Express, Discover), ACH transfers, and approved business checks. Established business customers may qualify for net terms (Net 30) following a credit approval process. Please contact our accounting department for more information on credit applications.'
      }
    ]);

    // Social media data
    const socialMedia = ref<SocialMedia[]>([
      { name: 'Facebook', icon: 'mdi-facebook', link: 'https://facebook.com/' },
      { name: 'Twitter', icon: 'mdi-twitter', link: 'https://twitter.com/' },
      { name: 'LinkedIn', icon: 'mdi-linkedin', link: 'https://linkedin.com/' },
      { name: 'Instagram', icon: 'mdi-instagram', link: 'https://instagram.com/' },
      { name: 'YouTube', icon: 'mdi-youtube', link: 'https://youtube.com/' }
    ]);

    // Submit form function
    const submitForm = async () => {
      const valid = await contactForm.value?.validate();

      if (!valid.valid) {
        return;
      }

      formSubmitting.value = true;

      try {
        // Here you would submit the form data to your API
        // For demonstration purposes, we'll simulate a successful submission
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Generate a reference number
        referenceNumber.value = `CNX-${Math.floor(Date.now() / 1000)}-${Math.floor(Math.random() * 1000)}`;

        // Show success dialog
        showSuccessDialog.value = true;

        // Reset form
        contactForm.value?.reset();
        Object.keys(formData).forEach(key => {
          formData[key as keyof typeof formData] = '';
        });

      } catch (error) {
        console.error('Error submitting form:', error);
        // Here you would handle submission errors
      } finally {
        formSubmitting.value = false;
      }
    };

    // Subscribe to newsletter function
    const subscribeNewsletter = async () => {
      if (!newsletterEmail.value || !/.+@.+\..+/.test(newsletterEmail.value)) {
        return;
      }

      newsletterSubmitting.value = true;

      try {
        // Here you would submit the email to your newsletter API
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Show success message or handle as needed
        alert('Thank you for subscribing to our newsletter!');
        newsletterEmail.value = '';

      } catch (error) {
        console.error('Error subscribing to newsletter:', error);
      } finally {
        newsletterSubmitting.value = false;
      }
    };

    return {
      // Form
      contactForm,
      formValid,
      formSubmitting,
      formData,
      businessTypes,
      inquiryTypes,
      rules,
      submitForm,

      // Newsletter
      newsletterEmail,
      newsletterSubmitting,
      subscribeNewsletter,

      // Success dialog
      showSuccessDialog,
      referenceNumber,

      // Data
      contactOptions,
      locations,
      departments,
      faqs,
      socialMedia
    };
  }
});
</script>

<style scoped>
.contact-hero {
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
</style>
