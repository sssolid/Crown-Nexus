<!-- src/components/navigation/Breadcrumbs.vue -->
<template>
  <v-breadcrumbs
    :items="processedItems"
    :divider="divider"
    :density="density"
    :bg-color="bgColor"
    :rounded="rounded"
    :active-class="activeClass"
    :active-color="activeColor"
    :class="containerClass"
  >
    <template v-slot:prepend v-if="showHomeIcon">
      <slot name="home-icon">
        <v-icon icon="mdi-home" size="small" @click="handleHomeClick" class="home-icon"></v-icon>
      </slot>
    </template>

    <template v-slot:item="{ item }">
      <v-breadcrumbs-item
        :to="item.to"
        :href="item.href"
        :disabled="item.disabled"
        :exact="item.exact"
        :active-class="activeClass"
        :class="item.class"
      >
        <v-icon v-if="item.icon" :icon="item.icon" size="small" class="me-1"></v-icon>
        {{ item.title }}
      </v-breadcrumbs-item>
    </template>
  </v-breadcrumbs>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

interface BreadcrumbItem {
  title: string
  to?: string | Record<string, any>
  href?: string
  disabled?: boolean
  exact?: boolean
  icon?: string
  class?: string
}

const props = defineProps({
  items: {
    type: Array as PropType<BreadcrumbItem[]>,
    default: () => [],
  },
  divider: {
    type: String,
    default: '/',
  },
  density: {
    type: String,
    default: 'default',
    validator: (value: string) => ['default', 'comfortable', 'compact'].includes(value),
  },
  bgColor: {
    type: String,
    default: undefined,
  },
  rounded: {
    type: [Boolean, String, Number],
    default: false,
  },
  activeClass: {
    type: String,
    default: 'v-breadcrumbs-item--active',
  },
  activeColor: {
    type: String,
    default: 'primary',
  },
  containerClass: {
    type: String,
    default: '',
  },
  showHomeIcon: {
    type: Boolean,
    default: true,
  },
  homePath: {
    type: String,
    default: '/',
  },
  useRouteMatching: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['home-click'])

const router = useRouter()

// Process items to ensure they have the necessary properties
const processedItems = computed(() => {
  return props.items.map(item => ({
    ...item,
    title: item.title || '',
    disabled: item.disabled || false,
    exact: item.exact || false,
  }))
})

// Handle home icon click
const handleHomeClick = () => {
  emit('home-click')
  if (props.homePath) {
    router.push(props.homePath)
  }
}
</script>

<style scoped>
.home-icon {
  cursor: pointer;
}
</style>
