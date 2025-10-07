"""
Main Telegram Moderator Bot
Modern 2025 implementation with AI-powered moderation
"""
import logging
from typing import Optional
from telegram import Update, ChatMember
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.error import TelegramError

from config import Config
from database import Database
from ai_moderator import AIContentModerator
from admin_commands import AdminCommands

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class ModeratorBot:
    """Main bot class"""
    
    def __init__(self):
        """Initialize the bot"""
        Config.validate()
        
        self.db = Database()
        self.ai_moderator = AIContentModerator()
        self.admin_commands = AdminCommands(self.db)
        
        # Build application
        self.app = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register all command and message handlers"""
        
        # Admin commands
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("warn", self.cmd_warn))
        self.app.add_handler(CommandHandler("unwarn", self.cmd_unwarn))
        self.app.add_handler(CommandHandler("ban", self.cmd_ban))
        self.app.add_handler(CommandHandler("unban", self.cmd_unban))
        self.app.add_handler(CommandHandler("kick", self.cmd_kick))
        self.app.add_handler(CommandHandler("mute", self.cmd_mute))
        self.app.add_handler(CommandHandler("unmute", self.cmd_unmute))
        
        # Configuration commands
        self.app.add_handler(CommandHandler("setwarnlimit", self.admin_commands.set_warn_limit))
        self.app.add_handler(CommandHandler("setbanduration", self.admin_commands.set_ban_duration))
        self.app.add_handler(CommandHandler("toggleai", self.admin_commands.toggle_ai_moderation))
        self.app.add_handler(CommandHandler("setfloodlimit", self.admin_commands.set_flood_limit))
        self.app.add_handler(CommandHandler("config", self.admin_commands.show_config))
        self.app.add_handler(CommandHandler("setrules", self.admin_commands.set_rules))
        self.app.add_handler(CommandHandler("rules", self.admin_commands.show_rules))
        self.app.add_handler(CommandHandler("userstats", self.admin_commands.get_user_stats))
        
        # Message handlers
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        ))
        
        # New member handler
        self.app.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            self.handle_new_member
        ))
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = f"""
👋 **Welcome to {Config.BOT_NAME}!**

I'm a modern AI-powered moderation bot designed to keep your Telegram group safe and clean.

**🤖 Features:**
• AI-powered content moderation
• Automatic spam detection
• Flood protection
• Configurable warning system
• Flexible ban/kick system
• Detailed user statistics

**📚 Quick Start:**
1. Add me as an administrator in your group
2. Grant me permission to delete messages and ban users
3. Use /help to see all available commands
4. Use /config to view current settings

**💡 Need Help?**
Type /help to see all commands or visit our documentation.

Version: {Config.BOT_VERSION}
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📖 **ModeratorBot Commands**

**👮 Moderation Commands (Admin Only):**
/warn - Warn a user (reply to their message)
/unwarn - Remove warnings from a user
/ban - Ban a user permanently
/kick - Kick a user from the chat
/mute - Mute a user temporarily
/unmute - Unmute a user
/unban - Unban a user

**⚙️ Configuration Commands (Admin Only):**
/setwarnlimit <number> - Set warnings before ban
/setbanduration <seconds> - Set default ban duration
/toggleai - Enable/disable AI moderation
/setfloodlimit <msgs> <secs> - Set flood protection
/config - View current configuration
/setrules <text> - Set chat rules
/userstats - Get user statistics

**ℹ️ General Commands:**
/start - Show welcome message
/help - Show this help message
/rules - View chat rules

**🤖 Auto-Moderation:**
The bot automatically detects:
• Spam messages
• Profanity
• Toxic content
• Flood/message spam
• Suspicious links

