// frontend/src/router/index.ts
/**
 * Application routing configuration.
 *
 * This module defines all routes and navigation guards for:
 * - Authentication protection
 * - Role-based access control
 * - Lazy loading for improved performance
 * - Error handling and redirection
 */

import { createRouter, createWebHistory, RouteRecordRaw, RouteLocationNormalized, NavigationGuardNext } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { notificationService } from '@/utils/notification';

// Route meta types
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;
    requiresAdmin?: boolean;
    title?: string;
    layout?: string;
  }
}

// Define routes
const routes: RouteRecordRaw[] = [
  // Public routes - Marketing & Information
  {
    path: '/',
    name: 'Landing',
    component: () => import('@/views/LandingPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'Welcome to Crown Nexus'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'About Us'
    }
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('@/views/ServicesPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'Our Services'
    }
  },
  {
    path: '/resources',
    name: 'Resources',
    component: () => import('@/views/ResourcesPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'Resources'
    }
  },
  {
    path: '/blog',
    name: 'Blog',
    component: () => import('@/views/Blog.vue'),
    meta: {
      requiresAuth: false,
      title: 'Blog'
    }
  },
  {
    path: '/careers',
    name: 'Careers',
    component: () => import('@/views/Careers.vue'),
    meta: {
      requiresAuth: false,
      title: 'Careers'
    }
  },
  {
    path: '/partners',
    name: 'Partners',
    component: () => import('@/views/Partners.vue'),
    meta: {
      requiresAuth: false,
      title: 'Partners'
    }
  },
  {
    path: '/testimonials',
    name: 'Testimonials',
    component: () => import('@/views/Testimonials.vue'),
    meta: {
      requiresAuth: false,
      title: 'Testimonials'
    }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('@/views/ContactPage.vue'),
    meta: {
      requiresAuth: false,
      title: 'Contact Us'
    }
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('@/views/Pricing.vue'),
    meta: {
      requiresAuth: false,
      title: 'Pricing'
    }
  },
  {
    path: '/faq',
    name: 'FAQ',
    component: () => import('@/views/FAQ.vue'),
    meta: {
      requiresAuth: false,
      title: 'Frequently Asked Questions'
    }
  },

  // Legal pages
  {
    path: '/terms',
    name: 'TermsOfService',
    component: () => import('@/views/TermsOfService.vue'),
    meta: {
      requiresAuth: false,
      title: 'Terms of Service'
    }
  },
  {
    path: '/privacy',
    name: 'PrivacyPolicy',
    component: () => import('@/views/PrivacyPolicy.vue'),
    meta: {
      requiresAuth: false,
      title: 'Privacy Policy'
    }
  },
  {
    path: '/shipping-returns',
    name: 'ShippingReturns',
    component: () => import('@/views/ShippingReturns.vue'),
    meta: {
      requiresAuth: false,
      title: 'Shipping & Returns'
    }
  },

  // Authentication
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      requiresAuth: false,
      title: 'Login',
      layout: 'blank'
    }
  },

  // Protected routes - Customer Dashboard
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {
      requiresAuth: true,
      title: 'Dashboard'
    }
  },
  {
    path: '/account',
    name: 'AccountDashboard',
    component: () => import('@/views/AccountDashboard.vue'),
    meta: {
      requiresAuth: true,
      title: 'Account Dashboard'
    }
  },
  {
    path: '/orders',
    name: 'OrderHistory',
    component: () => import('@/views/OrderHistory.vue'),
    meta: {
      requiresAuth: true,
      title: 'Order History'
    }
  },
  {
    path: '/saved-lists',
    name: 'SavedLists',
    component: () => import('@/views/SavedLists.vue'),
    meta: {
      requiresAuth: true,
      title: 'Saved Lists'
    }
  },

  // Product routes
  {
    path: '/products',
    name: 'ProductCatalog',
    component: () => import('@/views/ProductCatalog.vue'),
    meta: {
      requiresAuth: true,
      title: 'Product Catalog'
    }
  },
  {
    path: '/products/:id',
    name: 'ProductDetail',
    component: () => import('@/views/ProductDetail.vue'),
    meta: {
      requiresAuth: true,
      title: 'Product Details'
    }
  },
  {
    path: '/products/new',
    name: 'ProductCreate',
    component: () => import('@/views/ProductForm.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Create Product'
    }
  },
  {
    path: '/products/:id/edit',
    name: 'ProductEdit',
    component: () => import('@/views/ProductForm.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Edit Product'
    }
  },
  {
    path: '/products/:id/fitments',
    name: 'ProductFitments',
    component: () => import('@/views/ProductFitments.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Product Fitments'
    }
  },
  {
    path: '/products/:id/media',
    name: 'ProductMedia',
    component: () => import('@/views/ProductMedia.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Product Media'
    }
  },

  // Fitment routes
  {
    path: '/fitments',
    name: 'FitmentCatalog',
    component: () => import('@/views/FitmentCatalog.vue'),
    meta: {
      requiresAuth: true,
      title: 'Fitment Catalog'
    }
  },
  {
    path: '/fitments/:id',
    name: 'FitmentDetail',
    component: () => import('@/views/FitmentDetail.vue'),
    meta: {
      requiresAuth: true,
      title: 'Fitment Details'
    }
  },
  {
    path: '/fitments/new',
    name: 'FitmentCreate',
    component: () => import('@/views/FitmentForm.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Create Fitment'
    }
  },
  {
    path: '/fitments/:id/edit',
    name: 'FitmentEdit',
    component: () => import('@/views/FitmentForm.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Edit Fitment'
    }
  },

  // User management routes (admin only)
  {
    path: '/users',
    name: 'UserManagement',
    component: () => import('@/views/UserManagement.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'User Management'
    }
  },
  {
    path: '/users/:id',
    name: 'UserDetail',
    component: () => import('@/views/UserDetail.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'User Details'
    }
  },
  {
    path: '/users/new',
    name: 'UserCreate',
    component: () => import('@/views/UserForm.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Create User'
    }
  },
  {
    path: '/users/:id/edit',
    name: 'UserEdit',
    component: () => import('@/views/UserForm.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Edit User'
    }
  },

  // Media Library
  {
    path: '/media',
    name: 'MediaLibrary',
    component: () => import('@/views/MediaLibrary.vue'),
    meta: {
      requiresAuth: true,
      title: 'Media Library'
    }
  },

  // Settings & Profile
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      requiresAuth: true,
      title: 'Settings'
    }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: () => import('@/views/UserProfile.vue'),
    meta: {
      requiresAuth: true,
      title: 'Your Profile'
    }
  },

  // Fitment Management
  {
    path: '/fitment/model-mappings',
    name: 'ModelMappingsManager',
    component: () => import('@/views/ModelMappingsManager.vue'),
    meta: {
      requiresAuth: true,
      requiresAdmin: true,
      title: 'Model Mappings Manager'
    }
  },

  // Error pages
  {
    path: '/unauthorized',
    name: 'Unauthorized',
    component: () => import('@/views/Unauthorized.vue'),
    meta: {
      requiresAuth: false,
      title: 'Unauthorized'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      requiresAuth: false,
      title: 'Page Not Found'
    }
  }
];

