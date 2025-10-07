# 🚀 Quick Start Guide

Get your Telegram Moderator Bot running in 5 minutes!

## Step 1: Install Python (if needed)

Make sure you have Python 3.11 or higher installed:

```bash
python3.11 --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

## Step 2: Run Setup Script

We've made it super easy! Just run:

```bash
# Make the script executable (first time only)
chmod +x setup.sh

# Run setup
./setup.sh
```

This will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Create your `.env` file

## Step 3: Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name: `My Moderator Bot`
4. Choose a username: `my_moderator_bot` (must end with 'bot')
5. **Copy the token** (looks like: `123456789:ABCdefGhIjKlmNoPQRsTUVwxyZ`)

## Step 4: Configure Your Bot

Open the `.env` file and add your token:

```bash
# Edit with your favorite editor
nano .env
# or
vim .env
# or
code .env  # VS Code
```

Replace this line:
```
BOT_TOKEN=your_bot_token_here_from_botfather
```

With your actual token:
```
BOT_TOKEN=123456789:ABCdefGhIjKlmNoPQRsTUVwxyZ
```

Save and exit.

## Step 5: Run Your Bot

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the bot
python bot.py
```

You should see:
```
INFO - Starting ModeratorBot 2025 v1.0.0
INFO - Database initialized
```

**🎉 Your bot is running!**

## Step 6: Add Bot to Your Group

1. Open your Telegram group
2. Click the group name → "Add Members"
3. Search for your bot's username
4. Add it to the group

## Step 7: Make Bot an Administrator

1. Go to group settings → "Administrators"
2. Click "Add Administrator"
3. Select your bot
4. Grant these permissions:
   - ✅ Delete messages
   - ✅ Ban users
   - ✅ Restrict members
   - ✅ Pin messages
   - ✅ Invite users via link

## Step 8: Test Your Bot

In the group chat, send:

```
/start
```

You should get a welcome message!

Try:
```
/help
```

To see all available commands.

## 🎯 Common First Actions

### Set Warning Limit
```
/setwarnlimit 3
```

### Set Ban Duration (1 hour = 3600 seconds)
```
/setbanduration 3600
```

### View Configuration
```
/config
```

### Set Chat Rules
```
/setrules Be respectful, no spam, no NSFW content
```

### Test Moderation
Have someone send a test message with profanity - the bot should automatically detect and warn them!

## 🆘 Troubleshooting

### Bot not responding?
- Check if `bot.py` is still running
- Make sure you added the correct token in `.env`
- Verify bot is an administrator in the group

### Can't run setup.sh?
Run manually:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Permission errors?
Make sure bot has admin permissions in the group!

## 📚 Next Steps

- Read the full [README.md](README.md) for all features
- Customize AI moderation in `ai_moderator.py`
- Set up automatic startup (see README advanced section)
- Join our community for support!

---

**Need help?** Check [README.md](README.md) or create an issue on GitHub!

