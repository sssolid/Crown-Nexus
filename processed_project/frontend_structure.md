# frontend Frontend Structure
Generated on 2025-03-17 01:41:36

## Project Overview
- Project Name: frontend
- Project Type: Vue 3
- Root Path: /home/runner/work/Crown-Nexus/Crown-Nexus/frontend

### Dependencies
**Production Dependencies:**
- @mdi/font: ^7.4.47
- axios: ^1.8.1
- date-fns: ^4.1.0
- package.json: ^2.0.1
- pinia: ^2.3.1
- vue: ^3.5.13
- vue-i18n: ^10.0.6
- vue-router: ^4.5.0
- vuetify: ^3.7.15

**Development Dependencies:**
- @types/node: ^22.13.9
- @vitejs/plugin-vue: ^5.2.1
- @vitejs/plugin-vue-jsx: ^4.1.1
- @vue/test-utils: ^2.4.6
- @vue/tsconfig: ^0.7.0
- jsdom: ^26.0.0
- typescript: ~5.7.2
- vite: ^6.2.0
- vitest: ^3.0.7
- vue-tsc: ^2.2.4

## Directory Structure
```
frontend/
├── public/
│   └── vite.svg
├── src/
│   ├── assets/
│   │   ├── brand_identity/
│   │   │   ├── brand_pattern_background.png
│   │   │   ├── brand_pattern_background2.png
│   │   │   ├── icon.png
│   │   │   ├── icon2.png
│   │   │   ├── logo.png
│   │   │   └── logo2.png
│   │   ├── dashboard_ui/
│   │   │   ├── dashboard_welcome_banner.png
│   │   │   ├── dashboard_welcome_banner2.png
│   │   │   ├── empty_state_charts.png
│   │   │   ├── empty_state_charts2.png
│   │   │   ├── widget_card_header_fitments.png
│   │   │   ├── widget_card_header_fitments2.png
│   │   │   ├── widget_card_header_order_sales.png
│   │   │   ├── widget_card_header_order_sales2.png
│   │   │   ├── widget_card_header_products.png
│   │   │   ├── widget_card_header_products2.png
│   │   │   └── widget_card_header_user_account.png
│   │   ├── documentation_help/
│   │   │   ├── database_relationship_diagram.png
│   │   │   ├── database_relationship_diagram2.png
│   │   │   ├── fitment_association_workflow.png
│   │   │   ├── import_export_workflow.png
│   │   │   ├── import_export_workflow2.png
│   │   │   ├── order_processing_workflow.png
│   │   │   ├── order_processing_workflow2.png
│   │   │   ├── product_creation_workflow.png
│   │   │   ├── product_creation_workflow2.png
│   │   │   ├── tutorial_screenshots.png
│   │   │   ├── tutorial_screenshots2.png
│   │   │   ├── user_permission_management.png
│   │   │   └── user_permission_management2.png
│   │   ├── email_notification/
│   │   │   ├── account_alerts.png
│   │   │   ├── account_alerts2.png
│   │   │   ├── email_header.png
│   │   │   ├── email_header2.png
│   │   │   ├── newsletter_updates.png
│   │   │   ├── newsletter_updates2.png
│   │   │   ├── order_confirmation.png
│   │   │   ├── order_confirmation2.png
│   │   │   ├── password_reset_security.png
│   │   │   ├── password_reset_security2.png
│   │   │   └── welcome_onboarding.png
│   │   ├── fitment_related/
│   │   │   ├── fitment_compatibility.png
│   │   │   ├── fitment_compatibility2.png
│   │   │   ├── vehicle_make_icons.png
│   │   │   ├── vehicle_make_icons2.png
│   │   │   ├── vehicle_position_diagrams.png
│   │   │   └── vehicle_position_diagrams2.png
│   │   ├── marketing_landing/
│   │   │   ├── analytics_reporting.png
│   │   │   ├── catalog_management.png
│   │   │   ├── catalog_management2.png
│   │   │   ├── fitment_compatibility.png
│   │   │   ├── fitment_compatibility2.png
│   │   │   ├── home_page_hero_banner.png
│   │   │   ├── home_page_hero_banner2.png
│   │   │   ├── order_processing.png
│   │   │   ├── order_processing2.png
│   │   │   ├── testimonial_background.png
│   │   │   └── testimonial_background2.png
│   │   ├── mobile_responsive/
│   │   │   ├── header_collapsed.png
│   │   │   ├── header_collapsed2.png
│   │   │   ├── menu_button_states.png
│   │   │   ├── menu_button_states2.png
│   │   │   └── simplified_illustration.png
│   │   ├── navigation_ui/
│   │   │   ├── action_button_icons.png
│   │   │   ├── action_button_icons2.png
│   │   │   ├── main_navigation_icons.png
│   │   │   └── main_navigation_icons2.png
│   │   ├── product_catalog/
│   │   │   ├── brake_systems.png
│   │   │   ├── brake_systems2.png
│   │   │   ├── detail_gallery.png
│   │   │   ├── detail_gallery2.png
│   │   │   ├── electrical_systems.png
│   │   │   ├── electrical_systems2.png
│   │   │   ├── engine_components.png
│   │   │   ├── engine_components2.png
│   │   │   ├── exterior_accessories.png
│   │   │   ├── exterior_accessories2.png
│   │   │   ├── interior_accessories.png
│   │   │   ├── interior_accessories2.png
│   │   │   ├── maintenance_items.png
│   │   │   ├── maintenance_items2.png
│   │   │   ├── no_image_available.png
│   │   │   ├── no_image_available2.png
│   │   │   ├── performance_parts.png
│   │   │   ├── performance_parts2.png
│   │   │   ├── suspension_parts.png
│   │   │   ├── suspension_parts2.png
│   │   │   ├── thumbnail_template.png
│   │   │   └── thumbnail_template2.png
│   │   ├── status_notification/
│   │   │   ├── empty_fitment_catalog.png
│   │   │   ├── empty_fitment_catalog2.png
│   │   │   ├── empty_product_list.png
│   │   │   ├── empty_product_list2.png
│   │   │   ├── no_notifications.png
│   │   │   ├── no_order_history.png
│   │   │   ├── no_order_history2.png
│   │   │   ├── no_search_results.png
│   │   │   ├── status_icons.png
│   │   │   └── status_icons2.png
│   │   ├── testimonials/
│   │   │   ├── auto_repair.jpg
│   │   │   ├── citywide.jpg
│   │   │   ├── gt_performance.jpg
│   │   │   ├── midwest_auto.jpg
│   │   │   ├── pacific_auto.jpg
│   │   │   └── velocity_performance.jpg
│   │   └── vue.svg
│   ├── components/
│   │   ├── chat/
│   │   │   ├── AddMemberDialog.vue
│   │   │   ├── ChatContainer.vue
│   │   │   ├── ChatHeader.vue
│   │   │   ├── ChatInput.vue
│   │   │   ├── ChatMembers.vue
│   │   │   ├── ChatMessage.vue
│   │   │   ├── ChatMessages.vue
│   │   │   ├── ChatRoomDialog.vue
│   │   │   └── ChatRoomItem.vue
│   │   ├── common/
│   │   │   ├── ConfirmDialog.vue
│   │   │   └── NotificationSystem.vue
│   │   ├── faq/
│   │   │   └── FaqAccordion.vue
│   │   ├── layout/
│   │   │   ├── BlankLayout.vue
│   │   │   ├── DashboardFooter.vue
│   │   │   ├── DashboardLayout.vue
│   │   │   ├── MainFooter.vue
│   │   │   └── PublicLayout.vue
│   │   ├── HelloWorld.vue
│   │   └── LanguageSwitcher.vue
│   ├── i18n/
│   │   ├── locales/
│   │   │   └── en.json
│   │   └── index.ts
│   ├── router/
│   │   └── index.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── chat.ts
│   │   ├── fitment.ts
│   │   ├── fitmentProcessing.ts
│   │   ├── media.ts
│   │   ├── modelMapping.ts
│   │   ├── product.ts
│   │   └── user.ts
│   ├── stores/
│   │   └── auth.ts
│   ├── types/
│   │   ├── chat.ts
│   │   ├── fitment.ts
│   │   ├── media.ts
│   │   ├── product.ts
│   │   └── user.ts
│   ├── utils/
│   │   ├── error-handler.ts
│   │   ├── formatters.ts
│   │   └── notification.ts
│   ├── views/
│   │   ├── AboutPage.vue
│   │   ├── AccountDashboard.vue
│   │   ├── Blog.vue
│   │   ├── Careers.vue
│   │   ├── ChatPage.vue
│   │   ├── ContactPage.vue
│   │   ├── Dashboard.vue
│   │   ├── FAQ.vue
│   │   ├── FitmentCatalog.vue
│   │   ├── FitmentDetail.vue
│   │   ├── FitmentForm.vue
│   │   ├── LandingPage.vue
│   │   ├── Login.vue
│   │   ├── MediaLibrary.vue
│   │   ├── ModelMappingsManager.vue
│   │   ├── NotFound.vue
│   │   ├── OrderHistory.vue
│   │   ├── Partners.vue
│   │   ├── Pricing.vue
│   │   ├── PrivacyPolicy.vue
│   │   ├── ProductCatalog.vue
│   │   ├── ProductDetail.vue
│   │   ├── ProductFitments.vue
│   │   ├── ProductForm.vue
│   │   ├── ProductMedia.vue
│   │   ├── ResourcesPage.vue
│   │   ├── SavedLists.vue
│   │   ├── ServicesPage.vue
│   │   ├── Settings.vue
│   │   ├── ShippingReturns.vue
│   │   ├── TermsOfService.vue
│   │   ├── Testimonials.vue
│   │   ├── Unauthorized.vue
│   │   ├── UserDetail.vue
│   │   ├── UserForm.vue
│   │   ├── UserManagement.vue
│   │   └── UserProfile.vue
│   ├── App.vue
│   ├── main.ts
│   ├── style.css
│   └── vite-env.d.ts
├── README.md
├── index.html
├── package-lock.json
├── package.json
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

## Components
### AboutPage
**Path:** `src/views/AboutPage.vue`
**Type:** Composition API (script setup)

### AccountDashboard
**Path:** `src/views/AccountDashboard.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `accountMenu`: [
      { title: 'Dashboard', icon: 'mdi-view-dashboard', to: '/account/dashboard' },
      { title: 'Profile', icon: 'mdi-account', to: '/account/profile' },
      { title: 'Company Information', icon: 'mdi-domain', to: '/account/company' },
      { title: 'Payment Methods', icon: 'mdi-credit-card', to: '/account/payment-methods' },
      { title: 'Shipping Addresses', icon: 'mdi-map-marker', to: '/account/shipping-addresses' },
      { title: 'Team Members', icon: 'mdi-account-group', to: '/account/team' }
    ]
