#!/bin/bash

# Quick start script for Streamlit Dashboard

echo "🚀 Starting DataFrame Q&A Benchmark Dashboard..."
echo ""

# Check if results exist
RESULT_COUNT=$(ls results/*.json 2>/dev/null | wc -l)

if [ $RESULT_COUNT -eq 0 ]; then
    echo "⚠️  Warning: No benchmark results found in results/ directory"
    echo ""
    echo "Run benchmarks first:"
    echo "  python3 main.py --dataset iris --save-results"
    echo "  ./benchmark_external.sh"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Found $RESULT_COUNT benchmark result(s)"
fi

echo ""
echo "📊 Launching Streamlit dashboard..."
echo ""
echo "Dashboard will open at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

# Start Streamlit
streamlit run streamlit_app.py
