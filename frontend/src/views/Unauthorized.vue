<!-- frontend/src/views/Unauthorized.vue -->
<template>
  <div class="d-flex align-center justify-center" style="height: 80vh">
    <v-card class="text-center pa-6" max-width="550" elevation="3">
      <v-card-title class="text-h3 font-weight-bold mb-4">Unauthorized</v-card-title>
      <v-card-subtitle class="text-h5 mb-4">Access Denied</v-card-subtitle>

      <v-card-text>
        <v-img
          src="@/assets/unauthorized.svg"
          alt="Unauthorized access"
          height="250"
          class="mb-6"
          contain
        >
          <!-- Fallback content if the image is not available -->
          <template v-slot:placeholder>
            <v-icon icon="mdi-shield-lock" size="x-large" color="error"></v-icon>
          </template>
        </v-img>

        <p class="text-body-1 mb-6">
          Sorry, you don't have permission to access this page.
          Please contact your system administrator if you believe this is a mistake.
        </p>

        <v-alert
          v-if="errorMessage"
          type="error"
          variant="tonal"
          class="mb-6 text-left"
        >
          {{ errorMessage }}
        </v-alert>

        <div class="d-flex flex-column flex-sm-row justify-center gap-4">
          <v-btn
            color="primary"
            size="large"
            variant="elevated"
            @click="goBack"
          >
            <v-icon icon="mdi-arrow-left" start></v-icon>
            Go Back
          </v-btn>

          <v-btn
            color="secondary"
            size="large"
            to="/"
            variant="tonal"
          >
            <v-icon icon="mdi-home" start></v-icon>
            Home
          </v-btn>

          <v-btn
            v-if="!isLoggedIn"
            color="info"
            size="large"
            to="/login"
            variant="tonal"
          >
            <v-icon icon="mdi-login" start></v-icon>
            Login
          </v-btn>
        </div>
      </v-card-text>

      <v-card-actions class="justify-center pt-4">
        <v-btn
          variant="text"
          color="grey"
          size="small"
          prepend-icon="mdi-lifebuoy"
          @click="showContactDialog = true"
        >
          Contact Support
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Contact Support Dialog -->
    <v-dialog v-model="showContactDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 pa-4">
          Contact Support
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pa-4">
          <p class="mb-4">
            If you need assistance with access permissions, please contact our support team:
          </p>

          <v-list density="compact">
            <v-list-item prepend-icon="mdi-email">
              <v-list-item-title>support@crownnexus.com</v-list-item-title>
            </v-list-item>
            <v-list-item prepend-icon="mdi-phone">
              <v-list-item-title>1-800-555-0123</v-list-item-title>
            </v-list-item>
            <v-list-item prepend-icon="mdi-clock">
              <v-list-item-title>Monday - Friday, 9AM - 5PM EST</v-list-item-title>
            </v-list-item>
          </v-list>

          <p class="mt-4 text-medium-emphasis">
            Please include your username and the page you were trying to access for faster assistance.
          </p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="tonal"
            @click="showContactDialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'Unauthorized',

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();

    const errorMessage = ref('');
    const showContactDialog = ref(false);

    // Check if the user is logged in
    const isLoggedIn = computed(() => authStore.isLoggedIn);

    // Get the error message from route query if available
    onMounted(() => {
      const queryError = route.query.error as string;
      if (queryError) {
        errorMessage.value = decodeURIComponent(queryError);
      }
    });

    // Go back to the previous page
    const goBack = () => {
      router.back();
    };

    return {
      isLoggedIn,
      errorMessage,
      showContactDialog,
      goBack
    };
  }
});
</script>

<style scoped>
/* Ensuring spacing even with custom component elements */
.gap-4 {
  gap: 1rem;
}

@media (max-width: 600px) {
  .gap-4 {
    gap: 0.75rem;
  }
}
</style>
