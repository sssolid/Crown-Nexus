// frontend/src/components/layout/DashboardFooter.vue
<template>
  <v-footer app class="px-4 py-2 bg-grey-lighten-4">
    <v-row no-gutters align="center" justify="space-between">
      <v-col cols="auto">
        <span class="text-caption text-grey-darken-1">
          &copy; {{ new Date().getFullYear() }} Crown Nexus
        </span>
      </v-col>

      <v-col cols="auto">
        <v-btn
          v-for="link in links"
          :key="link.text"
          :to="link.to"
          variant="text"
          color="grey-darken-1"
          density="compact"
          class="text-caption mx-1"
        >
          {{ link.text }}
        </v-btn>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

interface FooterLink {
  text: string;
  to: string;
}

export default defineComponent({
  name: 'DashboardFooter',

  setup() {
    const links = ref<FooterLink[]>([
      { text: 'Privacy Policy', to: '/privacy' },
      { text: 'Terms of Service', to: '/terms' },
      { text: 'Help', to: '/faq' },
      { text: 'Contact Support', to: '/contact' },
    ]);

    return {
      links,
    };
  },
});
</script>
