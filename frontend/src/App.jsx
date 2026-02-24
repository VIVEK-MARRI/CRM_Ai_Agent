import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, Users, Zap, Target, Shield } from 'lucide-react'
import KPICard from './components/KPICard'
import LeadTable from './components/LeadTable'
import ScoreLead from './components/ScoreLead'
import AnalyticsOverview from './components/AnalyticsOverview'
import { leadAPI } from './services/api'

/**
 * Main Application Component
 * 
 * Features:
 * - Lead scoring form
 * - Lead management table
 * - Analytics dashboard
 * - Real-time updates
 */
export default function App() {
  const [leads, setLeads] = useState([])
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('dashboard')
  const [page, setPage] = useState(0)
  const [totalLeads, setTotalLeads] = useState(0)

  // Fetch leads and analytics on mount and when tab changes
  useEffect(() => {
    fetchData()
  }, [page, activeTab])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Fetch leads
      if (activeTab === 'dashboard') {
        const leadsData = await leadAPI.getLeads(page, 20, 'score')
        setLeads(leadsData.leads || [])
        setTotalLeads(leadsData.total || 0)

        // Fetch analytics
        const analyticsData = await leadAPI.getAnalytics()
        setAnalytics(analyticsData)
      } else if (activeTab === 'leads') {
        const leadsData = await leadAPI.getLeads(page, 20, 'score')
        setLeads(leadsData.leads || [])
        setTotalLeads(leadsData.total || 0)
      }
    } catch (err) {
      setError(err?.message || 'Failed to fetch data')
      console.error('Error fetching data:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleLeadScored = async (newLead) => {
    // Refresh data after scoring
    await fetchData()
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center">
                <Target className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Lead Scoring Agent</h1>
                <p className="text-sm text-gray-600">AI-Powered CRM Integration</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-primary-600">
                {analytics?.total_leads || 0}
              </p>
              <p className="text-sm text-gray-600">Total Leads</p>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex gap-8" aria-label="Tabs">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: TrendingUp },
              { id: 'score', label: 'Score Lead', icon: Zap },
              { id: 'leads', label: 'All Leads', icon: Users },
            ].map(tab => {
              const Icon = tab.icon
              return (
                <motion.button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setPage(0)
                  }}
                  className={`
                    px-4 py-4 font-medium text-sm border-b-2 transition-colors
                    ${activeTab === tab.id
                      ? 'border-primary-600 text-primary-600'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                    }
                  `}
                  whileHover={{ y: -2 }}
                  whileTap={{ y: 0 }}
                >
                  <div className="flex items-center gap-2">
                    <Icon className="w-4 h-4" />
                    {tab.label}
                  </div>
                </motion.button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <motion.div
            className="mb-6 p-4 bg-danger-50 border border-danger-200 rounded-lg text-danger-700"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {error}
          </motion.div>
        )}

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* KPI Cards */}
            {analytics && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <KPICard
                  title="Avg Score"
                  value={analytics.average_score}
                  unit="/100"
                  icon={TrendingUp}
                  trend="up"
                />
                <KPICard
                  title="High Intent"
                  value={analytics.high_intent_percentage}
                  unit="%"
                  icon={Zap}
                  trend={analytics.high_intent_percentage > 30 ? 'up' : 'down'}
                />
                <KPICard
                  title="Conversion Forecast"
                  value={(analytics.conversion_forecast * 100).toFixed(1)}
                  unit="%"
                  icon={Target}
                />
                <KPICard
                  title="Avg Confidence"
                  value={analytics.average_confidence}
                  unit="%"
                  icon={Shield}
                />
              </div>
            )}

            {/* Analytics Section */}
            {analytics && <AnalyticsOverview analytics={analytics} />}
          </motion.div>
        )}

        {/* Score Lead Tab */}
        {activeTab === 'score' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <ScoreLead onLeadScored={handleLeadScored} />
          </motion.div>
        )}

        {/* Leads Table Tab */}
        {activeTab === 'leads' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
          >
            <LeadTable
              leads={leads}
              loading={loading}
              page={page}
              onPageChange={setPage}
              totalLeads={totalLeads}
            />
          </motion.div>
        )}
      </main>
    </div>
  )
}
