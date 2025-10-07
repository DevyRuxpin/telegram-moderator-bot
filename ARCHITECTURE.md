# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Telegram API                             │
│                    (Bot API v8.3 - 2025)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Updates/Messages
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       bot.py (Main Bot)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │        Application (python-telegram-bot v22.0)          │   │
│  │  • Command Handlers                                     │   │
│  │  • Message Handlers                                     │   │
│  │  • Event Handlers                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────┬────────────┬────────────┬────────────┬──────────────────┘
       │            │            │            │
       ▼            ▼            ▼            ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐
│ Config  │  │ Database │  │    AI    │  │  Admin  │
│ Manager │  │  Layer   │  │Moderator │  │Commands │
└─────────┘  └──────────┘  └──────────┘  └─────────┘
│ config.py│  │database.py│  │ai_moderator│  │admin_  │
│          │  │           │  │    .py   │  │commands│
│• .env    │  │• SQLite   │  │• NLP     │  │  .py   │
│• Defaults│  │• Async    │  │• Filters │  │• Perms │
└─────────┘  └──────────┘  └──────────┘  └─────────┘
                    │
                    ▼
         ┌────────────────────┐
         │  bot_database.db   │
         │  • warnings        │
         │  • bans            │
         │  • chat_config     │
         │  • user_messages   │
         │  • admins          │
         └────────────────────┘
```

---

## Component Details

### 1. Main Bot (`bot.py`)

**Responsibilities:**
- Handle incoming updates from Telegram
- Route commands to appropriate handlers
- Coordinate between modules
- Manage bot lifecycle

**Key Classes:**
- `ModeratorBot`: Main bot orchestrator

**Key Methods:**
- `handle_message()`: Process all incoming messages
- `cmd_*()`: Command handlers (warn, ban, kick, etc.)
- `_ban_user()`: Core ban logic
- `_handle_flood()`: Flood detection handler

---

### 2. Configuration (`config.py`)

**Responsibilities:**
- Load environment variables
- Provide default settings
- Validate configuration

**Configuration Sources:**
1. `.env` file (highest priority)
2. Environment variables
3. Hard-coded defaults (fallback)

**Settings Managed:**
- Bot token
- Warning limits
- Ban durations
- AI settings
- Flood protection

---

### 3. Database Layer (`database.py`)

**Responsibilities:**
- Manage SQLite database
- Provide async operations
- Handle data integrity

**Database Schema:**

```sql
warnings
├── id (PRIMARY KEY)
├── user_id
├── chat_id
├── username
├── reason
├── warned_by
└── timestamp

bans
├── id (PRIMARY KEY)
├── user_id
├── chat_id
├── username
├── reason
├── banned_by
├── ban_until
├── is_permanent
└── timestamp

chat_config
├── chat_id (PRIMARY KEY)
├── warn_limit
├── ban_duration
├── enable_ai_moderation
├── flood_threshold
├── flood_time_window
├── auto_delete_spam
├── welcome_message
└── rules

user_messages
├── id (PRIMARY KEY)
├── user_id
├── chat_id
└── timestamp

admins
├── user_id
├── chat_id (COMPOSITE PRIMARY KEY)
├── added_by
└── timestamp
```

**Key Methods:**
- `add_warning()`: Record warning
- `get_warnings()`: Retrieve warnings
- `add_ban()`: Record ban
- `is_banned()`: Check ban status
- `get_chat_config()`: Get chat settings
- `track_message()`: Record message for flood detection

---

### 4. AI Moderator (`ai_moderator.py`)

**Responsibilities:**
- Analyze message content
- Detect violations
- Calculate confidence scores

**Detection Modules:**

```
AIContentModerator
├── Profanity Filter
│   └── better-profanity library
├── Spam Detector
│   ├── URL patterns
│   ├── Character repetition
│   ├── Excessive caps
│   └── Emoji spam
├── Toxicity Analyzer
│   ├── Keyword matching
│   └── Sentiment analysis (TextBlob)
└── Behavior Monitor
    └── Pattern detection
```

**Analysis Pipeline:**

```
Input Message
     │
     ▼
┌─────────────┐
│  Profanity  │ → has_profanity: bool
└─────────────┘
     │
     ▼
┌─────────────┐
│    Spam     │ → is_spam: bool
└─────────────┘
     │
     ▼
┌─────────────┐
│  Toxicity   │ → is_toxic: bool
└─────────────┘
     │
     ▼
┌─────────────┐
│ Confidence  │ → confidence: float (0-1)
└─────────────┘
     │
     ▼
   Result
