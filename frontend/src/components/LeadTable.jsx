import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, AlertCircle } from 'lucide-react'
import { getScoreColor, formatDate } from '../utils/helpers'
import ScoreExplanationDrawer from './ScoreExplanationDrawer'

/**
 * Lead Table Component
 * Displays leads in a responsive table with sorting and filtering
 */
export default function LeadTable({ leads, loading, page, onPageChange, totalLeads }) {
  const [expandedLeadId, setExpandedLeadId] = useState(null)
  const [selectedLead, setSelectedLead] = useState(null)
  const [showExplanation, setShowExplanation] = useState(false)

  const itemsPerPage = 20
  const totalPages = Math.ceil(totalLeads / itemsPerPage)

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (leads.length === 0) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No leads found</p>
      </div>
    )
  }

  return (
    <>
      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        {/* Table Header */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 bg-gray-50">
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Lead Name
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Company
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Score
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Intent
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Action
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Date
                </th>
                <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">
                  Details
                </th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence>
                {leads.map((lead, idx) => {
                  const scoreColor = getScoreColor(lead.score)
                  const isExpanded = expandedLeadId === lead.id

                  return (
                    <motion.tr
                      key={lead.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className={`border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                        isExpanded ? 'bg-primary-50' : ''
                      }`}
                    >
                      <td className="px-6 py-4 text-sm">
                        <p className="font-medium text-gray-900">{lead.name}</p>
                        <p className="text-xs text-gray-600">{lead.email}</p>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {lead.company || 'N/A'}
                      </td>
                      <td className="px-6 py-4">
                        <motion.div
                          className={`inline-flex items-center justify-center w-12 h-12 rounded-full font-bold text-sm`}
                          style={{
                            backgroundColor: scoreColor.bgColor,
                            color: scoreColor.color,
                          }}
                          initial={{ scale: 0.8 }}
                          animate={{ scale: 1 }}
                        >
                          {lead.score.toFixed(0)}
                        </motion.div>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${scoreColor.tailwindClass} border-current`}
                        >
                          {scoreColor.label}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm">
                        <p className="text-gray-700 font-medium">
                          {lead.recommended_action}
                        </p>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {formatDate(lead.created_at)}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <button
                          onClick={() => {
                            setSelectedLead(lead)
                            setShowExplanation(true)
                          }}
                          className="inline-flex items-center gap-2 px-3 py-1 text-sm font-medium text-primary-600 hover:text-primary-700 hover:bg-primary-50 rounded transition-colors"
                        >
                          <ChevronDown className="w-4 h-4" />
                          View
                        </button>
                      </td>
                    </motion.tr>
                  )
                })}
              </AnimatePresence>
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="bg-white border-t border-gray-200 px-6 py-4 flex items-center justify-between">
          <div className="text-sm text-gray-600">
            Page {page + 1} of {totalPages} • {totalLeads} total leads
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => onPageChange(Math.max(0, page - 1))}
              disabled={page === 0}
              className="px-4 py-2 text-sm font-medium border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              onClick={() => onPageChange(Math.min(totalPages - 1, page + 1))}
              disabled={page >= totalPages - 1}
              className="px-4 py-2 text-sm font-medium border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>

      {/* Explanation Drawer */}
      {selectedLead && (
        <ScoreExplanationDrawer
          lead={selectedLead}
          open={showExplanation}
          onClose={() => setShowExplanation(false)}
        />
      )}
    </>
  )
}