// Create router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
});

// Navigation guards
router.beforeEach(async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  // Set page title
  document.title = to.meta.title
    ? `${to.meta.title} - Crown Nexus`
    : 'Crown Nexus';

  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);

  // Initialize auth if token exists but not yet loaded
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchUserProfile();
    } catch (error) {
      // If fetching profile fails, clear auth and redirect to login
      authStore.logout();

      // Store intended destination for redirect after login
      if (to.path !== '/login') {
        localStorage.setItem('redirectPath', to.fullPath);
      }

      notificationService.error('Your session has expired. Please log in again.');
      return next('/login');
    }
  }

  // Check if route requires authentication
  if (requiresAuth && !authStore.isAuthenticated) {
    // Store intended destination for redirect after login
    localStorage.setItem('redirectPath', to.fullPath);

    notificationService.warning('Please log in to access this page.');
    return next('/login');
  }

  // Check if route requires admin role
  if (requiresAdmin && !authStore.isAdmin) {
    notificationService.error('You do not have permission to access this page.');
    return next('/unauthorized');
  }

  // Redirect to dashboard if authenticated user tries to access login page
  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/dashboard');
  }

  // Optional: Auto-redirect authenticated users from landing page to dashboard
  // if (to.path === '/' && authStore.isAuthenticated) {
  //   return next('/dashboard');
  // }

  next();
});

export default router;
