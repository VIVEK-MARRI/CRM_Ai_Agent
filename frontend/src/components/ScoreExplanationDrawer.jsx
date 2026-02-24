import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, AlertCircle } from 'lucide-react'
import { getScoreColor, getUrgencyColor, formatDate } from '../utils/helpers'
import ScoreCircle from './ScoreCircle'

/**
 * Score Explanation Drawer
 * Detailed explanation of lead score and recommendation
 */
export default function ScoreExplanationDrawer({ lead, open, onClose }) {
  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Drawer */}
          <motion.div
            className="fixed right-0 top-0 bottom-0 w-full md:w-96 bg-white shadow-xl z-50 overflow-y-auto"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          >
            <div className="p-8">
              {/* Header */}
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Lead Details</h2>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Lead Info */}
              <div className="mb-8 pb-8 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">{lead.name}</h3>
                <div className="space-y-3">
                  <div>
                    <p className="text-xs text-gray-600 mb-1">Email</p>
                    <p className="text-sm font-medium text-gray-900">{lead.email}</p>
                  </div>
                  {lead.company && (
                    <div>
                      <p className="text-xs text-gray-600 mb-1">Company</p>
                      <p className="text-sm font-medium text-gray-900">{lead.company}</p>
                    </div>
                  )}
                  <div>
                    <p className="text-xs text-gray-600 mb-1">Date Added</p>
                    <p className="text-sm font-medium text-gray-900">
                      {formatDate(lead.created_at)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Score Section */}
              <div className="mb-8 pb-8 border-b border-gray-200">
                <p className="text-xs text-gray-600 mb-4 uppercase font-semibold">Score</p>
                <div className="flex justify-center mb-6">
                  <ScoreCircle score={lead.score} size={120} />
                </div>

                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-primary-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-900 mb-1">
                        Intent Level
                      </p>
                      <span
                        className={`inline-flex px-3 py-1 rounded-full text-xs font-medium border ${getScoreColor(lead.score).tailwindClass}`}
                      >
                        {getScoreColor(lead.score).label}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Confidence */}
              <div className="mb-8 pb-8 border-b border-gray-200">
                <p className="text-xs text-gray-600 mb-3 uppercase font-semibold">Confidence</p>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <motion.div
                    className="bg-primary-600 h-2 rounded-full"
                    initial={{ width: 0 }}
                    animate={{ width: `${lead.confidence}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
                <p className="text-sm font-medium text-gray-700">
                  {lead.confidence?.toFixed(1)}%
                </p>
              </div>

              {/* Recommended Action */}
              <div className="mb-8 pb-8 border-b border-gray-200">
                <p className="text-xs text-gray-600 mb-3 uppercase font-semibold">
                  Recommended Action
                </p>
                <div className={`p-4 rounded-lg border ${getUrgencyColor('Immediate')}`}>
                  <p className="font-medium">{lead.recommended_action}</p>
                </div>
              </div>

              {/* Feature Contributions */}
              <div>
                <p className="text-xs text-gray-600 mb-4 uppercase font-semibold">
                  Contributing Factors
                </p>
                <div className="space-y-3">
                  {lead.feature_contributions?.slice(0, 5).map((contrib, idx) => (
                    <motion.div
                      key={idx}
                      className="p-3 bg-gray-50 rounded-lg"
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <p className="text-sm font-medium text-gray-900">
                          {contrib.feature?.replace(/_/g, ' ')}
                        </p>
                        <span className="text-xs font-semibold text-primary-600">
                          {contrib.impact?.toFixed(1)}%
                        </span>
                      </div>
                      {contrib.reason && (
                        <p className="text-xs text-gray-600">{contrib.reason}</p>
                      )}
                      <div className="w-full bg-gray-200 rounded-full h-1.5 mt-2">
                        <div
                          className="bg-primary-600 h-1.5 rounded-full"
                          style={{ width: `${Math.min(contrib.impact, 100)}%` }}
                        />
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
