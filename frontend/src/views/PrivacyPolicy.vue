<!-- frontend/src/views/PrivacyPolicy.vue -->
<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" lg="10" class="mx-auto">
          <div class="text-center mb-8">
            <h1 class="text-h3 font-weight-bold mb-3">Privacy Policy</h1>
            <p class="text-subtitle-1">Last Updated: March 1, 2023</p>
          </div>

          <!-- Table of Contents -->
          <v-card class="mb-8" variant="outlined">
            <v-card-title class="font-weight-bold">
              Table of Contents
            </v-card-title>
            <v-card-text>
              <v-list density="compact" nav>
                <v-list-item 
                  v-for="(section, index) in sections" 
                  :key="index"
                  :title="section.title"
                  @click="scrollToSection(section.id)"
                  class="rounded"
                  color="primary"
                ></v-list-item>
              </v-list>
            </v-card-text>
          </v-card>

          <!-- Policy Content -->
          <div class="privacy-policy-content">
            <section 
              v-for="(section, index) in sections" 
              :key="index"
              :id="section.id"
              class="mb-10"
            >
              <h2 class="text-h4 font-weight-bold mb-4">{{ section.title }}</h2>
              <div v-html="section.content"></div>
            </section>
          </div>

          <!-- Contact Information -->
          <v-card color="primary-lighten-5" variant="outlined" class="mt-10 mb-8">
            <v-card-title class="font-weight-bold">
              Questions About Our Privacy Policy?
            </v-card-title>
            <v-card-text>
              <p>If you have any questions or concerns about our privacy policy, please contact our privacy team:</p>
              <div class="d-flex align-center mt-4">
                <v-icon icon="mdi-email" class="mr-2" color="primary"></v-icon>
                <a href="mailto:privacy@crownnexus.com" class="text-primary">privacy@crownnexus.com</a>
              </div>
              <div class="d-flex align-center mt-2">
                <v-icon icon="mdi-phone" class="mr-2" color="primary"></v-icon>
                <a href="tel:+18009876543" class="text-primary">1-800-987-6543</a>
              </div>
              <div class="d-flex align-center mt-2">
                <v-icon icon="mdi-map-marker" class="mr-2" color="primary"></v-icon>
                <span>Crown Nexus, Inc., 123 Business Ave, Suite 500, Chicago, IL 60601</span>
              </div>
            </v-card-text>
          </v-card>

          <!-- Print Button -->
          <div class="text-center mb-8">
            <v-btn 
              prepend-icon="mdi-printer"
              color="secondary"
              variant="tonal"
              @click="printPolicy"
            >
              Print Privacy Policy
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'PrivacyPolicy',

  setup() {
    const sections = ref([
      {
        id: 'introduction',
        title: '1. Introduction',
        content: `
          <p>Crown Nexus ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you visit our website, use our platform, or engage with our services.</p>
          
          <p>Please read this Privacy Policy carefully. By accessing or using our platform, you acknowledge that you have read, understood, and agree to be bound by all the terms outlined in this Privacy Policy. If you do not agree with our policies and practices, please do not use our services.</p>
          
          <p>We reserve the right to make changes to this Privacy Policy at any time and for any reason. We will alert you about any changes by updating the "Last Updated" date of this Privacy Policy. You are encouraged to periodically review this Privacy Policy to stay informed of updates.</p>
        `
      },
      {
        id: 'information-collection',
        title: '2. Information We Collect',
        content: `
          <p>We may collect information about you in various ways. The information we collect may include:</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.1 Personal Data</h3>
          <p>Personally identifiable information that you voluntarily provide to us when registering with our platform, expressing an interest in obtaining information about us or our products and services, or otherwise contacting us. This personal data may include:</p>
          
          <ul class="ml-6 mb-4">
            <li>Name</li>
            <li>Email address</li>
            <li>Phone number</li>
            <li>Business name and address</li>
            <li>Job title and department</li>
            <li>Login credentials</li>
            <li>Billing information</li>
            <li>Other information you choose to provide</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.2 Derivative Data</h3>
          <p>Information our servers automatically collect when you access our platform, such as your IP address, browser type, operating system, access times, and the pages you have viewed directly before and after accessing our site.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.3 Financial Data</h3>
          <p>Financial information, such as data related to your payment method (e.g., credit card number, bank account information) that we may collect when you purchase our products or services. We store only very limited, if any, financial information that we collect. Otherwise, all financial information is stored by our payment processor, and you are encouraged to review their privacy policy and contact them directly for responses to your questions.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.4 Commercial Data</h3>
          <p>Business transaction data, including information about the products and services you purchase, order history, customer account information, shipping information, and other data related to your use of our platform for commercial purposes.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.5 Mobile Device Data</h3>
          <p>Device information, such as your mobile device ID, model, and manufacturer, and information about the location of your device, if you access our platform from a mobile device.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.6 Third-Party Data</h3>
          <p>Information from third parties, such as business partners, affiliate programs, or other third-party integrations within our platform. This may include information about your interactions with our partners or publicly available information about you or your business.</p>
        `
      },
      {
        id: 'information-use',
        title: '3. How We Use Your Information',
        content: `
          <p>We may use the information we collect about you for various purposes, including:</p>
          
          <ul class="ml-6 mb-4">
            <li>Creating and managing your account</li>
            <li>Processing transactions and sending order confirmations</li>
            <li>Providing customer service and responding to inquiries</li>
            <li>Personalizing your experience on our platform</li>
            <li>Delivering targeted advertising, newsletters, and other information about our products and services</li>
            <li>Conducting market research and analyzing user behavior to improve our platform and offerings</li>
            <li>Developing new products, services, and features</li>
            <li>Preventing fraudulent transactions and monitoring against errors</li>
            <li>Administering promotions, surveys, contests, or other site features</li>
            <li>Sending administrative information, such as updates to our terms, conditions, and policies</li>
            <li>Compiling anonymous statistical data for our own use or for a third party's use</li>
            <li>Complying with legal obligations</li>
          </ul>
          
          <p>We may also use your information for any other purpose disclosed to you at the time we collect or receive the information, or otherwise with your consent.</p>
        `
      },
      {
        id: 'information-disclosure',
        title: '4. Disclosure of Your Information',
        content: `
          <p>We may share information we have collected about you in certain situations. Your information may be disclosed as follows:</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.1 By Law or to Protect Rights</h3>
          <p>If we believe the release of information about you is necessary to respond to legal process, to investigate or remedy potential violations of our policies, or to protect the rights, property, and safety of others, we may share your information as permitted or required by any applicable law, rule, or regulation.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.2 Third-Party Service Providers</h3>
          <p>We may share your information with third parties that perform services for us or on our behalf, including payment processing, data analysis, email delivery, hosting services, customer service, and marketing assistance. These service providers are contractually obligated to use your information only for the purposes of providing services to us and to maintain the confidentiality and security of your information.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.3 Business Partners</h3>
          <p>We may share your information with our business partners to offer you certain products, services, or promotions.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.4 Business Transfers</h3>
          <p>If we or our subsidiaries are involved in a merger, acquisition, asset sale, or bankruptcy, your information may be transferred as part of that transaction. We will notify you before your information is transferred and becomes subject to a different Privacy Policy.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.5 Interactions with Other Users</h3>
          <p>If you interact with other users of our platform, those users may see your name, profile information, and descriptions of your activity.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.6 Online Postings</h3>
          <p>When you post comments, contributions, or other content to our platform, your posts may be viewed by all users and may be publicly distributed outside the platform in perpetuity.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.7 With Your Consent</h3>
          <p>We may disclose your information for any other purpose with your consent.</p>
        `
      },
      {
        id: 'tracking-cookies',
        title: '5. Tracking Technologies & Cookies',
        content: `
          <p>We may use cookies, web beacons, tracking pixels, and other tracking technologies on our platform to help customize and improve your experience. By using our platform, you agree to our use of these technologies as described in this Privacy Policy.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">5.1 Cookies</h3>
          <p>A cookie is a data file placed on your device when you visit our platform. We use cookies to enhance your experience, analyze usage patterns, remember your preferences, and for marketing purposes. Most web browsers are set to accept cookies by default. You can set your browser to refuse all or some cookies, or to alert you when cookies are being sent. However, if you disable or refuse cookies, some parts of our platform may be inaccessible or not function properly.</p>
          
          <p>We use the following types of cookies:</p>
          
          <ul class="ml-6 mb-4">
            <li><strong>Essential Cookies:</strong> Required for the basic functionality of our platform, such as security, authentication, and session management.</li>
            <li><strong>Functional Cookies:</strong> Allow us to remember your preferences and settings to enhance your experience.</li>
            <li><strong>Analytics Cookies:</strong> Help us understand how users interact with our platform, allowing us to improve functionality and performance.</li>
            <li><strong>Marketing Cookies:</strong> Used to track visitors across websites to enable targeted advertising.</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">5.2 Web Beacons and Tracking Pixels</h3>
          <p>Web beacons, also known as clear GIFs, pixel tags, or tracking pixels, are tiny graphics files that contain a unique identifier that enables us to recognize when someone has visited our platform or opened an email we have sent them. This allows us to monitor the traffic patterns of users from one page within our platform to another, deliver or communicate with cookies, understand whether you have come to our platform from an online advertisement displayed on a third-party website, and improve site performance.</p>
        `
      },
      {
        id: 'third-party-websites',
        title: '6. Third-Party Websites',
        content: `
          <p>Our platform may contain links to third-party websites and applications. Once you leave our platform or are redirected to a third-party website or application, you are no longer governed by this Privacy Policy. We are not responsible for the privacy practices of these third-party websites and encourage you to read their privacy policies.</p>
          
          <p>Our platform may also use third-party services to support certain functionalities, such as payment processing, data analysis, email delivery, and hosting. These third-party service providers have access to your information only to perform these tasks on our behalf and are obligated not to disclose or use it for any other purpose.</p>
        `
      },
      {
        id: 'data-security',
        title: '7. Data Security',
        content: `
          <p>We implement security measures designed to protect your information from unauthorized access, disclosure, alteration, or destruction. These measures include:</p>
          
          <ul class="ml-6 mb-4">
            <li>Using industry-standard encryption to protect sensitive data transmission</li>
            <li>Limiting access to your information to employees who need it to perform job functions</li>
            <li>Implementing physical, electronic, and procedural safeguards</li>
            <li>Regularly reviewing and updating our security practices</li>
            <li>Requiring strong authentication for account access</li>
          </ul>
          
          <p>However, no security system is impenetrable, and we cannot guarantee the security of our systems 100%. In the event that any information under our control is compromised as a result of a breach of security, we will take reasonable steps to investigate the situation and, where appropriate, notify those individuals whose information may have been compromised and take other steps in accordance with any applicable laws and regulations.</p>
        `
      },
      {
        id: 'data-retention',
        title: '8. Data Retention',
        content: `
          <p>We will retain your information for as long as your account is active, as necessary to provide you with the services you have requested, to comply with our legal obligations, resolve disputes, and enforce our agreements.</p>
          
          <p>When we no longer need personal information for the purposes for which we collected it, we will take reasonable steps to destroy or permanently de-identify that information, unless we are required by law or business purpose to keep it.</p>
        `
      },
      {
        id: 'children-privacy',
        title: '9. Children\'s Privacy',
        content: `
          <p>Our platform is not intended for use by children under the age of 18. We do not knowingly collect personally identifiable information from children under 18. If you are a parent or guardian and you believe we have collected information from your child, please contact us immediately. If we discover that a child under 18 has provided us with personal information, we will promptly delete such information from our systems.</p>
        `
      },
      {
        id: 'your-rights',
        title: '10. Your Rights and Choices',
        content: `
          <p>You have certain rights regarding your personal information. These may include:</p>
          
          <ul class="ml-6 mb-4">
            <li><strong>Access and Update:</strong> You can review and change your personal information by logging into your account settings.</li>
            <li><strong>Opt-Out:</strong> You can opt-out of marketing communications by following the unsubscribe instructions included in each email, or by contacting us directly.</li>
            <li><strong>Cookie Settings:</strong> Most web browsers are set to accept cookies by default. You can usually modify your browser settings to decline cookies if you prefer.</li>
            <li><strong>Do Not Track:</strong> We do not currently respond to Do Not Track (DNT) signals. However, you may disable certain tracking as discussed in this Privacy Policy.</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.1 Rights for Users in Certain Jurisdictions</h3>
          <p>Depending on your location, you may have additional rights regarding your personal information, such as:</p>
          
          <ul class="ml-6 mb-4">
            <li>The right to request access to your personal information</li>
            <li>The right to request correction of inaccurate personal information</li>
            <li>The right to request deletion of your personal information</li>
            <li>The right to restrict processing of your personal information</li>
            <li>The right to data portability</li>
            <li>The right to object to processing of your personal information</li>
            <li>The right to withdraw consent</li>
          </ul>
          
          <p>If you wish to exercise any of these rights, please contact us using the information provided at the end of this Privacy Policy.</p>
        `
      },
      {
        id: 'california-privacy',
        title: '11. California Privacy Rights',
        content: `
          <p>California Civil Code Section 1798.83, also known as the "Shine The Light" law, permits users who are California residents to request and obtain from us, once a year and free of charge, information about categories of personal information (if any) we disclosed to third parties for direct marketing purposes and the names and addresses of all third parties with which we shared personal information in the immediately preceding calendar year.</p>
          
          <p>California residents may also have additional rights under the California Consumer Privacy Act (CCPA) regarding their personal information. These rights may include:</p>
          
          <ul class="ml-6 mb-4">
            <li>The right to know about personal information collected, disclosed, or sold</li>
            <li>The right to request deletion of personal information</li>
            <li>The right to opt-out of the sale of personal information</li>
            <li>The right to non-discrimination for exercising their CCPA rights</li>
          </ul>
          
          <p>To make such a request, please contact us using the information provided at the end of this Privacy Policy.</p>
        `
      },
      {
        id: 'international-transfers',
        title: '12. International Data Transfers',
        content: `
          <p>We are based in the United States and process information on servers located in the United States and other countries. If you are located outside the United States, please be aware that information we collect will be transferred to and processed in the United States. By using our platform or providing us with any information, you consent to the transfer, processing, and storage of your information in the United States and other countries where the privacy laws may not be as comprehensive as those in the country where you reside.</p>
          
          <p>We take appropriate measures to ensure that your personal information is treated securely and in accordance with this Privacy Policy and applicable data protection laws, regardless of where it is processed or stored.</p>
        `
      },
      {
        id: 'policy-updates',
        title: '13. Privacy Policy Updates',
        content: `
          <p>We may update this Privacy Policy from time to time. The updated version will be indicated by an updated "Last Updated" date and the updated version will be effective as soon as it is accessible. We encourage you to review this Privacy Policy frequently to be informed of how we are protecting your information.</p>
          
          <p>If we make material changes to this Privacy Policy, we may notify you either by prominently posting a notice of such changes or by directly sending you a notification. We encourage you to review this Privacy Policy frequently to be informed of how we are protecting your information.</p>
        `
      },
      {
        id: 'contact-us',
        title: '14. Contact Us',
        content: `
          <p>If you have questions or comments about this Privacy Policy, please contact us at:</p>
          
          <p class="mt-4">
            <strong>Crown Nexus, Inc.</strong><br>
            123 Business Ave, Suite 500<br>
            Chicago, IL 60601<br>
            Email: privacy@crownnexus.com<br>
            Phone: 1-800-987-6543
          </p>
        `
      }
    ]);

    // Scroll to specific section
    const scrollToSection = (sectionId: string) => {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    };

    // Print policy function
    const printPolicy = () => {
      window.print();
    };

    return {
      sections,
      scrollToSection,
      printPolicy
    };
  }
});
</script>

<style scoped>
.privacy-policy-content {
  line-height: 1.6;
}

@media print {
  .v-app-bar,
  .v-footer,
  v-btn {
    display: none !important;
  }
  
  .privacy-policy-content {
    font-size: 12pt;
  }
}
</style>