```

**Output:**
```python
{
    'is_toxic': bool,
    'is_spam': bool,
    'has_profanity': bool,
    'confidence': float,
    'reason': str,
    'should_flag': bool
}
```

---

### 5. Admin Commands (`admin_commands.py`)

**Responsibilities:**
- Handle admin-only commands
- Verify permissions
- Update configurations

**Permission Hierarchy:**

```
Bot Owner (Full Access)
    │
    ▼
Group Owner
    │
    ▼
Administrators
    │
    ▼
Regular Users (No Admin Access)
```

**Command Categories:**

1. **Moderation**
   - `/warn`, `/unwarn`
   - `/ban`, `/unban`
   - `/kick`, `/mute`, `/unmute`

2. **Configuration**
   - `/setwarnlimit`
   - `/setbanduration`
   - `/toggleai`
   - `/setfloodlimit`

3. **Information**
   - `/config`
   - `/userstats`
   - `/rules`, `/setrules`

---

## Data Flow Diagrams

### Warning Flow

```
User Posts Message
        │
        ▼
    AI Analysis
        │
        ├─→ [Clean] → No Action
        │
        └─→ [Violation Detected]
                │
                ▼
        Delete Message (if spam/profanity)
                │
                ▼
        Add Warning to DB
                │
                ▼
        Check Warning Count
                │
                ├─→ [< Limit] → Send Warning Message
                │
                └─→ [≥ Limit] → Ban User
                                    │
                                    ▼
                            Send Ban Notification
```

### Configuration Update Flow

```
Admin sends /setwarnlimit 5
        │
        ▼
Check if User is Admin
        │
        ├─→ [No] → Send "Not Authorized"
        │
        └─→ [Yes]
                │
                ▼
        Validate Input (1-10)
                │
                ├─→ [Invalid] → Send Error
                │
                └─→ [Valid]
                        │
                        ▼
                Update Database
                        │
                        ▼
                Send Confirmation
```

### Flood Detection Flow

```
User Sends Message
        │
        ▼
Track in Database
        │
        ▼
Count Recent Messages (last N seconds)
        │
        ├─→ [< Threshold] → Process Normally
        │
        └─→ [≥ Threshold] → FLOOD DETECTED
                                    │
                                    ▼
                            Delete Message
                                    │
                                    ▼
                            Add Warning
                                    │
                                    ▼
                            Check Warning Count
                                    │
                                    └─→ May Trigger Ban
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────┐
│                  Application Layer                  │
│         (bot.py, admin_commands.py, etc.)          │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│                   Service Layer                     │
│        (AI Moderator, Database Manager)            │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│                   Library Layer                     │
│  python-telegram-bot | TextBlob | better-profanity │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│                  Data Layer                         │
│              SQLite Database                        │
└─────────────────────────────────────────────────────┘
                        │
┌─────────────────────────────────────────────────────┐
│               Infrastructure Layer                  │
│        Python 3.11 | asyncio | OS                  │
└─────────────────────────────────────────────────────┘
```

---

## Async Architecture

The bot uses Python's `asyncio` for non-blocking operations:

```python
# Example async flow
async def handle_message(update, context):
    # 1. Track message (async DB write)
    await db.track_message(user_id, chat_id)
    
    # 2. Get config (async DB read)
    config = await db.get_chat_config(chat_id)
    
    # 3. AI analysis (sync, but fast)
    analysis = ai_moderator.analyze_message(text)
    
    # 4. Take action (async Telegram API call)
    if analysis['should_flag']:
        await context.bot.delete_message(chat_id, msg_id)
        await db.add_warning(user_id, chat_id, reason)
