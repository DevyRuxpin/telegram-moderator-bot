# 🧪 Testing Guide

Complete guide for testing the Telegram Moderator Bot to verify 100% functionality.

---

## Quick Test

Run the automated test suite:

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python test_bot.py
```

This will test all core functionality and show you a detailed report.

---

## Testing Methods

### 1. 🤖 Automated Unit Tests

**File:** `test_bot.py`

Tests all core functionality without requiring a live bot:
- ✅ Configuration loading
- ✅ Database operations (CRUD)
- ✅ AI content detection
- ✅ Integration flows
- ✅ Data persistence
- ✅ Error handling

**Run it:**
```bash
python test_bot.py
```

**Expected output:**
```
✅ PASS - Database initialization
✅ PASS - Add warning to database
✅ PASS - Profanity detection
...
🎉 ALL TESTS PASSED! Bot is fully functional!
```

---

### 2. 🔴 Live Bot Testing

Test the bot in a real Telegram environment.

#### Prerequisites:
1. Bot token from @BotFather
2. Test Telegram group
3. Bot is admin in the group

#### Setup:
```bash
# Configure bot
nano .env  # Add your BOT_TOKEN

# Run bot
python bot.py
```

#### Manual Test Checklist:

**Basic Commands (5 min):**
- [ ] Send `/start` - Should show welcome message
- [ ] Send `/help` - Should show all commands
- [ ] Send `/rules` - Should show "No rules set" or your rules
- [ ] Send invalid command - Bot should ignore

**Admin Verification (2 min):**
- [ ] Regular user tries `/warn` - Should get "admins only" message
- [ ] Admin tries `/warn` - Should work
- [ ] Admin tries `/config` - Should show current settings

**Warning System (5 min):**
- [ ] Admin replies to message with `/warn Test reason`
- [ ] User should receive warning notification
- [ ] Warning count should increment
- [ ] Send `/userstats` on that user - Should show 1 warning
- [ ] Add more warnings until limit reached
- [ ] User should get automatically banned

**Ban System (5 min):**
- [ ] Admin `/ban` on a user - User should be banned
- [ ] Banned user tries to send message - Should be blocked by Telegram
- [ ] Admin `/unban` - User should be unbanned
- [ ] User can send messages again

**Kick System (3 min):**
- [ ] Admin `/kick` on a user - User removed from group
- [ ] User can rejoin (unlike ban)

**Mute System (3 min):**
- [ ] Admin `/mute` on a user - User muted
- [ ] User tries to send message - Should be blocked
- [ ] Admin `/unmute` - User can message again

**AI Moderation (10 min):**
- [ ] Send clean message - No action
- [ ] Send message with profanity - Should get warning
- [ ] Send spam (many links) - Should get warning/deletion
- [ ] Send ALL CAPS SPAM - Should get detected
- [ ] Send repeated characters "AAAAAAA" - Should flag
- [ ] Trigger flood by sending many messages quickly - Should warn

**Configuration (5 min):**
- [ ] `/setwarnlimit 5` - Should confirm change
- [ ] `/config` - Should show new limit of 5
- [ ] `/setbanduration 7200` - Should confirm (2 hours)
- [ ] `/toggleai` - AI should toggle off
- [ ] Send profanity - Should NOT get warned (AI off)
- [ ] `/toggleai` - AI back on
- [ ] `/setfloodlimit 10 15` - Should set new flood limit
- [ ] `/setrules Be nice` - Should set rules
- [ ] `/rules` - Should show "Be nice"

**Edge Cases (5 min):**
- [ ] Try to warn a bot - Should handle gracefully
- [ ] Try to warn yourself - Should handle gracefully
- [ ] Send very long message - Should process
- [ ] Send emojis only - Should process
- [ ] Send empty `/warn` - Should show usage

**Persistence (2 min):**
- [ ] Add warnings to a user
- [ ] Stop bot (Ctrl+C)
- [ ] Restart bot
- [ ] Check `/userstats` - Warnings should still be there

---

### 3. 📊 Performance Testing

Test bot under load:

#### Message Rate Test:
```bash
# In your group, have multiple people send messages rapidly
# Bot should handle all without crashing
# Flood protection should kick in automatically
```

#### Long-Running Test:
```bash
# Run bot for 24 hours
# Monitor for memory leaks or crashes
# Check logs for errors

python bot.py > bot_test.log 2>&1 &
# Wait 24 hours
# Check if still running: ps aux | grep bot.py
# Check logs: tail -f bot_test.log
```

---

### 4. 🔍 Database Testing

Verify database integrity:

```bash
# Check database was created
ls -lh bot_database.db

# Verify tables exist
sqlite3 bot_database.db ".tables"
# Should show: admins bans chat_config user_messages warnings

