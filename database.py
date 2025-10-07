"""
Database module for storing warnings, bans, and configurations
"""
import aiosqlite
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple
from config import Config


class Database:
    """Async SQLite database manager"""
    
    def __init__(self, db_path: str = Config.DATABASE_PATH):
        self.db_path = db_path
    
    async def initialize(self):
        """Initialize database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Warnings table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS warnings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    username TEXT,
                    reason TEXT,
                    warned_by INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bans table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS bans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    username TEXT,
                    reason TEXT,
                    banned_by INTEGER,
                    ban_until DATETIME,
                    is_permanent BOOLEAN DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Chat configurations table
            await db.execute('''
                CREATE TABLE IF NOT EXISTS chat_config (
                    chat_id INTEGER PRIMARY KEY,
                    warn_limit INTEGER DEFAULT 3,
                    ban_duration INTEGER DEFAULT 3600,
                    enable_ai_moderation BOOLEAN DEFAULT 1,
                    flood_threshold INTEGER DEFAULT 5,
                    flood_time_window INTEGER DEFAULT 10,
                    auto_delete_spam BOOLEAN DEFAULT 1,
                    welcome_message TEXT,
                    rules TEXT
                )
            ''')
            
            # User message tracking (for flood protection)
            await db.execute('''
                CREATE TABLE IF NOT EXISTS user_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Admin list
            await db.execute('''
                CREATE TABLE IF NOT EXISTS admins (
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    added_by INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, chat_id)
                )
            ''')
            
            await db.commit()
    
    async def add_warning(self, user_id: int, chat_id: int, username: str, 
                         reason: str, warned_by: int) -> int:
        """Add a warning for a user"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO warnings (user_id, chat_id, username, reason, warned_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, chat_id, username, reason, warned_by))
            await db.commit()
            return cursor.lastrowid
    
    async def get_warnings(self, user_id: int, chat_id: int) -> List[Dict]:
        """Get all warnings for a user in a chat"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('''
                SELECT * FROM warnings 
                WHERE user_id = ? AND chat_id = ?
                ORDER BY timestamp DESC
            ''', (user_id, chat_id)) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_warning_count(self, user_id: int, chat_id: int) -> int:
        """Get warning count for a user"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT COUNT(*) FROM warnings 
                WHERE user_id = ? AND chat_id = ?
            ''', (user_id, chat_id)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0
    
    async def clear_warnings(self, user_id: int, chat_id: int) -> int:
        """Clear all warnings for a user"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                DELETE FROM warnings 
                WHERE user_id = ? AND chat_id = ?
            ''', (user_id, chat_id))
            await db.commit()
            return cursor.rowcount
    
    async def add_ban(self, user_id: int, chat_id: int, username: str,
                     reason: str, banned_by: int, duration: Optional[int] = None) -> int:
        """Add a ban record"""
        ban_until = None
        is_permanent = duration is None
        
        if duration:
            ban_until = (datetime.now() + timedelta(seconds=duration)).isoformat()
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO bans (user_id, chat_id, username, reason, banned_by, 
                                 ban_until, is_permanent)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, chat_id, username, reason, banned_by, ban_until, is_permanent))
            await db.commit()
            return cursor.lastrowid
    
    async def is_banned(self, user_id: int, chat_id: int) -> bool:
        """Check if user is currently banned"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT is_permanent, ban_until FROM bans
                WHERE user_id = ? AND chat_id = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (user_id, chat_id)) as cursor:
                result = await cursor.fetchone()
                if not result:
                    return False
                
                is_permanent, ban_until = result
                if is_permanent:
                    return True
                
                if ban_until:
                    ban_time = datetime.fromisoformat(ban_until)
                    return datetime.now() < ban_time
                
                return False
    
    async def get_chat_config(self, chat_id: int) -> Dict:
        """Get configuration for a chat"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute('''
                SELECT * FROM chat_config WHERE chat_id = ?
            ''', (chat_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
                else:
                    # Return defaults if no config exists
                    return {
                        'chat_id': chat_id,
                        'warn_limit': Config.DEFAULT_WARN_LIMIT,
                        'ban_duration': Config.DEFAULT_BAN_DURATION,
                        'enable_ai_moderation': Config.ENABLE_AI_MODERATION,
                        'flood_threshold': Config.FLOOD_THRESHOLD,
                        'flood_time_window': Config.FLOOD_TIME_WINDOW,
                        'auto_delete_spam': True,
                        'welcome_message': None,
                        'rules': None
                    }
    
    async def set_chat_config(self, chat_id: int, **kwargs):
        """Update chat configuration"""
        async with aiosqlite.connect(self.db_path) as db:
            # First, ensure config exists
            await db.execute('''
                INSERT OR IGNORE INTO chat_config (chat_id) VALUES (?)
            ''', (chat_id,))
            
            # Update provided settings
            for key, value in kwargs.items():
                if key != 'chat_id':
                    await db.execute(f'''
                        UPDATE chat_config 
                        SET {key} = ?
                        WHERE chat_id = ?
                    ''', (value, chat_id))
            
            await db.commit()
    
    async def track_message(self, user_id: int, chat_id: int):
        """Track a user message for flood detection"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO user_messages (user_id, chat_id)
                VALUES (?, ?)
            ''', (user_id, chat_id))
            await db.commit()
    
    async def get_recent_message_count(self, user_id: int, chat_id: int, 
                                       time_window: int) -> int:
        """Get message count in time window"""
        cutoff_time = (datetime.now() - timedelta(seconds=time_window)).isoformat()
        
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('''
                SELECT COUNT(*) FROM user_messages
                WHERE user_id = ? AND chat_id = ? 
                AND timestamp > ?
            ''', (user_id, chat_id, cutoff_time)) as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0
    
    async def cleanup_old_messages(self, hours: int = 24):
        """Clean up old message tracking records"""
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                DELETE FROM user_messages WHERE timestamp < ?
            ''', (cutoff_time,))
            await db.commit()
    
    async def get_user_stats(self, user_id: int, chat_id: int) -> Dict:
        """Get statistics for a user"""
        warnings = await self.get_warning_count(user_id, chat_id)
        is_banned = await self.is_banned(user_id, chat_id)
        
        return {
            'warnings': warnings,
            'is_banned': is_banned
        }