- `loading`: true
- `orderMenu`: [
      { title: 'Order History', icon: 'mdi-history', to: '/account/orders' },
      { title: 'Saved Lists', icon: 'mdi-format-list-bulleted', to: '/account/saved-lists' },
      { title: 'Quick Order', icon: 'mdi-flash', to: '/account/quick-order' },
      { title: 'Quotes & Estimates', icon: 'mdi-file-document-outline', to: '/account/quotes' },
      { title: 'Returns', icon: 'mdi-keyboard-return', to: '/account/returns' }
    ]
- `quickActions`: [
      { title: 'New Order', icon: 'mdi-cart-plus', to: '/products', color: 'primary' },
      { title: 'Quick Order', icon: 'mdi-flash', to: '/account/quick-order', color: 'secondary' },
      { title: 'Track Orders', icon: 'mdi-truck-delivery', to: '/account/orders', color: 'info' },
      { title: 'Support', icon: 'mdi-lifebuoy', to: '/account/support-tickets', color: 'error' },
      { title: 'Reorder', icon: 'mdi-refresh', to: '/account/orders?filter=reorder', color: 'success' },
      { title: 'Returns', icon: 'mdi-keyboard-return', to: '/account/returns', color: 'warning' }
    ]
- `quickStats`: [
      { title: 'Orders', value: '24', icon: 'mdi-package-variant', color: 'primary-lighten-5' },
      { title: 'Pending', value: '3', icon: 'mdi-clock-outline', color: 'warning-lighten-5' },
      { title: 'Returns', value: '1', icon: 'mdi-keyboard-return', color: 'error-lighten-5' },
      { title: 'Lists', value: '5', icon: 'mdi-format-list-bulleted', color: 'success-lighten-5' }
    ]
- `supportMenu`: [
      { title: 'Support Tickets', icon: 'mdi-lifebuoy', to: '/account/support-tickets' },
      { title: 'Downloads', icon: 'mdi-download', to: '/account/downloads' },
      { title: 'Settings', icon: 'mdi-cog', to: '/account/settings' }
    ]

#### Computed Properties
- `user`

#### Methods
- `async fetchAccountData()`
- `getOrderStatusColor()`
- `getUserInitials()`
- `isActiveRoute()`
- `logout()`
- `markAsRead()`

### AddMemberDialog
**Path:** `src/components/chat/AddMemberDialog.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| modelValue | boolean | Yes | - |
| roomId | string | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| role | - |
| update | - |
| userId | - |
| value | - |

#### Reactive State
**Refs:**
- `isSubmitting`: false
- `loadingUsers`: false
- `selectedRole`: ChatMemberRole.MEMBER

#### Methods
- `closeDialog()`
- `async loadUsers()`
- `resetForm()`
- `async submitForm()`

#### Watchers
- `() => props.modelValue`

#### Lifecycle Hooks
- `mounted`

### App
**Path:** `src/App.vue`
**Type:** Composition API

#### Computed Properties
- `layout`

### BlankLayout
**Path:** `src/components/layout/BlankLayout.vue`
**Type:** Options API

### Blog
**Path:** `src/views/Blog.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `categories`: [
      'Industry News',
      'Product Updates',
      'Technical Tips',
      'Case Studies',
      'Market Trends',
      'Company News'
    ]
- `deleteDialog`: false
- `deleteLoading`: false
- `email`: ''
- `itemsPerPage`: 5
- `loading`: true
- `page`: 1
- `privacyConsent`: false
- `searchQuery`: ''
- `sortOptions`: [
      { title: 'Newest First', value: 'newest' },
      { title: 'Oldest First', value: 'oldest' },
      { title: 'Most Popular', value: 'popular' },
      { title: 'Alphabetical', value: 'alphabetical' }
    ]
- `sortOrder`: 'newest'
- `subscribeDialog`: false
- `subscribing`: false
- `totalItems`: 0

#### Computed Properties
- `isAdmin`

#### Methods
- `applyFilters()`
- `clearSearch()`
- `confirmDelete()`
- `async deletePost()`
- `async fetchPosts()`
- `filterPosts()`
- `getCategoryCount()`
- `resetFilters()`
- `searchPosts()`
- `async subscribeNewsletter()`

### Careers
**Path:** `src/views/Careers.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `benefits`: [
      {
        title: 'Innovate & Make an Impact',
        icon: 'lightbulb',
        description: 'Work on cutting-edge technology that\'s transforming an entire industry. Your contributions will directly impact thousands of businesses and help shape the future of automotive commerce.'
      },
      {
        title: 'Collaborative & Inclusive Culture',
        icon: 'account-group',
        description: 'Join a diverse team that values different perspectives and fosters collaboration. We believe the best solutions come from combining our unique strengths and experiences.'
      },
      {
        title: 'Grow Your Career',
        icon: 'chart-line',
        description: 'We\'re committed to your professional development with clear career paths, mentorship programs, continuous learning opportunities, and regular feedback to help you reach your goals.'
      },
      {
        title: 'Work-Life Balance',
        icon: 'balance-scale',
        description: 'We believe in sustainable performance. Enjoy flexible work arrangements, generous PTO, and a culture that respects boundaries to ensure you can perform at your best.'
      },
      {
        title: 'Be Part of Something Bigger',
        icon: 'earth',
        description: 'Our platform helps reduce waste, optimize supply chains, and improve efficiency across the automotive aftermarket. Your work will contribute to more sustainable practices in a major global industry.'
      },
      {
        title: 'Competitive Compensation',
        icon: 'cash-multiple',
        description: 'We offer competitive salaries, performance bonuses, equity options for eligible positions, and a comprehensive benefits package designed to support your health and financial wellbeing.'
      }
    ]
- `companyStats`: [
      { value: '5,000+', label: 'Business Customers' },
      { value: '120+', label: 'Team Members' },
      { value: '4', label: 'Office Locations' },
      { value: '25+', label: 'Countries Served' }
    ]
- `galleryDialog`: false
- `galleryIndex`: 0
- `loading`: true
- `perks`: [
      { title: 'Health Insurance', icon: 'heart-pulse' },
      { title: 'Dental & Vision', icon: 'eye' },
      { title: '401(k

#### Computed Properties
- `departments`
- `filteredJobs`

#### Methods
- `async fetchJobs()`
- `nextImage()`
- `openGallery()`
- `prevImage()`
- `scrollToJobs()`

### ChatContainer
**Path:** `src/components/chat/ChatContainer.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `searchQuery`: ''
- `showAddMemberDialog`: false
- `showCreateRoomDialog`: false
- `showMembersPanel`: false
- `showRemoveMemberDialog`: false
- `sidebarCollapsed`: false

#### Computed Properties
- `activeRoomId`
- `currentUserId`

#### Methods
- `async addMember(userId: string, role: string)`
- `confirmRemoveMember(member: ChatMember)`
- `async createRoom(name: string, type: ChatRoomType, members: any[])`
- `deleteMessage(messageId: string)`
- `editMessage(messageId: string, content: string)`
- `handleReaction(messageId: string, reaction: string, isAdding: boolean)`
- `handleTyping(isTyping: boolean)`
- `joinRoom(roomId: string)`
- `loadMoreMessages(beforeId: string)`
- `async removeMemberConfirmed()`
- `sendMessage(content: string)`
- `toggleSidebar()`
- `async updateMemberRole(userId: string, role: string)`

#### Watchers
- `() => router.currentRoute.value.query.room`

#### Lifecycle Hooks
- `mounted`

### ChatHeader
**Path:** `src/components/chat/ChatHeader.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| onlineCount | number | Yes | - |
| room | ChatRoom | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |

#### Reactive State
**Refs:**
- `notificationLevel`: 'all'
- `showLeaveDialog`: false
- `showNotificationSettings`: false
- `showRoomInfo`: false

#### Computed Properties
- `avatarText`
- `canLeaveRoom`
- `displayName`
- `roomTypeDisplay`
- `statusText`

#### Methods
- `confirmLeaveRoom()`
- `formatDate(dateStr: string)`
- `async leaveRoom()`
- `async saveNotificationSettings()`

### ChatInput
**Path:** `src/components/chat/ChatInput.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| roomId | string | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| content | - |
| e | - |
| isTyping | - |

#### Reactive State
**Refs:**
- `isTyping`: false
- `messageText`: ''

#### Computed Properties
- `canSend`
- `fileIcon`
- `typingText`
- `typingUsers`

#### Methods
- `clearAttachment()`
- `formatFileSize(bytes: number)`
- `getMessageType(file: File)`
- `handleBlur()`
- `handleFileSelected(event: Event)`
- `handleFocus()`
- `handleInput()`
- `handleKeydown(event: KeyboardEvent)`
- `sendMessage()`
- `startTyping()`
- `stopTyping()`

#### Lifecycle Hooks
- `beforeunmount`

### ChatMembers
**Path:** `src/components/chat/ChatMembers.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| currentUserId | string | Yes | - |
| members | ChatMember[] | Yes | - |
| room | ChatRoom | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| member | - |
| role | - |
| userId | - |

#### Reactive State
**Refs:**
- `searchQuery`: ''
- `showMenu`: false

#### Computed Properties
- `currentUserRole`
- `filteredMembers`
- `offlineMembers`
- `onlineMembers`

#### Methods
- `canManageUser(member: ChatMember)`
- `getMemberInitials(name: string)`
- `getMemberRoleDisplay(role: string)`
- `isCurrentUser(member: ChatMember)`
- `removeMember(member: ChatMember)`
- `updateMemberRole(userId: string, role: string)`

### ChatMessage
**Path:** `src/components/chat/ChatMessage.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| isOwnMessage | boolean | Yes | - |
| message | ChatMessage | Yes | - |
| showSender | boolean | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| content | - |
| e | - |
| isAdding | - |
| messageId | - |
| reaction | - |

#### Reactive State
**Refs:**
- `editContent`: ''
- `isEditing`: false
- `showDeleteDialog`: false
- `showReactionMenu`: false

#### Computed Properties
- `canDelete`
- `canEdit`
- `currentUserId`
- `hasReactions`

#### Methods
- `addReaction(reaction: string)`
- `cancelEdit()`
- `confirmDelete()`
- `deleteMessage()`
- `formatTime(dateStr: string)`
- `saveEdit()`
- `startEdit()`
- `toggleReaction(reaction: string, users: string[])`

### ChatMessages
**Path:** `src/components/chat/ChatMessages.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| currentUserId | string | Yes | - |
| messages | ChatMessage[] | Yes | - |
| roomId | string | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| beforeId | - |
| content | - |
| e | - |
| isAdding | - |
| messageId | - |
| reaction | - |

#### Reactive State
**Refs:**
- `hasReachedTop`: false
- `isLoadingMore`: false
- `lastHeight`: 0
- `lastScrollTop`: 0
- `shouldScrollToBottom`: true

#### Computed Properties
- `canLoadMore`
- `typingText`
- `typingUsers`

#### Methods
- `formatDateSeparator(dateStr: string)`
- `handleDelete(messageId: string)`
- `handleEdit(messageId: string, content: string)`
- `handleReaction(messageId: string, reaction: string, isAdding: boolean)`
- `handleScroll()`
- `loadMore()`
- `restoreScrollPosition()`
- `scrollToBottom()`
- `shouldShowDateSeparator(message: ChatMessage, index: number)`
- `shouldShowSender(message: ChatMessage, index: number)`

#### Lifecycle Hooks
- `mounted`
- `updated`

### ChatPage
**Path:** `src/views/ChatPage.vue`
**Type:** Composition API (script setup)

#### Lifecycle Hooks
- `beforeunmount`
- `mounted`

### ChatRoomDialog
**Path:** `src/components/chat/ChatRoomDialog.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| modelValue | boolean | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| members | - |
| name | - |
| type | - |
| update | - |
| value | - |

