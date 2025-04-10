<!-- src/components/tabs/BaseTabs.vue -->
<template>
  <div class="base-tabs" :class="containerClass">
    <v-card v-if="useCard" :elevation="cardElevation" :class="cardClass">
      <v-tabs
        v-model="localTab"
        :align-tabs="alignTabs"
        :center-active="centerActive"
        :color="color"
        :direction="direction"
        :fixed-tabs="fixedTabs"
        :grow="grow"
        :height="height"
        :hide-slider="hideSlider"
        :show-arrows="showArrows"
        :slider-color="sliderColor"
        :bg-color="bgColor"
        :density="density"
        @update:model-value="onTabChange"
      >
        <template v-for="(tab, index) in tabs" :key="index">
          <v-tab
            :value="tab.value"
            :to="tab.to"
            :exact="tab.exact"
            :disabled="tab.disabled"
            :class="{ 'v-tab--active': localTab === tab.value }"
          >
            <v-icon v-if="tab.icon" :icon="tab.icon" class="me-2"></v-icon>
            {{ tab.title }}
          </v-tab>
        </template>
      </v-tabs>

      <v-divider v-if="showDivider"></v-divider>

      <v-window
        v-model="localTab"
        :touch="touch"
        :continuous="continuous"
        :reverse="reverse"
        :direction="windowDirection || direction"
        :transition="transition"
      >
        <v-window-item v-for="(tab, index) in tabs" :key="index" :value="tab.value">
          <div class="tab-content pa-4">
            <slot :name="`tab-${tab.value}`">
              <slot :name="tab.value"></slot>
            </slot>
          </div>
        </v-window-item>
      </v-window>
    </v-card>

    <template v-else>
      <v-tabs
        v-model="localTab"
        :align-tabs="alignTabs"
        :center-active="centerActive"
        :color="color"
        :direction="direction"
        :fixed-tabs="fixedTabs"
        :grow="grow"
        :height="height"
        :hide-slider="hideSlider"
        :show-arrows="showArrows"
        :slider-color="sliderColor"
        :bg-color="bgColor"
        :density="density"
        @update:model-value="onTabChange"
      >
        <template v-for="(tab, index) in tabs" :key="index">
          <v-tab
            :value="tab.value"
            :to="tab.to"
            :exact="tab.exact"
            :disabled="tab.disabled"
            :class="{ 'v-tab--active': localTab === tab.value }"
          >
            <v-icon v-if="tab.icon" :icon="tab.icon" class="me-2"></v-icon>
            {{ tab.title }}
          </v-tab>
        </template>
      </v-tabs>

      <v-divider v-if="showDivider"></v-divider>

      <v-window
        v-model="localTab"
        :touch="touch"
        :continuous="continuous"
        :reverse="reverse"
        :direction="windowDirection || direction"
        :transition="transition"
      >
        <v-window-item v-for="(tab, index) in tabs" :key="index" :value="tab.value">
          <div class="tab-content pa-4">
            <slot :name="`tab-${tab.value}`">
              <slot :name="tab.value"></slot>
            </slot>
          </div>
        </v-window-item>
      </v-window>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface Tab {
  title: string
  value: string | number
  icon?: string
  to?: string
  exact?: boolean
  disabled?: boolean
}

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: null,
  },
  tabs: {
    type: Array as PropType<Tab[]>,
    required: true,
  },
  alignTabs: {
    type: String,
    default: 'start',
    validator: (value: string) => ['start', 'center', 'end'].includes(value),
  },
  centerActive: {
    type: Boolean,
    default: false,
  },
  color: {
    type: String,
    default: 'primary',
  },
  direction: {
    type: String,
    default: 'horizontal',
    validator: (value: string) => ['horizontal', 'vertical'].includes(value),
  },
  fixedTabs: {
    type: Boolean,
    default: false,
  },
  grow: {
    type: Boolean,
    default: false,
  },
  height: {
    type: [Number, String],
    default: undefined,
  },
  hideSlider: {
    type: Boolean,
    default: false,
  },
  showArrows: {
    type: Boolean,
    default: false,
  },
  sliderColor: {
    type: String,
    default: undefined,
  },
  bgColor: {
    type: String,
    default: undefined,
  },
  density: {
    type: String,
    default: 'default',
    validator: (value: string) => ['default', 'comfortable', 'compact'].includes(value),
  },
  useCard: {
    type: Boolean,
    default: false,
  },
  cardElevation: {
    type: [Number, String],
    default: 1,
  },
  cardClass: {
    type: String,
    default: '',
  },
  showDivider: {
    type: Boolean,
    default: true,
  },
  containerClass: {
    type: String,
    default: '',
  },
  touch: {
    type: Boolean,
    default: true,
  },
  continuous: {
    type: Boolean,
    default: false,
  },
  reverse: {
    type: Boolean,
    default: false,
  },
  windowDirection: {
    type: String,
    default: null,
  },
  transition: {
    type: String,
    default: 'v-window-x-transition',
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

// We need to track the local tab state
const localTab = ref<string | number>(props.modelValue || (props.tabs.length > 0 ? props.tabs[0].value : null))

// Watch for external changes to modelValue
watch(() => props.modelValue, (newValue) => {
  if (newValue !== null && newValue !== undefined) {
    localTab.value = newValue
  }
})

// Watch for local changes and emit events
watch(localTab, (newValue) => {
  emit('update:modelValue', newValue)
})

// Handle tab change
const onTabChange = (value: string | number) => {
  emit('change', value)
}

// Expose methods to parent component
defineExpose({
  setTab: (value: string | number) => {
    localTab.value = value
  },
  getCurrentTab: () => localTab.value,
})
</script>

<style scoped>
.base-tabs {
  width: 100%;
}

.tab-content {
  min-height: 100px;
}
</style>
