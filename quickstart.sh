#!/bin/bash

# Lead Scoring Agent - Quick Start Script

echo "🚀 Lead Scoring Agent - Installation & Setup"
echo "=============================================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null
then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

echo "✓ Docker found"

# Option to use Docker Compose
echo ""
echo "Choose deployment option:"
echo "1) Docker Compose (Recommended)"
echo "2) Local Development (Python + Node)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "📦 Starting with Docker Compose..."
    docker-compose up --build
    
elif [ "$choice" = "2" ]; then
    echo ""
    echo "🐍 Setting up Python backend..."
    cd backend
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo ""
    echo "🌱 Initializing database..."
    python -m seed_data.init_seed
    
    echo ""
    echo "⚙️ Starting backend server..."
    python -m uvicorn app.main:app --reload &
    BACKEND_PID=$!
    
    echo ""
    echo "📦 Installing frontend dependencies..."
    cd ../frontend
    npm install
    
    echo ""
    echo "🎨 Starting frontend dev server..."
    npm run dev &
    FRONTEND_PID=$!
    
    echo ""
    echo "✅ Application started!"
    echo "   Backend: http://localhost:8000"
    echo "   Frontend: http://localhost:5173"
    echo ""
    echo "Press Ctrl+C to stop..."
    
    wait
else
    echo "❌ Invalid choice"
    exit 1
fi
