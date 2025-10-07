# 👥 User Guide - Telegram Moderator Bot

**For Group Administrators**

This guide explains how to use the bot in simple terms - no technical knowledge required!

---

## 🎯 What This Bot Does

**In Simple Terms:**

Your bot automatically:
- ⚠️ Warns users who break rules
- 🚫 Bans repeat offenders
- 🤖 Detects spam and profanity
- 🛡️ Protects against message flooding
- 📊 Tracks user violations

**You control:**
- How many warnings before a ban
- How long bans last
- What gets detected
- Chat rules

---

## 🚀 Getting Started (First Time Setup)

### Step 1: Add Bot to Your Group
1. Open your Telegram group
2. Click group name → "Add Members"
3. Search for your bot
4. Add it

### Step 2: Make Bot an Administrator
1. Group settings → "Administrators"
2. Add your bot as admin
3. **Grant these permissions:**
   - ✅ Delete messages
   - ✅ Ban users
   - ✅ Restrict members
   - ✅ Pin messages (optional)

### Step 3: Say Hello!
Send this in your group:
```
/start
```

The bot should reply with a welcome message.

**If it doesn't reply, check:**
- Is the bot running? (Ask your IT person)
- Is it an admin? (Check permissions)
- Did you spell the command correctly? (starts with /)

---

## 📱 Basic Commands

### For Everyone

```
/start
```
Shows welcome message

```
/help
```
Lists all available commands

