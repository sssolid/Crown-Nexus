<!-- frontend/src/components/LanguageSwitcher.vue -->
<template>
  <div class="language-switcher">
    <select v-model="currentLocale" @change="changeLocale">
      <option v-for="locale in availableLocales" :key="locale.code" :value="locale.code">
        {{ locale.name }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLocale } from '@/i18n'

// Initialize i18n
const { locale } = useI18n()

// Available locales
const availableLocales = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' }
]

// Current locale
const currentLocale = ref(locale.value)

// Change locale
const changeLocale = async () => {
  await setLocale(currentLocale.value)
}

// Set initial locale
onMounted(() => {
  currentLocale.value = locale.value
})
</script>
