<!-- frontend/src/components/faq/FaqAccordion.vue -->
<template>
  <div class="faq-accordion">
    <v-expansion-panels v-model="expandedPanels" multiple variant="accordion">
      <v-expansion-panel
        v-for="(faq, index) in faqs"
        :key="faq.id"
        :value="index"
        :title="faq.question"
        :text="faq.answer"
        class="mb-3"
        rounded="lg"
      >
        <template>
          <div class="d-flex align-center">
            <div class="text-subtitle-1 font-weight-medium">
              {{ faq.question }}
            </div>
            <v-spacer></v-spacer>
            <v-chip
              v-if="faq.is_popular"
              color="secondary"
              size="small"
              variant="tonal"
              class="mr-2 d-none d-sm-flex"
            >
              Popular
            </v-chip>
            <div v-if="isAdmin" class="d-flex align-center">
              <v-btn
                icon
                size="small"
                color="primary"
                variant="text"
                class="mr-1"
                :to="`/faqs/${faq.id}/edit`"
                @click.stop
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-btn
                icon
                size="small"
                color="error"
                variant="text"
                @click.stop="confirmDelete(faq)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
          </div>
        </template>
        <v-expansion-panel-text>
          <!-- Answer content with rich text formatting -->
          <div class="pt-2 pb-4" v-html="formatAnswer(faq.answer)"></div>

          <!-- Feedback buttons -->
          <div class="d-flex align-center pt-3 mt-3 border-top">
            <span class="text-caption mr-4">Was this helpful?</span>
            <v-btn
              size="small"
              variant="text"
              color="success"
              prepend-icon="mdi-thumb-up"
              @click="submitFeedback(faq.id, true)"
              :disabled="feedbackSubmitted[faq.id]"
            >
              Yes
            </v-btn>
            <v-btn
              size="small"
              variant="text"
              color="error"
              prepend-icon="mdi-thumb-down"
              @click="submitFeedback(faq.id, false)"
              :disabled="feedbackSubmitted[faq.id]"
              class="ml-2"
            >
              No
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              size="small"
              variant="text"
              color="primary"
              class="copy-link-btn"
              prepend-icon="mdi-link"
              @click="copyLink(faq.id)"
            >
              {{ copyStatus[faq.id] ? 'Copied!' : 'Copy Link' }}
            </v-btn>
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>

    <!-- Empty State -->
    <div v-if="faqs.length === 0" class="text-center py-8">
      <v-icon icon="mdi-help-circle-outline" size="64" color="grey-lighten-1"></v-icon>
      <h3 class="text-h5 mt-4">No FAQs in this Category</h3>
      <p class="text-body-1 mt-2">
        There are currently no FAQs available in this category.
      </p>
      <v-btn
        v-if="isAdmin"
        color="primary"
        variant="elevated"
        prepend-icon="mdi-plus"
        class="mt-4"
        to="/faqs/new"
      >
        Add FAQ
      </v-btn>
    </div>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-error text-white pa-4">
          Confirm Delete
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p>Are you sure you want to delete this FAQ?</p>
          <p class="text-subtitle-1 font-weight-medium mt-2">
            "{{ faqToDelete?.question }}"
          </p>
          <p class="text-medium-emphasis mt-2">This action cannot be undone.</p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="tonal"
            @click="deleteDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            @click="deleteFaq"
            :loading="deleteLoading"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, PropType } from 'vue';

// FAQ interface - would be imported from types in a real app
interface Faq {
  id: string;
  question: string;
  answer: string;
  category_id: string;
  order: number;
  is_popular: boolean;
  created_at: string;
  updated_at: string;
}

export default defineComponent({
  name: 'FaqAccordion',

  props: {
    faqs: {
      type: Array as PropType<Faq[]>,
      required: true
    },
    isAdmin: {
      type: Boolean,
      default: false
    }
  },

  setup(props) {
    // Track expanded panels
    const expandedPanels = ref<number[]>([]);

    // Feedback tracking
    const feedbackSubmitted = ref<Record<string, boolean>>({});

    // Copy link status
    const copyStatus = ref<Record<string, boolean>>({});

    // Delete functionality
    const deleteDialog = ref(false);
    const deleteLoading = ref(false);
    const faqToDelete = ref<Faq | null>(null);

    // Format answer text with simple HTML support
    const formatAnswer = (answer: string) => {
      // In a real implementation, you might use a markdown renderer or sanitize HTML
      // For now, we'll just return the text as-is with paragraph breaks
      return answer.replace(/\n\n/g, '<br><br>').replace(/\n/g, '<br>');
    };

    // Submit feedback on FAQ helpfulness
    const submitFeedback = async (faqId: string, isHelpful: boolean) => {
      try {
        // In a real implementation, this would be an API call
        // await api.post('/faqs/feedback', { faq_id: faqId, is_helpful: isHelpful });

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));

        // Mark feedback as submitted for this FAQ
        feedbackSubmitted.value[faqId] = true;

        // Show success message
        // In a real implementation, you might use a notification service
        alert(`Thank you for your feedback! ${isHelpful ? '👍' : '👎'}`);
      } catch (error) {
        console.error('Error submitting feedback:', error);
      }
    };

    // Copy direct link to FAQ
    const copyLink = async (faqId: string) => {
      try {
        // Generate a URL that will open the FAQ directly
        const url = `${window.location.origin}/faqs?id=${faqId}`;

        // Copy to clipboard
        await navigator.clipboard.writeText(url);

        // Update copy status
        copyStatus.value[faqId] = true;

        // Reset after 2 seconds
        setTimeout(() => {
          copyStatus.value[faqId] = false;
        }, 2000);
      } catch (error) {
        console.error('Error copying link:', error);
        alert('Failed to copy link. Please try again.');
      }
    };

    // Confirm FAQ deletion
    const confirmDelete = (faq: Faq) => {
      faqToDelete.value = faq;
      deleteDialog.value = true;
    };

    // Delete FAQ
    const deleteFaq = async () => {
      if (!faqToDelete.value) return;

      deleteLoading.value = true;

      try {
        // In a real implementation, this would be an API call
        // await api.delete(`/faqs/${faqToDelete.value.id}`);

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));

        // Close dialog
        deleteDialog.value = false;

        // Show success message
        alert('FAQ deleted successfully');

        // In a real implementation, you would emit an event to refresh the parent component
        // emit('faq-deleted', faqToDelete.value.id);
      } catch (error) {
        console.error('Error deleting FAQ:', error);
      } finally {
        deleteLoading.value = false;
      }
    };

    return {
      expandedPanels,
      feedbackSubmitted,
      copyStatus,
      deleteDialog,
      deleteLoading,
      faqToDelete,
      formatAnswer,
      submitFeedback,
      copyLink,
      confirmDelete,
      deleteFaq
    };
  }
});
</script>

<style scoped>
.faq-accordion {
  margin-bottom: 20px;
}

.border-top {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.copy-link-btn {
  min-width: 100px;
}
</style>