# Check data
sqlite3 bot_database.db "SELECT COUNT(*) FROM warnings;"
sqlite3 bot_database.db "SELECT COUNT(*) FROM bans;"
```

---

## Test Scenarios

### Scenario 1: New Group Setup
1. Add bot to fresh group
2. Make bot admin
3. Test `/start` and `/help`
4. Set configuration with `/setwarnlimit 3`
5. Set rules with `/setrules`
6. Test moderation on a user

**Expected:** Bot should work perfectly in new group

### Scenario 2: Multiple Violations
1. User sends profanity (violation 1)
2. User sends spam links (violation 2)
3. User floods messages (violation 3)
4. User should be auto-banned after 3 warnings

**Expected:** Progressive warnings → auto-ban

### Scenario 3: Admin Override
1. User gets 2 warnings
2. Admin uses `/unwarn` to clear
3. User gets 3 new warnings
4. Should take 3 more to ban (not 1)

**Expected:** Warning reset works correctly

### Scenario 4: Multiple Admins
1. Admin A sets `/setwarnlimit 5`
2. Admin B checks `/config` - should see 5
3. Admin A warns user
4. Admin B checks `/userstats` - should see warning

**Expected:** Config and data shared across admins

### Scenario 5: Bot Restart
1. Add warnings to users
2. Configure settings
3. Stop bot
4. Start bot
5. Check warnings and config

**Expected:** All data persists

---

## Verification Checklist

### ✅ Core Functionality
- [ ] Bot starts without errors
- [ ] Bot responds to commands
- [ ] Database is created
- [ ] Logging works

### ✅ Moderation Features
- [ ] Warning system works
- [ ] Ban system works
- [ ] Kick system works
- [ ] Mute/unmute works
- [ ] Auto-ban at limit works

### ✅ AI Features
- [ ] Profanity detected
- [ ] Spam detected
- [ ] Flood protection works
- [ ] Can toggle AI on/off

### ✅ Admin Features
- [ ] Only admins can use admin commands
- [ ] Configuration changes apply
- [ ] Changes persist
- [ ] User stats accurate

### ✅ Data Integrity
- [ ] Warnings saved correctly
- [ ] Bans recorded properly
- [ ] Config changes persist
- [ ] Data survives restart

### ✅ Error Handling
- [ ] Invalid commands ignored
- [ ] Permission errors handled
- [ ] Empty inputs handled
- [ ] Bot doesn't crash

---

## Success Criteria

Your bot passes testing if:

✅ **All automated tests pass** (test_bot.py)
✅ **All manual tests pass** (checklist above)
✅ **No crashes during 24hr test**
✅ **All data persists across restarts**
✅ **Performance is acceptable** (< 1 sec response)
✅ **Error handling works** (no unhandled exceptions)

---

## Common Issues

### Bot doesn't respond
- Check bot token is correct
- Verify bot is admin in group
- Check bot is running (ps aux | grep bot.py)

### Commands don't work
- Make sure you're an admin
- Check bot has correct permissions
- Try `/start` first

### AI not detecting
- Check AI is enabled: `/config`
- Toggle it: `/toggleai`
- Test with obvious profanity

### Database errors
- Check disk space
- Check file permissions
- Delete and recreate: `rm bot_database.db`

---

## Automated Testing Commands

```bash
# Run unit tests
python test_bot.py

# Check for syntax errors
python -m py_compile bot.py
python -m py_compile database.py
python -m py_compile ai_moderator.py
python -m py_compile admin_commands.py

# Check for common issues
python -m flake8 bot.py --ignore=E501,W503

# Type checking (if mypy installed)
mypy bot.py --ignore-missing-imports
```

---

## Performance Benchmarks

Expected performance on standard hardware:

| Operation | Time | Notes |
|-----------|------|-------|
| Command response | < 100ms | Should be instant |
| AI analysis | < 500ms | Content dependent |
| Database query | < 50ms | Very fast |
| Ban/kick action | < 200ms | Telegram API call |

---

## Test Report Template

```
TELEGRAM BOT TEST REPORT
Date: [DATE]
Tester: [NAME]
Bot Version: 1.0.0

AUTOMATED TESTS:
- Unit tests: [PASS/FAIL]
- Total tests run: [NUMBER]
- Pass rate: [PERCENTAGE]

MANUAL TESTS:
- Basic commands: [PASS/FAIL]
- Moderation: [PASS/FAIL]
- AI detection: [PASS/FAIL]
- Configuration: [PASS/FAIL]
- Persistence: [PASS/FAIL]

ISSUES FOUND:
1. [Issue description]
2. [Issue description]

OVERALL RESULT: [PASS/FAIL]
```

---

## Continuous Testing

For production deployment:

1. **Run tests before deployment**
   ```bash
   python test_bot.py && echo "✅ Safe to deploy"
   ```

2. **Monitor logs in production**
   ```bash
   tail -f bot.log | grep -i error
   ```

3. **Set up health checks**
   ```bash
   # Check bot is running
   */5 * * * * pgrep -f "python bot.py" || systemctl restart telegram-bot
   ```

4. **Regular database backups**
   ```bash
   # Daily backup
   0 2 * * * cp bot_database.db backups/bot_database_$(date +\%Y\%m\%d).db
   ```

---

## Video Demonstration

To create a verification video:

1. Record screen
2. Show bot.py running
3. Run automated tests
4. Show test passing
5. Open Telegram
6. Demonstrate each feature
7. Show database data
8. Restart bot and verify persistence

This provides undeniable proof the bot works!

---

## Questions?

If any test fails:
1. Check error message
2. Review logs
3. Check configuration
4. Verify permissions
5. Consult TROUBLESHOOTING section in README.md

**All tests passing = Bot is 100% functional!** 🎉

