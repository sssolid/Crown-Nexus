<!-- frontend/src/views/SavedLists.vue -->
<template>
  <div>
    <v-container fluid>
      <!-- Page Header -->
      <v-row class="mb-6">
        <v-col cols="12" md="8">
          <h1 class="text-h3 font-weight-bold">Saved Lists</h1>
          <p class="text-subtitle-1">Manage your saved product lists for quick reordering</p>
        </v-col>
        <v-col cols="12" md="4" class="d-flex justify-end align-center">
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            @click="createNewList"
          >
            Create New List
          </v-btn>
        </v-col>
      </v-row>

      <!-- Lists Grid -->
      <div v-if="loading" class="d-flex justify-center my-12">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
      </div>
      
      <template v-else>
        <!-- Empty State -->
        <v-card 
          v-if="savedLists.length === 0"
          class="text-center pa-8 my-6"
        >
          <v-icon
            icon="mdi-playlist-star"
            size="64"
            color="grey-lighten-2"
          ></v-icon>
          <h2 class="text-h5 mt-4">No Saved Lists Yet</h2>
          <p class="text-body-1 mt-2 mb-6">
            Create lists to save frequently ordered products for easy reordering.
          </p>
          <v-btn
            color="primary"
            size="large"
            @click="createNewList"
          >
            Create Your First List
          </v-btn>
        </v-card>
        
        <!-- Lists Grid -->
        <v-row v-else>
          <v-col 
            v-for="list in savedLists"
            :key="list.id"
            cols="12"
            sm="6"
            md="4"
          >
            <v-card 
              :class="{'list-card-active': activeList?.id === list.id}"
              @click="viewList(list)"
              height="100%"
              class="list-card"
            >
              <v-card-item>
                <v-card-title>
                  <div class="d-flex align-center">
                    <span class="text-truncate">{{ list.name }}</span>
                    <v-spacer></v-spacer>
                    <v-menu>
                      <template v-slot:activator="{ props }">
                        <v-btn
                          icon="mdi-dots-vertical"
                          variant="text"
                          size="small"
                          v-bind="props"
                          @click.stop
                        ></v-btn>
                      </template>
                      <v-list>
                        <v-list-item
                          title="Rename List"
                          prepend-icon="mdi-pencil"
                          @click.stop="renameList(list)"
                        ></v-list-item>
                        <v-list-item
                          title="Delete List"
                          prepend-icon="mdi-delete"
                          @click.stop="confirmDeleteList(list)"
                        ></v-list-item>
                        <v-list-item
                          title="Add All to Cart"
                          prepend-icon="mdi-cart-plus"
                          @click.stop="addAllToCart(list)"
                        ></v-list-item>
                        <v-list-item
                          title="Share List"
                          prepend-icon="mdi-share-variant"
                          @click.stop="shareList(list)"
                        ></v-list-item>
                        <v-list-item
                          title="Export List"
                          prepend-icon="mdi-export"
                          @click.stop="exportList(list)"
                        ></v-list-item>
                      </v-list>
                    </v-menu>
                  </div>
                </v-card-title>
                <v-card-subtitle>
                  {{ list.items.length }} {{ list.items.length === 1 ? 'item' : 'items' }} · Last updated {{ formatDate(list.updated_at) }}
                </v-card-subtitle>
              </v-card-item>
              
              <v-card-text>
                <div class="d-flex mb-3">
                  <v-chip
                    v-if="list.is_favorite"
                    size="small"
                    color="warning"
                    variant="tonal"
                    prepend-icon="mdi-star"
                    class="mr-2"
                  >
                    Favorite
                  </v-chip>
                  <v-chip
                    size="small"
                    :color="getListTypeColor(list.type)"
                    variant="tonal"
                  >
                    {{ list.type }}
                  </v-chip>
                </div>
                
                <div class="text-body-2 text-truncate-2-lines">
                  {{ list.description || 'No description' }}
                </div>
                
                <v-divider class="my-3"></v-divider>
                
                <div class="d-flex align-center justify-space-between text-body-2">
                  <span>
                    <strong>Total Value:</strong> {{ formatCurrency(calculateListTotal(list)) }}
                  </span>
                  <span>
                    <v-icon icon="mdi-clock-outline" size="small" class="mr-1"></v-icon>
                    {{ list.is_scheduled ? 'Scheduled' : 'Manual' }}
                  </span>
                </div>
              </v-card-text>
              
              <v-card-actions>
                <v-btn
                  variant="text"
                  color="primary"
                  @click.stop="viewList(list)"
                >
                  View Details
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn
                  variant="tonal"
                  color="primary"
                  prepend-icon="mdi-cart-plus"
                  @click.stop="addAllToCart(list)"
                >
                  Add All to Cart
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <!-- List Detail Section -->
      <v-row class="mt-8" v-if="activeList">
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex align-center">
              <span class="text-truncate">{{ activeList.name }}</span>
              <v-btn
                icon="mdi-pencil"
                variant="text"
                size="small"
                class="ml-2"
                @click="renameList(activeList)"
              ></v-btn>
              <v-btn
                icon="mdi-star"
                variant="text"
                size="small"
                :color="activeList.is_favorite ? 'warning' : undefined"
                @click="toggleFavorite(activeList)"
              ></v-btn>
              <v-spacer></v-spacer>
              <v-btn
                variant="text"
                color="primary"
                size="small"
                prepend-icon="mdi-plus"
                @click="showAddProductsDialog = true"
              >
                Add Products
              </v-btn>
              <v-btn
                variant="tonal"
                color="primary"
                size="small"
                prepend-icon="mdi-cart-plus"
                @click="addAllToCart(activeList)"
                class="ml-2"
              >
                Add All to Cart
              </v-btn>
            </v-card-title>
            
            <v-divider></v-divider>
            
            <v-card-text v-if="activeList.description" class="bg-grey-lighten-5">
              <p>{{ activeList.description }}</p>
            </v-card-text>
            
            <v-data-table
              :headers="tableHeaders"
              :items="activeList.items"
              :loading="listLoading"
              class="elevation-0"
            >
              <!-- Product Column -->
              <template v-slot:item.product="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="40" class="mr-3">
                    <v-img
                      :src="item.raw.image || 'https://via.placeholder.com/50'"
                      alt="Product image"
                    ></v-img>
                  </v-avatar>
                  <div>
                    <div class="font-weight-medium">{{ item.raw.product_name }}</div>
                    <div class="text-caption text-grey">SKU: {{ item.raw.sku }}</div>
                  </div>
                </div>
              </template>
              
              <!-- Price Column -->
              <template v-slot:item.price="{ item }">
                {{ formatCurrency(item.raw.price) }}
              </template>
              
              <!-- Quantity Column -->
              <template v-slot:item.quantity="{ item }">
                <v-text-field
                  v-model="item.raw.quantity"
                  type="number"
                  min="1"
                  variant="outlined"
                  density="compact"
                  hide-details
                  class="quantity-field"
                  style="max-width: 100px"
                  @update:model-value="updateQuantity(item.raw)"
                ></v-text-field>
              </template>
              
              <!-- Subtotal Column -->
              <template v-slot:item.subtotal="{ item }">
                {{ formatCurrency(item.raw.price * item.raw.quantity) }}
              </template>
              
              <!-- In Stock Column -->
              <template v-slot:item.in_stock="{ item }">
                <v-chip
                  size="small"
                  :color="item.raw.in_stock ? 'success' : 'error'"
                  variant="tonal"
                >
                  {{ item.raw.in_stock ? 'In Stock' : 'Out of Stock' }}
                </v-chip>
              </template>
              
              <!-- Actions Column -->
              <template v-slot:item.actions="{ item }">
                <div class="d-flex">
                  <v-btn
                    icon
                    variant="text"
                    size="small"
                    color="primary"
                    @click="addToCart(item.raw)"
                    :disabled="!item.raw.in_stock"
                  >
                    <v-icon>mdi-cart-plus</v-icon>
                  </v-btn>
                  <v-btn
                    icon
                    variant="text"
                    size="small"
                    color="error"
                    @click="removeFromList(item.raw)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </div>
              </template>
              
              <!-- No items placeholder -->
              <template v-slot:no-data>
                <div class="text-center pa-6">
                  <v-icon
                    icon="mdi-format-list-text"
                    size="48"
                    color="grey-lighten-2"
                  ></v-icon>
                  <p class="text-body-1 mt-4 mb-6">
                    This list is empty. Add some products to get started.
                  </p>
                  <v-btn
                    color="primary"
                    @click="showAddProductsDialog = true"
                  >
                    Add Products
                  </v-btn>
                </div>
              </template>
            </v-data-table>
          </v-card>
        </v-col>
      </v-row>

      <!-- Quick Order Section -->
      <v-row class="mt-12">
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h4 font-weight-bold">Quick Order</v-card-title>
            <v-card-subtitle>Quickly order products by entering SKUs or part numbers</v-card-subtitle>
            <v-divider></v-divider>
            
            <v-card-text>
              <p class="mb-4">
                Enter SKUs or part numbers, one per line or separated by commas. You can also specify quantities by adding a colon followed by the quantity (e.g., "SKU123:5").
              </p>
              
              <v-textarea
                v-model="quickOrderText"
                label="Enter SKUs or Part Numbers"
                variant="outlined"
                rows="4"
                placeholder="Example: ABC123, DEF456:3, GHI789:2"
                class="mb-4"
              ></v-textarea>
              
              <div class="d-flex justify-end">
                <v-btn
                  color="primary"
                  :loading="quickOrderLoading"
                  :disabled="!quickOrderText"
                  @click="processQuickOrder"
                >
                  Process Quick Order
                </v-btn>
              </div>
            </v-card-text>
            
            <!-- Quick Order Results -->
            <div v-if="quickOrderResults.length > 0">
              <v-divider></v-divider>
              <v-card-text>
                <h3 class="text-h6 mb-4">Quick Order Results</h3>
                
                <v-data-table
                  :headers="quickOrderHeaders"
                  :items="quickOrderResults"
                  density="compact"
                >
                  <!-- Product Column -->
                  <template v-slot:item.product_name="{ item }">
                    <div v-if="item.raw.found">
                      <div class="font-weight-medium">{{ item.raw.product_name }}</div>
                      <div class="text-caption text-grey">SKU: {{ item.raw.sku }}</div>
                    </div>
                    <div v-else class="text-error">
                      Product not found: {{ item.raw.sku }}
                    </div>
                  </template>
                  
                  <!-- Price Column -->
                  <template v-slot:item.price="{ item }">
                    <span v-if="item.raw.found">{{ formatCurrency(item.raw.price) }}</span>
                    <span v-else>—</span>
                  </template>
                  
                  <!-- Quantity Column -->
                  <template v-slot:item.quantity="{ item }">
                    <v-text-field
                      v-if="item.raw.found"
                      v-model="item.raw.quantity"
                      type="number"
                      min="1"
                      variant="outlined"
                      density="compact"
                      hide-details
                      class="quantity-field"
                      style="max-width: 100px"
                    ></v-text-field>
                    <span v-else>—</span>
                  </template>
                  
                  <!-- Subtotal Column -->
                  <template v-slot:item.subtotal="{ item }">
                    <span v-if="item.raw.found">{{ formatCurrency(item.raw.price * item.raw.quantity) }}</span>
                    <span v-else>—</span>
                  </template>
                  
                  <!-- Status Column -->
                  <template v-slot:item.status="{ item }">
                    <v-chip
                      size="small"
                      :color="getStatusColor(item.raw)"
                      variant="tonal"
                    >
                      {{ getStatusText(item.raw) }}
                    </v-chip>
                  </template>
                  
                  <!-- Actions Column -->
                  <template v-slot:item.actions="{ item }">
                    <v-btn
                      v-if="item.raw.found"
                      icon
                      variant="text"
                      size="small"
                      color="primary"
                      @click="addToCart(item.raw)"
                      :disabled="!item.raw.in_stock"
                    >
                      <v-icon>mdi-cart-plus</v-icon>
                    </v-btn>
                  </template>
                </v-data-table>
                
                <div class="d-flex justify-end mt-4 gap-2">
                  <v-btn
                    color="primary"
                    variant="outlined"
                    @click="saveQuickOrderAsList"
                    :disabled="!hasValidQuickOrderItems"
                  >
                    Save as List
                  </v-btn>
                  <v-btn
                    color="primary"
                    @click="addAllQuickOrderToCart"
                    :disabled="!hasValidQuickOrderItems"
                  >
                    Add All to Cart
                  </v-btn>
                </div>
              </v-card-text>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- New List Dialog -->
    <v-dialog v-model="newListDialog.show" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          {{ newListDialog.isEdit ? 'Edit List' : 'Create New List' }}
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <v-text-field
            v-model="newListDialog.name"
            label="List Name"
            variant="outlined"
            :rules="[rules.required]"
            class="mb-4"
          ></v-text-field>
          
          <v-textarea
            v-model="newListDialog.description"
            label="Description (Optional)"
            variant="outlined"
            rows="3"
            class="mb-4"
          ></v-textarea>
          
          <v-select
            v-model="newListDialog.type"
            label="List Type"
            :items="listTypes"
            variant="outlined"
            class="mb-4"
          ></v-select>
          
          <v-checkbox
            v-model="newListDialog.is_favorite"
            label="Mark as Favorite"
            hide-details
            class="mb-4"
          ></v-checkbox>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="newListDialog.show = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="saveList"
            :loading="newListDialog.loading"
            :disabled="!newListDialog.name"
          >
            {{ newListDialog.isEdit ? 'Update' : 'Create' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete List Confirmation -->
    <v-dialog v-model="deleteDialog.show" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-error text-white pa-4">
          Delete List
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p>Are you sure you want to delete the list "{{ deleteDialog.listName }}"? This action cannot be undone.</p>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="deleteDialog.show = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="error"
            @click="deleteList"
            :loading="deleteDialog.loading"
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Share List Dialog -->
    <v-dialog v-model="shareDialog.show" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          Share List
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <p class="mb-4">Share "{{ shareDialog.listName }}" with your team members or other accounts.</p>
          
          <v-tabs v-model="shareDialog.activeTab" class="mb-4">
            <v-tab value="email">Email</v-tab>
            <v-tab value="link">Share Link</v-tab>
          </v-tabs>
          
          <v-window v-model="shareDialog.activeTab">
            <!-- Email Tab -->
            <v-window-item value="email">
              <v-text-field
                v-model="shareDialog.email"
                label="Email Address"
                variant="outlined"
                :rules="[rules.email]"
                class="mb-3"
              ></v-text-field>
              
              <v-select
                v-model="shareDialog.permission"
                label="Permission Level"
                :items="permissionLevels"
                variant="outlined"
                class="mb-3"
              ></v-select>
              
              <v-textarea
                v-model="shareDialog.message"
                label="Message (Optional)"
                variant="outlined"
                rows="3"
                placeholder="Add a personal message..."
              ></v-textarea>
            </v-window-item>
            
            <!-- Link Tab -->
            <v-window-item value="link">
              <v-text-field
                v-model="shareDialog.link"
                label="Shareable Link"
                variant="outlined"
                readonly
                class="mb-3"
                append-inner-icon="mdi-content-copy"
                @click:append-inner="copyShareLink"
              ></v-text-field>
              
              <v-select
                v-model="shareDialog.linkPermission"
                label="Link Permission"
                :items="permissionLevels"
                variant="outlined"
                class="mb-3"
              ></v-select>
              
              <v-checkbox
                v-model="shareDialog.expiresEnabled"
                label="Set Expiration Date"
                hide-details
                class="mb-2"
              ></v-checkbox>
              
              <v-text-field
                v-if="shareDialog.expiresEnabled"
                v-model="shareDialog.expiresDate"
                label="Expiration Date"
                type="date"
                variant="outlined"
              ></v-text-field>
            </v-window-item>
          </v-window>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="shareDialog.show = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="submitShare"
            :loading="shareDialog.loading"
            :disabled="isShareButtonDisabled"
          >
            {{ shareDialog.activeTab === 'email' ? 'Send' : 'Generate Link' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Add Products Dialog -->
    <v-dialog v-model="showAddProductsDialog" max-width="900">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          Add Products to List
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <v-text-field
            v-model="productSearch"
            label="Search Products"
            variant="outlined"
            prepend-inner-icon="mdi-magnify"
            clearable
            @keyup.enter="searchProducts"
            @click:prepend-inner="searchProducts"
            class="mb-4"
          ></v-text-field>
          
          <v-data-table
            :headers="productSearchHeaders"
            :items="searchResults"
            :loading="searchLoading"
            class="mb-4"
          >
            <!-- Product Column -->
            <template v-slot:item.product="{ item }">
              <div class="d-flex align-center">
                <v-avatar size="40" class="mr-3">
                  <v-img
                    :src="item.raw.image || 'https://via.placeholder.com/50'"
                    alt="Product image"
                  ></v-img>
                </v-avatar>
                <div>
                  <div class="font-weight-medium">{{ item.raw.product_name }}</div>
                  <div class="text-caption text-grey">SKU: {{ item.raw.sku }}</div>
                </div>
              </div>
            </template>
            
            <!-- Price Column -->
            <template v-slot:item.price="{ item }">
              {{ formatCurrency(item.raw.price) }}
            </template>
            
            <!-- Quantity Column -->
            <template v-slot:item.quantity="{ item }">
              <v-text-field
                v-model="item.raw.quantity"
                type="number"
                min="1"
                variant="outlined"
                density="compact"
                hide-details
                class="quantity-field"
                style="max-width: 100px"
              ></v-text-field>
            </template>
            
            <!-- In Stock Column -->
            <template v-slot:item.in_stock="{ item }">
              <v-chip
                size="small"
                :color="item.raw.in_stock ? 'success' : 'error'"
                variant="tonal"
              >
                {{ item.raw.in_stock ? 'In Stock' : 'Out of Stock' }}
              </v-chip>
            </template>
            
            <!-- Actions Column -->
            <template v-slot:item.actions="{ item }">
              <v-btn
                icon
                variant="text"
                size="small"
                color="primary"
                @click="addProductToList(item.raw)"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
          </v-data-table>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="showAddProductsDialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="primary"
            @click="addSelectedProducts"
            :disabled="!hasSelectedProducts"
          >
            Add Selected
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Save Quick Order Dialog -->
    <v-dialog v-model="saveQuickOrderDialog.show" max-width="500">
      <v-card>
        <v-card-title class="text-h5 bg-primary text-white pa-4">
          Save Quick Order as List
        </v-card-title>
        <v-card-text class="pa-4 pt-6">
          <v-text-field
            v-model="saveQuickOrderDialog.name"
            label="List Name"
            variant="outlined"
            :rules="[rules.required]"
            class="mb-4"
          ></v-text-field>
          
          <v-textarea
            v-model="saveQuickOrderDialog.description"
            label="Description (Optional)"
            variant="outlined"
            rows="3"
            class="mb-4"
          ></v-textarea>
          
          <v-select
            v-model="saveQuickOrderDialog.type"
            label="List Type"
            :items="listTypes"
            variant="outlined"
            class="mb-4"
          ></v-select>
          
          <v-checkbox
            v-model="saveQuickOrderDialog.is_favorite"
            label="Mark as Favorite"
            hide-details
          ></v-checkbox>
        </v-card-text>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="grey"
            variant="text"
            @click="saveQuickOrderDialog.show = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="saveQuickOrderList"
            :loading="saveQuickOrderDialog.loading"
            :disabled="!saveQuickOrderDialog.name"
          >
            Save List
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { formatDate, formatCurrency } from '@/utils/formatters';
import { notificationService } from '@/utils/notification';

// Product interface
interface Product {
  id: string;
  sku: string;
  product_name: string;
  price: number;
  quantity: number;
  in_stock: boolean;
  image?: string;
  found?: boolean;
  status?: string;
}

// List interface
interface SavedList {
  id: string;
  name: string;
  description: string;
  type: string;
  items: Product[];
  is_favorite: boolean;
  is_scheduled: boolean;
  created_at: string;
  updated_at: string;
}

// New List Dialog interface
interface NewListDialog {
  show: boolean;
  isEdit: boolean;
  listId?: string;
  name: string;
  description: string;
  type: string;
  is_favorite: boolean;
  loading: boolean;
}

// Delete Dialog interface
interface DeleteDialog {
  show: boolean;
  listId?: string;
  listName: string;
  loading: boolean;
}

// Share Dialog interface
interface ShareDialog {
  show: boolean;
  listId?: string;
  listName: string;
  activeTab: string;
  email: string;
  permission: string;
  message: string;
  link: string;
  linkPermission: string;
  expiresEnabled: boolean;
  expiresDate: string;
  loading: boolean;
}

// Save Quick Order Dialog interface
interface SaveQuickOrderDialog {
  show: boolean;
  name: string;
  description: string;
  type: string;
  is_favorite: boolean;
  loading: boolean;
}

export default defineComponent({
  name: 'SavedLists',

  setup() {
    const authStore = useAuthStore();
    
    // Loading states
    const loading = ref(true);
    const listLoading = ref(false);
    const searchLoading = ref(false);
    const quickOrderLoading = ref(false);
    
    // Saved lists
    const savedLists = ref<SavedList[]>([]);
    
    // Active list
    const activeList = ref<SavedList | null>(null);
    
    // New list dialog
    const newListDialog = ref<NewListDialog>({
      show: false,
      isEdit: false,
      name: '',
      description: '',
      type: 'Standard',
      is_favorite: false,
      loading: false
    });
    
    // Delete dialog
    const deleteDialog = ref<DeleteDialog>({
      show: false,
      listName: '',
      loading: false
    });
    
    // Share dialog
    const shareDialog = ref<ShareDialog>({
      show: false,
      listName: '',
      activeTab: 'email',
      email: '',
      permission: 'View',
      message: '',
      link: '',
      linkPermission: 'View',
      expiresEnabled: false,
      expiresDate: '',
      loading: false
    });
    
    // Save quick order dialog
    const saveQuickOrderDialog = ref<SaveQuickOrderDialog>({
      show: false,
      name: 'Quick Order List',
      description: '',
      type: 'Standard',
      is_favorite: false,
      loading: false
    });
    
    // Add products dialog
    const showAddProductsDialog = ref(false);
    const productSearch = ref('');
    const searchResults = ref<Product[]>([]);
    
    // Quick order
    const quickOrderText = ref('');
    const quickOrderResults = ref<Product[]>([]);
    
    // Form validation rules
    const rules = {
      required: (v: string) => !!v || 'This field is required',
      email: (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid'
    };
    
    // List types
    const listTypes = ref([
      'Standard',
      'Favorites',
      'Reorder',
      'Wishlist',
      'Seasonal',
      'Regular Stock'
    ]);
    
    // Permission levels
    const permissionLevels = ref([
      'View',
      'Edit',
      'Full Access'
    ]);
    
    // Table headers
    const tableHeaders = ref([
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Subtotal', key: 'subtotal', sortable: true },
      { title: 'Status', key: 'in_stock', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]);
    
    // Quick order headers
    const quickOrderHeaders = ref([
      { title: 'Product', key: 'product_name', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Subtotal', key: 'subtotal', sortable: true },
      { title: 'Status', key: 'status', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]);
    
    // Product search headers
    const productSearchHeaders = ref([
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Availability', key: 'in_stock', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]);
    
    // Check if there are valid quick order items
    const hasValidQuickOrderItems = computed(() => {
      return quickOrderResults.value.some(item => item.found);
    });
    
    // Check if there are selected products in search
    const hasSelectedProducts = computed(() => {
      return searchResults.value.some(item => item.quantity > 0);
    });
    
    // Check if the share button should be disabled
    const isShareButtonDisabled = computed(() => {
      if (shareDialog.value.activeTab === 'email') {
        return !shareDialog.value.email || !/.+@.+\..+/.test(shareDialog.value.email);
      } else {
        return false;
      }
    });
    
    // Fetch saved lists
    const fetchSavedLists = async () => {
      loading.value = true;
      
      try {
        // In a real implementation, this would be an API call
        // const response = await api.get('/account/saved-lists');
        
        // Mock data for demonstration
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Sample lists
        savedLists.value = [
          {
            id: 'list-001',
            name: 'Regular Service Items',
            description: 'Frequently used items for regular service jobs',
            type: 'Regular Stock',
            is_favorite: true,
            is_scheduled: false,
            created_at: '2023-01-10T09:30:00Z',
            updated_at: '2023-02-18T08:30:00Z',
            items: [
              {
                id: 'prod-1',
                sku: 'OIL-5W30-1',
                product_name: '5W-30 Synthetic Oil (1 Quart)',
                price: 8.99,
                quantity: 10,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Oil'
              },
              {
                id: 'prod-2',
                sku: 'FIL-OIL-4562',
                product_name: 'Premium Oil Filter',
                price: 5.49,
                quantity: 5,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Filter'
              },
              {
                id: 'prod-3',
                sku: 'FIL-AIR-7890',
                product_name: 'Engine Air Filter',
                price: 12.99,
                quantity: 3,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Air'
              },
              {
                id: 'prod-4',
                sku: 'FIL-CAB-1234',
                product_name: 'Cabin Air Filter',
                price: 14.99,
                quantity: 2,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Cabin'
              },
              {
                id: 'prod-5',
                sku: 'WIPERS-20',
                product_name: '20" Wiper Blades',
                price: 15.99,
                quantity: 2,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Wiper'
              }
            ]
          },
          {
            id: 'list-002',
            name: 'Monthly Restock',
            description: 'Items to restock at the beginning of each month',
            type: 'Standard',
            is_favorite: false,
            is_scheduled: true,
            created_at: '2023-01-15T11:45:00Z',
            updated_at: '2023-02-10T11:45:00Z',
            items: [
              {
                id: 'prod-6',
                sku: 'OIL-5W30-CASE',
                product_name: '5W-30 Synthetic Oil (Case of 12)',
                price: 89.99,
                quantity: 2,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Oil'
              },
              {
                id: 'prod-7',
                sku: 'FIL-OIL-BULK',
                product_name: 'Premium Oil Filters (Pack of 12)',
                price: 49.99,
                quantity: 1,
                in_stock: false,
                image: 'https://via.placeholder.com/50?text=Filters'
              },
              {
                id: 'prod-8',
                sku: 'BRAKE-PAD-FRONT',
                product_name: 'Front Brake Pads (Assorted)',
                price: 149.99,
                quantity: 1,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Brakes'
              }
            ]
          },
          {
            id: 'list-003',
            name: 'Workshop Supplies',
            description: 'General workshop supplies and consumables',
            type: 'Standard',
            is_favorite: false,
            is_scheduled: false,
            created_at: '2023-01-20T14:20:00Z',
            updated_at: '2023-01-25T14:20:00Z',
            items: [
              {
                id: 'prod-9',
                sku: 'GLOVES-L',
                product_name: 'Nitrile Gloves Large (Box of 100)',
                price: 18.99,
                quantity: 2,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Gloves'
              },
              {
                id: 'prod-10',
                sku: 'TOWEL-BLUE',
                product_name: 'Shop Towels (Roll of 200)',
                price: 24.99,
                quantity: 3,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Towels'
              },
              {
                id: 'prod-11',
                sku: 'CLEANER-GAL',
                product_name: 'Parts Cleaner (1 Gallon)',
                price: 15.99,
                quantity: 1,
                in_stock: true,
                image: 'https://via.placeholder.com/50?text=Cleaner'
              }
            ]
          }
        ];
      } catch (error) {
        console.error('Error fetching saved lists:', error);
        notificationService.error('Failed to load saved lists. Please try again later.');
      } finally {
        loading.value = false;
      }
    };
    
    // Get color for list type
    const getListTypeColor = (type: string) => {
      switch (type) {
        case 'Favorites':
          return 'warning';
        case 'Reorder':
          return 'success';
        case 'Wishlist':
          return 'info';
        case 'Seasonal':
          return 'error';
        case 'Regular Stock':
          return 'secondary';
        default:
          return 'primary';
      }
    };
    
    // Calculate total value of list
    const calculateListTotal = (list: SavedList) => {
      return list.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    };
    
    // View list details
    const viewList = (list: SavedList) => {
      activeList.value = { ...list };
    };
    
    // Create new list
    const createNewList = () => {
      newListDialog.value = {
        show: true,
        isEdit: false,
        name: '',
        description: '',
        type: 'Standard',
        is_favorite: false,
        loading: false
      };
    };
    
    // Rename list
    const renameList = (list: SavedList) => {
      newListDialog.value = {
        show: true,
        isEdit: true,
        listId: list.id,
        name: list.name,
        description: list.description,
        type: list.type,
        is_favorite: list.is_favorite,
        loading: false
      };
    };
    
    // Save list (create or update)
    const saveList = async () => {
      if (!newListDialog.value.name) {
        notificationService.warning('Please enter a list name');
        return;
      }
      
      newListDialog.value.loading = true;
      
      try {
        // In a real implementation, this would be an API call
        // const payload = {
        //   name: newListDialog.value.name,
        //   description: newListDialog.value.description,
        //   type: newListDialog.value.type,
        //   is_favorite: newListDialog.value.is_favorite
        // };
        
        // if (newListDialog.value.isEdit) {
        //   await api.put(`/account/saved-lists/${newListDialog.value.listId}`, payload);
        // } else {
        //   await api.post('/account/saved-lists', payload);
        // }
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        if (newListDialog.value.isEdit && newListDialog.value.listId) {
          // Update local list
          const listIndex = savedLists.value.findIndex(list => list.id === newListDialog.value.listId);
          if (listIndex !== -1) {
            savedLists.value[listIndex] = {
              ...savedLists.value[listIndex],
              name: newListDialog.value.name,
              description: newListDialog.value.description,
              type: newListDialog.value.type,
              is_favorite: newListDialog.value.is_favorite,
              updated_at: new Date().toISOString()
            };
            
            // Update active list if it's the one being edited
            if (activeList.value && activeList.value.id === newListDialog.value.listId) {
              activeList.value = { ...savedLists.value[listIndex] };
            }
          }
          
          notificationService.success('List updated successfully');
        } else {
          // Create new list
          const newList: SavedList = {
            id: `list-${Date.now()}`,
            name: newListDialog.value.name,
            description: newListDialog.value.description,
            type: newListDialog.value.type,
            is_favorite: newListDialog.value.is_favorite,
            is_scheduled: false,
            items: [],
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          };
          
          savedLists.value.unshift(newList);
          activeList.value = newList;
          
          notificationService.success('List created successfully');
        }
        
        newListDialog.value.show = false;
      } catch (error) {
        console.error('Error saving list:', error);
        notificationService.error('Failed to save list. Please try again.');
      } finally {
        newListDialog.value.loading = false;
      }
    };
    
    // Confirm delete list
    const confirmDeleteList = (list: SavedList) => {
      deleteDialog.value = {
        show: true,
        listId: list.id,
        listName: list.name,
        loading: false
      };
    };
    
    // Delete list
    const deleteList = async () => {
      if (!deleteDialog.value.listId) return;
      
      deleteDialog.value.loading = true;
      
      try {
        // In a real implementation, this would be an API call
        // await api.delete(`/account/saved-lists/${deleteDialog.value.listId}`);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Remove list from local state
        savedLists.value = savedLists.value.filter(list => list.id !== deleteDialog.value.listId);
        
        // Clear active list if it's the one being deleted
        if (activeList.value && activeList.value.id === deleteDialog.value.listId) {
          activeList.value = null;
        }
        
        deleteDialog.value.show = false;
        notificationService.success('List deleted successfully');
      } catch (error) {
        console.error('Error deleting list:', error);
        notificationService.error('Failed to delete list. Please try again.');
      } finally {
        deleteDialog.value.loading = false;
      }
    };
    
    // Toggle favorite
    const toggleFavorite = async (list: SavedList) => {
      try {
        // In a real implementation, this would be an API call
        // await api.put(`/account/saved-lists/${list.id}/favorite`, { is_favorite: !list.is_favorite });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 200));
        
        // Update local state
        const listIndex = savedLists.value.findIndex(l => l.id === list.id);
        if (listIndex !== -1) {
          savedLists.value[listIndex].is_favorite = !list.is_favorite;
        }
        
        // Update active list if it's the one being modified
        if (activeList.value && activeList.value.id === list.id) {
          activeList.value.is_favorite = !list.is_favorite;
        }
        
        notificationService.success(list.is_favorite ? 'Removed from favorites' : 'Added to favorites');
      } catch (error) {
        console.error('Error toggling favorite:', error);
        notificationService.error('Failed to update favorite status. Please try again.');
      }
    };
    
    // Update item quantity
    const updateQuantity = async (item: Product) => {
      if (!activeList.value) return;
      
      try {
        // In a real implementation, this would be an API call
        // await api.put(`/account/saved-lists/${activeList.value.id}/items/${item.id}`, {
        //   quantity: item.quantity
        // });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 200));
        
        // Update is handled automatically through v-model binding
      } catch (error) {
        console.error('Error updating quantity:', error);
        notificationService.error('Failed to update quantity. Please try again.');
      }
    };
    
    // Remove item from list
    const removeFromList = async (item: Product) => {
      if (!activeList.value) return;
      
      try {
        // In a real implementation, this would be an API call
        // await api.delete(`/account/saved-lists/${activeList.value.id}/items/${item.id}`);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Update local state
        activeList.value.items = activeList.value.items.filter(i => i.id !== item.id);
        
        // Update list in saved lists
        const listIndex = savedLists.value.findIndex(list => list.id === activeList.value?.id);
        if (listIndex !== -1) {
          savedLists.value[listIndex].items = [...activeList.value.items];
        }
        
        notificationService.success('Item removed from list');
      } catch (error) {
        console.error('Error removing item from list:', error);
        notificationService.error('Failed to remove item. Please try again.');
      }
    };
    
    // Add to cart
    const addToCart = async (item: Product) => {
      try {
        // In a real implementation, this would be an API call
        // await api.post('/cart/items', {
        //   product_id: item.id,
        //   quantity: item.quantity
        // });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 300));
        
        notificationService.success(`Added ${item.quantity}x ${item.product_name} to cart`);
      } catch (error) {
        console.error('Error adding to cart:', error);
        notificationService.error('Failed to add to cart. Please try again.');
      }
    };
    
    // Add all to cart
    const addAllToCart = async (list: SavedList) => {
      try {
        // In a real implementation, this would be an API call
        // const items = list.items.map(item => ({
        //   product_id: item.id,
        //   quantity: item.quantity
        // }));
        // await api.post('/cart/bulk', { items });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        const inStockCount = list.items.filter(item => item.in_stock).length;
        notificationService.success(`Added ${inStockCount} items to your cart`);
      } catch (error) {
        console.error('Error adding all to cart:', error);
        notificationService.error('Failed to add items to cart. Please try again.');
      }
    };
    
    // Share list
    const shareList = (list: SavedList) => {
      // Generate a mock share link
      const shareLink = `https://crownnexus.com/shared-lists/${list.id}`;
      
      shareDialog.value = {
        show: true,
        listId: list.id,
        listName: list.name,
        activeTab: 'email',
        email: '',
        permission: 'View',
        message: '',
        link: shareLink,
        linkPermission: 'View',
        expiresEnabled: false,
        expiresDate: '',
        loading: false
      };
    };
    
    // Copy share link
    const copyShareLink = async () => {
      try {
        await navigator.clipboard.writeText(shareDialog.value.link);
        notificationService.success('Link copied to clipboard');
      } catch (error) {
        console.error('Error copying link:', error);
        notificationService.error('Failed to copy link. Please try again.');
      }
    };
    
    // Submit share
    const submitShare = async () => {
      shareDialog.value.loading = true;
      
      try {
        // In a real implementation, this would be an API call
        // if (shareDialog.value.activeTab === 'email') {
        //   await api.post(`/account/saved-lists/${shareDialog.value.listId}/share`, {
        //     email: shareDialog.value.email,
        //     permission: shareDialog.value.permission,
        //     message: shareDialog.value.message
        //   });
        // } else {
        //   await api.post(`/account/saved-lists/${shareDialog.value.listId}/share-link`, {
        //     permission: shareDialog.value.linkPermission,
        //     expires: shareDialog.value.expiresEnabled ? shareDialog.value.expiresDate : null
        //   });
        // }
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (shareDialog.value.activeTab === 'email') {
          notificationService.success(`List shared with ${shareDialog.value.email}`);
        } else {
          notificationService.success('Share link generated successfully');
        }
        
        shareDialog.value.show = false;
      } catch (error) {
        console.error('Error sharing list:', error);
        notificationService.error('Failed to share list. Please try again.');
      } finally {
        shareDialog.value.loading = false;
      }
    };
    
    // Export list
    const exportList = async (list: SavedList) => {
      try {
        // In a real implementation, this would be an API call that returns a file
        // const response = await api.get(`/account/saved-lists/${list.id}/export`, {
        //   responseType: 'blob'
        // });
        // 
        // const url = window.URL.createObjectURL(new Blob([response]));
        // const link = document.createElement('a');
        // link.href = url;
        // link.setAttribute('download', `${list.name}.csv`);
        // document.body.appendChild(link);
        // link.click();
        // link.remove();
        
        // Simulate export
        await new Promise(resolve => setTimeout(resolve, 500));
        
        notificationService.success(`Exporting list: ${list.name}`);
      } catch (error) {
        console.error('Error exporting list:', error);
        notificationService.error('Failed to export list. Please try again.');
      }
    };
    
    // Search products
    const searchProducts = async () => {
      if (!productSearch.value.trim()) return;
      
      searchLoading.value = true;
      
      try {
        // In a real implementation, this would be an API call
        // const response = await api.get('/products/search', {
        //   params: { q: productSearch.value }
        // });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Mock search results
        searchResults.value = [
          {
            id: 'prod-101',
            sku: 'OIL-10W30-1',
            product_name: '10W-30 Synthetic Oil (1 Quart)',
            price: 7.99,
            quantity: 1,
            in_stock: true,
            image: 'https://via.placeholder.com/50?text=Oil'
          },
          {
            id: 'prod-102',
            sku: 'OIL-10W40-1',
            product_name: '10W-40 Synthetic Oil (1 Quart)',
            price: 7.99,
            quantity: 1,
            in_stock: true,
            image: 'https://via.placeholder.com/50?text=Oil'
          },
          {
            id: 'prod-103',
            sku: 'OIL-5W20-1',
            product_name: '5W-20 Synthetic Oil (1 Quart)',
            price: 8.99,
            quantity: 1,
            in_stock: true,
            image: 'https://via.placeholder.com/50?text=Oil'
          },
          {
            id: 'prod-104',
            sku: 'OIL-0W20-1',
            product_name: '0W-20 Synthetic Oil (1 Quart)',
            price: 9.99,
            quantity: 1,
            in_stock: false,
            image: 'https://via.placeholder.com/50?text=Oil'
          }
        ];
      } catch (error) {
        console.error('Error searching products:', error);
        notificationService.error('Failed to search products. Please try again.');
      } finally {
        searchLoading.value = false;
      }
    };
    
    // Add product to list
    const addProductToList = async (product: Product) => {
      if (!activeList.value) return;
      
      try {
        // In a real implementation, this would be an API call
        // await api.post(`/account/saved-lists/${activeList.value.id}/items`, {
        //   product_id: product.id,
        //   quantity: product.quantity
        // });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Check if product already exists in list
        const existingProduct = activeList.value.items.find(item => item.id === product.id);
        
        if (existingProduct) {
          // Update existing product quantity
          existingProduct.quantity += product.quantity;
        } else {
          // Add product to list
          activeList.value.items.push({ ...product });
        }
        
        // Update list in saved lists
        const listIndex = savedLists.value.findIndex(list => list.id === activeList.value?.id);
        if (listIndex !== -1) {
          savedLists.value[listIndex].items = [...activeList.value.items];
          savedLists.value[listIndex].updated_at = new Date().toISOString();
        }
        
        notificationService.success(`Added ${product.product_name} to list`);
      } catch (error) {
        console.error('Error adding product to list:', error);
        notificationService.error('Failed to add product to list. Please try again.');
      }
    };
    
    // Add selected products
    const addSelectedProducts = () => {
      const selectedProducts = searchResults.value.filter(product => product.quantity > 0);
      
      if (selectedProducts.length === 0) {
        notificationService.warning('Please select at least one product');
        return;
      }
      
      // Add each selected product to the list
      selectedProducts.forEach(product => {
        addProductToList(product);
      });
      
      // Close dialog after adding products
      showAddProductsDialog.value = false;
    };
    
    // Process quick order
    const processQuickOrder = async () => {
      if (!quickOrderText.value.trim()) {
        notificationService.warning('Please enter at least one SKU or part number');
        return;
      }
      
      quickOrderLoading.value = true;
      
      try {
        // Parse the input text
        // Format: SKU1, SKU2:2, SKU3:3 (SKU:quantity)
        const lines = quickOrderText.value
          .split(/[\n,]/)
          .map(line => line.trim())
          .filter(line => line);
        
        // In a real implementation, this would be an API call
        // const response = await api.post('/products/bulk-info', { skus: lines });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock quick order results
        const results: Product[] = [];
        
        lines.forEach(line => {
          // Parse SKU and quantity
          const [sku, quantityStr] = line.split(':');
          const quantity = quantityStr ? parseInt(quantityStr, 10) : 1;
          
          // Mock product lookup
          const found = Math.random() > 0.2; // 80% chance of finding the product
          
          if (found) {
            results.push({
              id: `prod-${Date.now()}-${sku}`,
              sku: sku.toUpperCase(),
              product_name: `${sku.toUpperCase()} Product`,
              price: parseFloat((Math.random() * 100 + 5).toFixed(2)),
              quantity: quantity,
              in_stock: Math.random() > 0.3, // 70% chance of being in stock
              found: true,
              image: 'https://via.placeholder.com/50'
            });
          } else {
            results.push({
              id: `not-found-${Date.now()}-${sku}`,
              sku: sku.toUpperCase(),
              product_name: '',
              price: 0,
              quantity: quantity,
              in_stock: false,
              found: false
            });
          }
        });
        
        quickOrderResults.value = results;
      } catch (error) {
        console.error('Error processing quick order:', error);
        notificationService.error('Failed to process quick order. Please try again.');
      } finally {
        quickOrderLoading.value = false;
      }
    };
    
    // Get status color
    const getStatusColor = (product: Product) => {
      if (!product.found) return 'error';
      if (!product.in_stock) return 'warning';
      return 'success';
    };
    
    // Get status text
    const getStatusText = (product: Product) => {
      if (!product.found) return 'Not Found';
      if (!product.in_stock) return 'Out of Stock';
      return 'In Stock';
    };
    
    // Add all quick order items to cart
    const addAllQuickOrderToCart = async () => {
      const validItems = quickOrderResults.value.filter(item => item.found && item.in_stock);
      
      if (validItems.length === 0) {
        notificationService.warning('No valid items to add to cart');
        return;
      }
      
      try {
        // In a real implementation, this would be an API call
        // const items = validItems.map(item => ({
        //   product_id: item.id,
        //   quantity: item.quantity
        // }));
        // await api.post('/cart/bulk', { items });
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        notificationService.success(`Added ${validItems.length} items to your cart`);
        
        // Clear quick order results
        quickOrderResults.value = [];
        quickOrderText.value = '';
      } catch (error) {
        console.error('Error adding quick order to cart:', error);
        notificationService.error('Failed to add items to cart. Please try again.');
      }
    };
    
    // Save quick order as list
    const saveQuickOrderAsList = () => {
      // Only save found items
      if (!quickOrderResults.value.some(item => item.found)) {
        notificationService.warning('No valid items to save');
        return;
      }
      
      saveQuickOrderDialog.value = {
        show: true,
        name: 'Quick Order List',
        description: '',
        type: 'Standard',
        is_favorite: false,
        loading: false
      };
    };
    
    // Save quick order list
    const saveQuickOrderList = async () => {
      if (!saveQuickOrderDialog.value.name) {
        notificationService.warning('Please enter a list name');
        return;
      }
      
      saveQuickOrderDialog.value.loading = true;
      
      try {
        // In a real implementation, this would be an API call
        // const payload = {
        //   name: saveQuickOrderDialog.value.name,
        //   description: saveQuickOrderDialog.value.description,
        //   type: saveQuickOrderDialog.value.type,
        //   is_favorite: saveQuickOrderDialog.value.is_favorite,
        //   items: quickOrderResults.value.filter(item => item.found).map(item => ({
        //     product_id: item.id,
        //     quantity: item.quantity
        //   }))
        // };
        // const response = await api.post('/account/saved-lists', payload);
        
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Create new list with quick order items
        const newList: SavedList = {
          id: `list-${Date.now()}`,
          name: saveQuickOrderDialog.value.name,
          description: saveQuickOrderDialog.value.description,
          type: saveQuickOrderDialog.value.type,
          is_favorite: saveQuickOrderDialog.value.is_favorite,
          is_scheduled: false,
          items: quickOrderResults.value.filter(item => item.found),
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        };
        
        savedLists.value.unshift(newList);
        activeList.value = newList;
        
        notificationService.success('Quick order saved as list');
        
        // Clear quick order results
        quickOrderResults.value = [];
        quickOrderText.value = '';
        
        saveQuickOrderDialog.value.show = false;
      } catch (error) {
        console.error('Error saving quick order list:', error);
        notificationService.error('Failed to save list. Please try again.');
      } finally {
        saveQuickOrderDialog.value.loading = false;
      }
    };
    
    // Initialize component
    onMounted(() => {
      fetchSavedLists();
    });
    
    return {
      savedLists,
      loading,
      listLoading,
      activeList,
      newListDialog,
      deleteDialog,
      shareDialog,
      saveQuickOrderDialog,
      showAddProductsDialog,
      productSearch,
      searchResults,
      searchLoading,
      quickOrderText,
      quickOrderResults,
      quickOrderLoading,
      rules,
      listTypes,
      permissionLevels,
      tableHeaders,
      quickOrderHeaders,
      productSearchHeaders,
      hasValidQuickOrderItems,
      hasSelectedProducts,
      isShareButtonDisabled,
      getListTypeColor,
      calculateListTotal,
      viewList,
      createNewList,
      renameList,
      saveList,
      confirmDeleteList,
      deleteList,
      toggleFavorite,
      updateQuantity,
      removeFromList,
      addToCart,
      addAllToCart,
      shareList,
      copyShareLink,
      submitShare,
      exportList,
      searchProducts,
      addProductToList,
      addSelectedProducts,
      processQuickOrder,
      getStatusColor,
      getStatusText,
      addAllQuickOrderToCart,
      saveQuickOrderAsList,
      saveQuickOrderList,
      formatDate,
      formatCurrency
    };
  }
});
</script>

<style scoped>
.list-card {
  transition: all 0.2s ease;
  cursor: pointer;
}

.list-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.list-card-active {
  border: 2px solid rgb(var(--v-theme-primary));
}

.text-truncate-2-lines {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.quantity-field :deep(.v-field__input) {
  text-align: center;
}
</style>
