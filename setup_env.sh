#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the dependencies
pip install -r requirements.txt

echo "✅ Virtual environment created."
