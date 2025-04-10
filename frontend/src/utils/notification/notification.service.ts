// src/utils/notifications/notification.service.ts
import { reactive } from 'vue';
import {
  Notification,
  NotificationType,
  NotificationPosition,
  NotificationOptions
} from './notification.types';

const DEFAULT_TIMEOUT = 5000;
const DEFAULT_POSITION = NotificationPosition.BOTTOM;

const notifications = reactive<Notification[]>([]);
let nextId = 1;

/**
 * Creates a notification with the given options
 */
function createNotification(options: NotificationOptions): number {
  const id = options.id || nextId++;

  const notification: Notification = {
    id,
    title: options.title || '',
    message: options.message,
    type: options.type || NotificationType.INFO,
    timeout: options.timeout ?? DEFAULT_TIMEOUT,
    closeable: options.closeable ?? true,
    position: options.position || DEFAULT_POSITION,
    showIcon: options.showIcon ?? true,
    actionText: options.actionText || '',
    actionColor: options.actionColor || 'primary',
    onAction: options.onAction || (() => {}),
    createdAt: new Date(),
  };

  // Replace notification with same ID if it exists
  const existingIndex = notifications.findIndex(n => n.id === id);
  if (existingIndex !== -1) {
    notifications.splice(existingIndex, 1, notification);
  } else {
    notifications.push(notification);
  }

  // Auto-remove after timeout if timeout > 0
  if (notification.timeout > 0) {
    setTimeout(() => removeNotification(id), notification.timeout);
  }

  return id;
}

/**
 * Removes notification by ID
 */
function removeNotification(id: number): void {
  const index = notifications.findIndex(n => n.id === id);
  if (index !== -1) {
    notifications.splice(index, 1);
  }
}

/**
 * Gets all current notifications
 */
function getNotifications(): Notification[] {
  return notifications;
}

/**
 * Creates a success notification
 */
function success(message: string, options: Partial<NotificationOptions> = {}): number {
  return createNotification({
    message,
    type: NotificationType.SUCCESS,
    ...options,
  });
}

/**
 * Creates an error notification
 */
function error(message: string, options: Partial<NotificationOptions> = {}): number {
  return createNotification({
    message,
    type: NotificationType.ERROR,
    ...options,
  });
}

/**
 * Creates a warning notification
 */
function warning(message: string, options: Partial<NotificationOptions> = {}): number {
  return createNotification({
    message,
    type: NotificationType.WARNING,
    ...options,
  });
}

/**
 * Creates an info notification
 */
function info(message: string, options: Partial<NotificationOptions> = {}): number {
  return createNotification({
    message,
    type: NotificationType.INFO,
    ...options,
  });
}

/**
 * Creates a notification that requires user action
 */
function prompt(message: string, actionText: string, onAction: () => void, options: Partial<NotificationOptions> = {}): number {
  return createNotification({
    message,
    actionText,
    onAction,
    timeout: 0, // Don't auto-dismiss prompts
    ...options,
  });
}

/**
 * Clears all notifications
 */
function clearAll(): void {
  notifications.splice(0, notifications.length);
}

export const notificationService = {
  success,
  error,
  warning,
  info,
  prompt,
  create: createNotification,
  remove: removeNotification,
  getAll: getNotifications,
  clearAll,
};

export default notificationService;
