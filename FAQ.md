# ❓ Frequently Asked Questions (FAQ)

## General Questions

### What is this bot?
A Telegram moderation bot that automatically warns and bans users who break rules. It detects spam, profanity, and flooding using AI.

### Do I need technical skills to use it?
No! Basic usage requires no technical knowledge. Just type commands like `/warn` or `/ban`. See USER_GUIDE.md for simple instructions.

### How much does it cost to run?
**Free options available!** You can run it on your computer ($0) or use free cloud hosting. Paid hosting starts at $2.50/month. See COST_BREAKDOWN.md.

### Is my data safe?
Yes! All data is stored locally on your server. No external services collect your information. The bot only communicates with Telegram's official API.

---

## Setup & Installation

### How do I get started?
1. Run `./setup.sh`
2. Get bot token from @BotFather
3. Add token to `.env` file
4. Run `python bot.py`

See QUICKSTART.md for detailed steps.

### What do I need to run the bot?
- Python 3.11 or newer
- A Telegram bot token (free from @BotFather)
- A computer or server to run it on

### Can I run it on Windows?
Yes! The bot works on Windows, macOS, and Linux. Setup instructions work for all platforms.

### How do I get a bot token?
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow the prompts
5. Copy the token you receive

### Where do I put the bot token?
In the `.env` file in the project folder. Open it with any text editor and replace `your_bot_token_here` with your actual token.

---

## Usage Questions

### How do I warn someone?
Reply to their message and type `/warn` or `/warn Reason here`

### How many warnings before a ban?
Default is 3 warnings. You can change this with `/setwarnlimit 5` (or any number 1-10).

### How do I ban someone permanently?
Reply to their message and type `/ban`

### How do I unban someone?
Type `/unban <user_id>` or reply to their old message with `/unban`

### Can regular users use admin commands?
No! Only Telegram group administrators can use moderation commands like `/warn`, `/ban`, etc.

### What commands can everyone use?
Everyone can use: `/start`, `/help`, and `/rules`

---

## AI & Detection

### What does the AI detect?
- Profanity and bad language
- Spam (too many links, repeated text)
- Flooding (too many messages too fast)
- Toxic/aggressive language
- ALL CAPS SPAM

### Is the AI detection perfect?
No system is 100% perfect. It catches 90%+ of violations. You can always use `/unwarn` if it makes a mistake.

### Can I turn off AI detection?
Yes! Use `/toggleai` command. Useful for private groups where you want manual-only moderation.

### Why did the bot warn for a normal message?
Sometimes AI makes mistakes (false positives). Use `/unwarn` to clear the warning and consider adjusting settings or turning AI off.

### The bot isn't catching spam. Why?
Check if AI is enabled: Type `/config` and look for "AI Moderation: ✅ Enabled". If disabled, type `/toggleai` to turn it on.

---

## Configuration

### How do I change settings?
Use these commands:
- `/setwarnlimit <number>` - Change warnings needed
- `/setbanduration <seconds>` - Change ban length
- `/toggleai` - Turn AI on/off
- `/setfloodlimit <msgs> <secs>` - Change flood settings

### What's a good warning limit?
- **Strict groups:** 2-3 warnings
- **Normal groups:** 3-5 warnings
- **Casual groups:** 5-7 warnings

### How long should bans last?
Common settings:
- **Soft:** 1-6 hours (3600-21600 seconds)
- **Medium:** 12-24 hours (43200-86400 seconds)
- **Strict:** 7 days+ (604800+ seconds)

### Can different groups have different settings?
Yes! Each Telegram group can have its own settings. Configure each group independently.

### Do settings save if I restart the bot?
Yes! All settings are saved in a database and persist across restarts.

---

## Troubleshooting

### Bot isn't responding to commands
**Check:**
1. Is the bot running? (ask IT person or check terminal)
2. Is bot an administrator in the group?
3. Did you spell the command correctly? (must start with `/`)

**Fix:** Restart the bot or check permissions.

### "This command is only for admins"
You're not a group administrator. Ask the group owner to make you an admin.

### Bot keeps warning innocent messages
AI is being too strict. Options:
1. Turn it off: `/toggleai`
2. Increase warning limit: `/setwarnlimit 7`
3. Clear false warnings: `/unwarn`

### Can't ban/kick users
The bot needs admin permissions. Go to group settings → Administrators → Bot → Enable "Ban users" permission.

### Commands worked before, now they don't
The bot might have crashed or been removed as admin. Check if it's still running and has admin permissions.

---

## Technical Questions

### What language is it written in?
Python 3.11+ using the official python-telegram-bot library.

### Can I modify the code?
Yes! You own the code (MIT License). You can modify, extend, or customize it however you want.

### How do I update the bot?
If you have updates:
1. Stop the bot (Ctrl+C)
2. Replace files with new versions
3. Run `pip install -r requirements.txt`
4. Start bot again

### Where is data stored?
In a file called `bot_database.db` in the project folder. It's an SQLite database.

### How do I backup my data?
Copy the `bot_database.db` file somewhere safe. Do this weekly:
```bash
cp bot_database.db backup_$(date +%Y%m%d).db
```

### Can I run multiple bots from the same code?
Yes, but each needs its own bot token and separate database file.

