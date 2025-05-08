#!/bin/bash

# Startup Content Creator Setup Script
echo "Setting up Startup Content Creator..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p data output/reels

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# API ключ для OpenAI (необходим для генерации контента с использованием AI)
OPENAI_API_KEY=your_openai_api_key_here

# Настройки планировщика (время запуска в формате HH:MM)
SCHEDULER_TIME=09:00
EOL
    echo "Please edit the .env file and add your OpenAI API key."
fi

echo "Setup completed successfully!"
echo "To start using the system, run:"
echo "source venv/bin/activate && python main.py"
echo ""
echo "To schedule daily runs, use:"
echo "source venv/bin/activate && python scheduler.py" 