#### Reactive State
**Refs:**
- `isSubmitting`: false
- `loadingUsers`: false
- `roomName`: ''
- `roomType`: ChatRoomType.GROUP

#### Methods
- `closeDialog()`
- `async loadUsers()`
- `resetForm()`
- `async submitForm()`

#### Watchers
- `() => props.modelValue`

#### Lifecycle Hooks
- `mounted`

### ChatRoomItem
**Path:** `src/components/chat/ChatRoomItem.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| active | boolean | Yes | - |
| room | ChatRoom | Yes | - |

#### Computed Properties
- `avatarText`
- `displayName`
- `formattedTime`
- `messagePreview`

#### Methods
- `getOtherUserName()`

### ConfirmDialog
**Path:** `src/components/common/ConfirmDialog.vue`
**Type:** Composition API (script setup)

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| Boolean | Any | No | - |
| String | Any | No | - |
| cancelText | String | No | 'Cancel' |
| dangerConfirm | Boolean | No | false |
| message | String | No | 'Are you sure you want to proceed?' |
| modelValue | Boolean | Yes | - |

#### Emits
| Event | Payload |
| ----- | ------- |
| e | - |
| update | - |
| value | - |

#### Reactive State
**Refs:**
- `isLoading`: false

#### Methods
- `cancel()`
- `confirm()`

#### Watchers
- `() => props.dangerConfirm`

### ContactPage
**Path:** `src/views/ContactPage.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `formSubmitting`: false
- `formValid`: false
- `newsletterEmail`: ''
- `newsletterSubmitting`: false
- `referenceNumber`: ''
- `showSuccessDialog`: false

**Reactive Objects:**
- `formData`: {
      company: '',
      businessType: '',
      name: '',
      title: '',
      email: '',
      phone: '',
      inquiryType: '',
      message: ''
    }

#### Methods
- `async submitForm()`
- `async subscribeNewsletter()`

