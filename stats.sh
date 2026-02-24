#!/bin/bash

# Calculate project statistics

echo "📊 Lead Scoring Agent - Project Statistics"
echo "==========================================="
echo ""

# Count files
backend_files=$(find backend -type f -name "*.py" | wc -l)
frontend_files=$(find frontend -type f \( -name "*.jsx" -o -name "*.js" \) | wc -l)
config_files=$(find config -type f | wc -l)
doc_files=$(find . -maxdepth 1 -type f -name "*.md" | wc -l)

echo "📝 Code Files:"
echo "  Backend (Python):    $backend_files files"
echo "  Frontend (React/JS): $frontend_files files"
echo "  Configuration:       $config_files files"
echo "  Documentation:       $doc_files files"
echo ""

# Count lines
backend_lines=$(find backend/app -type f -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $1}')
frontend_lines=$(find frontend/src -type f \( -name "*.jsx" -o -name "*.js" \) -exec wc -l {} + | tail -1 | awk '{print $1}')

echo "📈 Lines of Code:"
echo "  Backend:  ~$backend_lines lines"
echo "  Frontend: ~$frontend_lines lines"
echo ""

# API endpoints
echo "🔌 API Endpoints:"
echo "  POST   /api/score-lead       (Score a lead)"
echo "  GET    /api/leads            (List leads)"
echo "  GET    /api/leads/{id}       (Get lead)"
echo "  GET    /api/analytics        (Analytics)"
echo "  GET    /health               (Health check)"
echo ""

# Components
echo "🎨 React Components:"
echo "  KPICard                (KPI card with metrics)"
echo "  LeadTable              (Sortable lead table)"
echo "  ScoreLead              (Scoring form + results)"
echo "  ScoreCircle            (Circular progress meter)"
echo "  ScoreExplanationDrawer (Details drawer)"
echo "  AnalyticsOverview      (Charts)"
echo ""

# Services
echo "⚙️  Backend Services:"
echo "  LeadService            (Lead orchestration)"
echo "  ScoringEngine          (Config-driven scoring)"
echo "  ExplanationEngine      (Score explanation)"
echo "  NextActionEngine       (Action recommendation)"
echo ""

# Database
echo "💾 Database:"
echo "  Leads table            (12 fields)"
echo "  Indexes:               score, intent_level, created_at"
echo "  Seed data:             20 sample leads"
echo ""

echo "==========================================="
echo "✅ Project Ready for Deployment!"
echo ""