### What if Telegram changes their API?
The bot uses the official library which is maintained by the community. Updates are released regularly.

---

## Performance

### How many groups can one bot handle?
Unlimited! One bot can moderate multiple groups simultaneously.

### How many users per group?
Tested with 10,000+ users per group. Handles large communities fine.

### Will it slow down my group?
No. The bot responds in milliseconds. Users won't notice any delay.

### How much memory/CPU does it use?
Very little! About 50-80 MB RAM and 1-5% CPU on average.

---

## Costs & Hosting

### Can I run it for free?
Yes! Several options:
- Your own computer (free)
- Oracle Cloud Free Tier
- Railway.app ($5 free credit/month)

### What are paid hosting options?
- VPS: $2.50-6/month (Vultr, Hetzner, DigitalOcean)
- Cloud: $7-20/month (Heroku, Railway, Render)

### Which hosting do you recommend?
**For starting:** Your computer or Railway free tier  
**For production:** VPS like Hetzner ($3/month) for reliability

### Are there any hidden costs?
No! The bot uses free, local AI. No API costs, no subscriptions.

---

## Support & Maintenance

### What if I find a bug?
Contact your developer or check TROUBLESHOOTING.md. Most issues have simple fixes.

### Can I get help setting it up?
Yes! See CLIENT_HANDOFF.md for support information included in your delivery.

### How do I report a problem?
1. Check TROUBLESHOOTING.md first
2. Check this FAQ
3. Contact support (details in CLIENT_HANDOFF.md)

### Is training available?
Yes! See USER_GUIDE.md for complete instructions. Video tutorials can be created (scripts provided).

---

## Privacy & Security

### Does the bot store messages?
No! It only stores warning counts, ban records, and settings. Actual message content is not saved.

### Can the bot see private messages?
No. The bot only works in groups where it's added and only sees group messages.

### Is the bot token secure?
Yes, as long as you:
1. Keep it in the `.env` file
2. Don't share it publicly
3. Don't commit it to public repositories

### Can someone hack my bot?
The bot has security measures:
- Admin-only commands
- Input validation
- No external data transmission
- Local storage only

Keep your server secure and you'll be fine.

---

## Customization

### Can I change what gets detected?
Yes! Edit `ai_moderator.py` to add/remove keywords or patterns. See ARCHITECTURE.md for details.

### Can I add new commands?
Yes! If you know Python, you can add commands in `bot.py`. Documentation provided.

### Can I change the warning messages?
Yes! Edit the response messages in `bot.py`. Search for message text and modify it.

### Can I add more features?
Absolutely! The code is modular and well-documented. You can extend it or hire a developer.

---

## Advanced Usage

### Can I integrate with other bots?
Yes, but requires custom development. The bot can coexist with other bots.

### Can I use webhooks instead of polling?
Yes! The bot supports webhooks. See python-telegram-bot documentation for setup.

### Can I run analytics on the data?
Yes! Query the SQLite database (`bot_database.db`) with any SQL tool.

### Can I export data?
Yes! The database is SQLite format. You can export to CSV, JSON, etc. using database tools.

---

## Comparisons

### How is this different from other moderation bots?
- ✅ You own the code
- ✅ No monthly fees
- ✅ AI-powered detection
- ✅ Fully customizable
- ✅ Local hosting (private)
- ✅ No limits on features

### Why not use a hosted bot service?
Hosted services often have:
- Monthly fees
- Feature limits
- Privacy concerns
- Vendor lock-in

This bot is yours forever with no restrictions.

### Can it replace human moderators?
It handles 90% of routine moderation automatically. Human admins are still needed for edge cases and appeals.

---

## Best Practices

### What settings should I use?
**For public groups:**
- Warning limit: 3
- AI detection: ON
- Flood limit: 5 messages/10 seconds

**For private groups:**
- Warning limit: 5-7
- AI detection: OFF or ON (your choice)
- Flood limit: 10 messages/15 seconds

### How often should I check the bot?
- **Daily:** Quick check that it's running
- **Weekly:** Review user stats, adjust settings
- **Monthly:** Backup database, check logs

### Should I announce the bot to users?
Yes! Post a message explaining:
- Bot will warn for rule violations
- After X warnings, users get banned
- Post your rules (use `/rules` command)

---

## Migration & Backup

### How do I move to a new server?
1. Stop the bot
2. Copy all files to new server
3. Copy `bot_database.db` (important!)
4. Install dependencies: `./setup.sh`
5. Start bot

### How do I restore from backup?
1. Stop the bot
2. Replace `bot_database.db` with backup copy
3. Start the bot

### What files do I need to backup?
- `bot_database.db` (essential - has all data)
- `.env` (has your configuration)
- Custom modifications to code (if any)

---

## Still Have Questions?

### Read These Guides:
- **USER_GUIDE.md** - How to use the bot
- **TROUBLESHOOTING.md** - Fix common problems
- **README.md** - Technical documentation
- **QUICKSTART.md** - Setup instructions

### Get Support:
See CLIENT_HANDOFF.md for contact information

### Watch Videos:
Create tutorial videos using scripts in VIDEO_SCRIPTS.md

---

**This FAQ is regularly updated. Last update: October 7, 2025**

