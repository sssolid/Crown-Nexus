// frontend/src/utils/error-handler.ts
/**
 * Error handling utilities.
 *
 * This module provides consistent error handling functions for:
 * - Extracting error messages from API responses
 * - Formatting error messages for display
 * - Handling common error scenarios
 */

import { AxiosError } from 'axios';

// Error severity levels
export enum ErrorSeverity {
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

// Structured error object
export interface ErrorInfo {
  message: string;
  code?: string;
  severity: ErrorSeverity;
  details?: string | Record<string, any>;
  field?: string;
}

/**
 * Extract a user-friendly error message from an API error.
 *
 * @param error - The error object
 * @returns A user-friendly error message
 */
export function getErrorMessage(error: any): string {
  if (!error) return 'An unknown error occurred';

  // Handle Axios errors
  if (isAxiosError(error)) {
    const response = error.response;

    // Extract error message from response data
    if (response?.data) {
      // Handle different error response formats
      if (typeof response.data === 'string') {
        return response.data;
      }

      if (response.data.detail) {
        return response.data.detail;
      }

      if (response.data.message) {
        return response.data.message;
      }

      if (response.data.error) {
        return response.data.error;
      }
    }

    // Fallback to status text or generic message
    if (response?.statusText) {
      return `Error: ${response.statusText}`;
    }

    return `Error ${response?.status || ''}: Request failed`;
  }

  // Handle error objects with message property
  if (error.message) {
    return error.message;
  }

  // Handle error strings
  if (typeof error === 'string') {
    return error;
  }

  // Fallback for other error types
  return 'An unexpected error occurred';
}

/**
 * Check if an error is an Axios error.
 *
 * @param error - The error to check
 * @returns True if the error is an Axios error
 */
export function isAxiosError(error: any): error is AxiosError {
  return error && error.isAxiosError === true;
}

/**
 * Parse validation errors from API response.
 *
 * @param error - The API error
 * @returns An object mapping field names to error messages
 */
export function parseValidationErrors(error: any): Record<string, string> {
  const validationErrors: Record<string, string> = {};

  if (isAxiosError(error) && error.response?.data) {
    const data = error.response.data;

    // Handle FastAPI validation error format
    if (data.detail && Array.isArray(data.detail)) {
      data.detail.forEach((err: any) => {
        if (err.loc && err.loc.length > 1) {
          // Get the field name (usually the second item in the loc array)
          const fieldName = err.loc[1];
          validationErrors[fieldName] = err.msg;
        }
      });
      return validationErrors;
    }

    // Handle generic field errors object
    if (typeof data === 'object' && !Array.isArray(data)) {
      Object.keys(data).forEach(key => {
        if (typeof data[key] === 'string') {
          validationErrors[key] = data[key];
        } else if (Array.isArray(data[key])) {
          validationErrors[key] = data[key].join(', ');
        }
      });
    }
  }

  return validationErrors;
}

/**
 * Create a structured error object from any error type.
 *
 * @param error - The original error
 * @param defaultMessage - Default message if none can be extracted
 * @returns A structured error object
 */
export function createErrorInfo(
  error: any,
  defaultMessage: string = 'An error occurred'
): ErrorInfo {
  // Default error info
  const errorInfo: ErrorInfo = {
    message: defaultMessage,
    severity: ErrorSeverity.ERROR
  };

  if (!error) return errorInfo;

  // Handle Axios errors
  if (isAxiosError(error)) {
    const status = error.response?.status || 500;

    // Set severity based on status code
    if (status >= 500) {
      errorInfo.severity = ErrorSeverity.CRITICAL;
    } else if (status >= 400) {
      errorInfo.severity = ErrorSeverity.ERROR;
    } else if (status >= 300) {
      errorInfo.severity = ErrorSeverity.WARNING;
    }

    // Extract error details
    errorInfo.message = getErrorMessage(error);
    errorInfo.code = `HTTP_${status}`;

    // Include validation errors in details if present
    const validationErrors = parseValidationErrors(error);
    if (Object.keys(validationErrors).length > 0) {
      errorInfo.details = validationErrors;
    }

    return errorInfo;
  }

  // Handle Error objects
  if (error instanceof Error) {
    errorInfo.message = error.message;
    errorInfo.details = error.stack;
    return errorInfo;
  }

  // Handle string errors
  if (typeof error === 'string') {
    errorInfo.message = error;
    return errorInfo;
  }

  // Handle object errors with message property
  if (typeof error === 'object' && error !== null) {
    if (error.message) {
      errorInfo.message = String(error.message);
    }
    if (error.code) {
      errorInfo.code = String(error.code);
    }
    if (error.details) {
      errorInfo.details = error.details;
    }
    return errorInfo;
  }

  return errorInfo;
}
