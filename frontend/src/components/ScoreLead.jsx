import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, CheckCircle, AlertCircle } from 'lucide-react'
import { leadAPI } from '../services/api'
import { getScoreColor } from '../utils/helpers'
import ScoreCircle from './ScoreCircle'

/**
 * Score Lead Component
 * Form to input lead data and get scoring results
 */
export default function ScoreLead({ onLeadScored }) {
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    company: '',
    demo_requested: false,
    registration: false,
    enquiry_call_whatsapp: false,
    enquiry_date: '',
    pricing_compared: false,
    lead_through_events: false,
    lead_through_call: false,
    lead_through_referral: false,
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const submitData = {
        ...formData,
        enquiry_date: formData.enquiry_date ? new Date(formData.enquiry_date).toISOString() : null,
      }

      const response = await leadAPI.scoreLead(submitData)
      setResult(response)
      onLeadScored(response)

      // Reset form
      setFormData({
        email: '',
        name: '',
        company: '',
        demo_requested: false,
        registration: false,
        enquiry_call_whatsapp: false,
        enquiry_date: '',
        pricing_compared: false,
        lead_through_events: false,
        lead_through_call: false,
        lead_through_referral: false,
      })
    } catch (err) {
      setError(err?.detail || 'Failed to score lead')
    } finally {
      setLoading(false)
    }
  }

  const checkboxes = [
    { name: 'demo_requested', label: 'Demo Requested' },
    { name: 'registration', label: 'Registration Completed' },
    { name: 'enquiry_call_whatsapp', label: 'Enquiry via Call/WhatsApp' },
    { name: 'pricing_compared', label: 'Pricing Compared' },
    { name: 'lead_through_events', label: 'Lead from Events' },
    { name: 'lead_through_call', label: 'Lead from Direct Call' },
    { name: 'lead_through_referral', label: 'Referral Lead' },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* Form Section */}
      <motion.div
        className="bg-white rounded-lg border border-gray-200 p-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-8">Score a New Lead</h2>

        {error && (
          <motion.div
            className="mb-6 p-4 bg-danger-50 border border-danger-200 rounded-lg text-danger-700 flex items-start gap-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <span>{error}</span>
          </motion.div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Text Inputs */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Email *
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                placeholder="john@example.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-900 mb-2">
                Name *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                placeholder="John Doe"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Company
            </label>
            <input
              type="text"
              name="company"
              value={formData.company}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
              placeholder="Acme Corp"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Enquiry Date
            </label>
            <input
              type="datetime-local"
              name="enquiry_date"
              value={formData.enquiry_date}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
            />
          </div>

          {/* Checkboxes */}
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-4">
              Engagement Signals
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {checkboxes.map(checkbox => (
                <motion.label
                  key={checkbox.name}
                  className="flex items-center gap-3 cursor-pointer p-2 hover:bg-gray-50 rounded transition-colors"
                  whileHover={{ x: 4 }}
                >
                  <input
                    type="checkbox"
                    name={checkbox.name}
                    checked={formData[checkbox.name]}
                    onChange={handleChange}
                    className="w-4 h-4 rounded border-gray-300 text-primary-600 cursor-pointer"
                  />
                  <span className="text-sm text-gray-700">{checkbox.label}</span>
                </motion.label>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <motion.button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 text-white font-medium py-3 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Scoring...
              </span>
            ) : (
              'Score Lead'
            )}
          </motion.button>
        </form>
      </motion.div>

      {/* Results Section */}
      <AnimatePresence>
        {result && (
          <motion.div
            className="bg-white rounded-lg border border-gray-200 p-8"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-8 flex items-center gap-2">
              <CheckCircle className="w-6 h-6 text-success-600" />
              Scoring Results
            </h2>

            {/* Score Circle */}
            <div className="mb-8 flex justify-center">
              <ScoreCircle score={result.score} size={200} />
            </div>

            {/* Results Details */}
            <div className="space-y-6">
              {/* Intent Level */}
              <div>
                <p className="text-sm text-gray-600 mb-2">Intent Level</p>
                <div className={`inline-flex items-center px-4 py-2 rounded-full font-medium border ${getScoreColor(result.score).tailwindClass}`}>
                  {getScoreColor(result.score).label}
                </div>
              </div>

              {/* Confidence */}
              <div>
                <p className="text-sm text-gray-600 mb-2">Confidence Score</p>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <motion.div
                    className="bg-primary-600 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${result.confidence}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
                <p className="text-sm font-medium text-gray-700 mt-2">
                  {result.confidence.toFixed(1)}%
                </p>
              </div>

              {/* Recommended Action */}
              <div>
                <p className="text-sm text-gray-600 mb-2">Recommended Action</p>
                <p className="font-medium text-gray-900">{result.recommended_action}</p>
              </div>

              {/* Top Contributions */}
              <div>
                <p className="text-sm text-gray-600 mb-3">Top Contributing Factors</p>
                <div className="space-y-2">
                  {result.explanation?.feature_contributions?.slice(0, 3).map((contrib, idx) => (
                    <motion.div
                      key={idx}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded"
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      <span className="text-sm font-medium text-gray-700">
                        {contrib.feature.replace(/_/g, ' ')}
                      </span>
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${Math.min(contrib.impact, 100)}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-600 w-10">
                          {contrib.impact.toFixed(0)}%
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
