#!/bin/bash

echo "====================================="
echo "Dashboard Q&A Benchmark - Quick Start"
echo "====================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""
echo "ℹ️  Примечание: requirements.txt устанавливает Streamlit UI; для CLI используйте requirements-benchmarks.txt"
echo ""

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your OPENAI_API_KEY"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

# Check if OPENAI_API_KEY is set
source .env 2>/dev/null
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY is not set in .env file"
    echo "   Please edit .env and add your OpenAI API key"
    echo ""
else
    echo "✓ OPENAI_API_KEY is configured"
    echo ""
fi

echo "====================================="
echo "Setup complete!"
echo "====================================="
echo ""
echo "To run the benchmark:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. List datasets: python main.py --list-datasets"
echo "  3. Run benchmark: python main.py --dataset iris"
echo ""
echo "For more options: python main.py --help"
echo ""
