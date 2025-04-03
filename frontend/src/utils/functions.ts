/**
 * Common utility functions
 */

/**
 * Creates a debounced function that delays invoking func until after wait milliseconds
 * @param func The function to debounce
 * @param wait The number of milliseconds to delay
 * @returns A debounced version of the original function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: number | undefined;

  return function(this: any, ...args: Parameters<T>): void {
    const context = this;

    const later = function() {
      timeout = undefined;
      func.apply(context, args);
    };

    clearTimeout(timeout);
    timeout = window.setTimeout(later, wait);
  };
}
