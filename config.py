"""
Configuration module for Telegram Moderator Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration class"""
    
    # Telegram Bot Token (get from @BotFather)
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    
    # Database
    DATABASE_PATH = 'bot_database.db'
    
    # Default moderation settings (can be overridden by admins)
    DEFAULT_WARN_LIMIT = int(os.getenv('DEFAULT_WARN_LIMIT', '3'))
    DEFAULT_BAN_DURATION = int(os.getenv('DEFAULT_BAN_DURATION', '3600'))  # seconds
    
    # AI Moderation
    ENABLE_AI_MODERATION = os.getenv('ENABLE_AI_MODERATION', 'true').lower() == 'true'
    
    # Flood Protection
    FLOOD_THRESHOLD = int(os.getenv('FLOOD_THRESHOLD', '5'))  # messages
    FLOOD_TIME_WINDOW = int(os.getenv('FLOOD_TIME_WINDOW', '10'))  # seconds
    
    # AI Model Settings
    AI_MODEL_NAME = "distilbert-base-uncased"  # Lightweight, free model
    TOXICITY_THRESHOLD = 0.7  # 0-1, higher = more strict
    
    # Bot Info
    BOT_VERSION = "1.0.0"
    BOT_NAME = "ModeratorBot 2025"
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required. Please set it in .env file")
        return True

