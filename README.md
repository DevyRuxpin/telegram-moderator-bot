# 🤖 Telegram Moderator Bot 2025

A modern, AI-powered Telegram moderation bot built with Python 3.11+ and the latest Telegram Bot API (v8.3). Features intelligent content moderation, configurable warning systems, and comprehensive admin controls.

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-8.3-blue.svg)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

### 🛡️ Advanced Moderation
- **AI-Powered Content Detection**: Automatically detects spam, profanity, and toxic content
- **Configurable Warning System**: Set custom warning limits before automatic bans
- **Flexible Ban System**: Temporary or permanent bans with customizable durations
- **Flood Protection**: Prevents message spam with configurable thresholds
- **Smart Mute/Kick**: Multiple moderation actions available

### ⚙️ Admin Controls
- **Real-time Configuration**: Adjust all settings without restarting the bot
- **Custom Rules**: Set and display chat-specific rules
- **User Statistics**: Track warnings and bans for any user
- **Granular Permissions**: Full admin command system

### 🤖 AI Capabilities
- **Natural Language Processing**: Uses TextBlob for sentiment analysis
- **Profanity Detection**: Advanced filtering with better-profanity library
- **Spam Pattern Recognition**: Regex-based spam detection
- **Behavior Analysis**: Monitors user patterns for suspicious activity

### 💾 Data Management
- **SQLite Database**: Persistent storage for all moderation data
- **Async Operations**: Non-blocking database operations for performance
- **Automatic Cleanup**: Old message tracking data is automatically cleaned

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- A Telegram account
- Basic command line knowledge

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/telegram-moderator-bot.git
cd telegram-moderator-bot
```

2. **Create and activate a virtual environment** (recommended)
```bash
# Create virtual environment
python3.11 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create your bot with BotFather**
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow the instructions
   - Choose a name and username for your bot
   - **Copy the API token** you receive (it looks like `123456789:ABCdefGhIjKlmNoPQRsTUVwxyZ`)

5. **Configure the bot**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your bot token
# Replace 'your_bot_token_here_from_botfather' with your actual token
```

6. **Run the bot**
```bash
python bot.py
```

### Adding Bot to Your Group

1. **Add the bot to your Telegram group**
   - Open your group in Telegram
   - Click on the group name → "Add Members"
   - Search for your bot and add it

2. **Make the bot an administrator**
   - Go to group settings → "Administrators"
   - Add your bot as an administrator
   - Grant the following permissions:
     - ✅ Delete messages
     - ✅ Ban users
     - ✅ Restrict members
     - ✅ Pin messages (optional)
     - ✅ Invite users via link (optional)

3. **Test the bot**
   - Send `/start` in the group to verify it's working
   - Send `/help` to see all available commands

## 📚 Commands

### 👮 Moderation Commands (Admin Only)

| Command | Description | Usage |
|---------|-------------|-------|
| `/warn` | Warn a user | Reply to their message with `/warn [reason]` |
| `/unwarn` | Remove warnings | Reply to their message with `/unwarn` |
| `/ban` | Ban a user permanently | Reply to their message with `/ban [reason]` |
| `/unban` | Unban a user | Reply to message or `/unban <user_id>` |
| `/kick` | Kick a user | Reply to their message with `/kick [reason]` |
| `/mute` | Mute a user | Reply to their message with `/mute` |
| `/unmute` | Unmute a user | Reply to their message with `/unmute` |

### ⚙️ Configuration Commands (Admin Only)

| Command | Description | Usage |
|---------|-------------|-------|
| `/setwarnlimit` | Set warnings before ban | `/setwarnlimit 3` |
| `/setbanduration` | Set default ban duration (seconds) | `/setbanduration 3600` |
| `/toggleai` | Enable/disable AI moderation | `/toggleai` |
| `/setfloodlimit` | Set flood protection | `/setfloodlimit 5 10` |
| `/config` | View current configuration | `/config` |
| `/setrules` | Set chat rules | `/setrules Be nice and respectful` |
| `/userstats` | Get user statistics | Reply to message with `/userstats` |

### ℹ️ General Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message |
| `/help` | Show help message |
| `/rules` | View chat rules |

## 🔧 Configuration

### Environment Variables

Edit the `.env` file to configure default settings:

```env
# Required
BOT_TOKEN=your_bot_token_here

