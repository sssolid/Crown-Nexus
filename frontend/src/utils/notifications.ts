// src/utils/notification.ts (enhanced)
import { reactive } from 'vue'
import {NotificationType} from "@/utils/notification/notification.types.ts";

// Keep your original interface but extend it
export interface Notification {
  id: number
  type: NotificationType
  message: string
  timeout?: number
  closeable?: boolean
  position?: 'top' | 'bottom'

  // New extended properties
  title?: string
  showIcon?: boolean
  actionText?: string
  actionColor?: string
  onAction?: () => void
  createdAt?: Date
}

// Add enhanced notification positions
export enum NotificationPosition {
  TOP = 'top',
  TOP_LEFT = 'top-left',
  TOP_RIGHT = 'top-right',
  BOTTOM = 'bottom',
  BOTTOM_LEFT = 'bottom-left',
  BOTTOM_RIGHT = 'bottom-right'
}

// Add enhanced notification options
export interface NotificationOptions {
  title?: string
  timeout?: number
  closeable?: boolean
  position?: NotificationPosition
  showIcon?: boolean
  actionText?: string
  actionColor?: string
  onAction?: () => void
}

const DEFAULT_TIMEOUT = 5000
const DEFAULT_POSITION = 'bottom'

// Keep your original reactive notifications array
const notifications = reactive<Notification[]>([])
let nextId = 1

// Enhance your existing notification methods but maintain backward compatibility
function createNotification(
  type: NotificationType,
  message: string,
  options: NotificationOptions = {}
): number {
  const id = nextId++

  const notification: Notification = {
    id,
    type,
    message,
    timeout: options.timeout ?? DEFAULT_TIMEOUT,
    closeable: options.closeable ?? true,
    position: convertPosition(options.position) || DEFAULT_POSITION,

    // New properties
    title: options.title,
    showIcon: options.showIcon ?? true,
    actionText: options.actionText,
    actionColor: options.actionColor || 'primary',
    onAction: options.onAction,
    createdAt: new Date(),
  }

  // Replace notification with same ID if it exists
  const existingIndex = notifications.findIndex(n => n.id === id)
  if (existingIndex !== -1) {
    notifications.splice(existingIndex, 1, notification)
  } else {
    notifications.push(notification)
  }

  if (notification.timeout > 0) {
    setTimeout(() => removeNotification(id), notification.timeout)
  }

  return id
}

// Helper to convert the enhanced positions to original format
function convertPosition(position?: NotificationPosition): 'top' | 'bottom' | undefined {
  if (!position) return undefined
  if (position.includes('top')) return 'top'
  if (position.includes('bottom')) return 'bottom'
  return undefined
}

// Keep your original methods but enhance them
function removeNotification(id: number): void {
  const index = notifications.findIndex(notification => notification.id === id)
  if (index !== -1) {
    notifications.splice(index, 1)
  }
}

function getNotifications(): Notification[] {
  return notifications
}

// Keep your original type-specific methods
function success(message: string, options: NotificationOptions = {}): number {
  return createNotification(NotificationType.SUCCESS, message, options)
}

function error(message: string, options: NotificationOptions = {}): number {
  return createNotification(NotificationType.ERROR, message, options)
}

function warning(message: string, options: NotificationOptions = {}): number {
  return createNotification(NotificationType.WARNING, message, options)
}

function info(message: string, options: NotificationOptions = {}): number {
  return createNotification(NotificationType.INFO, message, options)
}

// Add new methods that enhance functionality
function prompt(message: string, actionText: string, onAction: () => void, options: NotificationOptions = {}): number {
  return createNotification(NotificationType.INFO, message, {
    actionText,
    onAction,
    timeout: 0, // Don't auto-dismiss prompts
    ...options,
  })
}

// Export the enhanced service with all your original methods
export const notificationService = {
  success,
  error,
  warning,
  info,
  prompt, // New method
  create: createNotification,
  remove: removeNotification,
  getAll: getNotifications,
  clearAll: () => notifications.splice(0, notifications.length),
}

export default notificationService
