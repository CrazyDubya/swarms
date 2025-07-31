#!/bin/bash

# Quick-start script for AI Research Platform Demo
# This script sets up the environment and runs the demo

echo "🚀 AI Research Platform Demo - Quick Start"
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "demo_research_platform.py" ]; then
    echo "❌ Error: demo_research_platform.py not found"
    echo "Please run this script from the swarms repository root directory"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
python -c "import swarms" 2>/dev/null || {
    echo "⚠️  Installing swarms package..."
    pip install -e .
}

python -c "import termcolor" 2>/dev/null || {
    echo "⚠️  Installing termcolor..."
    pip install termcolor
}

# Run tests first
echo ""
echo "🧪 Running demo tests..."
python test_demo.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed! Starting interactive demo..."
    echo ""
    
    # Run the demo
    python demo_research_platform.py
else
    echo ""
    echo "❌ Tests failed. Please check the errors above."
    exit 1
fi

echo ""
echo "👋 Demo completed. Thank you for trying the Swarms framework!"