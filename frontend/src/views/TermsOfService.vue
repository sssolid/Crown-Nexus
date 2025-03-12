<!-- frontend/src/views/TermsOfService.vue -->
<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" lg="10" class="mx-auto">
          <div class="text-center mb-8">
            <h1 class="text-h3 font-weight-bold mb-3">Terms of Service</h1>
            <p class="text-subtitle-1">Last Updated: March 1, 2023</p>
          </div>

          <!-- Introduction Alert -->
          <v-alert
            type="info"
            variant="tonal"
            border="start"
            class="mb-6"
          >
            <strong>PLEASE READ THESE TERMS CAREFULLY BEFORE USING OUR SERVICES.</strong> By accessing or using Crown Nexus's platform, website, or services, you agree to be bound by these Terms of Service and all applicable laws and regulations. If you do not agree with any of these terms, you are prohibited from using or accessing our services.
          </v-alert>

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

          <!-- Terms Content -->
          <div class="terms-content">
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

          <!-- Print Button -->
          <div class="text-center mb-8">
            <v-btn 
              prepend-icon="mdi-printer"
              color="secondary"
              variant="tonal"
              @click="printTerms"
            >
              Print Terms of Service
            </v-btn>
          </div>

          <!-- Contact Card -->
          <v-card color="primary-lighten-5" variant="outlined" class="mt-10 mb-8">
            <v-card-title class="font-weight-bold">
              Questions About Our Terms of Service?
            </v-card-title>
            <v-card-text>
              <p>If you have any questions about these Terms of Service, please contact us:</p>
              <div class="d-flex align-center mt-4">
                <v-icon icon="mdi-email" class="mr-2" color="primary"></v-icon>
                <a href="mailto:legal@crownnexus.com" class="text-primary">legal@crownnexus.com</a>
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
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'TermsOfService',

  setup() {
    const sections = ref([
      {
        id: 'acceptance',
        title: '1. Acceptance of Terms',
        content: `
          <p>These Terms of Service ("Terms") govern your access to and use of Crown Nexus's website, platform, applications, products, and services (collectively, the "Services"). By registering for, accessing, or using our Services, you agree to be bound by these Terms and our Privacy Policy.</p>
          
          <p>If you are using our Services on behalf of a company, organization, or other entity, then "you" means both you individually and that entity. You represent and warrant that you are authorized to accept these Terms on behalf of that entity and bind them to these Terms, and that such entity agrees to indemnify us for violations of these Terms.</p>
          
          <p>We reserve the right to update and change these Terms at any time without notice. It is your responsibility to check this page periodically for changes. Your continued use of the Services following the posting of any changes constitutes your acceptance of such changes.</p>
        `
      },
      {
        id: 'account-registration',
        title: '2. Account Registration and Requirements',
        content: `
          <p>To access and use certain features of our Services, you must register for an account and provide certain information about yourself as prompted by the registration form. You represent and warrant that: (a) all required registration information you submit is truthful and accurate; (b) you will maintain the accuracy of such information; and (c) your use of the Services does not violate any applicable law or regulation.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.1 Business Account Requirements</h3>
          <p>Our Services are intended exclusively for business-to-business (B2B) transactions in the automotive aftermarket industry. To register for an account, you must:</p>
          
          <ul class="ml-6 mb-4">
            <li>Be a legally registered business entity</li>
            <li>Provide valid business identification (such as a tax ID, business license, or reseller certificate)</li>
            <li>Operate in the automotive aftermarket industry as a manufacturer, distributor, retailer, or service provider</li>
            <li>Be at least 18 years of age</li>
            <li>Provide accurate and complete business information</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.2 Account Security</h3>
          <p>You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account. You agree to:</p>
          
          <ul class="ml-6 mb-4">
            <li>Create a strong, unique password</li>
            <li>Keep your account credentials secure and confidential</li>
            <li>Restrict access to your account to authorized representatives only</li>
            <li>Notify us immediately of any unauthorized use of your account or any other breach of security</li>
            <li>Ensure that you log out from your account at the end of each session when accessing the Services from a shared computer</li>
          </ul>
          
          <p>We are not responsible for any loss or damage arising from your failure to comply with these security obligations.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">2.3 Account Termination</h3>
          <p>We reserve the right to disable or terminate your account, refuse service, remove or edit content, or cancel orders at our sole discretion if we believe that you have violated these Terms, engaged in illegal or fraudulent activity, or for any other reason we deem appropriate.</p>
        `
      },
      {
        id: 'service-usage',
        title: '3. Use of Services',
        content: `
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">3.1 License to Use</h3>
          <p>Subject to these Terms, we grant you a limited, non-exclusive, non-transferable, and revocable license to access and use the Services for your internal business purposes. This license does not include:</p>
          
          <ul class="ml-6 mb-4">
            <li>The right to resell or commercial use of the Services</li>
            <li>Collecting or harvesting any information from the Services for creating a database</li>
            <li>Any derivative use or making adaptations of the Services</li>
            <li>Downloading or copying account information for the benefit of another business</li>
            <li>Using data mining, robots, or similar data gathering and extraction tools</li>
            <li>Any use of the Services that places an unreasonable or disproportionately large load on our infrastructure</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">3.2 Acceptable Use</h3>
          <p>You agree not to use the Services to:</p>
          
          <ul class="ml-6 mb-4">
            <li>Upload, post, or transmit any content that is unlawful, harmful, threatening, abusive, harassing, defamatory, vulgar, obscene, or otherwise objectionable</li>
            <li>Impersonate any person or entity, or falsely state or otherwise misrepresent your affiliation with a person or entity</li>
            <li>Upload, post, or transmit any content that infringes any patent, trademark, trade secret, copyright, or other proprietary rights</li>
            <li>Upload, post, or transmit any unsolicited advertising, promotional materials, "junk mail," "spam," "chain letters," or any other form of solicitation</li>
            <li>Interfere with or disrupt the Services or servers or networks connected to the Services</li>
            <li>Attempt to gain unauthorized access to the Services, other accounts, computer systems, or networks connected to the Services</li>
            <li>Engage in any activity that is, in our sole judgment, harmful to other users or to us</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">3.3 API Usage and Integration</h3>
          <p>If you access our API (Application Programming Interface) or develop integrations with our Services:</p>
          
          <ul class="ml-6 mb-4">
            <li>You must comply with any additional API terms of service we provide</li>
            <li>You are responsible for securing any API keys or credentials we provide</li>
            <li>You may not exceed rate limits or otherwise abuse the API infrastructure</li>
            <li>We reserve the right to restrict, suspend, or terminate your API access at any time</li>
          </ul>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">3.4 Modifications to Services</h3>
          <p>We reserve the right to modify, suspend, or discontinue the Services (or any part or content thereof) at any time with or without notice. We will not be liable to you or to any third party for any modification, suspension, or discontinuance of the Services.</p>
        `
      },
      {
        id: 'orders-payments',
        title: '4. Orders and Payments',
        content: `
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.1 Order Acceptance</h3>
          <p>Your placement of an order does not necessarily constitute our acceptance of the order. We reserve the right to accept or decline your order for any reason, including but not limited to unavailability of products, errors in pricing or product information, or concerns about the authenticity of the order.</p>
          
          <p>An order is not considered accepted until we send you an order confirmation email or electronically send an order confirmation through the platform. We may verify information before accepting any order.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.2 Pricing and Payment</h3>
          <p>All prices listed on our platform are in U.S. dollars unless otherwise specified. Prices are subject to change without notice. We make every effort to ensure that prices displayed on our platform are correct, but errors may occur. If we discover an error in the price of items you have ordered, we will inform you as soon as possible and give you the option of reconfirming your order at the correct price or canceling it.</p>
          
          <p>Payment terms vary based on your account type and agreements with Crown Nexus:</p>
          
          <ul class="ml-6 mb-4">
            <li>Credit card payments are processed at the time of order placement</li>
            <li>Net terms (Net 30, Net 45, etc.) may be available for qualified accounts</li>
            <li>Other payment methods, such as ACH transfers or purchase orders, may be arranged based on your account status</li>
          </ul>
          
          <p>You agree to provide current, complete, and accurate billing information for all purchases. You further agree to promptly update your account and other information, including your email address and credit card numbers and expiration dates, so that we can complete your transactions and contact you as needed.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.3 Taxes</h3>
          <p>You are responsible for all applicable taxes, duties, and other governmental assessments associated with your purchase, except where we explicitly state otherwise. In states where we have a physical presence or nexus, we will collect and remit sales tax according to applicable state and local tax laws. For customers with valid tax exemption certificates, please submit the required documentation before placing an order.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">4.4 Shipping and Delivery</h3>
          <p>Shipping and delivery terms are as outlined in our Shipping & Returns Policy. Delivery dates and times are estimates only and are not guaranteed. We are not responsible for delays caused by circumstances beyond our reasonable control, including but not limited to, carrier delays, weather conditions, or natural disasters.</p>
          
          <p>Title and risk of loss for items purchased from us pass to you upon our delivery to the carrier or, if applicable, upon delivery to your designated shipping address.</p>
        `
      },
      {
        id: 'content-ownership',
        title: '5. Content and Intellectual Property',
        content: `
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">5.1 Our Content</h3>
          <p>All content included in or made available through our Services, such as text, graphics, logos, icons, images, audio clips, digital downloads, data compilations, and software, is the property of Crown Nexus or its licensors and is protected by United States and international copyright, trademark, and other intellectual property laws.</p>
          
          <p>The compilation of all content included in or made available through our Services is the exclusive property of Crown Nexus and is protected by U.S. and international copyright laws. All software used in our Services is the property of Crown Nexus or its licensors and is protected by U.S. and international copyright laws.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">5.2 Your Content</h3>
          <p>You retain ownership of any content that you upload, submit, store, send, or receive through the Services ("Your Content"). By uploading, submitting, storing, sending, or receiving Your Content through the Services, you grant us a worldwide, non-exclusive, royalty-free, sublicensable, and transferable license to use, reproduce, distribute, prepare derivative works of, display, and perform Your Content in connection with providing and promoting the Services.</p>
          
          <p>You represent and warrant that you have all rights, power, and authority necessary to grant the rights granted herein to Your Content; that Your Content does not violate any third-party rights, including intellectual property rights and rights of publicity and privacy; and that Your Content complies with all applicable laws and regulations.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">5.3 Trademarks</h3>
          <p>Crown Nexus, the Crown Nexus logo, and all other Crown Nexus trademarks, service marks, product names, and company names or logos cited herein are trademarks or registered trademarks of Crown Nexus. You may not use, copy, reproduce, republish, upload, post, transmit, distribute, or modify our trademarks in any way without our prior written consent. The use of our trademarks in connection with any product or service that is not ours, in a manner likely to cause confusion among customers, or in any manner that disparages or discredits us, is prohibited.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">5.4 Feedback</h3>
          <p>If you provide us with any feedback, suggestions, improvements, or ideas ("Feedback") regarding our Services, you hereby assign to us all rights in such Feedback and agree that we shall have the right to use and fully exploit such Feedback in any manner we deem appropriate. We will treat any Feedback as non-confidential and non-proprietary.</p>
        `
      },
      {
        id: 'disclaimer-warranties',
        title: '6. Disclaimer of Warranties',
        content: `
          <p>THE SERVICES AND ALL PRODUCTS OFFERED THROUGH THE SERVICES ARE PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, CROWN NEXUS DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND NON-INFRINGEMENT.</p>
          
          <p>CROWN NEXUS DOES NOT WARRANT THAT THE SERVICES OR PRODUCTS WILL MEET YOUR REQUIREMENTS, THAT THE SERVICES WILL BE UNINTERRUPTED, TIMELY, SECURE, OR ERROR-FREE, THAT THE INFORMATION PROVIDED THROUGH THE SERVICES WILL BE ACCURATE, RELIABLE, COMPLETE, OR CURRENT, OR THAT ANY DEFECTS IN THE SERVICES WILL BE CORRECTED.</p>
          
          <p>ANY MATERIAL DOWNLOADED OR OTHERWISE OBTAINED THROUGH THE USE OF THE SERVICES IS DONE AT YOUR OWN DISCRETION AND RISK, AND YOU WILL BE SOLELY RESPONSIBLE FOR ANY DAMAGE TO YOUR COMPUTER SYSTEM OR LOSS OF DATA THAT RESULTS FROM THE DOWNLOAD OF ANY SUCH MATERIAL.</p>
          
          <p>NO ADVICE OR INFORMATION, WHETHER ORAL OR WRITTEN, OBTAINED BY YOU FROM CROWN NEXUS OR THROUGH OR FROM THE SERVICES SHALL CREATE ANY WARRANTY NOT EXPRESSLY STATED IN THESE TERMS.</p>
          
          <p>SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF CERTAIN WARRANTIES, SO SOME OF THE ABOVE EXCLUSIONS MAY NOT APPLY TO YOU.</p>
        `
      },
      {
        id: 'limitation-liability',
        title: '7. Limitation of Liability',
        content: `
          <p>TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, CROWN NEXUS, ITS AFFILIATES, OFFICERS, EMPLOYEES, AGENTS, SUPPLIERS, AND LICENSORS WILL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING WITHOUT LIMITATION, LOSS OF PROFITS, DATA, USE, GOODWILL, OR OTHER INTANGIBLE LOSSES, RESULTING FROM (I) YOUR ACCESS TO OR USE OF OR INABILITY TO ACCESS OR USE THE SERVICES; (II) ANY CONDUCT OR CONTENT OF ANY THIRD PARTY ON THE SERVICES; (III) ANY CONTENT OBTAINED FROM THE SERVICES; AND (IV) UNAUTHORIZED ACCESS, USE, OR ALTERATION OF YOUR TRANSMISSIONS OR CONTENT, WHETHER BASED ON WARRANTY, CONTRACT, TORT (INCLUDING NEGLIGENCE), OR ANY OTHER LEGAL THEORY, WHETHER OR NOT WE HAVE BEEN INFORMED OF THE POSSIBILITY OF SUCH DAMAGE.</p>
          
          <p>IN NO EVENT WILL CROWN NEXUS'S TOTAL LIABILITY TO YOU FOR ALL DAMAGES, LOSSES, OR CAUSES OF ACTION EXCEED THE AMOUNT YOU HAVE PAID TO CROWN NEXUS IN THE LAST SIX (6) MONTHS, OR, IF GREATER, ONE HUNDRED DOLLARS ($100).</p>
          
          <p>THE LIMITATIONS OF LIABILITY IN THIS SECTION APPLY WHETHER THE ALLEGED LIABILITY IS BASED ON CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY, OR ANY OTHER BASIS, EVEN IF CROWN NEXUS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</p>
          
          <p>SOME JURISDICTIONS DO NOT ALLOW THE LIMITATION OR EXCLUSION OF LIABILITY FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES, SO THE ABOVE LIMITATIONS OR EXCLUSIONS MAY NOT APPLY TO YOU.</p>
        `
      },
      {
        id: 'indemnification',
        title: '8. Indemnification',
        content: `
          <p>You agree to defend, indemnify, and hold harmless Crown Nexus, its affiliates, officers, directors, employees, and agents, from and against any and all claims, damages, obligations, losses, liabilities, costs or debt, and expenses (including but not limited to attorney's fees) arising from:</p>
          
          <ul class="ml-6 mb-4">
            <li>Your use of and access to the Services</li>
            <li>Your violation of any term of these Terms</li>
            <li>Your violation of any third-party right, including without limitation any copyright, property, or privacy right</li>
            <li>Any claim that Your Content caused damage to a third party</li>
          </ul>
          
          <p>This defense and indemnification obligation will survive these Terms and your use of the Services.</p>
        `
      },
      {
        id: 'dispute-resolution',
        title: '9. Dispute Resolution',
        content: `
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">9.1 Governing Law</h3>
          <p>These Terms shall be governed by and construed in accordance with the laws of the State of Illinois, without regard to its conflict of law provisions. You agree to submit to the personal and exclusive jurisdiction of the courts located within Cook County, Illinois, to resolve any dispute or claim arising from these Terms.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">9.2 Arbitration</h3>
          <p>For any dispute you have with Crown Nexus, you agree to first contact us and attempt to resolve the dispute informally. If Crown Nexus has not been able to resolve the dispute with you informally, both parties agree to resolve any claim, controversy, or dispute arising out of or relating to these Terms through binding arbitration in Chicago, Illinois, in accordance with the Commercial Arbitration Rules of the American Arbitration Association.</p>
          
          <p>The arbitration will be conducted by a single arbitrator, and the arbitrator's award shall be binding and may be entered as a judgment in any court of competent jurisdiction. To the fullest extent permitted by applicable law, no arbitration under these Terms shall be joined to an arbitration involving any other party subject to these Terms, whether through class arbitration proceedings or otherwise.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">9.3 Waiver of Class Actions</h3>
          <p>YOU AND CROWN NEXUS AGREE THAT EACH MAY BRING CLAIMS AGAINST THE OTHER ONLY IN YOUR OR ITS INDIVIDUAL CAPACITY AND NOT AS A PLAINTIFF OR CLASS MEMBER IN ANY PURPORTED CLASS OR REPRESENTATIVE ACTION. Unless both you and Crown Nexus agree, no arbitrator or judge may consolidate more than one person's claims or otherwise preside over any form of a representative or class proceeding.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">9.4 Time Limitation on Claims</h3>
          <p>You agree that regardless of any statute or law to the contrary, any claim or cause of action arising out of or related to use of the Services or these Terms must be filed within one (1) year after such claim or cause of action arose or be forever barred.</p>
        `
      },
      {
        id: 'general-provisions',
        title: '10. General Provisions',
        content: `
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.1 Entire Agreement</h3>
          <p>These Terms, together with our Privacy Policy and any other legal notices or additional terms and conditions or policies published by Crown Nexus on the Services, shall constitute the entire agreement between you and Crown Nexus concerning the Services.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.2 Severability</h3>
          <p>If any provision of these Terms is deemed invalid by a court of competent jurisdiction, the invalidity of such provision shall not affect the validity of the remaining provisions of these Terms, which shall remain in full force and effect.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.3 Waiver</h3>
          <p>No waiver of any term of these Terms shall be deemed a further or continuing waiver of such term or any other term, and Crown Nexus's failure to assert any right or provision under these Terms shall not constitute a waiver of such right or provision.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.4 Assignment</h3>
          <p>These Terms, and any rights and licenses granted hereunder, may not be transferred or assigned by you, but may be assigned by Crown Nexus without restriction.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.5 Force Majeure</h3>
          <p>Crown Nexus shall not be liable for any failure to perform its obligations hereunder where such failure results from any cause beyond our reasonable control, including, without limitation, mechanical, electronic, or communications failure or degradation, acts of God, terrorist acts, natural disasters, pandemics, or government restrictions.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.6 Export Control</h3>
          <p>You agree to comply with all applicable export and re-export control laws and regulations, including the Export Administration Regulations maintained by the U.S. Department of Commerce, and trade and economic sanctions maintained by the Treasury Department's Office of Foreign Assets Control, in regard to products purchased through the Services.</p>
          
          <h3 class="text-h6 font-weight-bold mt-4 mb-2">10.7 Contact Information</h3>
          <p>If you have any questions about these Terms, please contact us at:</p>
          
          <p class="mt-4">
            <strong>Crown Nexus, Inc.</strong><br>
            123 Business Ave, Suite 500<br>
            Chicago, IL 60601<br>
            Email: legal@crownnexus.com<br>
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

    // Print terms function
    const printTerms = () => {
      window.print();
    };

    return {
      sections,
      scrollToSection,
      printTerms
    };
  }
});
</script>

<style scoped>
.terms-content {
  line-height: 1.6;
}

@media print {
  .v-app-bar,
  .v-footer,
  .v-btn {
    display: none !important;
  }
  
  .terms-content {
    font-size: 12pt;
  }
}
</style>
