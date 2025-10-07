# 🔧 Troubleshooting Guide

Quick solutions to common problems.

---

## 🚨 Emergency Quick Fixes

### Bot Completely Broken?
```bash
# Stop bot
Press Ctrl+C

# Restart bot
python bot.py
```

### Still Not Working?
```bash
# Reinstall dependencies
./setup.sh

# Restart
python bot.py
```

### Nuclear Option (Last Resort)
```bash
# Backup database
cp bot_database.db bot_database_backup.db

# Delete database (⚠️ loses all data!)
rm bot_database.db

# Restart bot (creates fresh database)
python bot.py
```

---

## 🤖 Bot Not Responding

### Symptom:
Commands don't work, bot doesn't reply

### Possible Causes & Solutions:

#### 1. Bot Not Running
**Check:**
```bash
ps aux | grep bot.py
```

**Fix:**
```bash
python bot.py
```

#### 2. Bot Not Admin
**Check:** Group settings → Administrators → Is bot listed?

**Fix:** Add bot as administrator with these permissions:
- ✅ Delete messages
- ✅ Ban users
- ✅ Restrict members

#### 3. Wrong Bot Token
**Check:** `.env` file has correct token

**Fix:**
```bash
nano .env
# Make sure BOT_TOKEN=... has your actual token
```

#### 4. Bot Removed from Group
**Check:** Is bot still in member list?

**Fix:** Re-add bot to group

---

## ⚠️ Commands Not Working

### Symptom:
You type commands but nothing happens

### Solutions by Error:

#### "This command is only for admins"
**Cause:** You're not a group admin

**Fix:**
- Ask group owner to make you admin
- OR use owner account

#### No Response at All
**Cause:** Command spelled wrong or bot not running

**Fix:**
1. Check spelling (commands start with `/`)
2. Try `/help` to see all commands
3. Verify bot is running: `ps aux | grep bot.py`

#### "Please reply to a user's message"
**Cause:** Some commands need you to reply to someone's message

**Fix:** 
1. Find a message from the user
2. Reply to it
3. Type the command

**Example:**
```
User sends: "Hello"
You: (Reply to their message) /warn Testing
```

---

## 🤖 AI Detection Issues

### AI Too Strict (False Positives)

**Symptom:** Bot warns innocent messages

**Quick Fix:**
```
/toggleai
```
Turns AI off, use manual moderation only

**Better Fix:** Make AI more lenient:
```
/setwarnlimit 7
```
Gives more warnings before ban

