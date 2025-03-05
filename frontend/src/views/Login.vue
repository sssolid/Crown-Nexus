<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title>Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="username"
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              ></v-text-field>
              
              <v-alert
                v-if="error"
                type="error"
                dismissible
                class="mt-3"
              >
                {{ error }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn 
              color="primary" 
              @click="login"
              :loading="loading"
            >
              Login
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

export default defineComponent({
  name: 'Login',
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    
    const username = ref('');
    const password = ref('');
    const loading = computed(() => authStore.loading);
    const error = computed(() => authStore.error);
    
    const login = async () => {
      if (!username.value || !password.value) {
        return;
      }
      
      try {
        await authStore.login({
          username: username.value,
          password: password.value,
        });
        
        router.push('/');
      } catch (err) {
        // Error already handled in store
      }
    };
    
    return {
      username,
      password,
      loading,
      error,
      login,
    };
  },
});
</script>
