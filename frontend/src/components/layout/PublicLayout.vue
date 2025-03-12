// frontend/src/components/layout/PublicLayout.vue
<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn
        to="/"
        variant="plain"
        class="text-h5 font-weight-bold text-white no-hover no-outline"
      >
        Crown Nexus
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn to="/about" text>About</v-btn>
      <v-btn to="/services" text>Services</v-btn>
      <v-btn to="/resources" text>Resources</v-btn>
      <v-btn to="/contact" text>Contact</v-btn>
      <v-btn to="/login" text>Login</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <slot></slot>
      </v-container>
    </v-main>

    <main-footer />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import MainFooter from './MainFooter.vue';

export default defineComponent({
  name: 'PublicLayout',
  components: {
    MainFooter
  }
});
</script>
