<template>
  <div>
    <h1>Dashboard</h1>
    <p>Welcome to Crown Nexus Dashboard</p>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Products Overview</v-card-title>
          <v-card-text>
            <p>View and manage automotive products</p>
          </v-card-text>
          <v-card-actions>
            <v-btn to="/products" color="primary">View Products</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Fitments Overview</v-card-title>
          <v-card-text>
            <p>View and manage product fitments</p>
          </v-card-text>
          <v-card-actions>
            <v-btn to="/fitments" color="primary">View Fitments</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Dashboard',
});
</script>
