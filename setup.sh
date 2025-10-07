#!/bin/bash

# Telegram Moderator Bot Setup Script
# This script automates the setup process

echo "🤖 Telegram Moderator Bot Setup"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 not found. Please install Python 3.11 or higher."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3.11 --version)
echo "✅ Found $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3.11 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: You need to edit .env and add your bot token!"
    echo "   1. Open .env in a text editor"
    echo "   2. Replace 'your_bot_token_here_from_botfather' with your actual token"
    echo "   3. Get your token from @BotFather on Telegram"
else
    echo "⚠️  .env file already exists. Skipping..."
fi
echo ""

echo "✨ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env and add your bot token (get it from @BotFather)"
echo "   2. Run the bot: python bot.py"
echo "   3. Add the bot to your group and make it an admin"
echo ""
echo "📚 For more information, see README.md"
echo ""