Users will be warned automatically, and after reaching the warning limit, they will be banned.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def cmd_warn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Warn a user"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        # Must reply to a message
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user's message to warn them.")
            return
        
        target_user = update.message.reply_to_message.from_user
        reason = ' '.join(context.args) if context.args else "No reason provided"
        
        # Add warning
        await self.db.add_warning(
            target_user.id,
            update.effective_chat.id,
            target_user.username or target_user.first_name,
            reason,
            update.effective_user.id
        )
        
        # Get warning count
        config = await self.db.get_chat_config(update.effective_chat.id)
        warn_count = await self.db.get_warning_count(target_user.id, update.effective_chat.id)
        
        # Send warning message
        await update.message.reply_text(
            f"⚠️ User @{target_user.username or target_user.first_name} has been warned!\n"
            f"Reason: {reason}\n"
            f"Warnings: {warn_count}/{config['warn_limit']}"
        )
        
        # Check if should ban
        if warn_count >= config['warn_limit']:
            await self._ban_user(
                update,
                context,
                target_user,
                f"Exceeded warning limit ({warn_count} warnings)",
                config['ban_duration']
            )
    
    async def cmd_unwarn(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Remove warnings from a user"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user's message.")
            return
        
        target_user = update.message.reply_to_message.from_user
        cleared = await self.db.clear_warnings(target_user.id, update.effective_chat.id)
        
        await update.message.reply_text(
            f"✅ Cleared {cleared} warning(s) for @{target_user.username or target_user.first_name}"
        )
    
    async def cmd_ban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ban a user"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user's message to ban them.")
            return
        
        target_user = update.message.reply_to_message.from_user
        reason = ' '.join(context.args) if context.args else "No reason provided"
        
        await self._ban_user(update, context, target_user, reason, None)  # Permanent ban
    
    async def cmd_unban(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unban a user"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not update.message.reply_to_message and not context.args:
            await update.message.reply_text("❌ Reply to a message or provide user ID.")
            return
        
        target_user_id = None
        if update.message.reply_to_message:
            target_user_id = update.message.reply_to_message.from_user.id
        elif context.args:
            try:
                target_user_id = int(context.args[0])
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID")
                return
        
        try:
            await context.bot.unban_chat_member(update.effective_chat.id, target_user_id)
            await update.message.reply_text(f"✅ User has been unbanned")
        except TelegramError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def cmd_kick(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Kick a user (ban then unban)"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user's message to kick them.")
            return
        
        target_user = update.message.reply_to_message.from_user
        reason = ' '.join(context.args) if context.args else "No reason provided"
        
        try:
            # Ban then immediately unban (this kicks the user)
            await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
            await context.bot.unban_chat_member(update.effective_chat.id, target_user.id)
            
            await update.message.reply_text(
                f"👢 @{target_user.username or target_user.first_name} has been kicked!\n"
                f"Reason: {reason}"
            )
        except TelegramError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def cmd_mute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mute a user"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user's message to mute them.")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        try:
            # Restrict user from sending messages
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                target_user.id,
                permissions={
                    'can_send_messages': False,
                    'can_send_media_messages': False,
                    'can_send_other_messages': False,
                }
            )
            
            await update.message.reply_text(
                f"🔇 @{target_user.username or target_user.first_name} has been muted"
            )
        except TelegramError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def cmd_unmute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unmute a user"""
        if not await self.admin_commands.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not update.message.reply_to_message:
            await update.message.reply_text("❌ Please reply to a user's message to unmute them.")
            return
        
        target_user = update.message.reply_to_message.from_user
        
        try:
            # Restore user permissions
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                target_user.id,
                permissions={
                    'can_send_messages': True,
                    'can_send_media_messages': True,
                    'can_send_other_messages': True,
                }
            )
            
            await update.message.reply_text(
                f"🔊 @{target_user.username or target_user.first_name} has been unmuted"
            )
        except TelegramError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages for moderation"""
        if not update.message or not update.effective_user:
            return
        
        # Skip bot messages
        if update.effective_user.is_bot:
            return
        
        # Skip admin messages
        if await self.admin_commands.is_admin(update, context):
            return
        
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Track message for flood detection
        await self.db.track_message(user_id, chat_id)
        
        # Get chat config
        config = await self.db.get_chat_config(chat_id)
        
        # Check for flood
        recent_msgs = await self.db.get_recent_message_count(
            user_id, chat_id, config['flood_time_window']
        )
        
        if self.ai_moderator.check_user_behavior(
            recent_msgs, 
            config['flood_time_window'], 
            config['flood_threshold']
        ):
            await self._handle_flood(update, context, config)
            return
        
        # AI moderation
        if config['enable_ai_moderation'] and update.message.text:
            analysis = self.ai_moderator.analyze_message(update.message.text)
            
            if analysis['should_flag']:
                await self._handle_flagged_message(update, context, analysis, config)
    
    async def handle_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle new members joining"""
        config = await self.db.get_chat_config(update.effective_chat.id)
        
        if config.get('welcome_message'):
            await update.message.reply_text(config['welcome_message'])
        
        # Show rules if available
        if config.get('rules'):
            for new_member in update.message.new_chat_members:
                await update.message.reply_text(
                    f"Welcome @{new_member.username or new_member.first_name}! "
                    f"Please read our rules: /rules"
                )
    
    async def _ban_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                       target_user, reason: str, duration: Optional[int] = None):
        """Ban a user"""
        try:
            await context.bot.ban_chat_member(
                update.effective_chat.id,
                target_user.id
            )
            
            # Record ban
            await self.db.add_ban(
                target_user.id,
                update.effective_chat.id,
                target_user.username or target_user.first_name,
                reason,
                update.effective_user.id,
                duration
            )
            
            ban_type = "temporarily banned" if duration else "permanently banned"
            time_info = f" for {duration // 3600}h" if duration else ""
            
            await update.message.reply_text(
                f"🚫 @{target_user.username or target_user.first_name} has been {ban_type}{time_info}!\n"
                f"Reason: {reason}"
            )
        except TelegramError as e:
            await update.message.reply_text(f"❌ Error banning user: {str(e)}")
    
    async def _handle_flood(self, update: Update, context: ContextTypes.DEFAULT_TYPE, config):
        """Handle flood detection"""
        user = update.effective_user
        
        # Delete the message
        try:
            await update.message.delete()
        except:
            pass
        
        # Warn the user
        await self.db.add_warning(
            user.id,
            update.effective_chat.id,
            user.username or user.first_name,
            "Flood/Spam (too many messages)",
            context.bot.id
        )
        
        warn_count = await self.db.get_warning_count(user.id, update.effective_chat.id)
        
        # Check if should ban
        if warn_count >= config['warn_limit']:
            await self._ban_user(
                update,
                context,
                user,
                f"Flood/Spam - {warn_count} warnings",
                config['ban_duration']
            )
        else:
            await update.message.reply_text(
                f"⚠️ @{user.username or user.first_name} slow down! "
                f"Warning {warn_count}/{config['warn_limit']}"
            )
    
    async def _handle_flagged_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     analysis: dict, config):
        """Handle AI-flagged message"""
        user = update.effective_user
        
        # Delete the message if spam
        if analysis['is_spam'] or analysis['has_profanity']:
            try:
                await update.message.delete()
            except:
                pass
        
        # Add warning
        await self.db.add_warning(
            user.id,
            update.effective_chat.id,
            user.username or user.first_name,
            f"AI Detection: {analysis['reason']}",
            context.bot.id
        )
        
        warn_count = await self.db.get_warning_count(user.id, update.effective_chat.id)
        
        # Check if should ban
        if warn_count >= config['warn_limit']:
            await self._ban_user(
                update,
                context,
                user,
                f"Multiple violations - {warn_count} warnings",
                config['ban_duration']
            )
        else:
            await update.message.reply_text(
                f"⚠️ @{user.username or user.first_name} your message was flagged!\n"
                f"Reason: {analysis['reason']}\n"
                f"Warning {warn_count}/{config['warn_limit']}"
            )
    
    async def post_init(self, application: Application):
        """Initialize database after app starts"""
        await self.db.initialize()
        logger.info("Database initialized")
    
    def run(self):
        """Run the bot"""
        logger.info(f"Starting {Config.BOT_NAME} v{Config.BOT_VERSION}")
        
        # Add post init callback
        self.app.post_init = self.post_init
        
        # Run bot
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Main entry point"""
    try:
        bot = ModeratorBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)


if __name__ == '__main__':
    main()

