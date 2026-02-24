import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown } from 'lucide-react'

/**
 * KPI Card Component
 * Displays key performance indicators with icons and trends
 */
export default function KPICard({ title, value, unit, icon: Icon, trend }) {
  if (!Icon) {
    console.warn(`KPICard: icon prop is required. Received: ${Icon}`)
    return null
  }
  
  return (
    <motion.div
      className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-lg"
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-2">{title}</p>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-gray-900">
              {parseFloat(value).toFixed(1)}
            </span>
            <span className="text-lg text-gray-500">{unit}</span>
          </div>
        </div>
        <div className="w-12 h-12 bg-primary-50 rounded-lg flex items-center justify-center">
          <Icon className="w-6 h-6 text-primary-600" />
        </div>
      </div>

      {trend && (
        <div className="mt-4 flex items-center gap-2">
          {trend === 'up' ? (
            <>
              <TrendingUp className="w-4 h-4 text-success-600" />
              <span className="text-sm text-success-600">Positive trend</span>
            </>
          ) : (
            <>
              <TrendingDown className="w-4 h-4 text-danger-600" />
              <span className="text-sm text-danger-600">Needs attention</span>
            </>
          )}
        </div>
      )}
    </motion.div>
  )
}