### Dashboard
**Path:** `src/views/Dashboard.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activities`: [
      {
        title: 'New product added: Brake Pads X500',
        timestamp: new Date(Date.now(
- `loading`: false
- `quickActions`: [
      {
        title: 'Add Product',
        icon: 'mdi-plus-circle',
        link: '/products/new'
      },
      {
        title: 'Add Fitment',
        icon: 'mdi-car-plus',
        link: '/fitments/new'
      },
      {
        title: 'Upload Media',
        icon: 'mdi-cloud-upload',
        link: '/media/upload'
      },
      {
        title: 'Search',
        icon: 'mdi-magnify',
        link: '/search'
      },
      {
        title: 'Reports',
        icon: 'mdi-chart-bar',
        link: '/reports'
      },
      {
        title: 'Settings',
        icon: 'mdi-cog',
        link: '/settings'
      }
    ]
- `stats`: [
      {
        title: 'Products',
        subtitle: 'Total products in catalog',
        value: '0',
        icon: 'mdi-package-variant-closed',
        color: 'primary',
        link: '/products'
      },
      {
        title: 'Fitments',
        subtitle: 'Vehicle compatibility',
        value: '0',
        icon: 'mdi-car',
        color: 'success',
        link: '/fitments'
      },
      {
        title: 'Media',
        subtitle: 'Images and documents',
        value: '0',
        icon: 'mdi-image-multiple',
        color: 'info',
        link: '/media'
      },
      {
        title: 'Users',
        subtitle: 'Active accounts',
        value: '0',
        icon: 'mdi-account-group',
        color: 'warning',
        link: '/users'
      }
    ]

#### Methods
- `async fetchDashboardData()`
- `refreshData()`

### DashboardFooter
**Path:** `src/components/layout/DashboardFooter.vue`
**Type:** Composition API

### DashboardLayout
**Path:** `src/components/layout/DashboardLayout.vue`
**Type:** Composition API

#### Methods
- `async initializeAuth()`
- `logout()`

### FAQ
**Path:** `src/views/FAQ.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'all'
- `loading`: true
- `searchQuery`: ''

#### Computed Properties
- `isAdmin`

#### Methods
- `async fetchFaqs()`
- `getFaqsByCategory()`
- `openLiveChat()`
- `searchFaqs()`

### FaqAccordion
**Path:** `src/components/faq/FaqAccordion.vue`
**Type:** Composition API

#### Props
| Prop | Type | Required | Default |
| ---- | ---- | -------- | ------- |
| faqs | Array | Yes | - |

#### Reactive State
**Refs:**
- `deleteDialog`: false
- `deleteLoading`: false

#### Methods
- `confirmDelete()`
- `async copyLink()`
- `async deleteFaq()`
- `formatAnswer()`
- `async submitFeedback()`

### FitmentCatalog
**Path:** `src/views/FitmentCatalog.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `deleteDialog`: false
- `deleteLoading`: false
- `itemsPerPage`: 10
- `loading`: false
- `page`: 1
- `totalItems`: 0
- `totalPages`: 1

#### Computed Properties
- `isAdmin`

#### Methods
- `confirmDelete()`
- `async deleteFitment()`
- `async fetchFitments()`
- `resetFilters()`

### FitmentDetail
**Path:** `src/views/FitmentDetail.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `addProductLoading`: false
- `deleteDialog`: false
- `deleteLoading`: false
- `loading`: true
- `productsLoading`: false
- `removeProductDialog`: false
- `removeProductLoading`: false
- `showAddProductDialog`: false

#### Computed Properties
- `isAdmin`

#### Methods
- `async addProduct()`
- `confirmDelete()`
- `confirmRemoveProduct()`
- `async deleteFitment()`
- `async fetchAvailableProducts()`
- `async fetchFitment()`
- `async fetchProducts()`
- `async fetchSimilarFitments()`
- `async removeProductAssociation()`

### FitmentForm
**Path:** `src/views/FitmentForm.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `formDirty`: false
- `formError`: ''
- `initialLoading`: false
- `isFormValid`: false
- `loading`: false
- `partApplications`: ''
- `processingApplications`: false
- `productId`: ''
- `showProcessingInfo`: false
- `showUnsavedDialog`: false

#### Methods
- `addAttribute()`
- `clearError()`
- `discardChanges()`
- `async fetchAssociatedProducts()`
- `async fetchFitment()`
- `navigationGuard()`
- `objectToAttributes()`
- `async processPartApplications()`
- `removeAttribute()`
- `async submitForm()`

### HelloWorld
**Path:** `src/components/HelloWorld.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `count`: 0

### LandingPage
**Path:** `src/views/LandingPage.vue`
**Type:** Composition API (script setup)

#### Methods
- `goToCategory()`

### LanguageSwitcher
**Path:** `src/components/LanguageSwitcher.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `currentLocale`: locale.value

#### Methods
- `async changeLocale()`

#### Lifecycle Hooks
- `mounted`

### Login
**Path:** `src/views/Login.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `password`: ''
- `rememberMe`: true
- `showPassword`: false
- `username`: ''

#### Computed Properties
- `loading`

#### Methods
- `async login()`

### MainFooter
**Path:** `src/components/layout/MainFooter.vue`
**Type:** Composition API

### MediaLibrary
**Path:** `src/views/MediaLibrary.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `associateForm`: {
      product_id: null as string | null
    }
- `associateLoading`: false
- `batchDeleteLoading`: false
- `dateMenu`: false
- `deleteLoading`: false
- `editForm`: {
      filename: '',
      alt_text: '',
      description: '',
      product_id: null as string | null
    }
- `editLoading`: false
- `fileTypeOptions`: [
      { title: 'All Files', value: 'all' },
      { title: 'Images', value: 'image' },
      { title: 'Documents', value: 'document' }
    ]
- `headers`: [
      { title: 'Filename', key: 'filename', sortable: true },
      { title: 'Type', key: 'mime_type', sortable: true },
      { title: 'Size', key: 'size', sortable: true },
      { title: 'Uploaded', key: 'created_at', sortable: true },
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]
- `isDragging`: false
- `isEditFormValid`: true
- `loading`: true
- `page`: 1
- `pageSize`: 20
- `search`: ''
- `showAdvancedFilters`: false
- `showAssociateDialog`: false
- `showBatchDeleteDialog`: false
- `showDeleteDialog`: false
- `showEditDialog`: false
- `showPreviewDialog`: false
- `showUploadDialog`: false
- `sortOption`: 'newest'
- `sortOptions`: [
      { title: 'Newest First', value: 'newest' },
      { title: 'Oldest First', value: 'oldest' },
      { title: 'Name A-Z', value: 'name_asc' },
      { title: 'Name Z-A', value: 'name_desc' },
      { title: 'Size (Largest
- `totalPages`: 1
- `uploadForm`: {
      product_id: null as string | null
    }
- `uploadProgress`: 0
- `uploading`: false

#### Computed Properties
- `dateRangeText`
- `documentCount`
- `hasSelectedWithProducts`
- `imageCount`
- `totalSize`

#### Methods
- `addFileToUpload()`
- `applyClientSideFilters()`
- `applyFilters()`
- `associateWithProduct()`
- `batchAssociateProduct()`
- `async batchDeleteMedia()`
- `bulkDownload()`
- `cancelUpload()`
- `clearDateRange()`
- `async confirmAssociate()`
- `confirmBatchDelete()`
- `confirmDeleteFromPreview()`
- `confirmDeleteMedia()`
- `async deleteMedia()`
- `downloadMedia()`
- `editFromPreview()`
- `editMedia()`
- `async fetchMedia()`
- `async fetchProductOptions()`
- `async fetchRecentUploads()`
- `handleFileDrop()`
- `handleFileSelect()`
- `openMediaPreview()`
- `removeFileFromUpload()`
- `resetFilters()`
- `async saveMediaEdit()`
- `toggleSelect()`
- `async uploadFiles()`

### ModelMappingsManager
**Path:** `src/views/ModelMappingsManager.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `currentPage`: 1
- `debug`: true
- `deleteDialog`: false
- `deletingMapping`: false
- `editMode`: false
- `filters`: {
      pattern: '',
    }
- `initialLoading`: true
- `itemsPerPage`: 10
- `loading`: false
- `mappingDialog`: false
- `savingMapping`: false
- `totalMappings`: 0
- `uploading`: false

#### Methods
- `applyFilter()`
- `confirmDelete()`
- `async deleteMapping()`
- `editMapping()`
- `async loadMappings()`
- `async refreshMappings()`
- `async saveMapping()`
- `saveMappingForm()`
- `showAddMappingDialog()`
- `async toggleActive()`
- `async uploadMappings()`

### NotFound
**Path:** `src/views/NotFound.vue`
**Type:** Composition API (script setup)

#### Methods
- `goBack()`

### NotificationSystem
**Path:** `src/components/common/NotificationSystem.vue`
**Type:** Composition API

#### Computed Properties
- `notifications`

#### Methods
- `closeNotification()`
- `getVariant()`

### OrderHistory
**Path:** `src/views/OrderHistory.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `cancellationReasons`: [
      'Ordered by mistake',
      'Found better price elsewhere',
      'Taking too long to ship',
      'Changed my mind',
      'Incorrect item(s
- `dateRange`: {
      from: '',
      to: ''
    }
- `itemsPerPage`: 10
- `loading`: true
- `orderStatuses`: [
      'Pending',
      'Processing',
      'Shipped',
      'Delivered',
      'Cancelled',
      'On Hold',
      'Backordered'
    ]
- `orderTypes`: [
      'Standard',
      'Rush',
      'Dropship',
      'Backorder',
      'Will Call'
    ]
- `page`: 1
- `paymentMethods`: [
      'Credit Card',
      'Purchase Order',
      'Net 30',
      'ACH Transfer',
      'Wire Transfer'
    ]
- `search`: ''
- `showAdvancedFilters`: false
- `tableHeaders`: [
      { title: 'Order #', key: 'order_number', sortable: true },
      { title: 'Date', key: 'order_date', sortable: true },
      { title: 'Total', key: 'total', sortable: true },
      { title: 'Status', key: 'status', sortable: true },
      { title: 'Shipping', key: 'shipping', sortable: false },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]

#### Computed Properties
- `filteredOrders`
- `paginatedMobileOrders`

#### Methods
- `applyFilters()`
- `canCancel()`
- `canReturn()`
- `cancelOrder()`
- `async confirmCancelOrder()`
- `downloadInvoice()`
- `exportToExcel()`
- `exportToPdf()`
- `async fetchOrders()`
- `getStatusColor()`
- `getTrackingUrl()`
- `printOrders()`
- `async reorder()`
- `resetFilters()`

### Partners
**Path:** `src/views/Partners.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'manufacturers'
- `techTab`: 'all'

#### Methods
- `filteredTechPartners()`

### Pricing
**Path:** `src/views/Pricing.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `additionalServices`: [
      {
        title: 'Data Migration & Setup',
        description: 'Our team will help migrate your existing product data, customer information, and historical orders into Crown Nexus to ensure a smooth transition.',
        image: 'https://via.placeholder.com/600x400?text=Data+Migration',
        link: '/services/data-migration'
      },
      {
        title: 'Custom Integration Development',
        description: 'Need to connect Crown Nexus with your ERP, CRM, or other business systems? Our developers can build custom integrations tailored to your specific requirements.',
        image: 'https://via.placeholder.com/600x400?text=Custom+Integration',
        link: '/services/custom-integration'
      },
      {
        title: 'Training & Implementation',
        description: 'Comprehensive training for your team to ensure everyone knows how to leverage Crown Nexus effectively. Includes personalized implementation support.',
        image: 'https://via.placeholder.com/600x400?text=Training',
        link: '/services/training'
      }
    ]
- `billingPeriod`: 'monthly'
- `faqs`: [
      {
        question: 'Can I upgrade or downgrade my plan later?',
        answer: 'Yes, you can upgrade your plan at any time, and the new pricing will be prorated for the remainder of your billing cycle. Downgrades take effect at the start of your next billing cycle.'
      },
      {
        question: 'What happens if I exceed my plan limits?',
        answer: 'If you exceed your plan limits (such as number of users or SKUs
- `growthDistributorBenefits`: [
      {
        icon: 'mdi-chart-line',
        title: 'Scalable Pricing',
        description: 'Pricing that grows with your business with predictable costs'
      },
      {
        icon: 'mdi-book-open-variant',
        title: 'Training & Onboarding',
        description: 'Comprehensive training program to get your team up to speed quickly'
      },
      {
        icon: 'mdi-tools',
        title: 'Business Development Tools',
        description: 'Access to tools and resources designed to help you grow your customer base'
      },
      {
        icon: 'mdi-account-group',
        title: 'Community Access',
        description: 'Join our distributor community for networking and knowledge sharing'
      },
      {
        icon: 'mdi-star',
        title: 'Pathway to Partner Program',
        description: 'Clear criteria and support to advance to our Partner Distributor Program'
      }
    ]
- `partnerDistributorBenefits`: [
      {
        icon: 'mdi-cash-multiple',
        title: 'Preferential Pricing',
        description: 'Access to wholesale pricing with volume-based discounts'
      },
      {
        icon: 'mdi-database',
        title: 'Enhanced Product Data',
        description: 'Premium access to comprehensive fitment data and rich product content'
      },
      {
        icon: 'mdi-api',
        title: 'Integration APIs',
        description: 'Enterprise-level API access for seamless integration with your existing systems'
      },
      {
        icon: 'mdi-account-tie',
        title: 'Dedicated Account Manager',
        description: 'Personal support from a dedicated account manager for your business'
      },
      {
        icon: 'mdi-handshake',
        title: 'Co-Marketing Opportunities',
        description: 'Joint marketing initiatives and promotional opportunities'
      }
    ]
- `plans`: [
      {
        id: 'starter',
        name: 'Starter',
        subtitle: 'For small businesses and startups',
        monthlyPrice: 249,
        annualPrice: 212, // 15% discount
        buttonText: 'Get Started',
        highlighted: false,
        features: [
          { text: 'Up to 3 users', included: true },
          { text: 'Product catalog management', included: true },
          { text: 'Basic fitment data', included: true },
          { text: '5,000 SKUs', included: true },
          { text: 'Standard support', included: true },
          { text: 'Inventory management', included: true },
          { text: 'Order processing', included: true },
          { text: 'Customer management', included: true },
          { text: 'Advanced analytics', included: false },
          { text: 'API access', included: false },
          { text: 'Custom branding', included: false },
          { text: 'Dedicated account manager', included: false }
        ]
      },
      {
        id: 'professional',
        name: 'Professional',
        subtitle: 'For growing businesses',
        monthlyPrice: 499,
        annualPrice: 424, // 15% discount
        buttonText: 'Get Started',
        highlighted: true,
        features: [
          { text: 'Up to 10 users', included: true },
          { text: 'Product catalog management', included: true },
          { text: 'Premium fitment data', included: true },
          { text: '25,000 SKUs', included: true },
          { text: 'Priority support', included: true },
          { text: 'Inventory management', included: true },
          { text: 'Order processing', included: true },
          { text: 'Customer management', included: true },
          { text: 'Advanced analytics', included: true },
          { text: 'API access', included: true },
          { text: 'Custom branding', included: true },
          { text: 'Dedicated account manager', included: false }
        ]
      },
      {
        id: 'enterprise',
        name: 'Enterprise',
        subtitle: 'For large organizations',
        monthlyPrice: 999,
        annualPrice: 849, // 15% discount
        buttonText: 'Contact Sales',
        highlighted: false,
        features: [
          { text: 'Unlimited users', included: true },
          { text: 'Product catalog management', included: true },
          { text: 'Premium fitment data', included: true },
          { text: 'Unlimited SKUs', included: true },
          { text: '24/7 premium support', included: true },
          { text: 'Inventory management', included: true },
          { text: 'Order processing', included: true },
          { text: 'Customer management', included: true },
          { text: 'Advanced analytics', included: true },
          { text: 'API access', included: true },
          { text: 'Custom branding', included: true },
          { text: 'Dedicated account manager', included: true }
        ]
      }
    ]
- `volumeTiers`: [
      {
        volume: '1-500 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '0%',
        discountedRate: '$2.50 per transaction'
      },
      {
        volume: '501-2,000 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '10%',
        discountedRate: '$2.25 per transaction'
      },
      {
        volume: '2,001-5,000 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '20%',
        discountedRate: '$2.00 per transaction'
      },
      {
        volume: '5,001-10,000 transactions/month',
        standardRate: '$2.50 per transaction',
        discount: '30%',
        discountedRate: '$1.75 per transaction'
      },
      {
        volume: '10,001+ transactions/month',
        standardRate: '$2.50 per transaction',
        discount: 'Custom',
        discountedRate: 'Contact Sales'
      }
    ]

#### Computed Properties
- `isMobile`

### PrivacyPolicy
**Path:** `src/views/PrivacyPolicy.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `sections`: [
      {
        id: 'introduction',
        title: '1. Introduction',
        content: `
          <p>Crown Nexus ("we," "our," or "us"

#### Methods
- `printPolicy()`
- `scrollToSection()`

### ProductCatalog
**Path:** `src/views/ProductCatalog.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `attributeFilter`: ''
- `deleteDialog`: false
- `deleteLoading`: false
- `itemsPerPage`: 10
- `loading`: false
- `page`: 1
- `search`: ''
- `showAdvancedFilters`: false
- `totalItems`: 0
- `totalPages`: 1

#### Computed Properties
- `isAdmin`

#### Methods
- `confirmDelete()`
- `async deleteProduct()`
- `async fetchCategories()`
- `async fetchProducts()`
- `resetFilters()`

### ProductDetail
**Path:** `src/views/ProductDetail.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `currentMediaIndex`: 0
- `deleteDialog`: false
- `deleteLoading`: false
- `loading`: true
- `mediaDialog`: false

#### Computed Properties
- `isAdmin`
- `productId`

#### Methods
- `confirmDelete()`
- `async deleteProduct()`
- `async fetchFitments()`
- `async fetchMedia()`
- `async fetchProduct()`
- `openMediaDialog()`

### ProductFitments
**Path:** `src/views/ProductFitments.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `addFilters`: {
      year: null as number | null,
      make: null as string | null,
      model: null as string | null,
      search: ''
    }
- `bulkLoading`: false
- `initialLoading`: true
- `loading`: false
- `page`: 1
- `pageSize`: 10
- `removeLoading`: false
- `removeMultipleLoading`: false
- `search`: ''
- `searchLoading`: false
- `searchPerformed`: false
- `showAddDialog`: false
- `showBulkDialog`: false
- `showRemoveDialog`: false
- `showRemoveMultipleDialog`: false
- `totalPages`: 1

#### Computed Properties
- `availableYears`
- `estimatedBulkCount`
- `productId`
- `totalFitments`
- `uniqueModels`
- `yearRange`

#### Methods
- `async addFitment()`
- `async bulkAddFitments()`
- `confirmRemoveSelected()`
- `confirmRemoveSingle()`
- `async fetchAvailableMakes()`
- `async fetchAvailableModels()`
- `async fetchAvailableYears()`
- `async fetchFitments()`
- `async fetchProduct()`
- `filterFitments()`
- `paginate()`
- `async removeFitment()`
- `async removeSelectedFitments()`
- `async searchFitments()`

### ProductForm
**Path:** `src/views/ProductForm.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `formDirty`: false
- `formError`: ''
- `initialLoading`: false
- `isFormValid`: false
- `loading`: false
- `showUnsavedDialog`: false

#### Methods
- `addAttribute()`
- `clearError()`
- `discardChanges()`
- `async fetchCategories()`
- `async fetchProduct()`
- `navigationGuard()`
- `objectToAttributes()`
- `removeAttribute()`
- `async submitForm()`

### ProductMedia
**Path:** `src/views/ProductMedia.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `deleteLoading`: false
- `editForm`: {
      filename: '',
      alt_text: '',
      description: ''
    }
- `editLoading`: false
- `initialLoading`: true
- `isDragging`: false
- `isEditFormValid`: true
- `reorderLoading`: false
- `showDeleteDialog`: false
- `showEditDialog`: false
- `showPreviewDialog`: false
- `showReorderDialog`: false
- `showUploadDialog`: false
- `uploadProgress`: 0
- `uploading`: false

#### Computed Properties
- `documentCount`
- `primaryMedia`
- `productId`

#### Methods
- `addFileToUpload()`
- `cancelUpload()`
- `confirmDeleteMedia()`
- `async deleteMedia()`
- `editMedia()`
- `async fetchMedia()`
- `async fetchProduct()`
- `handleFileDrop()`
- `handleFileSelect()`
- `openMediaPreview()`
- `removeFileFromUpload()`
- `async saveMediaEdit()`
- `async saveMediaOrder()`
- `async setPrimaryMedia()`
- `async uploadFiles()`

### PublicLayout
**Path:** `src/components/layout/PublicLayout.vue`
**Type:** Options API

### ResourcesPage
**Path:** `src/views/ResourcesPage.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'installation'
- `currentCategory`: 'all'
- `dateFilter`: ''
- `resourceTypeFilter`: ''
- `searchQuery`: ''
- `subscribeEmail`: ''
- `subscribeLoading`: false

#### Computed Properties
- `filteredResources`
- `getCurrentCategory`

#### Methods
- `downloadResource()`
- `getTechLibDocs()`
- `navigateTo()`
- `resetFilters()`
- `searchResources()`
- `subscribeToResources()`
- `viewDocument()`

### SavedLists
**Path:** `src/views/SavedLists.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `listLoading`: false
- `listTypes`: [
      'Standard',
      'Favorites',
      'Reorder',
      'Wishlist',
      'Seasonal',
      'Regular Stock'
    ]
- `loading`: true
- `permissionLevels`: [
      'View',
      'Edit',
      'Full Access'
    ]
- `productSearch`: ''
- `productSearchHeaders`: [
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Availability', key: 'in_stock', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]
- `quickOrderHeaders`: [
      { title: 'Product', key: 'product_name', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Subtotal', key: 'subtotal', sortable: true },
      { title: 'Status', key: 'status', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]
- `quickOrderLoading`: false
- `quickOrderText`: ''
- `searchLoading`: false
- `showAddProductsDialog`: false
- `tableHeaders`: [
      { title: 'Product', key: 'product', sortable: false },
      { title: 'Price', key: 'price', sortable: true },
      { title: 'Quantity', key: 'quantity', sortable: false },
      { title: 'Subtotal', key: 'subtotal', sortable: true },
      { title: 'Status', key: 'in_stock', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false, align: 'end' }
    ]

#### Computed Properties
- `hasSelectedProducts`
- `hasValidQuickOrderItems`
- `isShareButtonDisabled`

#### Methods
- `async addAllQuickOrderToCart()`
- `async addAllToCart()`
- `async addProductToList()`
- `addSelectedProducts()`
- `async addToCart()`
- `calculateListTotal()`
- `confirmDeleteList()`
- `async copyShareLink()`
- `createNewList()`
- `async deleteList()`
- `async exportList()`
- `async fetchSavedLists()`
- `getListTypeColor()`
- `getStatusColor()`
- `getStatusText()`
- `async processQuickOrder()`
- `async removeFromList()`
- `renameList()`
- `async saveList()`
- `saveQuickOrderAsList()`
- `async saveQuickOrderList()`
- `async searchProducts()`
- `shareList()`
- `async submitShare()`
- `async toggleFavorite()`
- `async updateQuantity()`
- `viewList()`

### ServicesPage
**Path:** `src/views/ServicesPage.vue`
**Type:** Composition API

### Settings
**Path:** `src/views/Settings.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeIntegrationTab`: 'api'
- `activeSection`: 'general'
- `clearingCache`: false
- `creatingBackup`: false
- `emailSettings`: {
      smtp_host: 'smtp.example.com',
      smtp_port: 587,
      smtp_username: 'username',
      smtp_password: 'password',
      smtp_encryption: true,
      from_email: 'noreply@crownnexus.com',
      from_name: 'Crown Nexus',
      email_template: 'default'
    }
- `generalSettings`: {
      company_name: 'Crown Nexus',
      currency: 'USD',
      date_format: 'MM/DD/YYYY',
      timezone: 'America/New_York',
      language: 'en',
      items_per_page: 20
    }
- `integrationSettings`: {
      api_enabled: true,
      api_url: 'https://api.crownnexus.com/v1',
      api_rate_limit: 100,
      api_key: 'sk_live_example123456789abcdef',
      webhooks_enabled: false,
      crm_provider: 'none' as 'none' | 'salesforce' | 'hubspot' | 'zoho' | 'dynamics',
      crm_api_key: '',
      crm_instance_url: '',
      crm_sync_customers: false,
      crm_sync_products: false
    }
- `isEmailFormValid`: true
- `isGeneralFormValid`: true
- `isUserSettingsFormValid`: true
- `rebuildingSearch`: false
- `savingEmail`: false
- `savingGeneral`: false
- `savingIntegration`: false
- `savingSystem`: false
- `savingTheme`: false
- `savingUserSettings`: false
- `sendingTestEmail`: false
- `systemInfo`: {
      version: '1.5.2',
      last_updated: new Date(Date.now(
- `systemSettings`: {
      maintenance_mode: false,
      maintenance_message: 'The system is currently undergoing scheduled maintenance. Please check back later.',
      log_level: 'info' as 'debug' | 'info' | 'warning' | 'error' | 'critical',
      auto_backup: true,
      backup_frequency: 'daily' as 'daily' | 'weekly' | 'monthly',
      backup_retention: 30
    }
- `testEmailAddress`: ''
- `testingCrm`: false
- `themeSettings`: {
      mode: 'light' as 'light' | 'dark' | 'system',
      primary_color: '#1976D2',
      secondary_color: '#424242'
    }
- `userSettings`: {
      require_strong_password: true,
      password_expiry_days: 90,
      enable_2fa: false,
      session_timeout: 30,
      registration_mode: 'closed' as 'closed' | 'approval' | 'open',
      default_role: UserRole.CLIENT
    }

#### Methods
- `addWebhook()`
- `async clearSystemCache()`
- `copyApiKey()`
- `async createBackup()`
- `downloadLogs()`
- `goToApiKeyManager()`
- `async rebuildSearch()`
- `async regenerateApiKey()`
- `removeWebhook()`
- `async saveEmailSettings()`
- `async saveGeneralSettings()`
- `async saveIntegrationSettings()`
- `async saveSystemSettings()`
- `async saveThemeSettings()`
- `async saveUserSettings()`
- `async sendTestEmail()`
- `async testCrmConnection()`
- `async testWebhook()`

### ShippingReturns
**Path:** `src/views/ShippingReturns.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activeTab`: 'shipping'
- `carriers`: [
      { name: 'FedEx', logo: 'https://via.placeholder.com/150x80?text=FedEx' },
      { name: 'UPS', logo: 'https://via.placeholder.com/150x80?text=UPS' },
      { name: 'USPS', logo: 'https://via.placeholder.com/150x80?text=USPS' },
      { name: 'DHL', logo: 'https://via.placeholder.com/150x80?text=DHL' },
      { name: 'XPO Logistics', logo: 'https://via.placeholder.com/150x80?text=XPO' },
      { name: 'Old Dominion', logo: 'https://via.placeholder.com/150x80?text=Old+Dominion' },
      { name: 'R+L Carriers', logo: 'https://via.placeholder.com/150x80?text=R%2BL' },
      { name: 'YRC Freight', logo: 'https://via.placeholder.com/150x80?text=YRC' }
    ]
- `commonQuestions`: [
      {
        question: 'How can I track my shipment?',
        answer: 'You can track your shipment in several ways:<br><br>1. Log into your Crown Nexus account and go to the "Orders" section<br>2. Click on the specific order to view tracking information<br>3. Click the tracking number to be redirected to the carrier\'s tracking page<br><br>You will also receive automated email updates with tracking information when your order ships and at key points during transit.'
      },
      {
        question: 'What if my shipment is damaged or items are missing?',
        answer: 'If you receive a damaged shipment or discover missing items:<br><br>1. Document the damage with photos before unpacking further<br>2. Note any damage on the delivery receipt when signing for the package<br>3. Contact our customer service team within 24 hours at 1-800-987-6543<br>4. Keep all original packaging materials until the claim is resolved<br><br>For missing items, please verify against the packing slip and contact customer service with the order number and details of the missing items.'
      },
      {
        question: 'Can I change my shipping address after placing an order?',
        answer: 'Address changes may be possible if the order has not yet been processed for shipping:<br><br>1. Log into your account and check your order status<br>2. If the status is "Processing" or earlier, contact customer service immediately<br>3. For orders already shipped, we cannot change the destination address<br>4. In some cases, we may be able to recall a package, but additional fees will apply<br><br>To avoid delivery issues, always verify your shipping address before completing your order.'
      },
      {
        question: 'What is your policy for partial shipments?',
        answer: 'Crown Nexus may split large orders into multiple shipments to ensure you receive available items as quickly as possible:<br><br>• You will not be charged extra shipping for partial shipments<br>• Each shipment will have its own tracking number<br>• You\'ll receive notification emails for each partial shipment<br>• Backordered items will ship as they become available<br><br>If you prefer to receive all items in a single shipment, please specify "Ship Complete" in the order notes during checkout or contact customer service.'
      },
      {
        question: 'How do I request a return for an incorrect item?',
        answer: 'If you received an incorrect item:<br><br>1. Contact customer service within 5 business days of receipt<br>2. Provide your order number and details about the incorrect item<br>3. We will issue an RMA and return shipping label at no cost to you<br>4. The correct item will be shipped as soon as possible<br>5. You are not responsible for restocking fees when we ship incorrect items<br><br>Please do not return items without an RMA number as this will delay processing and resolution.'
      }
    ]
- `customSolutions`: [
      {
        title: 'Dedicated Freight Program',
        subtitle: 'For high-volume customers with regular shipping needs',
        icon: 'truck-check'
      },
      {
        title: 'Cross-Dock Services',
        subtitle: 'Consolidate multiple shipments for more efficient delivery',
        icon: 'forklift'
      },
      {
        title: 'Just-In-Time Delivery',
        subtitle: 'Scheduled deliveries to support lean inventory management',
        icon: 'clock-time-five'
      },
      {
        title: 'Customized Packaging',
        subtitle: 'Special packaging solutions for unique product requirements',
        icon: 'package-variant'
      },
      {
        title: 'Managed Transportation',
        subtitle: 'Let our logistics team manage your entire shipping process',
        icon: 'truck-delivery'
      }
    ]
- `customsDocuments`: [
      {
        name: 'Commercial Invoice',
        description: 'Official document that details the sale transaction between seller and buyer, including item descriptions, quantities, and values.',
        requiredFor: 'All international shipments'
      },
      {
        name: 'Packing List',
        description: 'Detailed list of all items in the shipment, including quantities, weights, and dimensions.',
        requiredFor: 'All international shipments'
      },
      {
        name: 'Certificate of Origin',
        description: 'Document certifying the country where the goods were manufactured or produced.',
        requiredFor: 'Shipments to countries with preferential trade agreements'
      },
      {
        name: 'Shipper\'s Letter of Instruction',
        description: 'Detailed instructions from the shipper to the carrier about how to handle the shipment.',
        requiredFor: 'Most international shipments'
      },
      {
        name: 'Dangerous Goods Declaration',
        description: 'Document required for shipping hazardous materials, detailing the nature of the goods and safety precautions.',
        requiredFor: 'Shipments containing hazardous materials'
      },
      {
        name: 'Import License',
        description: 'Government-issued permit allowing the importation of specific goods into the destination country.',
        requiredFor: 'Certain restricted items in specific countries'
      }
    ]
- `expeditedOptions`: [
      {
        title: 'Same-Day Delivery',
        timing: 'Delivery within hours',
        color: 'error',
        icon: 'clock-fast',
        description: 'For critical parts needs, we offer same-day delivery service in select metro areas. Orders must be placed before 10 AM local time.',
        details: [
          { icon: 'mdi-map-marker', text: 'Available in major metro areas' },
          { icon: 'mdi-currency-usd', text: 'Premium pricing applies' },
          { icon: 'mdi-truck-fast', text: 'Direct courier delivery' },
          { icon: 'mdi-phone', text: 'Call for availability' }
        ]
      },
      {
        title: 'Next-Day Air',
        timing: 'Delivery by 10:30 AM next business day',
        color: 'warning',
        icon: 'airplane',
        description: 'Our premium overnight service guarantees delivery by 10:30 AM the next business day to most locations in the continental US.',
        details: [
          { icon: 'mdi-calendar-clock', text: 'Order by 4 PM EST for next-day delivery' },
          { icon: 'mdi-map', text: 'Available to most US locations' },
          { icon: 'mdi-truck-check', text: 'Full tracking and delivery confirmation' },
          { icon: 'mdi-account-check', text: 'Signature required on delivery' }
        ]
      }
    ]
- `freightGuidelines`: [
      'Orders over 150 lbs typically ship via freight',
      'Standard delivery is dock-to-dock',
      'Inside delivery available for additional fee',
      'Lift gate service available for locations without loading docks',
      'Freight shipments require a delivery appointment',
      'Inspection required at time of delivery'
    ]
- `internationalRegions`: [
      {
        name: 'North America',
        icon: 'earth',
        countries: ['Canada', 'Mexico']
      },
      {
        name: 'Latin America',
        icon: 'earth',
        countries: ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru', 'Panama']
      },
      {
        name: 'Europe',
        icon: 'earth',
        countries: ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 'Sweden']
      },
      {
        name: 'Asia Pacific',
        icon: 'earth',
        countries: ['Australia', 'Japan', 'South Korea', 'Singapore', 'Thailand', 'New Zealand']
      },
      {
        name: 'Middle East',
        icon: 'earth',
        countries: ['United Arab Emirates', 'Saudi Arabia', 'Qatar']
      },
      {
        name: 'Africa',
        icon: 'earth',
        countries: ['South Africa', 'Egypt', 'Morocco']
      }
    ]
- `internationalReturns`: [
      {
        title: 'International Return Process',
        description: 'Our international returns process is designed to make cross-border returns as smooth as possible:',
        points: [
          'Standard 30-day return window applies to international orders',
          'Return shipping costs are the responsibility of the customer unless the item is defective',
          'All returns require an RMA number before shipping',
          'Return shipping method should match or be slower than the original shipping method',
          'Customer is responsible for all duties and taxes on return shipments'
        ]
      },
      {
        title: 'Customs Documentation for Returns',
        description: 'Proper documentation is crucial for international returns to clear customs efficiently:',
        points: [
          'Mark packages as "Return of Goods" or "Warranty Return" as appropriate',
          'Include commercial invoice stating "No Commercial Value - Returned Goods"',
          'Reference the original order number and RMA number on all documents',
          'Include copy of original commercial invoice if available',
          'Declare actual value for customs purposes (even for warranty returns
- `internationalShippingMethods`: [
      {
        name: 'Economy International',
        delivery: '7-14 business days',
        bestFor: 'Non-urgent shipments and budget-conscious customers',
        tracking: true
      },
      {
        name: 'Standard International',
        delivery: '5-10 business days',
        bestFor: 'Regular international shipments with balanced cost and speed',
        tracking: true
      },
      {
        name: 'Expedited International',
        delivery: '3-5 business days',
        bestFor: 'Time-sensitive shipments needing faster delivery',
        tracking: true
      },
      {
        name: 'Priority International',
        delivery: '2-3 business days',
        bestFor: 'Urgent shipments requiring quick delivery',
        tracking: true
      },
      {
        name: 'International Air Freight',
        delivery: '5-7 business days',
        bestFor: 'Large volume shipments too heavy for standard service',
        tracking: true
      },
      {
        name: 'International Ocean Freight',
        delivery: '30-45 days',
        bestFor: 'Very large shipments where time is not critical',
        tracking: true
      }
    ]
- `ltlRequirements`: [
      'Proper packaging for freight handling',
      'Items must be palletized or crated',
      'Accurate dimensions and weight required',
      'Hazardous materials must be declared',
      'Commercial address with loading dock preferred',
      'Delivery contact information required'
    ]
- `orderProcessingSteps`: [
      {
        title: 'Order Placement',
        timing: 'Day 0',
        description: 'Order is submitted through website, EDI, or phone',
        color: 'primary'
      },
      {
        title: 'Order Verification',
        timing: 'Within 30 minutes',
        description: 'Order is checked for accuracy and availability',
        color: 'primary'
      },
      {
        title: 'Payment Processing',
        timing: 'Within 1 hour',
        description: 'Payment method is verified or terms are applied',
        color: 'primary'
      },
      {
        title: 'Picking & Packing',
        timing: 'Same day for orders before 2 PM',
        description: 'Items are picked from warehouse and packaged',
        color: 'secondary'
      },
      {
        title: 'Shipping',
        timing: 'Same day for orders before cutoff',
        description: 'Order is handed off to carrier with tracking',
        color: 'info'
      },
      {
        title: 'Delivery',
        timing: 'Based on shipping method',
        description: 'Carrier delivers to specified address',
        color: 'success'
      }
    ]
- `packagingPractices`: [
      {
        title: 'Multiple Box Sizes',
        icon: 'package-variant-closed',
        description: 'We use the appropriate box size for each order to minimize shipping costs and environmental impact while ensuring product protection.'
      },
      {
        title: 'Eco-Friendly Materials',
        icon: 'leaf',
        description: 'Whenever possible, we use recyclable and biodegradable packaging materials, including recycled cardboard and paper-based void fill.'
      },
      {
        title: 'Part-Specific Protection',
        icon: 'shield',
        description: 'Delicate parts receive additional protection with custom inserts, bubble wrap, or foam padding to prevent damage during transit.'
      },
      {
        title: 'Consolidation',
        icon: 'package-variant',
        description: 'Multiple items in a single order are consolidated whenever possible to reduce packaging materials and shipping costs.'
      }
    ]
- `returnPolicies`: [
      {
        title: 'Standard Returns',
        description: 'Our standard return policy for most products:',
        points: [
          '30-day return window from delivery date',
          'Items must be in original condition and packaging',
          'Return shipping paid by customer for non-defective items',
          'Restocking fee may apply (typically 15%
- `returnsProcess`: [
      {
        title: 'Request Return Authorization',
        description: 'Submit a return request through your account dashboard or by contacting customer service with your order number and reason for return.',
        icon: 'file-document-edit',
        color: 'primary'
      },
      {
        title: 'Receive RMA and Instructions',
        description: 'Once approved, you\'ll receive a Return Merchandise Authorization (RMA
- `returnsResources`: [
      {
        title: 'Returns Portal',
        icon: 'laptop',
        description: 'Manage all your returns online through our self-service returns portal. Request RMAs, print shipping labels, and track return status.',
        link: '/account/returns',
        buttonText: 'Access Portal',
        image: 'https://via.placeholder.com/400x200?text=Returns+Portal'
      },
      {
        title: 'RMA Generator',
        icon: 'note-text',
        description: 'Quickly generate return merchandise authorizations for multiple items or orders with our easy-to-use RMA tool.',
        link: '/tools/rma-generator',
        buttonText: 'Generate RMA',
        image: 'https://via.placeholder.com/400x200?text=RMA+Generator'
      },
      {
        title: 'Returns Guide',
        icon: 'book-open-variant',
        description: 'Download our comprehensive returns guide with step-by-step instructions, packaging requirements, and tips for efficient returns processing.',
        link: '/resources/returns-guide',
        buttonText: 'Download Guide',
        image: 'https://via.placeholder.com/400x200?text=Returns+Guide'
      }
    ]
- `shippingMethods`: [
      {
        name: 'Standard Ground',
        delivery: '3-5 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Regular restocking orders'
      },
      {
        name: 'Expedited Ground',
        delivery: '2-3 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Time-sensitive orders'
      },
      {
        name: 'Priority Overnight',
        delivery: 'Next business day',
        availability: 'Continental US & Canada',
        bestFor: 'Emergency parts needs'
      },
      {
        name: 'LTL Freight',
        delivery: '3-7 business days',
        availability: 'Continental US & Canada',
        bestFor: 'Large or heavy shipments'
      },
      {
        name: 'Will Call',
        delivery: 'Same day pickup',
        availability: 'Distribution center locations',
        bestFor: 'Local customers needing immediate parts'
      }
    ]
- `shippingPolicies`: [
      {
        title: 'Order Processing Times',
        content: 'Crown Nexus processes orders according to the following schedule:<br><br>• Orders received before 2 PM EST on business days are processed the same day<br>• Orders received after 2 PM EST are processed the next business day<br>• Processing time does not include weekends or holidays<br><br>Orders are processed in the sequence they are received, with priority given to emergency orders and expedited shipping requests.'
      },
      {
        title: 'Shipping Cutoff Times',
        content: 'To ensure your order ships on the same day, please place your order before these cutoff times:',
        bulletPoints: [
          'Standard Ground: 2 PM EST',
          'Expedited Ground: 2 PM EST',
          'Priority Overnight: 3 PM EST (may vary by location
- `shippingTools`: [
      {
        name: 'Shipping Rate Calculator',
        description: 'Calculate shipping costs based on weight, dimensions, and destination',
        icon: 'calculator',
        link: '/tools/shipping-calculator'
      },
      {
        name: 'Transit Time Estimator',
        description: 'Get estimated delivery times for any shipping method to your location',
        icon: 'clock-outline',
        link: '/tools/transit-estimator'
      },
      {
        name: 'Order Tracking Portal',
        description: 'Track all your shipments in one place with real-time updates',
        icon: 'map-marker-path',
        link: '/account/order-tracking'
      },
      {
        name: 'Shipping Documentation Generator',
        description: 'Generate shipping labels, packing slips, and customs forms',
        icon: 'file-document-outline',
        link: '/tools/documentation'
      }
    ]
- `warrantyInformation`: [
      {
        title: 'Manufacturer Warranties',
        description: 'All products sold through Crown Nexus come with the original manufacturer warranty. Warranty terms vary by manufacturer and product category.',
        coverage: [
          { category: 'Brake Components', standard: '12 months / 12,000 miles', extended: '24 months / 24,000 miles' },
          { category: 'Engine Parts', standard: '12 months / 12,000 miles', extended: '36 months / 36,000 miles' },
          { category: 'Suspension Components', standard: '24 months / 24,000 miles', extended: 'Lifetime (limited

### TermsOfService
**Path:** `src/views/TermsOfService.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `sections`: [
      {
        id: 'acceptance',
        title: '1. Acceptance of Terms',
        content: `
          <p>These Terms of Service ("Terms"

#### Methods
- `printTerms()`
- `scrollToSection()`

### Testimonials
**Path:** `src/views/Testimonials.vue`
**Type:** Composition API (script setup)

#### Reactive State
**Refs:**
- `industryOptions`: [
  'Auto Repair Shop',
  'Parts Retailer',
  'Distributor',
  'Dealership',
  'Fleet Service',
  'Performance Shop'
]
- `itemsPerPage`: 9
- `loading`: true
- `page`: 1
- `ratingOptions`: [
  { title: '5 Stars', value: 5 },
  { title: '4+ Stars', value: 4 },
  { title: '3+ Stars', value: 3 }
]
- `totalItems`: 0

#### Computed Properties
- `isAdmin`

#### Methods
- `async fetchTestimonials()`
- `filterTestimonials()`
- `resetFilters()`

#### Lifecycle Hooks
- `mounted`

### Unauthorized
**Path:** `src/views/Unauthorized.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `errorMessage`: ''
- `showContactDialog`: false

#### Computed Properties
- `isLoggedIn`

#### Methods
- `goBack()`

### UserDetail
**Path:** `src/views/UserDetail.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `activityLoading`: false
- `activityPage`: 1
- `activityPageSize`: 10
- `deleteDialog`: false
- `deleteLoading`: false
- `hasMoreActivity`: false
- `impersonateDialog`: false
- `impersonateLoading`: false
- `loading`: true
- `resetDialog`: false
- `resetLoading`: false
- `statusDialog`: false
- `statusLoading`: false

#### Computed Properties
- `userId`

#### Methods
- `confirmDelete()`
- `confirmImpersonateUser()`
- `confirmPasswordReset()`
- `confirmToggleStatus()`
- `async deleteUser()`
- `async fetchActivityLog()`
- `async fetchUser()`
- `async impersonateUser()`
- `loadMoreActivity()`
- `refreshActivityLog()`
- `async sendPasswordReset()`
- `async toggleUserStatus()`

### UserForm
**Path:** `src/views/UserForm.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `confirmPassword`: ''
- `formDirty`: false
- `formError`: ''
- `initialLoading`: false
- `isFormValid`: false
- `loading`: false
- `showPassword`: false
- `showPasswordFields`: false
- `showUnsavedDialog`: false

#### Computed Properties
- `currentUser`
- `passwordRules`

#### Methods
- `clearError()`
- `discardChanges()`
- `async fetchCompanies()`
- `async fetchUser()`
- `navigationGuard()`
- `async submitForm()`

### UserManagement
**Path:** `src/views/UserManagement.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `deleteDialog`: false
- `deleteLoading`: false
- `itemsPerPage`: 10
- `loading`: false
- `page`: 1
- `search`: ''
- `totalItems`: 0
- `totalPages`: 1

#### Computed Properties
- `currentUserId`

#### Methods
- `confirmDelete()`
- `async deleteUser()`
- `async fetchUsers()`
- `resetFilters()`

### UserProfile
**Path:** `src/views/UserProfile.vue`
**Type:** Composition API

#### Reactive State
**Refs:**
- `apiKeyForm`: {
      name: '',
      expiration: '90d'
    }
- `apiKeyLoading`: false
- `disableTwoFactorPassword`: ''
- `editingProfile`: false
- `isApiKeyFormValid`: false
- `isPasswordFormValid`: false
- `isProfileFormValid`: false
- `loading`: true
- `newApiKey`: ''
- `passwordForm`: {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
- `passwordFormError`: ''
- `passwordLastChanged`: new Date(Date.now(
- `preferences`: {
      theme: 'light' as 'light' | 'dark' | 'system',
      language: 'en',
      timezone: 'America/New_York',
      notifications_enabled: true,
      dashboard_widgets: ['recent_activity', 'product_stats', 'quick_actions']
    }
- `profileForm`: {
      full_name: '',
      email: ''
    }
- `profileFormError`: ''
- `revokeKeyLoading`: false
- `showActivityDialog`: false
- `showApiKeyDialog`: false
- `showCurrentPassword`: false
- `showNewPassword`: false
- `showRevokeKeyDialog`: false
- `showTwoFactorDialog`: false
- `twoFactorCode`: ''
- `twoFactorEnabled`: false
- `twoFactorLoading`: false
- `updatingPassword`: false
- `updatingPreferences`: false
- `updatingProfile`: false

#### Methods
- `cancelApiKeyDialog()`
- `cancelEditingProfile()`
- `async changePassword()`
- `clearPasswordError()`
- `clearProfileError()`
- `confirmRevokeKey()`
- `copyApiKey()`
- `async disableTwoFactor()`
- `async enableTwoFactor()`
- `async generateApiKey()`
- `async revokeApiKey()`
- `startEditingProfile()`
- `async updatePreferences()`
- `async updateProfile()`

## TypeScript Types
### api
**Path:** `src/services/api.ts`

#### Interface: `ApiError`
| Property | Type |
| -------- | ---- |
| detail | string |
| status | number |
| title | string |
| type | string |

### auth
**Path:** `src/stores/auth.ts`

#### Interface: `AuthState`
| Property | Type |
| -------- | ---- |
| error | string | null |
| isAuthenticated | boolean |
| loading | boolean |
| token | string | null |
| tokenExpiration | number | null |
| user | User | null |

#### Interface: `LoginCredentials`
| Property | Type |
| -------- | ---- |
| password | string |
| rememberMe | boolean |
| username | string |

#### Interface: `LoginResponse`
| Property | Type |
| -------- | ---- |
| access_token | string |
| token_type | string |

#### Interface: `TokenPayload`
| Property | Type |
| -------- | ---- |
| exp | number |
| role | UserRole |
| sub | string |

### chat
**Path:** `src/types/chat.ts`

#### Interface: `ChatMember`
| Property | Type |
| -------- | ---- |
| is_online | boolean |
| last_read_at | string | null |
| role | ChatMemberRole |
| user_id | string |
| user_name | string |

#### Enum: `ChatMemberRole`
| Property | Type |
| -------- | ---- |
| ADMIN | 'admin' |
| GUEST | 'guest' |
| MEMBER | 'member' |
| OWNER | 'owner' |

#### Interface: `ChatMessage`
| Property | Type |
| -------- | ---- |
| content | string |
| created_at | string |
| id | string |
| is_deleted | boolean |
| is_edited | boolean |
| message_type | MessageType |
| metadata | Record<string, any> |
| reactions | Record<string, string[]> |
| room_id | string |
| sender_id | string | null |
| sender_name | string | null |
| updated_at | string |

#### Interface: `ChatNotification`
| Property | Type |
| -------- | ---- |
| content | string |
| created_at | string |
| id | string |
| is_read | boolean |
| message_id | string |
| room_id | string |
| type | string |

#### Interface: `ChatRoom`
| Property | Type |
| -------- | ---- |
| company_id | string | null |
| created_at | string |
| id | string |
| last_message | ChatMessage | null |
| member_count | number |
| metadata | Record<string, any> |
| name | string | null |
| type | ChatRoomType |
| unread_count | number |
| user_role | ChatMemberRole |

#### Enum: `ChatRoomType`
| Property | Type |
| -------- | ---- |
| COMPANY | 'company' |
| DIRECT | 'direct' |
| GROUP | 'group' |
| SUPPORT | 'support' |

#### Interface: `ChatServiceState`
| Property | Type |
| -------- | ---- |
| activeRoom | ChatRoom | null |
| activeRoomId | string | null |
| activeRoomMembers | ChatMember[] |
| activeRoomMessages | ChatMessage[] |
| chatRooms | Record<string, ChatRoom> |
| typingUsers | Record<string, TypingIndicator[]> |

#### Enum: `MessageType`
| Property | Type |
| -------- | ---- |
| ACTION | 'action' |
| FILE | 'file' |
| IMAGE | 'image' |
| SYSTEM | 'system' |
| TEXT | 'text' |

#### Interface: `TypingIndicator`
| Property | Type |
| -------- | ---- |
| room_id | string |
| timestamp | number |
| user_id | string |
| user_name | string |

#### Interface: `UserPresence`
| Property | Type |
| -------- | ---- |
| is_online | boolean |
| last_seen_at | string | null |
| status | string | null |
| user_id | string |

#### Interface: `WebSocketCommand`
| Property | Type |
| -------- | ---- |
| command | string |
| data | Record<string, any> |
| room_id | string |

#### Interface: `WebSocketResponse`
| Property | Type |
| -------- | ---- |
| data | Record<string, any> |
| error | string |
| success | boolean |
| type | string |

### error-handler
**Path:** `src/utils/error-handler.ts`

#### Interface: `ErrorInfo`
| Property | Type |
| -------- | ---- |
| code | string |
| details | string | Record<string, any> |
| field | string |
| message | string |
| severity | ErrorSeverity |

#### Enum: `ErrorSeverity`
| Property | Type |
| -------- | ---- |
| CRITICAL | 'critical' |
| ERROR | 'error' |
| INFO | 'info' |
| WARNING | 'warning' |

### fitment
**Path:** `src/types/fitment.ts`

#### Interface: `Fitment`
| Property | Type |
| -------- | ---- |
| attributes | Record<string, any> |
| created_at | string |
| engine | string |
| id | string |
| make | string |
| model | string |
| transmission | string |
| updated_at | string |
| year | number |

#### Interface: `FitmentFilters`
| Property | Type |
| -------- | ---- |
| attributes | Record<string, any> |
| engine | string |
| make | string |
| model | string |
| page | number |
| page_size | number |
| transmission | string |
| year | number |

#### Interface: `FitmentListResponse`
| Property | Type |
| -------- | ---- |
| items | Fitment[] |
| page | number |
| page_size | number |
| pages | number |
| total | number |

### fitmentProcessing
**Path:** `src/services/fitmentProcessing.ts`

#### Interface: `FitmentValidationResult`
| Property | Type |
| -------- | ---- |
| attributes | Record<string, any> |
| engine | string |
| fitment | {
    vehicle: {
      year: number |
| make | string |
| message | string |
| model | string |
| original_text | string |
| status | string |
| submodel | string |
| suggestions | string[] |
| transmission | string |

#### Interface: `ProcessFitmentResponse`
| Property | Type |
| -------- | ---- |
| error_count | number |
| results | Record<string, FitmentValidationResult[]> |
| valid_count | number |
| warning_count | number |

### index
**Path:** `src/router/index.ts`

#### Interface: `RouteMeta`
| Property | Type |
| -------- | ---- |
| layout | string |
| requiresAdmin | boolean |
| requiresAuth | boolean |
| title | string |

### media
**Path:** `src/types/media.ts`

#### Interface: `Media`
| Property | Type |
| -------- | ---- |
| alt_text | string |
| created_at | string |
| description | string |
| filename | string |
| id | string |
| media_type | string |
| mime_type | string |
| product | any |
| size | number |
| thumbnail_url | string |
| updated_at | string |
| url | string |

### modelMapping
**Path:** `src/services/modelMapping.ts`

#### Interface: `ModelMapping`
| Property | Type |
| -------- | ---- |
| active | boolean |
| created_at | string |
| id | number |
| mapping | string |
| pattern | string |
| priority | number |
| updated_at | string |

#### Interface: `ModelMappingListResponse`
| Property | Type |
| -------- | ---- |
| items | ModelMapping[] |
| total | number |

#### Interface: `ModelMappingRequest`
| Property | Type |
| -------- | ---- |
| active | boolean |
| mapping | string |
| pattern | string |
| priority | number |

### notification
**Path:** `src/utils/notification.ts`

#### Interface: `Notification`
| Property | Type |
| -------- | ---- |
| closeable | boolean |
| id | number |
| message | string |
| position | 'top' | 'bottom' |
| timeout | number |
| type | NotificationType |

#### Enum: `NotificationType`
| Property | Type |
| -------- | ---- |
| ERROR | 'error' |
| INFO | 'info' |
| SUCCESS | 'success' |
| WARNING | 'warning' |

### product
**Path:** `src/types/product.ts`

#### Interface: `Brand`
| Property | Type |
| -------- | ---- |
| created_at | string |
| id | string |
| name | string |
| parent_company | any |
| parent_company_id | string |

#### Interface: `BrandCreateDTO`
| Property | Type |
| -------- | ---- |
| name | string |
| parent_company_id | string |

#### Interface: `BrandUpdateDTO`
| Property | Type |
| -------- | ---- |
| name | string |
| parent_company_id | string | null |

#### Enum: `DescriptionType`
| Property | Type |
| -------- | ---- |
| KEYWORDS | "Keywords" |
| LONG | "Long" |
| NOTES | "Notes" |
| SHORT | "Short" |
| SLANG | "Slang" |

#### Enum: `MarketingType`
| Property | Type |
| -------- | ---- |
| AD_COPY | "Ad Copy" |
| BULLET_POINT | "Bullet Point" |

#### Interface: `Product`
| Property | Type |
| -------- | ---- |
| activities | ProductActivity[] |
| application | string |
| created_at | string |
| descriptions | ProductDescription[] |
| id | string |
| is_active | boolean |
| late_model | boolean |
| marketing | ProductMarketing[] |
| measurements | ProductMeasurement[] |
| part_number | string |
| part_number_stripped | string |
| soft | boolean |
| stock | ProductStock[] |
| superseded_by | ProductSupersession[] |
| supersedes | ProductSupersession[] |
| universal | boolean |
| updated_at | string |
| vintage | boolean |

#### Interface: `ProductActivity`
| Property | Type |
| -------- | ---- |
| changed_at | string |
| changed_by | any |
| changed_by_id | string |
| id | string |
| product_id | string |
| reason | string |
| status | ProductStatus |

#### Interface: `ProductCreateDTO`
| Property | Type |
| -------- | ---- |
| application | string |
| descriptions | ProductDescriptionCreateDTO[] |
| is_active | boolean |
| late_model | boolean |
| marketing | ProductMarketingCreateDTO[] |
| part_number | string |
| part_number_stripped | string |
| soft | boolean |
| universal | boolean |
| vintage | boolean |

#### Interface: `ProductDescription`
| Property | Type |
| -------- | ---- |
| created_at | string |
| description | string |
| description_type | DescriptionType |
| id | string |
| product_id | string |

#### Interface: `ProductDescriptionCreateDTO`
| Property | Type |
| -------- | ---- |
| description | string |
| description_type | DescriptionType |

#### Interface: `ProductDescriptionUpdateDTO`
| Property | Type |
| -------- | ---- |
| description | string |
| description_type | DescriptionType |

#### Interface: `ProductFilters`
| Property | Type |
| -------- | ---- |
| is_active | boolean |
| late_model | boolean |
| page | number |
| page_size | number |
| search | string |
| soft | boolean |
| universal | boolean |
| vintage | boolean |

#### Interface: `ProductListResponse`
| Property | Type |
| -------- | ---- |
| items | Product[] |
| page | number |
| page_size | number |
| pages | number |
| total | number |

#### Interface: `ProductMarketing`
| Property | Type |
| -------- | ---- |
| content | string |
| created_at | string |
| id | string |
| marketing_type | MarketingType |
| position | number |
| product_id | string |

#### Interface: `ProductMarketingCreateDTO`
| Property | Type |
| -------- | ---- |
| content | string |
| marketing_type | MarketingType |
| position | number |

#### Interface: `ProductMarketingUpdateDTO`
| Property | Type |
| -------- | ---- |
| content | string |
| marketing_type | MarketingType |
| position | number |

#### Interface: `ProductMeasurement`
| Property | Type |
| -------- | ---- |
| dimensional_weight | number |
| effective_date | string |
| height | number |
| id | string |
| length | number |
| manufacturer | any |
| manufacturer_id | string |
| product_id | string |
| volume | number |
| weight | number |
| width | number |

#### Interface: `ProductMeasurementCreateDTO`
| Property | Type |
| -------- | ---- |
| dimensional_weight | number |
| height | number |
| length | number |
| manufacturer_id | string |
| volume | number |
| weight | number |
| width | number |

#### Enum: `ProductStatus`
| Property | Type |
| -------- | ---- |
| ACTIVE | "active" |
| DISCONTINUED | "discontinued" |
| INACTIVE | "inactive" |
| OUT_OF_STOCK | "out_of_stock" |
| PENDING | "pending" |

#### Interface: `ProductStock`
| Property | Type |
| -------- | ---- |
| id | string |
| last_updated | string |
| product_id | string |
| quantity | number |
| warehouse | any |
| warehouse_id | string |

#### Interface: `ProductStockCreateDTO`
| Property | Type |
| -------- | ---- |
| quantity | number |
| warehouse_id | string |

#### Interface: `ProductStockUpdateDTO`
| Property | Type |
| -------- | ---- |
| quantity | number |

#### Interface: `ProductSupersession`
| Property | Type |
| -------- | ---- |
| changed_at | string |
| id | string |
| new_product | any |
| new_product_id | string |
| old_product | any |
| old_product_id | string |
| reason | string |

#### Interface: `ProductSupersessionCreateDTO`
| Property | Type |
| -------- | ---- |
| new_product_id | string |
| old_product_id | string |
| reason | string |

#### Interface: `ProductUpdateDTO`
| Property | Type |
| -------- | ---- |
| application | string |
| is_active | boolean |
| late_model | boolean |
| part_number | string |
| soft | boolean |
| universal | boolean |
| vintage | boolean |

### user
**Path:** `src/types/user.ts`

#### Interface: `User`
| Property | Type |
| -------- | ---- |
| account_number | string |
| account_type | string |
| company | {
    id: string |
| created_at | string |
| email | string |
| full_name | string |
| id | string |
| is_active | boolean |
| is_admin | boolean |
| name | string |
| role | UserRole |
| updated_at | string |

#### Enum: `UserRole`
| Property | Type |
| -------- | ---- |
| ADMIN | 'admin' |
| CLIENT | 'client' |
| DISTRIBUTOR | 'distributor' |
| MANAGER | 'manager' |
| READ_ONLY | 'read_only' |

## Utility Functions
### api
**Path:** `src/services/api.ts`

#### Function: `handleApiError(error: any) → void`

### auth
**Path:** `src/stores/auth.ts`

#### Function: `getTokenExpiration(token: string | null) → number | null`

### error-handler
**Path:** `src/utils/error-handler.ts`

#### Function: `createErrorInfo(error: any, defaultMessage: string = 'An error occurred') → ErrorInfo`

#### Function: `getErrorMessage(error: any) → string`

#### Function: `isAxiosError(error: any) → error is AxiosError`

#### Function: `parseValidationErrors(error: any) → Record<string, string>`

### formatters
**Path:** `src/utils/formatters.ts`

#### Function: `formatCurrency(amount: number, currency: string = 'USD', locale: string = 'en-US') → string`

#### Function: `formatDate(dateInput: string | Date | number, format: 'short' | 'medium' | 'long' | 'full' = 'medium') → string`

#### Function: `formatDateTime(dateInput: string | Date | number, format: 'short' | 'medium' | 'long' | 'full' = 'medium') → string`

#### Function: `formatFileSize(bytes: number, decimals: number = 2) → string`

#### Function: `formatNumber(num: number, decimals: number = 0) → string`

#### Function: `toTitleCase(text: string) → string`

#### Function: `truncateText(text: string, maxLength: number = 50) → string`

### notification
**Path:** `src/utils/notification.ts`

#### Function: `createNotification(type: NotificationType, message: string, timeout: number = DEFAULT_TIMEOUT, closeable: boolean = true, position: 'top' | 'bottom' = DEFAULT_POSITION) → number`

#### Function: `error(message: string, timeout?: number) → number`

#### Function: `getNotifications() → Notification[]`

#### Function: `info(message: string, timeout?: number) → number`

#### Function: `removeNotification(id: number) → void`

#### Function: `success(message: string, timeout?: number) → number`

#### Function: `warning(message: string, timeout?: number) → number`
