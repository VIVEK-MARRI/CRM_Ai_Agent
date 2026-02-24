/**
 * Utility functions for common operations
 */

/**
 * Get color configuration for score
 */
export const getScoreColor = (score) => {
  if (score >= 80) {
    return {
      color: '#10b981',
      bgColor: '#ecfdf5',
      label: 'High Intent',
      tailwindClass: 'bg-success-50 text-success-600'
    }
  } else if (score >= 60) {
    return {
      color: '#f59e0b',
      bgColor: '#fffbeb',
      label: 'Medium Intent',
      tailwindClass: 'bg-warning-50 text-warning-600'
    }
  } else {
    return {
      color: '#ef4444',
      bgColor: '#fef2f2',
      label: 'Low Intent',
      tailwindClass: 'bg-danger-50 text-danger-600'
    }
  }
}

/**
 * Format date to readable string
 */
export const formatDate = (date) => {
  if (!date) return 'N/A'
  const d = new Date(date)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

/**
 * Format number with decimals
 */
export const formatNumber = (num, decimals = 1) => {
  return parseFloat(num).toFixed(decimals)
}

/**
 * Get urgency color
 */
export const getUrgencyColor = (urgency) => {
  const colors = {
    'Immediate': 'bg-danger-50 text-danger-600 border-danger-200',
    'High': 'bg-warning-50 text-warning-600 border-warning-200',
    'Medium': 'bg-primary-50 text-primary-600 border-primary-200',
    'Low': 'bg-gray-50 text-gray-600 border-gray-200',
  }
  return colors[urgency] || colors['Low']
}
