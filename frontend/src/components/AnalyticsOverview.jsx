import React from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Users, Target, TrendingUp } from 'lucide-react'

/**
 * Analytics Overview Component
 * Displays distribution charts and metrics
 */
export default function AnalyticsOverview({ analytics }) {
  // Intent distribution data
  const intentData = [
    {
      name: 'High Intent',
      value: analytics.high_intent_count,
      percentage: analytics.high_intent_percentage,
    },
    {
      name: 'Medium Intent',
      value: analytics.medium_intent_count,
      percentage: analytics.medium_intent_percentage,
    },
    {
      name: 'Low Intent',
      value: analytics.low_intent_count,
      percentage: analytics.low_intent_percentage,
    },
  ]

  const COLORS = ['#10b981', '#f59e0b', '#ef4444']

  // Source breakdown
  const sourceData = [
    {
      name: 'Demo Requested',
      value: analytics.source_breakdown?.demo_requested || 0,
    },
    {
      name: 'Registration',
      value: analytics.source_breakdown?.registration || 0,
    },
    {
      name: 'Referral',
      value: analytics.source_breakdown?.referral || 0,
    },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Intent Distribution */}
      <motion.div
        className="bg-white rounded-lg border border-gray-200 p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
          <Target className="w-5 h-5 text-primary-600" />
          Intent Distribution
        </h3>

        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={intentData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percentage }) => `${name}: ${percentage}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {COLORS.map((color, index) => (
                <Cell key={`cell-${index}`} fill={color} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${value} leads`} />
          </PieChart>
        </ResponsiveContainer>

        {/* Legend */}
        <div className="mt-6 space-y-3">
          {intentData.map((item, idx) => (
            <motion.div
              key={idx}
              className="flex items-center justify-between p-3 bg-gray-50 rounded"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + idx * 0.1 }}
            >
              <div className="flex items-center gap-3">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: COLORS[idx] }}
                />
                <span className="text-sm font-medium text-gray-900">{item.name}</span>
              </div>
              <div className="text-right">
                <p className="text-sm font-semibold text-gray-900">{item.value}</p>
                <p className="text-xs text-gray-600">{item.percentage}%</p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Source Performance */}
      <motion.div
        className="bg-white rounded-lg border border-gray-200 p-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
          <Users className="w-5 h-5 text-primary-600" />
          Lead Source Breakdown
        </h3>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={sourceData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#0ea5e9" Name="Leads" />
          </BarChart>
        </ResponsiveContainer>

        {/* Stats */}
        <div className="mt-6 space-y-3">
          {sourceData.map((item, idx) => (
            <motion.div
              key={idx}
              className="flex items-center justify-between p-3 bg-gray-50 rounded"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 + idx * 0.1 }}
            >
              <span className="text-sm font-medium text-gray-900">{item.name}</span>
              <span className="text-sm font-semibold text-primary-600">{item.value} leads</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}
