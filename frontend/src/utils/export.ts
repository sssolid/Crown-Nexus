/**
 * Utility functions for exporting data
 */

/**
 * Exports data to a CSV file
 * @param data Array of objects to export
 * @param filename Name of the file without extension
 */
export function exportToCSV(data: Record<string, any>[], filename: string): void {
  if (!data || !data.length) {
    console.warn('No data to export');
    return;
  }

  // Get headers from the first item
  const headers = Object.keys(data[0]);

  // Create CSV rows
  const csvRows = [];

  // Add the headers
  csvRows.push(headers.join(','));

  // Add the data
  for (const row of data) {
    const values = headers.map(header => {
      const value = row[header] || '';
      // Escape values with commas or quotes
      const escaped = String(value).replace(/"/g, '""');
      return `"${escaped}"`;
    });
    csvRows.push(values.join(','));
  }

  // Combine into CSV content
  const csvContent = csvRows.join('\n');

  // Create download link
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);

  // Create a link element and trigger download
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `${filename}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