```

**Benefits:**
- Non-blocking I/O operations
- Better resource utilization
- Higher throughput
- Responsive to multiple users

---

## Security Architecture

### Defense Layers

```
┌─────────────────────────────────────┐
│      Input Validation Layer         │
│  • Sanitize user inputs             │
│  • Validate command parameters      │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│    Permission Verification Layer    │
│  • Check admin status               │
│  • Verify bot permissions           │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│      Business Logic Layer           │
│  • Process commands                 │
│  • Execute moderation               │
└─────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────┐
│        Data Access Layer            │
│  • Transaction safety               │
│  • SQL injection prevention         │
└─────────────────────────────────────┘
```

### Security Measures

1. **Authentication**
   - Admin verification via Telegram API
   - No custom authentication needed

2. **Authorization**
   - Command-level permission checks
   - Action-level verification

3. **Data Protection**
   - Local storage only
   - No external data transmission
   - Auto-cleanup of old data

4. **Input Validation**
   - Type checking
   - Range validation
   - Regex pattern matching

---

## Scalability Considerations

### Current Capacity
- **Groups**: Unlimited
- **Users per group**: 10,000+
- **Messages/second**: 30 (Telegram limit)
- **Database size**: Unlimited (SQLite can handle TBs)

### Bottlenecks & Solutions

1. **Database Writes**
   - Problem: Many concurrent writes
   - Solution: Async operations, batch writes

2. **AI Processing**
   - Problem: CPU intensive
   - Solution: Lightweight models, caching

3. **Memory Usage**
   - Problem: Many tracked messages
   - Solution: Auto-cleanup, time-based expiry

4. **API Rate Limits**
   - Problem: Telegram limits (30 msg/sec)
   - Solution: Built-in rate limiting in library

### Horizontal Scaling (Future)

```
┌─────────┐  ┌─────────┐  ┌─────────┐
│  Bot 1  │  │  Bot 2  │  │  Bot N  │
│(Group A)│  │(Group B)│  │(Group N)│
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┴────────────┘
                  │
         ┌────────▼────────┐
         │  Shared Redis   │
         │  (Optional)     │
         └─────────────────┘
```

---

## Error Handling Strategy

```
Try to Execute
     │
     ├─→ [Success] → Log success, Continue
     │
     └─→ [Error]
            │
            ├─→ [Telegram Error]
            │       └─→ Log, Notify admin, Retry
            │
            ├─→ [Database Error]
            │       └─→ Log, Use defaults, Alert
            │
            └─→ [Other Error]
                    └─→ Log, Continue, Send error msg
```

### Error Categories

1. **Telegram API Errors**
   - Permission denied
   - User not found
   - Rate limit exceeded

2. **Database Errors**
   - Lock timeout
   - Disk full
   - Corruption

3. **Application Errors**
   - Invalid input
   - Logic errors
   - Resource exhaustion

---

## Monitoring & Observability

### Logging Strategy

```
DEBUG    → Development details
INFO     → Normal operations
WARNING  → Potential issues
ERROR    → Handled errors
CRITICAL → System failures
```

### Key Metrics to Monitor

1. **Performance**
   - Message processing time
   - Database query time
   - API response time

2. **Usage**
   - Messages per minute
   - Active groups
   - Warnings issued
   - Bans executed

3. **Health**
   - Uptime
   - Error rate
   - Memory usage
   - Database size

---

## Deployment Architecture

### Single Server (Simple)

```
┌─────────────────────────┐
│    VPS/Cloud Instance   │
│                         │
│  ┌──────────────────┐  │
│  │   Bot Process    │  │
│  │   (Python)       │  │
│  └──────────────────┘  │
│           │             │
│  ┌──────────────────┐  │
│  │   SQLite DB      │  │
│  └──────────────────┘  │
└─────────────────────────┘
```

### Docker (Recommended)

```
┌─────────────────────────┐
│   Docker Container      │
│                         │
│  ┌──────────────────┐  │
│  │   Bot Process    │  │
│  └──────────────────┘  │
│                         │
│  Volume Mount           │
│  ├─ .env (config)       │
│  └─ database.db (data)  │
└─────────────────────────┘
```

### High Availability (Advanced)

```
     ┌──────────────┐
     │ Load Balancer│
     └──────┬───────┘
            │
    ┌───────┴───────┐
    │               │
┌───▼───┐       ┌───▼───┐
│ Bot 1 │       │ Bot 2 │
└───┬───┘       └───┬───┘
    │               │
    └───────┬───────┘
            │
    ┌───────▼────────┐
    │  Shared Redis  │
    │  (State Sync)  │
    └────────────────┘
```

---

## Development Workflow

```
1. Local Development
   ├─ Edit code
   ├─ Test locally
   └─ Commit changes
        │
        ▼
2. Testing
   ├─ Create test group
   ├─ Test all features
   └─ Fix bugs
        │
        ▼
3. Deployment
   ├─ Push to git
   ├─ Deploy to server
   └─ Monitor logs
        │
        ▼
4. Maintenance
   ├─ Monitor performance
   ├─ Update dependencies
   └─ Add features
```

---

## Summary

This architecture provides:

✅ **Modularity**: Clear separation of concerns
✅ **Scalability**: Can handle growth
✅ **Maintainability**: Easy to update
✅ **Performance**: Async, non-blocking
✅ **Security**: Multiple defense layers
✅ **Reliability**: Error handling, logging
✅ **Flexibility**: Configurable, extensible

**The bot is production-ready and follows modern 2025 best practices!**

