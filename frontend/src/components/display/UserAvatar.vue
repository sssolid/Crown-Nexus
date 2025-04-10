<!-- src/components/display/UserAvatar.vue -->
<template>
  <div class="user-avatar-wrapper">
    <v-avatar
      :size="size"
      :rounded="rounded"
      :color="backgroundColor"
      :class="avatarClass"
      :image="avatarImage"
    >
      <template v-if="!avatarImage && !isLoading">
        <v-icon v-if="icon" :icon="icon" :size="iconSize" :color="iconColor"></v-icon>
        <span v-else-if="text" class="text-avatar" :style="{ fontSize: textSize }">
          {{ initials }}
        </span>
      </template>

      <template v-if="isLoading">
        <v-progress-circular indeterminate :size="loadingSize" :width="2" :color="loadingColor"></v-progress-circular>
      </template>
    </v-avatar>

    <v-badge
      v-if="showStatus"
      :color="statusColor"
      dot
      location="bottom end"
      offset-x="2"
      offset-y="2"
      bordered
      :model-value="true"
    ></v-badge>

    <slot name="badge"></slot>
  </div>

  <div v-if="showName && name" class="user-name" :class="nameClass">
    {{ name }}
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  name: {
    type: String,
    default: '',
  },
  image: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: 'mdi-account',
  },
  size: {
    type: [Number, String],
    default: 40,
  },
  rounded: {
    type: [Boolean, String],
    default: 'circle',
  },
  text: {
    type: String,
    default: '',
  },
  backgroundColor: {
    type: String,
    default: 'primary',
  },
  avatarClass: {
    type: String,
    default: '',
  },
  showName: {
    type: Boolean,
    default: false,
  },
  nameClass: {
    type: String,
    default: 'text-subtitle-2 text-center mt-1',
  },
  showStatus: {
    type: Boolean,
    default: false,
  },
  status: {
    type: String,
    default: 'offline',
    validator: (value: string) => ['online', 'offline', 'away', 'busy'].includes(value),
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  loadingColor: {
    type: String,
    default: 'white',
  },
})

// Compute avatar image source
const avatarImage = computed(() => props.image || '')

// Compute initials from name or text
const initials = computed(() => {
  const text = props.text || props.name

  if (!text) return ''

  return text
    .split(' ')
    .map(word => word.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('')
})

// Compute icon size based on avatar size
const iconSize = computed(() => {
  const size = typeof props.size === 'number' ? props.size : parseInt(props.size)
  return Math.max(size * 0.5, 16)
})

// Compute text size based on avatar size
const textSize = computed(() => {
  const size = typeof props.size === 'number' ? props.size : parseInt(props.size)
  return `${Math.max(size * 0.35, 12)}px`
})

// Compute loading indicator size
const loadingSize = computed(() => {
  const size = typeof props.size === 'number' ? props.size : parseInt(props.size)
  return Math.max(size * 0.6, 20)
})

// Compute status color
const statusColor = computed(() => {
  switch (props.status) {
    case 'online': return 'success'
    case 'away': return 'warning'
    case 'busy': return 'error'
    default: return 'grey'
  }
})
</script>

<style scoped>
.user-avatar-wrapper {
  position: relative;
  display: inline-flex;
}

.text-avatar {
  font-weight: 500;
}

.user-name {
  white-space: nowrap;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
