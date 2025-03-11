// frontend/src/utils/notification.ts
/**
 * Application notification system.
 *
 * This module provides a centralized way to display notifications
 * throughout the application. It uses Vuetify's snackbar component
 * to show different types of messages.
 */

import { reactive } from 'vue';

// Notification types
export enum NotificationType {
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning',
  INFO = 'info',
}

// Notification interface
export interface Notification {
  id: number;
  type: NotificationType;
  message: string;
  timeout?: number;
  closeable?: boolean;
  position?: 'top' | 'bottom';
}

// Default notification options
const DEFAULT_TIMEOUT = 5000; // 5 seconds
const DEFAULT_POSITION = 'bottom';

// Notification store
const notifications = reactive<Notification[]>([]);
let nextId = 1;

/**
 * Create a notification.
 *
 * @param type - Notification type
 * @param message - Notification message
 * @param timeout - Optional timeout in milliseconds
 * @param closeable - Whether the notification can be closed by the user
 * @param position - Position of the notification
 * @returns The notification ID
 */
function createNotification(
  type: NotificationType,
  message: string,
  timeout: number = DEFAULT_TIMEOUT,
  closeable: boolean = true,
  position: 'top' | 'bottom' = DEFAULT_POSITION
): number {
  const id = nextId++;

  const notification: Notification = {
    id,
    type,
    message,
    timeout,
    closeable,
    position,
  };

  notifications.push(notification);

  // If timeout is set, remove notification after timeout
  if (timeout > 0) {
    setTimeout(() => removeNotification(id), timeout);
  }

  return id;
}

/**
 * Remove a notification by ID.
 *
 * @param id - Notification ID
 */
function removeNotification(id: number): void {
  const index = notifications.findIndex(notification => notification.id === id);
  if (index !== -1) {
    notifications.splice(index, 1);
  }
}

/**
 * Get all active notifications.
 *
 * @returns Array of active notifications
 */
function getNotifications(): Notification[] {
  return notifications;
}

/**
 * Show a success notification.
 *
 * @param message - The notification message
 * @param timeout - Optional timeout in milliseconds
 * @returns The notification ID
 */
function success(message: string, timeout?: number): number {
  return createNotification(NotificationType.SUCCESS, message, timeout);
}

/**
 * Show an error notification.
 *
 * @param message - The notification message
 * @param timeout - Optional timeout in milliseconds
 * @returns The notification ID
 */
function error(message: string, timeout?: number): number {
  return createNotification(NotificationType.ERROR, message, timeout);
}

/**
 * Show a warning notification.
 *
 * @param message - The notification message
 * @param timeout - Optional timeout in milliseconds
 * @returns The notification ID
 */
function warning(message: string, timeout?: number): number {
  return createNotification(NotificationType.WARNING, message, timeout);
}

/**
 * Show an info notification.
 *
 * @param message - The notification message
 * @param timeout - Optional timeout in milliseconds
 * @returns The notification ID
 */
function info(message: string, timeout?: number): number {
  return createNotification(NotificationType.INFO, message, timeout);
}

// Export the notification functions
export const notificationService = {
  success,
  error,
  warning,
  info,
  remove: removeNotification,
  getAll: getNotifications,
};
