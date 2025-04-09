// src/utils/validators.ts
/**
 * Utility functions for validating data
 */

/**
 * Check if a value is defined (not null or undefined)
 * @param value The value to check
 * @returns Whether the value is defined
 */
export function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

/**
 * Check if a string is empty or whitespace
 * @param value The string to check
 * @returns Whether the string is empty or whitespace
 */
export function isEmptyString(value: string | null | undefined): boolean {
  return !value || value.trim().length === 0;
}

/**
 * Check if a number is valid (not NaN and finite)
 * @param value The number to check
 * @returns Whether the number is valid
 */
export function isValidNumber(value: number | null | undefined): value is number {
  return typeof value === 'number' && !isNaN(value) && isFinite(value);
}

/**
 * Check if a value is a positive number
 * @param value The value to check
 * @returns Whether the value is a positive number
 */
export function isPositiveNumber(value: number | null | undefined): value is number {
  return isValidNumber(value) && value > 0;
}

/**
 * Check if a value is a non-negative number (zero or positive)
 * @param value The value to check
 * @returns Whether the value is a non-negative number
 */
export function isNonNegativeNumber(value: number | null | undefined): value is number {
  return isValidNumber(value) && value >= 0;
}

/**
 * Check if a value is an integer
 * @param value The value to check
 * @returns Whether the value is an integer
 */
export function isInteger(value: number | null | undefined): value is number {
  return isValidNumber(value) && Number.isInteger(value);
}

/**
 * Check if a date is valid
 * @param value The date to check
 * @returns Whether the date is valid
 */
export function isValidDate(value: Date | string | number | null | undefined): boolean {
  if (!value) return false;

  const date = typeof value === 'object' ? value : new Date(value);
  return !isNaN(date.getTime());
}

/**
 * Check if a date is in the past
 * @param value The date to check
 * @returns Whether the date is in the past
 */
export function isDateInPast(value: Date | string | number | null | undefined): boolean {
  if (!isValidDate(value)) return false;

  const date = typeof value === 'object' ? value : new Date(value);
  return date.getTime() < Date.now();
}

/**
 * Check if a date is in the future
 * @param value The date to check
 * @returns Whether the date is in the future
 */
export function isDateInFuture(value: Date | string | number | null | undefined): boolean {
  if (!isValidDate(value)) return false;

  const date = typeof value === 'object' ? value : new Date(value);
  return date.getTime() > Date.now();
}

/**
 * Check if a value is an array
 * @param value The value to check
 * @returns Whether the value is an array
 */
export function isArray<T>(value: unknown): value is T[] {
  return Array.isArray(value);
}

/**
 * Check if an array is not empty
 * @param value The array to check
 * @returns Whether the array is not empty
 */
export function isNonEmptyArray<T>(value: T[] | null | undefined): value is T[] {
  return isArray(value) && value.length > 0;
}

/**
 * Check if a value is a valid email address
 * @param value The value to check
 * @returns Whether the value is a valid email address
 */
export function isValidEmail(value: string | null | undefined): boolean {
  if (isEmptyString(value)) return false;

  // Basic email validation regex
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(value as string);
}

/**
 * Check if a value is a valid URL
 * @param value The value to check
 * @returns Whether the value is a valid URL
 */
export function isValidUrl(value: string | null | undefined): boolean {
  if (isEmptyString(value)) return false;

  try {
    new URL(value as string);
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Check if a value is a valid year (4-digit number)
 * @param value The value to check
 * @returns Whether the value is a valid year
 */
export function isValidYear(value: number | null | undefined): boolean {
  return isInteger(value) && value >= 1900 && value <= 2100;
}

/**
 * Check if a value is a valid make ID
 * @param value The value to check
 * @returns Whether the value is a valid make ID
 */
export function isValidMakeId(value: number | null | undefined): boolean {
  return isPositiveNumber(value) && isInteger(value);
}

/**
 * Check if a value is a valid model ID
 * @param value The value to check
 * @returns Whether the value is a valid model ID
 */
export function isValidModelId(value: number | null | undefined): boolean {
  return isPositiveNumber(value) && isInteger(value);
}

/**
 * Check if a value is a valid part terminology ID
 * @param value The value to check
 * @returns Whether the value is a valid part terminology ID
 */
export function isValidPartTerminologyId(value: number | null | undefined): boolean {
  return isPositiveNumber(value) && isInteger(value);
}

/**
 * Check if a value is a valid qualifier ID
 * @param value The value to check
 * @returns Whether the value is a valid qualifier ID
 */
export function isValidQualifierId(value: number | null | undefined): boolean {
  return isPositiveNumber(value) && isInteger(value);
}
