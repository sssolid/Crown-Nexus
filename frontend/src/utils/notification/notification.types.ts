// src/utils/notifications/notification.types.ts
export enum NotificationType {
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning',
  INFO = 'info',
}

export enum NotificationPosition {
  TOP = 'top',
  TOP_LEFT = 'top-left',
  TOP_RIGHT = 'top-right',
  BOTTOM = 'bottom',
  BOTTOM_LEFT = 'bottom-left',
  BOTTOM_RIGHT = 'bottom-right',
}

export interface NotificationOptions {
  title?: string;
  message: string;
  type?: NotificationType;
  timeout?: number;
  closeable?: boolean;
  position?: NotificationPosition;
  showIcon?: boolean;
  actionText?: string;
  actionColor?: string;
  onAction?: () => void;
  id?: number;
}

export interface Notification extends Required<NotificationOptions> {
  id: number;
  createdAt: Date;
}
