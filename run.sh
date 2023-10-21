#!/bin/bash

# Set the virtual environment name
VENV_NAME="yt-dlp-GUI-venv"

# Determine the Python command to use
if command -v python3 &> /dev/null
then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null
then
    PYTHON_CMD="python"
else
    echo "Python not found. Please install Python and try again."
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"

# Check if the virtual environment exists
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv $VENV_NAME
else
    echo "Virtual environment $VENV_NAME found."
fi

echo "Activating virtual environment..."
source $VENV_NAME/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Launching program..."
$PYTHON_CMD ./yt-dlp-GUI/main.py