**Best Fix:** Clear false warnings:
```
/unwarn
```
(Reply to the user's message)

### AI Too Lenient (Misses Violations)

**Symptom:** Spam/profanity not detected

**Check if AI is enabled:**
```
/config
```
Look for "AI Moderation: ✅ Enabled"

**Fix if disabled:**
```
/toggleai
```

**If still not catching:**
- AI uses patterns/keywords, some things slip through
- Use manual `/warn` command
- Or edit `ai_moderator.py` to add patterns

---

## 🚫 Ban/Kick Not Working

### Symptom:
User doesn't get banned/kicked

### Solutions:

#### Bot Lacks Permissions
**Check:** Bot admin settings in group

**Fix:** Grant "Ban users" permission to bot

#### User is Admin
**Cause:** Can't ban other admins

**Fix:** Demote user first, then ban

#### Telegram Error
**Symptom:** Error message appears

**Common Errors:**
- "User not found" - They left already
- "Not enough rights" - Bot needs admin permissions
- "User is admin" - Can't ban admins

---

## 💾 Database Errors

### Symptom:
"Database locked" or "Database error"

### Solutions:

#### Database Locked
**Cause:** Multiple instances running or file locked

**Fix:**
```bash
# Stop all instances
pkill -f bot.py

# Restart once
python bot.py
```

#### Corrupted Database
**Symptom:** Crashes, weird errors

**Fix (with backup):**
```bash
# Stop bot
Ctrl+C

# Restore from backup
cp backups/bot_database_YYYYMMDD.db bot_database.db

# Restart
python bot.py
```

**Fix (no backup - ⚠️ loses data):**
```bash
# Delete corrupted database
rm bot_database.db

# Restart (creates fresh)
python bot.py
```

#### Permission Errors
**Symptom:** "Permission denied" on database file

**Fix:**
```bash
chmod 644 bot_database.db
```

---

## 🌊 Flood Protection Issues

### Users Getting Flood Warnings Incorrectly

**Symptom:** Normal users triggered flood protection

**Fix - Make More Lenient:**
```
/setfloodlimit 10 15
```
Allows 10 messages per 15 seconds (instead of default 5/10)

**Fix - Turn Off:**
```
/setfloodlimit 100 10
```
Basically disables flood protection

### Flood Protection Not Working

**Symptom:** Spammers not caught

**Fix - Make Stricter:**
```
/setfloodlimit 3 10
```
Only 3 messages per 10 seconds

**Check Settings:**
```
/config
```
Verify flood settings

---

## 🔑 Setup & Installation Issues

### "Module not found" Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'telegram'
```

**Fix:**
```bash
# Install dependencies
./setup.sh

# Or manually:
pip install -r requirements.txt
```

### "Permission denied: ./setup.sh"

**Fix:**
```bash
chmod +x setup.sh
./setup.sh
```

### Python Version Error

**Symptom:**
```
Python 3.11+ required
```

**Fix:**
- Install Python 3.11 or newer
- Use `python3.11` command specifically:
```bash
python3.11 bot.py
```

### "BOT_TOKEN not found"

**Symptom:**
```
ValueError: BOT_TOKEN is required
```

**Fix:**
```bash
# Create .env file
cp .env.example .env

# Edit and add your token
nano .env
```

---

## 🔄 Bot Keeps Crashing

### Symptom:
Bot starts but crashes after a while

### Common Causes:

#### 1. Memory Issues
**Check:**
```bash
free -h
```

**Fix:** Use lighter deployment (VPS with more RAM)

#### 2. Network Issues
**Check:** Internet connection stable?

**Fix:** Restart network or move to better hosting

#### 3. Telegram API Issues
**Check:** Can you access telegram.org?

**Fix:** Wait and retry (Telegram issues are temporary)

#### 4. Code Errors
**Check logs:** Look for error messages when it crashes

**Fix:** Report to developer with error message

### Run in Debug Mode:
```bash
python bot.py 2>&1 | tee bot_debug.log
```
This saves all output to a file for analysis

---

## 📊 Performance Issues

### Bot Slow to Respond

**Possible Causes:**
1. High load on server
2. Database too large
3. Network latency

**Fixes:**
```bash
# Clean old data
sqlite3 bot_database.db "DELETE FROM user_messages WHERE timestamp < datetime('now', '-7 days');"

# Vacuum database
sqlite3 bot_database.db "VACUUM;"

# Restart bot
pkill -f bot.py
python bot.py
```

### High CPU Usage

**Check:**
```bash
top
```

**Fixes:**
- Turn off AI if not needed: `/toggleai`
- Move to better server
- Check for infinite loops (rare, report to developer)

---

## 🔐 Security Concerns

### Bot Token Exposed

**If token leaked:**
1. Go to @BotFather
2. Send `/token`
3. Select your bot
4. Generate new token
5. Update `.env` file with new token
6. Restart bot

### Unauthorized Admin Commands

**Symptom:** Non-admins can use admin commands

**This shouldn't happen!** If it does:
1. Restart bot immediately
2. Check code hasn't been modified
3. Report to developer

---

## 📱 Telegram-Specific Issues

### "Bad Request: Message to Delete Not Found"

**Cause:** Trying to delete old/already deleted message

**Fix:** This is normal, just means message was already handled. Ignore.

### "Conflict: Terminated by Other getUpdates"

**Cause:** Two instances of bot running

**Fix:**
```bash
# Stop all instances
pkill -f bot.py

# Start one instance
python bot.py
```

### "Flood Wait" Error

**Cause:** Bot sending too many requests to Telegram

**Fix:** 
- Wait a few minutes
- Bot has built-in rate limiting
- If persistent, report to developer

---

## 🗂️ File & Directory Issues

### "No such file or directory"

**Symptom:** Bot can't find files

**Fix:**
```bash
# Make sure you're in the right directory
cd /path/to/telegram-bot

# Verify files exist
ls -la
```

### Database File Missing

**Symptom:** "bot_database.db not found" but it should exist

**Fix:**
- Bot creates it automatically on first run
- If deleted, bot will recreate (but data is lost)
- Restore from backup if needed

---

## 🌐 Networking Issues

### "Connection Timeout"

**Cause:** Can't reach Telegram servers

**Check:**
```bash
ping api.telegram.org
```

**Fix:**
- Check internet connection
- Check firewall isn't blocking
- Wait and retry (might be temporary)

### "SSL Certificate Error"

**Cause:** System time wrong or certificate issue

**Fix:**
```bash
# Check system time
date

# Update system if needed
# On Linux:
sudo apt update && sudo apt upgrade
```

---

## 🔄 Update & Migration Issues

### Bot Broken After Update

**Fix:**
```bash
# Restore from backup
cp backups/bot_database_backup.db bot_database.db

# Reinstall dependencies
pip install -r requirements.txt

# Restart
python bot.py
```

### Settings Lost After Restart

**This shouldn't happen!** Settings are in database.

**Check:**
- Is `bot_database.db` present?
- Was it accidentally deleted?
- Restore from backup

---

## 📋 Diagnostic Commands

### Check Bot Status
```bash
# Is it running?
ps aux | grep bot.py

# Check logs
tail -f bot.log

# Check process details
lsof -p $(pgrep -f bot.py)
```

### Check Database
```bash
# Open database
sqlite3 bot_database.db

# Count warnings
SELECT COUNT(*) FROM warnings;

# Count bans
SELECT COUNT(*) FROM bans;

# Exit
.exit
```

### Test Bot Health
```bash
# Run verification
./run_verification.sh

# Run tests
python test_bot.py
```

---

## 🆘 When to Get Help

### Try These First:
1. Restart bot
2. Check this guide
3. Check FAQ.md
4. Check error logs

### Get Help If:
- Bot won't start at all
- Database corrupted with no backup
- Errors you don't understand
- Security concerns
- Need custom features

### Contact Support:
See CLIENT_HANDOFF.md for support information

### Provide This Info:
1. Error message (exact text)
2. What you were doing when it happened
3. Output of `./run_verification.sh`
4. Bot version (see bot.py first line)

---

## 📝 Error Message Guide

### Common Errors Explained:

| Error | Meaning | Fix |
|-------|---------|-----|
| "Module not found" | Library not installed | Run `./setup.sh` |
| "Permission denied" | No admin rights | Make bot admin |
| "Token invalid" | Wrong bot token | Check `.env` file |
| "Database locked" | Multiple instances | Stop all, start one |
| "Connection timeout" | Network issue | Check internet |
| "Bad Request" | Telegram API error | Check bot permissions |

---

## 🔍 Debug Mode

### Enable Detailed Logging:

Edit `bot.py`, change logging level:
```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Change INFO to DEBUG
)
```

Then restart bot. You'll see much more detailed output.

**Remember to change back to INFO after debugging!**

---

## ✅ Prevention Tips

### Avoid Issues:

1. **Regular Backups**
   ```bash
   cp bot_database.db backups/bot_$(date +%Y%m%d).db
   ```

2. **Monitor Regularly**
   - Check bot is running daily
   - Review logs weekly
   - Test commands occasionally

3. **Keep Updated**
   - Update dependencies monthly
   - Watch for Telegram API changes

4. **Document Changes**
   - Note any custom modifications
   - Keep backup of original code

---

**Most issues can be fixed with a simple restart. When in doubt, try that first!**

**Need more help? See FAQ.md or contact support (CLIENT_HANDOFF.md)**

