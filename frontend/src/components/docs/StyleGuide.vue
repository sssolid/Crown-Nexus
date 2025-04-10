<!-- src/components/docs/StyleGuide.vue -->
<template>
  <div class="style-guide">
    <h1 class="text-h3 mb-8">Crown Nexus Design System</h1>

    <section id="colors" class="mb-12">
      <h2 class="text-h4 mb-4">Colors</h2>
      <v-row>
        <v-col v-for="(color, key) in themeColors" :key="key" cols="12" md="6" lg="4">
          <v-card class="mb-4">
            <div class="d-flex align-center">
              <div
                class="color-swatch"
                :style="{ backgroundColor: color }"
              ></div>
              <div class="pa-4">
                <div class="text-subtitle-1 font-weight-bold">{{ formatColorName(key) }}</div>
                <div class="text-body-2 text-lowercase">{{ color }}</div>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <section id="typography" class="mb-12">
      <h2 class="text-h4 mb-4">Typography</h2>

      <v-card class="mb-8">
        <v-card-text>
          <h1 class="text-h1 mb-2">Heading 1</h1>
          <h2 class="text-h2 mb-2">Heading 2</h2>
          <h3 class="text-h3 mb-2">Heading 3</h3>
          <h4 class="text-h4 mb-2">Heading 4</h4>
          <h5 class="text-h5 mb-2">Heading 5</h5>
          <h6 class="text-h6 mb-4">Heading 6</h6>

          <div class="text-subtitle-1 mb-2">Subtitle 1</div>
          <div class="text-subtitle-2 mb-4">Subtitle 2</div>

          <p class="text-body-1 mb-2">Body 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
          <p class="text-body-2 mb-2">Body 2: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        </v-card-text>
      </v-card>
    </section>

    <section id="buttons" class="mb-12">
      <h2 class="text-h4 mb-4">Buttons</h2>

      <v-card class="mb-8">
        <v-card-text>
          <div class="mb-4">
            <h3 class="text-h6 mb-2">Button Variants</h3>
            <div class="d-flex flex-wrap align-center gap-4">
              <base-button>Default</base-button>
              <base-button variant="text">Text</base-button>
              <base-button variant="elevated">Elevated</base-button>
              <base-button variant="tonal">Tonal</base-button>
              <base-button variant="outlined">Outlined</base-button>
              <base-button variant="plain">Plain</base-button>
            </div>
          </div>

          <div class="mb-4">
            <h3 class="text-h6 mb-2">Button Colors</h3>
            <div class="d-flex flex-wrap align-center gap-4">
              <base-button color="primary">Primary</base-button>
              <base-button color="secondary">Secondary</base-button>
              <base-button color="success">Success</base-button>
              <base-button color="info">Info</base-button>
              <base-button color="warning">Warning</base-button>
              <base-button color="error">Error</base-button>
            </div>
          </div>

          <div class="mb-4">
            <h3 class="text-h6 mb-2">Button Sizes</h3>
            <div class="d-flex flex-wrap align-center gap-4">
              <base-button size="x-small">X-Small</base-button>
              <base-button size="small">Small</base-button>
              <base-button>Default</base-button>
              <base-button size="large">Large</base-button>
              <base-button size="x-large">X-Large</base-button>
            </div>
          </div>

          <div class="mb-4">
            <h3 class="text-h6 mb-2">Button States</h3>
            <div class="d-flex flex-wrap align-center gap-4">
              <base-button>Normal</base-button>
              <base-button disabled>Disabled</base-button>
              <base-button loading>Loading</base-button>
              <base-button icon="mdi-check">With Icon</base-button>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </section>

    <section id="forms" class="mb-12">
      <h2 class="text-h4 mb-4">Form Components</h2>

      <v-card class="mb-8">
        <v-card-text>
          <div class="mb-6">
            <h3 class="text-h6 mb-4">Form Fields</h3>

            <div class="mb-4">
              <form-text-field
                v-model="formDemo.name"
                label="Text Field"
                placeholder="Enter your name"
              ></form-text-field>
            </div>

            <div class="mb-4">
              <form-select
                v-model="formDemo.country"
                label="Select Field"
                :items="countries"
                item-title="name"
                item-value="code"
                clearable
              ></form-select>
            </div>

            <div class="mb-4">
              <v-checkbox
                v-model="formDemo.subscribe"
                label="Checkbox"
                hint="Subscribe to newsletter"
              ></v-checkbox>
            </div>

            <div class="mb-4">
              <v-radio-group
                v-model="formDemo.gender"
                label="Radio Group"
              >
                <v-radio label="Male" value="male"></v-radio>
                <v-radio label="Female" value="female"></v-radio>
                <v-radio label="Other" value="other"></v-radio>
              </v-radio-group>
            </div>

            <div class="mb-4">
              <v-switch
                v-model="formDemo.darkMode"
                label="Switch"
                hint="Enable dark mode"
              ></v-switch>
            </div>

            <div class="mb-4">
              <v-slider
                v-model="formDemo.age"
                label="Slider"
                :min="0"
                :max="100"
                thumb-label
              ></v-slider>
            </div>

            <div class="mb-4">
              <v-textarea
                v-model="formDemo.message"
                label="Textarea"
                placeholder="Enter your message"
                rows="3"
                auto-grow
              ></v-textarea>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </section>

    <section id="tables" class="mb-12">
      <h2 class="text-h4 mb-4">Data Tables</h2>

      <data-table
        title="Example Table"
        :headers="tableHeaders"
        :items="tableItems"
        :total-items="tableItems.length"
        :page="1"
        :items-per-page="5"
        :searchable="true"
      ></data-table>
    </section>

    <section id="cards" class="mb-12">
      <h2 class="text-h4 mb-4">Cards</h2>

      <v-row>
        <v-col cols="12" md="6" lg="4">
          <base-card
            title="Basic Card"
            subtitle="With title and subtitle"
          >
            <p>This is a basic card with title and content.</p>
          </base-card>
        </v-col>

        <v-col cols="12" md="6" lg="4">
          <base-card title="Card with Actions">
            <p>This card has action buttons in the footer.</p>
            <template #actions>
              <v-spacer></v-spacer>
              <base-button variant="text">Cancel</base-button>
              <base-button>Submit</base-button>
            </template>
          </base-card>
        </v-col>

        <v-col cols="12" md="6" lg="4">
          <base-card
            title="Card with Custom Header"
          >
            <template #title-actions>
              <v-btn icon="mdi-dots-vertical" variant="text"></v-btn>
            </template>
            <p>This card has a custom action in the header.</p>
          </base-card>
        </v-col>
      </v-row>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { lightTheme } from '@/theme'

