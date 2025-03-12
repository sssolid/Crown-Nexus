// frontend/src/components/layout/MainFooter.vue
<template>
  <v-footer class="bg-grey-darken-4 pa-6">
    <v-container>
      <v-row>
        <v-col cols="12" md="4" class="mb-6 mb-md-0">
          <h3 class="text-h6 font-weight-bold text-white mb-4">Crown Nexus</h3>
          <p class="text-body-2 text-grey">
            The premier B2B platform for automotive aftermarket parts. We connect manufacturers, distributors, and retailers in one seamless ecosystem.
          </p>
          <div class="mt-4">
            <v-btn icon="mdi-facebook" variant="text" color="white" class="me-2"></v-btn>
            <v-btn icon="mdi-twitter" variant="text" color="white" class="me-2"></v-btn>
            <v-btn icon="mdi-linkedin" variant="text" color="white" class="me-2"></v-btn>
            <v-btn icon="mdi-instagram" variant="text" color="white"></v-btn>
          </div>
        </v-col>

        <v-col cols="12" md="8">
          <v-row>
            <v-col cols="6" sm="4">
              <h4 class="text-subtitle-1 font-weight-bold text-white mb-4">Products</h4>
              <v-list density="compact" bg-color="transparent" class="pa-0">
                <v-list-item v-for="link in productLinks" :key="link.text" :to="link.to" class="px-0">
                  <v-list-item-title class="text-grey">{{ link.text }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="6" sm="4">
              <h4 class="text-subtitle-1 font-weight-bold text-white mb-4">Company</h4>
              <v-list density="compact" bg-color="transparent" class="pa-0">
                <v-list-item v-for="link in companyLinks" :key="link.text" :to="link.to" class="px-0">
                  <v-list-item-title class="text-grey">{{ link.text }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-col>

            <v-col cols="6" sm="4">
              <h4 class="text-subtitle-1 font-weight-bold text-white mb-4">Support</h4>
              <v-list density="compact" bg-color="transparent" class="pa-0">
                <v-list-item v-for="link in supportLinks" :key="link.text" :to="link.to" class="px-0">
                  <v-list-item-title class="text-grey">{{ link.text }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-divider class="my-6 bg-grey-darken-2"></v-divider>

      <div class="text-center text-grey text-caption">
        &copy; {{ new Date().getFullYear() }} Crown Nexus. All rights reserved.
      </div>
    </v-container>
  </v-footer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

interface FooterLink {
  text: string;
  to: string;
}

export default defineComponent({
  name: 'MainFooter',

  setup() {
    // Footer links
    const productLinks = ref<FooterLink[]>([
      { text: 'Catalog', to: '/products' },
      { text: 'Fitments', to: '/fitments' },
      { text: 'New Arrivals', to: '/products?sort=newest' },
      { text: 'Featured Items', to: '/products?featured=true' },
      { text: 'Media Library', to: '/media' },
    ]);

    const companyLinks = ref<FooterLink[]>([
      { text: 'About Us', to: '/about' },
      { text: 'Services', to: '/services' },
      { text: 'Careers', to: '/careers' },
      { text: 'Partners', to: '/partners' },
      { text: 'Testimonials', to: '/testimonials' },
      { text: 'Contact', to: '/contact' },
      { text: 'Blog', to: '/blog' },
    ]);

    const supportLinks = ref<FooterLink[]>([
      { text: 'FAQ', to: '/faq' },
      { text: 'Resources', to: '/resources' },
      { text: 'Privacy Policy', to: '/privacy' },
      { text: 'Terms of Service', to: '/terms' },
      { text: 'Shipping & Returns', to: '/shipping-returns' },
      { text: 'Pricing', to: '/pricing' },
    ]);

    return {
      productLinks,
      companyLinks,
      supportLinks,
    };
  },
});
</script>