# Optional (defaults shown)
DEFAULT_WARN_LIMIT=3              # Warnings before ban
DEFAULT_BAN_DURATION=3600         # Ban duration in seconds (1 hour)
ENABLE_AI_MODERATION=true         # Enable AI content filtering
FLOOD_THRESHOLD=5                 # Messages allowed...
FLOOD_TIME_WINDOW=10              # ...in this many seconds
```

### Runtime Configuration

All settings can be changed while the bot is running using admin commands:

```bash
/setwarnlimit 5           # Allow 5 warnings before ban
/setbanduration 7200      # Set 2-hour default ban
/toggleai                 # Toggle AI moderation
/setfloodlimit 10 15      # Allow 10 messages per 15 seconds
```

## 🧠 AI Moderation

The bot uses multiple techniques to detect problematic content:

### Detection Methods

1. **Profanity Filter**: Uses the `better-profanity` library with an extensive word list
2. **Spam Detection**: Recognizes patterns like:
   - Excessive URLs
   - Repeated characters
   - ALL CAPS MESSAGES
   - Too many emojis
3. **Sentiment Analysis**: Uses TextBlob to detect negative/aggressive language
4. **Keyword Matching**: Flags toxic keywords and harassment patterns
5. **Behavior Monitoring**: Tracks user patterns for flood detection

### Customization

To customize AI behavior, edit `ai_moderator.py`:

```python
# Add custom toxic keywords
self.toxic_keywords = [
    'your_keyword_here',
    # ... more keywords
]

# Adjust spam patterns
self.spam_patterns = [
    r'your_regex_pattern',
    # ... more patterns
]
```

## 📊 Database Schema

The bot uses SQLite with the following tables:

- **warnings**: User warnings with reasons and timestamps
- **bans**: Ban records with durations
- **chat_config**: Per-chat configuration settings
- **user_messages**: Message tracking for flood detection
- **admins**: Admin user list (future feature)

## 🔒 Security & Privacy

- ✅ All data stored locally in SQLite
- ✅ No external API calls (except Telegram)
- ✅ No user message content stored permanently
- ✅ Admin-only access to moderation commands
- ✅ Message tracking data auto-expires after 24 hours

## 🐛 Troubleshooting

### Bot Not Responding
1. Check if bot is running: `python bot.py`
2. Verify bot token in `.env` file
3. Ensure bot has admin permissions in the group
4. Check console for error messages

### AI Moderation Too Strict/Lenient
- Adjust settings in `ai_moderator.py`
- Or disable AI and use manual moderation: `/toggleai`

### Database Errors
- Delete `bot_database.db` to reset (⚠️ loses all data)
- Or restore from backup

### Permission Errors
- Verify bot is an administrator
- Check that required permissions are granted
- Some features require specific permissions

## 🚀 Advanced Usage

### Running as a Service (Linux)

Create a systemd service file `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Moderator Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/telegram-bot
Environment="PATH=/path/to/telegram-bot/venv/bin"
ExecStart=/path/to/telegram-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t telegram-moderator-bot .
docker run -d --name modbot --env-file .env telegram-moderator-bot
```

### Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI, then:
heroku create your-bot-name
git push heroku main
heroku config:set BOT_TOKEN=your_token_here
```

#### Railway
1. Connect your GitHub repository
2. Add `BOT_TOKEN` environment variable
3. Deploy automatically

#### VPS (DigitalOcean, Linode, etc.)
```bash
# SSH into your VPS
ssh user@your-vps-ip

# Clone and setup
git clone https://github.com/yourusername/telegram-moderator-bot.git
cd telegram-moderator-bot
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env file
nano .env

# Run with screen or tmux for persistence
screen -S telegram-bot
python bot.py
# Press Ctrl+A then D to detach
```

## 📈 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Custom filter rules
- [ ] Integration with external APIs
- [ ] Machine learning model training
- [ ] Webhook support for better performance
- [ ] Web-based admin panel
- [ ] Backup and restore functionality
- [ ] Rate limiting per user
- [ ] Captcha for new members

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://python-telegram-bot.org/) - The amazing library that powers this bot
- [Telegram](https://telegram.org/) - For providing an excellent Bot API
- [better-profanity](https://github.com/snguyenthanh/better_profanity) - Profanity detection
- [TextBlob](https://textblob.readthedocs.io/) - NLP and sentiment analysis

## 📧 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/telegram-moderator-bot/issues)
3. Create a new issue with detailed information
4. Join our [Telegram support group](https://t.me/your_support_group)

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ for the Telegram community**

**Version 1.0.0** | **October 2025**