// Demo data for the form
const formDemo = reactive({
  name: '',
  country: null,
  subscribe: false,
  gender: '',
  darkMode: false,
  age: 25,
  message: '',
})

// Country options for the select field
const countries = [
  { name: 'United States', code: 'US' },
  { name: 'United Kingdom', code: 'UK' },
  { name: 'Canada', code: 'CA' },
  { name: 'Australia', code: 'AU' },
  { name: 'Germany', code: 'DE' },
  { name: 'France', code: 'FR' },
  { name: 'Japan', code: 'JP' },
]

// Table demo data
const tableHeaders = [
  { title: 'ID', key: 'id', align: 'start', sortable: true },
  { title: 'Name', key: 'name', align: 'start', sortable: true },
  { title: 'Email', key: 'email', align: 'start', sortable: true },
  { title: 'Status', key: 'status', align: 'center', sortable: true },
]

const tableItems = [
  { id: 1, name: 'John Doe', email: 'john@example.com', status: 'Active' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com', status: 'Inactive' },
  { id: 3, name: 'Michael Brown', email: 'michael@example.com', status: 'Active' },
  { id: 4, name: 'Susan Wilson', email: 'susan@example.com', status: 'Pending' },
  { id: 5, name: 'Robert Johnson', email: 'robert@example.com', status: 'Active' },
  { id: 6, name: 'Emily Davis', email: 'emily@example.com', status: 'Inactive' },
]

// Extract colors from the theme
const themeColors = computed(() => {
  return lightTheme.colors || {}
})

// Format color name for display
const formatColorName = (name: string) => {
  return name
    .replace(/([A-Z])/g, ' $1') // Add space before capital letters
    .replace(/-/g, ' ') // Replace hyphens with spaces
    .replace(/^./, str => str.toUpperCase()) // Capitalize first letter
}
</script>

<style scoped>
.style-guide {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.color-swatch {
  width: 80px;
  height: 80px;
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}

.gap-4 {
  gap: 16px;
}
</style>
