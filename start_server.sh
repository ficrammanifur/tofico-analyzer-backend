#!/bin/bash
echo "🚀 Starting Tofico Analyzer Backend..."
echo "📊 Port: 8000"
echo "🗄️ Database: tofico_analyzer"
echo ""

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate  # Windows
fi

# Install dependencies if needed
if [ ! -f "requirements_installed.flag" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements_normalized.txt
    touch requirements_installed.flag
fi

# Setup database if needed
if [ ! -f "database_setup.flag" ]; then
    echo "🗄️ Setting up database..."
    python setup_normalized_db.py
    touch database_setup.flag
fi

# Start server
echo "🚀 Starting FastAPI server on port 8000..."
python main_normalized.py
