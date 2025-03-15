// frontend/src/i18n/index.ts
import { createI18n } from 'vue-i18n'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

// Import base messages
import en from './locales/en.json'

// Create i18n instance
export const i18n = createI18n({
  legacy: false, // Use Composition API
  locale: 'en', // Set default locale
  fallbackLocale: 'en', // Set fallback locale
  messages: {
    en // Load English messages by default
  },
  silentTranslationWarn: process.env.NODE_ENV === 'production',
  silentFallbackWarn: process.env.NODE_ENV === 'production'
})

// Load locale messages
const loadedLanguages: string[] = ['en']

/**
 * Load locale messages from the backend
 *
 * @param locale - The locale to load
 * @returns Promise for loading completion
 */
export async function loadLanguageAsync(locale: string): Promise<string> {
  // If the language was already loaded
  if (loadedLanguages.includes(locale)) {
    i18n.global.locale.value = locale
    document.querySelector('html')?.setAttribute('lang', locale)
    return Promise.resolve(locale)
  }

  // Load locale from backend API
  try {
    const response = await axios.get(`/api/v1/i18n/messages/${locale}`)

    // Set the locale messages
    i18n.global.setLocaleMessage(locale, response.data)
    loadedLanguages.push(locale)

    // Set locale
    i18n.global.locale.value = locale
    document.querySelector('html')?.setAttribute('lang', locale)

    return locale
  } catch (error) {
    console.error(`Could not load language: ${locale}`, error)
    return i18n.global.locale.value
  }
}

/**
 * Set application locale
 *
 * @param locale - The locale to set
 * @returns Promise for locale change completion
 */
export async function setLocale(locale: string): Promise<string> {
  const authStore = useAuthStore()

  // Load the language
  await loadLanguageAsync(locale)

  // Save user preference if logged in
  if (authStore.isLoggedIn) {
    try {
      await authStore.updateUserPreferences(authStore.user!.id, {
        language: locale
      })
    } catch (error) {
      console.error('Could not save language preference', error)
    }
  }

  // Store in localStorage for guests
  localStorage.setItem('locale', locale)

  return locale
}

/**
 * Initialize i18n with the user's preferred language
 */
export async function initializeI18n(): Promise<void> {
  const authStore = useAuthStore()
  let locale = 'en'

  // Try to get locale from user preferences if logged in
  if (authStore.isLoggedIn && authStore.user?.preferences?.language) {
    locale = authStore.user.preferences.language
  }
  // Otherwise try from localStorage
  else {
    const savedLocale = localStorage.getItem('locale')
    if (savedLocale) {
      locale = savedLocale
    }
    // Or browser preference
    else {
      const browserLang = navigator.language.split('-')[0]
      if (browserLang && ['en', 'es', 'fr', 'de'].includes(browserLang)) {
        locale = browserLang
      }
    }
  }

  await loadLanguageAsync(locale)
}
