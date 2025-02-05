#!/bin/bash

# Create and activate virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
if ! command -v ollama &> /dev/null; then
    curl https://ollama.ai/install.sh | sh
fi

# Pull the Mistral model
ollama pull mistral 