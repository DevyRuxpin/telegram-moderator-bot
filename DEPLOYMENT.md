# 🚀 Deployment Guide

This guide covers various deployment options for running your Telegram Moderator Bot 24/7.

## Table of Contents
1. [Local Development](#local-development)
2. [VPS Deployment](#vps-deployment)
3. [Cloud Platform Deployment](#cloud-platform-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development

Perfect for testing and development:

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python bot.py

# Keep running in background (macOS/Linux)
nohup python bot.py > bot.log 2>&1 &
```

**Pros:** Easy, free, full control
**Cons:** Computer must stay on, not reliable for production

---

## VPS Deployment

### Option 1: Using systemd (Recommended for Linux)

1. **SSH into your VPS:**
```bash
ssh user@your-vps-ip
```

2. **Clone and setup:**
```bash
# Install Python 3.11 if needed
sudo apt update
sudo apt install python3.11 python3.11-venv

# Clone repository
git clone https://github.com/yourusername/telegram-moderator-bot.git
cd telegram-moderator-bot

# Run setup
chmod +x setup.sh
./setup.sh

# Configure .env
nano .env  # Add your BOT_TOKEN
```

3. **Create systemd service:**
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Add this content:
```ini
[Unit]
Description=Telegram Moderator Bot
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/telegram-moderator-bot
Environment="PATH=/home/YOUR_USERNAME/telegram-moderator-bot/venv/bin"
ExecStart=/home/YOUR_USERNAME/telegram-moderator-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

4. **Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot

# Check status
sudo systemctl status telegram-bot

# View logs
sudo journalctl -u telegram-bot -f
```

### Option 2: Using screen/tmux

```bash
# Install screen
sudo apt install screen

# Start a screen session
screen -S telegram-bot

# Run bot
source venv/bin/activate
python bot.py

# Detach: Press Ctrl+A then D
# Reattach: screen -r telegram-bot
```

**VPS Providers:**
- **DigitalOcean** - $4-6/month, easy to use
- **Linode** - $5/month, great performance
- **Vultr** - $2.50/month (smallest plan)
- **Hetzner** - €3.29/month, excellent value

---

## Cloud Platform Deployment

### Railway (Easiest - Recommended for Beginners)

1. **Create account:** [railway.app](https://railway.app)

2. **Deploy from GitHub:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize and select your repository
   - Railway auto-detects Python

3. **Add environment variable:**
   - Go to your project → Variables
   - Add: `BOT_TOKEN` = your token
   - Save

4. **Deploy:**
   - Railway automatically deploys
   - View logs in the dashboard

**Pros:** 
- Free tier available ($5 credit/month)
- Auto-deploys on git push
- Easy setup

**Cons:**
- Limited free tier
- Less control than VPS

### Heroku

1. **Install Heroku CLI:**
```bash
brew install heroku/brew/heroku  # macOS
# or download from heroku.com
```

2. **Create Procfile:**
```bash
echo "worker: python bot.py" > Procfile
```

3. **Deploy:**
```bash
heroku login
heroku create your-bot-name
git push heroku main
heroku config:set BOT_TOKEN=your_token_here
heroku ps:scale worker=1
```

4. **Monitor:**
```bash
heroku logs --tail
```

**Note:** Heroku removed free tier in 2022. Starts at $7/month.

### Render

1. **Create account:** [render.com](https://render.com)

2. **New Background Worker:**
   - Connect GitHub repository
   - Select "Background Worker"
   - Build command: `pip install -r requirements.txt`
   - Start command: `python bot.py`

3. **Add environment variable:**
   - Add `BOT_TOKEN` in Environment section

**Pros:** Free tier available, similar to Heroku
**Cons:** Limited resources on free tier

### Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch
flyctl launch

# Set secret
flyctl secrets set BOT_TOKEN=your_token_here

# Deploy
flyctl deploy
```

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run bot
CMD ["python", "bot.py"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    container_name: telegram-moderator-bot
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./bot_database.db:/app/bot_database.db
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### Docker Hub Deployment

```bash
# Build
docker build -t yourusername/telegram-moderator-bot:latest .

# Push to Docker Hub
docker login
docker push yourusername/telegram-moderator-bot:latest

# Run on any server
docker run -d \
  --name telegram-bot \
  --restart unless-stopped \
  -e BOT_TOKEN=your_token_here \
  -v $(pwd)/bot_database.db:/app/bot_database.db \
  yourusername/telegram-moderator-bot:latest
```

---

## Monitoring & Maintenance

### Health Checks

Add to `bot.py`:
```python
import time

# Add to ModeratorBot class
async def health_check(self):
    """Periodic health check"""
    while True:
        logger.info("Bot is running - Health check OK")
        await asyncio.sleep(3600)  # Every hour
```

### Logging

View logs:
```bash
# systemd
sudo journalctl -u telegram-bot -f

# Docker
docker-compose logs -f

# Direct file
tail -f bot.log
```

### Backup Database

```bash
#!/bin/bash
# backup.sh - Run daily via cron

DATE=$(date +%Y%m%d_%H%M%S)
cp bot_database.db "backups/bot_database_$DATE.db"

# Keep only last 7 days
find backups/ -name "bot_database_*.db" -mtime +7 -delete
```

Add to crontab:
```bash
crontab -e

# Add this line (daily at 2 AM)
0 2 * * * /path/to/backup.sh
```

### Auto-restart on Failure

**systemd** (already configured with `Restart=always`)

**Docker** (already configured with `restart: unless-stopped`)

**cron:**
```bash
crontab -e

# Add this line - check every 5 minutes
*/5 * * * * cd /path/to/telegram-moderator-bot && /path/to/venv/bin/python bot.py >> bot.log 2>&1 &
```

### Update Bot

```bash
# Pull latest changes
git pull origin main

# Restart service (systemd)
sudo systemctl restart telegram-bot

# Or restart Docker
docker-compose restart

# Or kill and restart process
pkill -f "python bot.py"
source venv/bin/activate
nohup python bot.py > bot.log 2>&1 &
```

---

## Performance Tips

1. **Database Optimization:**
   - Run cleanup regularly: Add to bot as scheduled task
   - Vacuum database monthly: `sqlite3 bot_database.db "VACUUM;"`

2. **Memory Management:**
   - Monitor memory usage: `htop` or `docker stats`
   - Restart bot weekly if needed

3. **Rate Limiting:**
   - Bot handles 30 messages/second automatically
   - No additional configuration needed

4. **Logs:**
   - Rotate logs to prevent disk space issues
   - Use `logrotate` on Linux

---

## Troubleshooting

### Bot Crashes on Startup

```bash
# Check logs
sudo journalctl -u telegram-bot -n 50

# Common issues:
# 1. Missing BOT_TOKEN in .env
# 2. Wrong Python version
# 3. Missing dependencies - reinstall: pip install -r requirements.txt
```

### High Memory Usage

```bash
# Check memory
free -h

# Restart bot
sudo systemctl restart telegram-bot

# If persistent, consider upgrading VPS
```

### Database Locked

```bash
# Stop bot
sudo systemctl stop telegram-bot

# Check for other processes
lsof | grep bot_database.db

# Restart
sudo systemctl start telegram-bot
```

### Can't Connect to Telegram

```bash
# Check network
ping api.telegram.org

# Check firewall
sudo ufw status

# Test bot token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

---

## Security Checklist

- ✅ Keep `.env` file secure (never commit to git)
- ✅ Use environment variables for sensitive data
- ✅ Keep bot token secret
- ✅ Regular security updates: `sudo apt update && sudo apt upgrade`
- ✅ Use firewall: `sudo ufw enable`
- ✅ SSH key authentication (disable password login)
- ✅ Regular backups
- ✅ Monitor logs for suspicious activity

---

## Cost Comparison

| Platform | Price/Month | Best For |
|----------|-------------|----------|
| **Local PC** | $0 | Development only |
| **Railway** | $0-5 | Small groups, testing |
| **Vultr VPS** | $2.50-6 | Production, multiple bots |
| **DigitalOcean** | $4-6 | Easy setup, reliability |
| **Heroku** | $7 | Quick deployment |
| **Hetzner** | €3.29 | Best value in Europe |

---

## Need Help?

- 📖 Check [README.md](README.md)
- 💬 Create a GitHub issue
- 🐛 Enable debug logging: Set `level=logging.DEBUG` in bot.py

**Happy deploying! 🚀**

