#!/bin/bash

# Run all available datasets benchmarks

echo "🚀 Running All Dataset Benchmarks"
echo "=================================="
echo ""

# List of all available datasets
DATASETS=(
    "iris"
    "wine" 
    "diabetes"
    "sales"
    "ecommerce"
    "employees"
    "titanic"
    "happiness"
    "supermarket"
    "covid"
    "stackoverflow"
    "california_housing"
)

TOTAL=${#DATASETS[@]}
CURRENT=0

for dataset in "${DATASETS[@]}"; do
    CURRENT=$((CURRENT + 1))
    echo "[$CURRENT/$TOTAL] Running benchmark for: $dataset"
    echo "-------------------------------------------"
    
    python3 main.py --dataset "$dataset" --save-results
    
    if [ $? -eq 0 ]; then
        echo "✅ Completed: $dataset"
    else
        echo "❌ Failed: $dataset"
    fi
    
    echo ""
done

echo "=================================="
echo "🎉 All benchmarks completed!"
echo ""
echo "Results saved in: results/"
echo "Total datasets: $TOTAL"
echo ""
echo "Next steps:"
echo "  1. Launch dashboard: python3 -m streamlit run streamlit_app.py"
echo "  2. View results and enable LLM Judge"
echo "  3. Download datasets and logs as needed"
echo ""
