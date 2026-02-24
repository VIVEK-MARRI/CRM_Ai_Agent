import React from 'react'
import { motion } from 'framer-motion'
import { getScoreColor } from '../utils/helpers'

/**
 * Score Circle Component
 * Animated circular progress meter for displaying scores
 */
export default function ScoreCircle({ score, size = 200 }) {
  const radius = (size - 20) / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (score / 100) * circumference

  const scoreColor = getScoreColor(score)

  return (
    <div className="inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="8"
        />

        {/* Progress circle */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={scoreColor.color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          animate={{ strokeDashoffset }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          strokeLinecap="round"
        />
      </svg>

      {/* Center text */}
      <div className="absolute flex flex-col items-center justify-center">
        <motion.div
          className="text-4xl font-bold"
          style={{ color: scoreColor.color }}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          {score.toFixed(0)}
        </motion.div>
        <div
          className="text-sm font-medium mt-1"
          style={{ color: scoreColor.color }}
        >
          {scoreColor.label}
        </div>
      </div>
    </div>
  )
}
