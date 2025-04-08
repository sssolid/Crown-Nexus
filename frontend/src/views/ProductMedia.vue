<!-- frontend/src/views/ProductMedia.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Loading State -->
      <div v-if="initialLoading" class="d-flex justify-center my-6">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>

      <template v-else-if="product">
        <!-- Page Header with Back Button -->
        <v-row class="mb-6">
          <v-col cols="12">
            <div class="d-flex align-center">
              <v-btn
                icon
                variant="text"
                :to="{ name: 'ProductDetail', params: { id: productId } }"
                class="mr-4"
              >
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>

              <div>
                <h1 class="text-h3 font-weight-bold">Manage Media</h1>
                <p class="text-subtitle-1">
                  <v-chip
                    color="primary"
                    variant="flat"
                    class="mr-2"
                    size="small"
                    :to="{ name: 'ProductDetail', params: { id: productId } }"
                  >
                    {{ product.sku }}
                  </v-chip>
                  {{ product.name }}
                </p>
              </div>
            </div>
          </v-col>
        </v-row>

        <!-- Main Content -->
        <v-row>
          <!-- Media Gallery -->
          <v-col cols="12" md="8">
            <v-card>
              <v-card-title class="d-flex align-center">
                Media Gallery
                <v-spacer></v-spacer>

                <!-- Upload Button -->
                <v-btn
                  color="primary"
                  prepend-icon="mdi-upload"
                  @click="showUploadDialog = true"
                >
                  Upload Media
                </v-btn>
              </v-card-title>
              <v-divider></v-divider>

              <!-- Media Content -->
              <v-card-text v-if="mediaItems.length > 0" class="pa-2">
                <v-row>
                  <v-col
                    v-for="(item, index) in mediaItems"
                    :key="item.id"
                    cols="12"
                    sm="6"
                    md="4"
                    class="pa-2"
                  >
                    <v-card
                      variant="outlined"
                      class="media-item"
                      :class="{ 'primary-media': item.is_primary }"
                    >
                      <v-img
                        :src="item.url"
                        height="180"
                        contain
                        class="media-thumbnail"
                        @click="openMediaPreview(item)"
                      ></v-img>

                      <v-divider></v-divider>

                      <v-card-actions class="pa-2">
                        <div class="text-caption text-truncate mr-2">{{ item.filename }}</div>
                        <v-spacer></v-spacer>

                        <!-- Make Primary Button -->
                        <v-tooltip text="Set as Primary" v-if="!item.is_primary">
                          <template v-slot:activator="{ props }">
                            <v-btn
                              icon
                              size="small"
                              color="primary"
                              v-bind="props"
                              @click="setPrimaryMedia(item)"
                            >
                              <v-icon>mdi-star</v-icon>
                            </v-btn>
                          </template>
                        </v-tooltip>

                        <!-- Primary Indicator -->
                        <v-tooltip text="Primary Image" v-else>
                          <template v-slot:activator="{ props }">
                            <v-btn
                              icon
                              size="small"
                              color="primary"
                              variant="flat"
                              v-bind="props"
                              disabled
                            >
                              <v-icon>mdi-star</v-icon>
                            </v-btn>
                          </template>
                        </v-tooltip>

                        <!-- Edit Button -->
                        <v-tooltip text="Edit Details">
                          <template v-slot:activator="{ props }">
                            <v-btn
                              icon
                              size="small"
                              color="info"
                              v-bind="props"
                              @click="editMedia(item)"
                              class="ml-2"
                            >
                              <v-icon>mdi-pencil</v-icon>
                            </v-btn>
                          </template>
                        </v-tooltip>

                        <!-- Delete Button -->
                        <v-tooltip text="Delete">
                          <template v-slot:activator="{ props }">
                            <v-btn
                              icon
                              size="small"
                              color="error"
                              v-bind="props"
                              @click="confirmDeleteMedia(item)"
                              class="ml-2"
                            >
                              <v-icon>mdi-delete</v-icon>
                            </v-btn>
                          </template>
                        </v-tooltip>
                      </v-card-actions>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>

              <!-- Empty State -->
              <v-card-text v-else class="text-center py-6">
                <v-icon icon="mdi-image-off" size="large" class="mb-2"></v-icon>
                <p>No media files available for this product</p>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-upload"
                  @click="showUploadDialog = true"
                  class="mt-4"
                >
                  Upload Media
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>

          <!-- Sidebar: Upload and Options -->
          <v-col cols="12" md="4">
            <!-- Quick Actions Card -->
            <v-card class="mb-6">
              <v-card-title>Quick Actions</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="primary"
                      variant="outlined"
                      prepend-icon="mdi-swap-horizontal"
                      @click="showReorderDialog = true"
                      :disabled="mediaItems.length < 2"
                    >
                      Reorder Media
                    </v-btn>
                  </v-col>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="secondary"
                      variant="outlined"
                      prepend-icon="mdi-view-gallery"
                      :to="{ name: 'MediaLibrary' }"
                    >
                      Media Library
                    </v-btn>
                  </v-col>
                  <v-col cols="12">
                    <v-btn
                      block
                      color="secondary"
                      variant="outlined"
                      prepend-icon="mdi-view-list"
                      :to="{ name: 'ProductDetail', params: { id: productId } }"
                    >
                      Back to Product
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Media Info Card -->
            <v-card>
              <v-card-title>Media Information</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-list density="compact" lines="two">
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="primary" variant="tonal">
                        <v-icon>mdi-image-multiple</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Total Media</v-list-item-title>
                    <v-list-item-subtitle>{{ mediaItems.length }} items</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="info" variant="tonal">
                        <v-icon>mdi-image</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Images</v-list-item-title>
                    <v-list-item-subtitle>{{ imageCount }} items</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="success" variant="tonal">
                        <v-icon>mdi-file-document</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Documents</v-list-item-title>
                    <v-list-item-subtitle>{{ documentCount }} items</v-list-item-subtitle>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:prepend>
                      <v-avatar color="warning" variant="tonal">
                        <v-icon>mdi-star</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>Primary Image</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ primaryMedia ? primaryMedia.filename : 'None set' }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Media Preview Dialog -->
        <v-dialog v-model="showPreviewDialog" max-width="800">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span class="text-truncate">{{ selectedMedia?.filename || 'Media Preview' }}</span>
              <v-btn icon @click="showPreviewDialog = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-0">
              <v-img
                v-if="selectedMedia && isImage(selectedMedia)"
                :src="selectedMedia.url"
                height="500"
                contain
                class="mx-auto"
              ></v-img>
              <div
                v-else-if="selectedMedia && isDocument(selectedMedia)"
                class="d-flex flex-column align-center justify-center pa-6"
                style="height: 300px"
              >
                <v-icon icon="mdi-file-document" size="x-large" color="primary" class="mb-4"></v-icon>
                <p class="text-h6">{{ selectedMedia.filename }}</p>
                <p class="text-caption">{{ formatFileSize(selectedMedia.size) }}</p>
                <v-btn
                  color="primary"
                  variant="tonal"
                  prepend-icon="mdi-download"
                  class="mt-4"
                  :href="selectedMedia.url"
                  target="_blank"
                >
                  Download
                </v-btn>
              </div>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <div class="d-flex align-center">
                <span class="text-caption text-medium-emphasis">{{ selectedMedia ? formatDateTime(selectedMedia.created_at) : '' }}</span>
              </div>
              <v-spacer></v-spacer>
              <v-btn
                v-if="selectedMedia && !selectedMedia.is_primary && isImage(selectedMedia)"
                color="warning"
                variant="tonal"
                prepend-icon="mdi-star"
                @click="setPrimaryMedia(selectedMedia)"
              >
                Set as Primary
              </v-btn>
              <v-btn
                color="error"
                variant="tonal"
                prepend-icon="mdi-delete"
                @click="confirmDeleteMedia(selectedMedia)"
              >
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Upload Dialog -->
        <v-dialog v-model="showUploadDialog" max-width="800" persistent>
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Upload Media
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <p class="mb-4">
                Upload images or documents to associate with this product. Allowed file types:
                JPG, PNG, GIF, SVG, PDF, DOCX.
              </p>

              <!-- Drag and Drop Upload Area -->
              <v-card
                :variant="isDragging ? 'flat' : 'outlined'"
                :color="isDragging ? 'primary' : undefined"
                class="upload-dropzone pa-6 mb-4"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleFileDrop"
                @click="$refs.fileInput.click()"
              >
                <input
                  ref="fileInput"
                  type="file"
                  @change="handleFileSelect"
                  multiple
                  accept=".jpg,.jpeg,.png,.gif,.svg,.pdf,.docx"
                  style="display: none"
                />
                <div class="text-center">
                  <v-icon
                    :icon="isDragging ? 'mdi-cloud-upload' : 'mdi-file-upload'"
                    size="64"
                    :color="isDragging ? 'white' : 'primary'"
                    class="mb-4"
                  ></v-icon>
                  <h3 class="text-h6 mb-2">
                    {{ isDragging ? 'Drop files here' : 'Click or drag files here to upload' }}
                  </h3>
                  <p class="text-caption text-medium-emphasis" v-if="!isDragging">
                    Maximum file size: 10MB
                  </p>
                </div>
              </v-card>

              <!-- Selected Files List -->
              <div v-if="filesToUpload.length > 0">
                <p class="text-subtitle-1 mb-2">Selected Files:</p>
                <v-list lines="two">
                  <v-list-item
                    v-for="(file, index) in filesToUpload"
                    :key="index"
                  >
                    <template v-slot:prepend>
                      <v-avatar size="40" color="grey-lighten-3">
                        <v-icon :icon="getFileIcon(file)"></v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>{{ file.name }}</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ formatFileSize(file.size) }}
                    </v-list-item-subtitle>
                    <template v-slot:append>
                      <v-btn
                        icon
                        size="small"
                        color="error"
                        variant="text"
                        @click="removeFileFromUpload(index)"
                      >
                        <v-icon>mdi-close</v-icon>
                      </v-btn>
                    </template>
                  </v-list-item>
                </v-list>
              </div>

              <!-- Upload Progress -->
              <div v-if="uploading">
                <v-progress-linear
                  v-model="uploadProgress"
                  color="primary"
                  height="10"
                  striped
                  class="mt-4"
                ></v-progress-linear>
                <div class="d-flex justify-space-between mt-2">
                  <span class="text-caption">Uploading...</span>
                  <span class="text-caption">{{ uploadProgress.toFixed(0) }}%</span>
                </div>
              </div>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="cancelUpload"
                :disabled="uploading"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="uploadFiles"
                :loading="uploading"
                :disabled="filesToUpload.length === 0"
              >
                Upload Files
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Media Edit Dialog -->
        <v-dialog v-model="showEditDialog" max-width="600">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Edit Media Details
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <v-form ref="editForm" v-model="isEditFormValid">
                <v-text-field
                  v-model="editForm.filename"
                  label="Filename"
                  variant="outlined"
                  :rules="[rules.required]"
                  class="mb-4"
                ></v-text-field>

                <v-text-field
                  v-model="editForm.alt_text"
                  label="Alt Text"
                  variant="outlined"
                  hint="Text description for accessibility"
                  persistent-hint
                  class="mb-4"
                ></v-text-field>

                <v-textarea
                  v-model="editForm.description"
                  label="Description"
                  variant="outlined"
                  rows="3"
                  auto-grow
                ></v-textarea>
              </v-form>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showEditDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="saveMediaEdit"
                :loading="editLoading"
                :disabled="!isEditFormValid"
              >
                Save Changes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Reorder Media Dialog -->
        <v-dialog v-model="showReorderDialog" max-width="700">
          <v-card>
            <v-card-title class="text-h5 pa-4">
              Reorder Media
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="pa-4">
              <p class="mb-4">
                Drag and drop media items to change the display order. The first item will appear
                as the primary image in listings.
              </p>

              <v-list lines="two" class="reorder-list">
                <Draggable
                  v-model="reorderList"
                  item-key="id"
                  handle=".handle"
                  ghost-class="ghost"
                >
                  <template #item="{ element }">
                    <v-list-item class="mb-2 pa-2 bg-grey-lighten-4 rounded">
                      <template v-slot:prepend>
                        <v-avatar size="40">
                          <v-img :src="element.url" cover></v-img>
                        </v-avatar>
                        <v-icon class="handle ml-2 cursor-move">mdi-drag</v-icon>
                      </template>
                      <v-list-item-title>{{ element.filename }}</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ isImage(element) ? 'Image' : 'Document' }}
                      </v-list-item-subtitle>
                      <template v-slot:append>
                        <v-chip
                          v-if="element.is_primary"
                          color="warning"
                          size="small"
                          variant="tonal"
                        >
                          Primary
                        </v-chip>
                      </template>
                    </v-list-item>
                  </template>
                </Draggable>
              </v-list>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showReorderDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="primary"
                @click="saveMediaOrder"
                :loading="reorderLoading"
              >
                Save Order
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Delete Confirmation Dialog -->
        <v-dialog v-model="showDeleteDialog" max-width="500">
          <v-card>
            <v-card-title class="text-h5 bg-error text-white pa-4">
              Delete Media
            </v-card-title>
            <v-card-text class="pa-4 pt-6">
              <p>
                Are you sure you want to delete the media file
                <strong>{{ mediaToDelete?.filename }}</strong>?
              </p>
              <p class="text-medium-emphasis mt-2">
                This action cannot be undone. The file will be permanently removed from the server.
              </p>
              <v-alert
                v-if="mediaToDelete?.is_primary"
                type="warning"
                variant="tonal"
                class="mt-4"
              >
                This is the primary image for this product. Deleting it will require setting a new primary image.
              </v-alert>
            </v-card-text>
            <v-card-actions class="pa-4">
              <v-spacer></v-spacer>
              <v-btn
                color="secondary"
                variant="tonal"
                @click="showDeleteDialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                color="error"
                @click="deleteMedia"
                :loading="deleteLoading"
              >
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>

      <!-- Not Found State -->
      <div v-else class="text-center my-12">
        <v-icon icon="mdi-alert-circle" color="warning" size="64"></v-icon>
        <h2 class="text-h4 mt-4">Product Not Found</h2>
        <p class="text-body-1 mt-2">The product you're looking for doesn't exist or has been removed.</p>
        <v-btn
          color="primary"
          class="mt-4"
          @click="router.push({ name: 'ProductCatalog' })"
        >
          Back to Products
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import productService from '@/services/product';
import mediaService from '@/services/media';
import { Product } from '@/types/product';
import { Media } from '@/types/media';
import { formatDateTime, formatFileSize } from '@/utils/formatters';
import { notificationService } from '@/utils/notification';
import Draggable from 'vuedraggable';

