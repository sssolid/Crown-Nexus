// frontend/src/utils/formatters.ts
/**
 * Formatting utility functions.
 *
 * This module provides helper functions for formatting data like:
 * - Dates and times
 * - Numbers and currencies
 * - File sizes
 * - Text formatting
 *
 * Using these utilities ensures consistent formatting throughout the application.
 */

/**
 * Format a date to a readable string.
 *
 * @param dateInput - Date input (string, Date, or timestamp)
 * @param format - Format style ('short', 'medium', 'long', 'full')
 * @returns Formatted date string
 */
export function formatDate(
  dateInput: string | Date | number,
  format: 'short' | 'medium' | 'long' | 'full' = 'medium'
): string {
  if (!dateInput) return '';

  const date = typeof dateInput === 'string' ? new Date(dateInput) :
    typeof dateInput === 'number' ? new Date(dateInput) : dateInput;

  // Check if date is valid
  if (isNaN(date.getTime())) return 'Invalid date';

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: format === 'short' ? '2-digit' : 'long',
    day: 'numeric'
  };

  return new Intl.DateTimeFormat('en-US', options).format(date);
}

/**
 * Format a date and time to a readable string.
 *
 * @param dateInput - Date input (string, Date, or timestamp)
 * @param format - Format style ('short', 'medium', 'long', 'full')
 * @returns Formatted date and time string
 */
export function formatDateTime(
  dateInput: string | Date | number,
  format: 'short' | 'medium' | 'long' | 'full' = 'medium'
): string {
  if (!dateInput) return '';

  const date = typeof dateInput === 'string' ? new Date(dateInput) :
    typeof dateInput === 'number' ? new Date(dateInput) : dateInput;

  // Check if date is valid
  if (isNaN(date.getTime())) return 'Invalid date';

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: format === 'short' ? '2-digit' : 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: format === 'short' ? undefined : '2-digit'
  };

  return new Intl.DateTimeFormat('en-US', options).format(date);
}

/**
 * Format a currency amount.
 *
 * @param amount - Numeric amount
 * @param currency - Currency code (default: 'USD')
 * @param locale - Locale code (default: 'en-US')
 * @returns Formatted currency string
 */
export function formatCurrency(
  amount: number,
  currency: string = 'USD',
  locale: string = 'en-US'
): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(amount);
}

/**
 * Format a file size to a human-readable string.
 *
 * @param bytes - File size in bytes
 * @param decimals - Number of decimal places (default: 2)
 * @returns Formatted file size string
 */
export function formatFileSize(bytes: number, decimals: number = 2): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
}

/**
 * Truncate text to a specified length with ellipsis.
 *
 * @param text - Input text
 * @param maxLength - Maximum length (default: 50)
 * @returns Truncated text with ellipsis if needed
 */
export function truncateText(text: string, maxLength: number = 50): string {
  if (!text || text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
}

/**
 * Convert a string to title case.
 *
 * @param text - Input text
 * @returns Text in title case
 */
export function toTitleCase(text: string): string {
  if (!text) return '';
  return text.replace(
    /\w\S*/g,
    txt => txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase()
  );
}

/**
 * Format a number with thousands separators.
 *
 * @param num - Input number
 * @param decimals - Number of decimal places
 * @returns Formatted number string
 */
export function formatNumber(num: number, decimals: number = 0): string {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(num);
}
