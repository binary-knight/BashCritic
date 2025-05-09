#!/bin/bash

set -e

echo "Installing BashCritic..."

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "Python3 not found. Please install Python 3."
  exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate

# Upgrade pip & install requirements
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

# Check Ollama
if ! command -v ollama &> /dev/null; then
  echo "Installing Ollama..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "Ollama is already installed."
fi

# Extract model name from config
MODEL=$(grep '^model:' config.yaml | awk '{print $2}' || echo "mistral")

# Pull model if not already present
echo "Pulling model: $MODEL"
ollama pull "$MODEL"

# Create reports folder
mkdir -p reports
echo "Created reports/ folder"

echo "BashCritic installation complete!"
echo ""
echo "To activate your environment and run:"
echo "  source venv/bin/activate && python3 bashcritic.py --file yourscript.sh"