export default defineComponent({
  name: 'ProductMedia',

  components: {
    Draggable
  },

  setup() {
    const router = useRouter();
    const route = useRoute();
    const authStore = useAuthStore();
    const fileInput = ref<HTMLInputElement | null>(null);

    // Loading states
    const initialLoading = ref(true);
    const uploading = ref(false);
    const editLoading = ref(false);
    const deleteLoading = ref(false);
    const reorderLoading = ref(false);

    // Product data
    const product = ref<Product | null>(null);
    const mediaItems = ref<Media[]>([]);

    // Dialog states
    const showPreviewDialog = ref(false);
    const showUploadDialog = ref(false);
    const showEditDialog = ref(false);
    const showDeleteDialog = ref(false);
    const showReorderDialog = ref(false);

    // Media operations
    const selectedMedia = ref<Media | null>(null);
    const mediaToDelete = ref<Media | null>(null);

    // Edit form
    const editForm = ref({
      filename: '',
      alt_text: '',
      description: ''
    });
    const isEditFormValid = ref(true);

    // Upload
    const isDragging = ref(false);
    const filesToUpload = ref<File[]>([]);
    const uploadProgress = ref(0);

    // Reorder
    const reorderList = ref<Media[]>([]);

    // Form validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required'
    };

    // Get product ID from route
    const productId = computed(() => route.params.id as string);

    // Computed properties
    const imageCount = computed(() => {
      return mediaItems.value.filter(item => isImage(item)).length;
    });

    const documentCount = computed(() => {
      return mediaItems.value.filter(item => isDocument(item)).length;
    });

    const primaryMedia = computed(() => {
      return mediaItems.value.find(item => item.is_primary);
    });

    // Type checking utilities
    const isImage = (media: Media): boolean => {
      const imageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml'];
      return imageTypes.includes(media.mime_type);
    };

    const isDocument = (media: Media): boolean => {
      const docTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      return docTypes.includes(media.mime_type);
    };

    // Get icon for file type
    const getFileIcon = (file: File): string => {
      if (file.type.startsWith('image/')) {
        return 'mdi-file-image';
      } else if (file.type === 'application/pdf') {
        return 'mdi-file-pdf';
      } else if (file.type.includes('document')) {
        return 'mdi-file-document';
      } else {
        return 'mdi-file';
      }
    };

    // Fetch product data
    const fetchProduct = async () => {
      initialLoading.value = true;

      try {
        product.value = await productService.getProduct(productId.value);

        // Fetch media after product is loaded
        await fetchMedia();
      } catch (error) {
        console.error('Error fetching product:', error);
        product.value = null;
        notificationService.error('Failed to load product details');
      } finally {
        initialLoading.value = false;
      }
    };

    // Fetch media for the product
    const fetchMedia = async () => {
      try {
        mediaItems.value = await mediaService.getProductMedia(productId.value);
      } catch (error) {
        console.error('Error fetching media:', error);
        notificationService.error('Failed to load product media');
        mediaItems.value = [];
      }
    };

    // Open media preview
    const openMediaPreview = (media: Media) => {
      selectedMedia.value = media;
      showPreviewDialog.value = true;
    };

    // Edit media
    const editMedia = (media: Media) => {
      selectedMedia.value = media;
      editForm.value = {
        filename: media.filename,
        alt_text: media.alt_text || '',
        description: media.description || ''
      };
      showEditDialog.value = true;
    };

    // Save media edit
    const saveMediaEdit = async () => {
      if (!selectedMedia.value) return;

      editLoading.value = true;

      try {
        const updatedMedia = await mediaService.updateMedia(selectedMedia.value.id, {
          filename: editForm.value.filename,
          alt_text: editForm.value.alt_text,
          description: editForm.value.description
        });

        // Update media in list
        const index = mediaItems.value.findIndex(m => m.id === selectedMedia.value?.id);
        if (index !== -1) {
          mediaItems.value[index] = updatedMedia;
        }

        showEditDialog.value = false;
        selectedMedia.value = null;

        notificationService.success('Media details updated successfully');
      } catch (error) {
        console.error('Error updating media:', error);
        notificationService.error('Failed to update media details');
      } finally {
        editLoading.value = false;
      }
    };

    // Set primary media
    const setPrimaryMedia = async (media: Media) => {
      try {
        await mediaService.setPrimaryMedia(productId.value, media.id);

        // Update media items
        mediaItems.value.forEach(item => {
          item.is_primary = item.id === media.id;
        });

        // If in preview dialog, update selectedMedia
        if (selectedMedia.value) {
          selectedMedia.value.is_primary = selectedMedia.value.id === media.id;
        }

        notificationService.success('Primary image updated successfully');
      } catch (error) {
        console.error('Error setting primary media:', error);
        notificationService.error('Failed to set primary image');
      }
    };

    // Confirm delete media
    const confirmDeleteMedia = (media: Media | null) => {
      if (!media) return;

      mediaToDelete.value = media;
      showDeleteDialog.value = true;

      // If preview dialog is open, close it
      if (showPreviewDialog.value) {
        showPreviewDialog.value = false;
      }
    };

    // Delete media
    const deleteMedia = async () => {
      if (!mediaToDelete.value) return;

      deleteLoading.value = true;

      try {
        await mediaService.deleteMedia(mediaToDelete.value.id);

        // Remove from media items
        mediaItems.value = mediaItems.value.filter(item => item.id !== mediaToDelete.value?.id);

        showDeleteDialog.value = false;
        mediaToDelete.value = null;

        notificationService.success('Media deleted successfully');
      } catch (error) {
        console.error('Error deleting media:', error);
        notificationService.error('Failed to delete media');
      } finally {
        deleteLoading.value = false;
      }
    };

    // Handle file select for upload
    const handleFileSelect = (event: Event) => {
      const input = event.target as HTMLInputElement;
      if (input.files) {
        for (let i = 0; i < input.files.length; i++) {
          addFileToUpload(input.files[i]);
        }
      }
    };

    // Handle file drop for upload
    const handleFileDrop = (event: DragEvent) => {
      isDragging.value = false;

      if (event.dataTransfer?.files) {
        for (let i = 0; i < event.dataTransfer.files.length; i++) {
          addFileToUpload(event.dataTransfer.files[i]);
        }
      }
    };

    // Add file to upload list
    const addFileToUpload = (file: File) => {
      // Check file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        notificationService.error(`File ${file.name} exceeds the 10MB size limit`);
        return;
      }

      // Check if already added
      if (filesToUpload.value.some(f => f.name === file.name && f.size === file.size)) {
        notificationService.warning(`File ${file.name} is already selected`);
        return;
      }

      // Add to list
      filesToUpload.value.push(file);
    };

    // Remove file from upload list
    const removeFileFromUpload = (index: number) => {
      filesToUpload.value.splice(index, 1);
    };

    // Cancel upload
    const cancelUpload = () => {
      if (uploading.value) return;

      filesToUpload.value = [];
      uploadProgress.value = 0;
      showUploadDialog.value = false;
    };

    // Upload files
    const uploadFiles = async () => {
      if (filesToUpload.value.length === 0) return;

      uploading.value = true;
      uploadProgress.value = 0;

      try {
        // In a real implementation, we'd track progress for each file
        // For simulation, we'll increment the progress bar
        const totalFiles = filesToUpload.value.length;
        const progressIncrement = 100 / totalFiles;

        for (let i = 0; i < filesToUpload.value.length; i++) {
          // Upload each file
          await mediaService.uploadMedia(filesToUpload.value[i], productId.value);

          // Update progress
          uploadProgress.value += progressIncrement;
        }

        // Reload media after upload
        await fetchMedia();

        // Reset upload state
        filesToUpload.value = [];
        uploadProgress.value = 100;

        // Close dialog
        setTimeout(() => {
          showUploadDialog.value = false;
          uploading.value = false;
          uploadProgress.value = 0;
        }, 1000);

        notificationService.success(`${totalFiles} file(s) uploaded successfully`);
      } catch (error) {
        console.error('Error uploading files:', error);
        notificationService.error('Failed to upload files');
        uploading.value = false;
      }
    };

    // Reorder media
    const saveMediaOrder = async () => {
      reorderLoading.value = true;

      try {
        // Get media IDs in new order
        const mediaIds = reorderList.value.map(item => item.id);

        // Update order
        await mediaService.reorderProductMedia(productId.value, mediaIds);

        // If first item is not primary, set it as primary
        if (reorderList.value.length > 0 && !reorderList.value[0].is_primary) {
          await mediaService.setPrimaryMedia(productId.value, reorderList.value[0].id);
        }

        // Update media items with new order
        mediaItems.value = [...reorderList.value];

        // Update primary status
        mediaItems.value.forEach((item, index) => {
          item.is_primary = index === 0;
        });

        showReorderDialog.value = false;

        notificationService.success('Media order updated successfully');
      } catch (error) {
        console.error('Error reordering media:', error);
        notificationService.error('Failed to update media order');
      } finally {
        reorderLoading.value = false;
      }
    };

    // Initialize component
    onMounted(() => {
      fetchProduct();
    });

    // When reorder dialog is opened, initialize the reorder list
    watch(showReorderDialog, (isOpen) => {
      if (isOpen) {
        reorderList.value = [...mediaItems.value];
      }
    });

    return {
      router,
      fileInput,
      product,
      productId,
      initialLoading,
      uploading,
      editLoading,
      deleteLoading,
      reorderLoading,
      mediaItems,
      showPreviewDialog,
      showUploadDialog,
      showEditDialog,
      showDeleteDialog,
      showReorderDialog,
      selectedMedia,
      mediaToDelete,
      editForm,
      isEditFormValid,
      isDragging,
      filesToUpload,
      uploadProgress,
      reorderList,
      rules,
      imageCount,
      documentCount,
      primaryMedia,
      formatDateTime,
      formatFileSize,
      isImage,
      isDocument,
      getFileIcon,
      openMediaPreview,
      editMedia,
      saveMediaEdit,
      setPrimaryMedia,
      confirmDeleteMedia,
      deleteMedia,
      handleFileSelect,
      handleFileDrop,
      removeFileFromUpload,
      cancelUpload,
      uploadFiles,
      saveMediaOrder
    };
  }
});
</script>

<style scoped>
.media-item {
  transition: all 0.2s ease;
  position: relative;
}

.media-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.primary-media {
  border: 2px solid var(--v-primary-base);
}

.media-thumbnail {
  cursor: pointer;
}

.upload-dropzone {
  border: 2px dashed #ccc;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.upload-dropzone:hover {
  border-color: var(--v-primary-base);
}

.cursor-move {
  cursor: move;
}

.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}

.reorder-list {
  min-height: 200px;
}
</style>