```
/rules
```
Shows your group rules (if you've set them)

### For Administrators Only

```
/warn
```
Warn a user (reply to their message)
Example: Reply to spam with `/warn Spamming links`

```
/ban
```
Ban a user permanently (reply to their message)
Example: `/ban Repeated violations`

```
/kick
```
Remove user from group (they can rejoin)
Example: `/kick Breaking rules`

```
/mute
```
Stop user from sending messages (reply to their message)

```
/unmute
```
Allow muted user to message again

```
/unban
```
Unban a previously banned user

---

## ⚙️ Configuration Commands

### Set Warning Limit

**What it does:** Decides how many warnings before auto-ban

```
/setwarnlimit 3
```
User gets banned after 3 warnings (default)

```
/setwarnlimit 5
```
More lenient - 5 warnings before ban

**Recommended:** 3-5 warnings

### Set Ban Duration

**What it does:** How long bans last (in seconds)

```
/setbanduration 3600
```
1 hour ban (3600 seconds)

```
/setbanduration 86400
```
24 hour ban

**Common durations:**
- 1 hour = 3600
- 12 hours = 43200
- 1 day = 86400
- 1 week = 604800

**Tip:** Use Google to convert time to seconds

### Toggle AI Detection

**What it does:** Turn automatic detection on/off

```
/toggleai
```
Switches AI detection on or off

**When to turn OFF:**
- Private group with friends
- Too many false positives
- You want manual-only moderation

**When to keep ON:**
- Public groups
- Large communities
- Spam problems

### Set Flood Protection

**What it does:** Prevents users from sending too many messages too fast

```
/setfloodlimit 5 10
```
Allows 5 messages in 10 seconds

```
/setfloodlimit 10 15
```
More lenient - 10 messages in 15 seconds

**Recommended:** 5 messages in 10 seconds

### View Current Settings

```
/config
```
Shows all current settings

**Example output:**
```
⚙️ Chat Configuration

Warning Limit: 3 warnings
Ban Duration: 1h 0m
AI Moderation: ✅ Enabled
Flood Threshold: 5 messages
Time Window: 10 seconds
```

---

## 📋 Managing Rules

### Set Your Rules

```
/setrules Be respectful, no spam, no NSFW content
```

Sets custom rules for your group

**Tips for good rules:**
- Keep them clear and simple
- List specific behaviors (no spam, no profanity, etc.)
- Make them visible (pin the message)

### Show Rules

```
/rules
```

Displays current rules

**Tip:** Ask new members to read rules when they join!

---

## 👤 User Management

### Check User Statistics

**To see a user's warnings:**
1. Reply to their message
2. Send `/userstats`

**Example output:**
```
📊 User Statistics

User: @username (ID: 12345)
⚠️ Warnings: 2
🔒 Status: ✅ Active

Recent Warnings:
1. Spam - 2024-10-05
2. Profanity - 2024-10-06
```

### Clear Warnings

**To give user a fresh start:**
1. Reply to their message
2. Send `/unwarn`

All their warnings are erased.

---

## 🤖 How AI Detection Works

### What Gets Detected Automatically:

**Profanity**
- Bad words, swearing
- Action: Warns user, deletes message

**Spam**
- Too many links
- Repeated characters (AAAAAA)
- ALL CAPS MESSAGES
- Too many emojis
- Action: Warns user, deletes message

**Flooding**
- Sending messages too fast
- Action: Warns user

**Toxic Content**
- Aggressive language
- Harassment
- Threats
- Action: Warns user

### What Doesn't Get Detected:

- Normal conversation
- Regular links (just 1-2)
- Occasional CAPS for emphasis
- Appropriate emoji use

---

## 📖 Common Scenarios

### Scenario 1: Someone Spams Links

**What happens automatically:**
1. Bot detects spam
2. Deletes the message
3. Warns the user
4. If user hits warning limit → auto-ban

**What you do:**
Nothing! It's automatic.

**If you want to ban immediately:**
Reply to message with `/ban Spamming`

### Scenario 2: User Uses Profanity

**What happens:**
1. Bot detects profanity
2. Deletes message
3. Warns user

**What you can do:**
- Nothing (let it handle automatically)
- `/ban` if you want immediate ban
- `/unwarn` if it was a false positive

### Scenario 3: False Positive

**Bot warned someone incorrectly:**

```
/unwarn
```
(Reply to their message)

This clears the false warning.

**If AI is too strict:**
```
/toggleai
```
Turn it off, moderate manually

### Scenario 4: Repeat Offender

**User keeps breaking rules:**

1. They get warned each time
2. At warning limit (e.g., 3), auto-banned
3. You can check their history: `/userstats`

**To ban immediately:**
```
/ban Repeated violations
```

### Scenario 5: User Apologizes

**They want a second chance:**

```
/unwarn
```
(Reply to their message)

Clears their warnings, fresh start.

---

## 💡 Pro Tips

### For Busy Admins

1. **Set appropriate limits**
   - 3 warnings for strict moderation
   - 5 warnings for casual groups

2. **Use AI detection**
   - Saves you time
   - Handles 90% automatically

3. **Check stats regularly**
   - Use `/userstats` on problem users
   - Track patterns

### For Large Groups

1. **Keep AI ON**
   - Essential for large communities
   - Can't manually moderate everything

2. **Stricter settings**
   - Lower warning limit (3)
   - Shorter ban duration (24 hours)
   - Strict flood limits

3. **Clear rules**
   - Pin rules message
   - Reference them when warning

### For Small/Private Groups

1. **More lenient**
   - Higher warning limit (5-7)
   - Longer time before ban
   - Relaxed flood limits

2. **Consider AI OFF**
   - Friends might joke around
   - Less spam in small groups
   - Manual moderation works

---

## ⚠️ Important Dos and Don'ts

### ✅ DO:

- Set clear rules with `/setrules`
- Check user stats before banning
- Give warnings before permanent bans
- Use `/unwarn` for false positives
- Adjust settings for your community

### ❌ DON'T:

- Don't abuse the ban command
- Don't set warning limit too low (minimum 2)
- Don't ignore the bot's warnings
- Don't disable AI without reason
- Don't warn people for no reason

---

## 🆘 Troubleshooting

### Bot Not Responding

**Check:**
1. Is bot still in the group?
2. Is it an administrator?
3. Is it running? (ask IT person)
4. Did you spell command correctly? (must start with /)

**Try:**
- Restart bot (ask IT person)
- Check bot permissions
- Send `/start` to wake it up

### Commands Not Working

**If you see "Only for admins":**
- You're not a group admin
- Ask group owner for admin rights

**If nothing happens:**
- Check spelling (use `/help` to see all commands)
- Make sure you're in the group (not private chat)
- Verify bot has permissions

### AI Too Strict

**Bot warns for everything:**

```
/toggleai
```
Turns AI off, use manual moderation

**OR adjust settings:**
```
/setwarnlimit 7
```
More warnings before ban

### AI Too Lenient

**Bot not catching problems:**

**Check it's enabled:**
```
/config
```
Look for "AI Moderation: ✅ Enabled"

**If disabled:**
```
/toggleai
```
Turn it back on

---

## 📞 Getting Help

### Quick Help

```
/help
```
Shows all commands in the bot

### Read Documentation

- **This Guide** - How to use
- **QUICKSTART.md** - Setup help
- **FAQ.md** - Common questions
- **TROUBLESHOOTING.md** - Fix problems

### Contact Support

**If bot is broken:**
Contact your IT person or developer

**If you need help using it:**
Read the FAQ.md file

---

## 📊 Understanding the Dashboard

### When you type `/config`:

```
⚙️ Chat Configuration

📊 Moderation Settings:
• Warning Limit: 3 warnings
• Ban Duration: 1h 0m
• AI Moderation: ✅ Enabled

🌊 Flood Protection:
• Threshold: 5 messages
• Time Window: 10 seconds
```

**What each means:**

**Warning Limit:** How many strikes before ban  
**Ban Duration:** How long bans last  
**AI Moderation:** Automatic detection on/off  
**Flood Threshold:** Max messages allowed...  
**Time Window:** ...in this many seconds  

---

## 🎯 Quick Reference Card

```
MOST USED COMMANDS:

/warn - Warn user (reply to message)
/ban - Ban user (reply to message)
/unwarn - Clear warnings (reply to message)
/config - View settings
/userstats - Check user history (reply to message)

CONFIGURATION:

/setwarnlimit <number> - Set warnings needed
/toggleai - Turn AI on/off
/setrules <text> - Set group rules
/rules - Show rules

Remember: All admin commands require replying to the user's message!
```

---

## ✅ Success Checklist

You're using the bot successfully if:

- ✅ Spam is reduced in your group
- ✅ Rules violations are handled quickly
- ✅ You understand the basic commands
- ✅ Settings are configured for your group
- ✅ Bot moderates automatically
- ✅ Your community is cleaner

---

## 🎓 Training New Admins

**To train new admins:**

1. Have them read this guide (15 minutes)
2. Show them `/help` command
3. Practice `/warn` on a test message
4. Explain your group's settings
5. Show them `/userstats`

**Key points to teach:**
- How to warn users
- When to ban vs warn
- How to check user history
- Where to find help

---

**Need more help? See FAQ.md or TROUBLESHOOTING.md**

**Happy moderating!** 🎉

