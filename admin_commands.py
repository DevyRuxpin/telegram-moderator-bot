"""
Admin commands module for bot configuration
"""
from telegram import Update, ChatMember
from telegram.ext import ContextTypes
from database import Database
from config import Config


class AdminCommands:
    """Admin command handlers"""
    
    def __init__(self, db: Database):
        self.db = db
    
    async def is_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if user is admin"""
        if not update.effective_chat or not update.effective_user:
            return False
        
        try:
            chat_member = await context.bot.get_chat_member(
                update.effective_chat.id,
                update.effective_user.id
            )
            return chat_member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]
        except:
            return False
    
    async def set_warn_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set warning limit before ban"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not context.args or len(context.args) != 1:
            await update.message.reply_text("Usage: /setwarnlimit <number>\nExample: /setwarnlimit 3")
            return
        
        try:
            limit = int(context.args[0])
            if limit < 1 or limit > 10:
                await update.message.reply_text("⚠️ Warn limit must be between 1 and 10")
                return
            
            await self.db.set_chat_config(update.effective_chat.id, warn_limit=limit)
            await update.message.reply_text(f"✅ Warning limit set to {limit}")
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid number")
    
    async def set_ban_duration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set default ban duration"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not context.args or len(context.args) != 1:
            await update.message.reply_text(
                "Usage: /setbanduration <seconds>\n"
                "Example: /setbanduration 3600 (1 hour)"
            )
            return
        
        try:
            duration = int(context.args[0])
            if duration < 60 or duration > 2592000:  # 1 min to 30 days
                await update.message.reply_text("⚠️ Duration must be between 60s and 30 days")
                return
            
            await self.db.set_chat_config(update.effective_chat.id, ban_duration=duration)
            
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            time_str = f"{hours}h {minutes}m" if hours else f"{minutes}m"
            
            await update.message.reply_text(f"✅ Default ban duration set to {time_str}")
        except ValueError:
            await update.message.reply_text("❌ Please provide a valid number")
    
    async def toggle_ai_moderation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle AI moderation"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        config = await self.db.get_chat_config(update.effective_chat.id)
        new_state = not config['enable_ai_moderation']
        
        await self.db.set_chat_config(update.effective_chat.id, enable_ai_moderation=new_state)
        
        status = "✅ enabled" if new_state else "❌ disabled"
        await update.message.reply_text(f"AI moderation is now {status}")
    
    async def set_flood_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set flood protection limit"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not context.args or len(context.args) != 2:
            await update.message.reply_text(
                "Usage: /setfloodlimit <messages> <seconds>\n"
                "Example: /setfloodlimit 5 10"
            )
            return
        
        try:
            threshold = int(context.args[0])
            time_window = int(context.args[1])
            
            if threshold < 2 or threshold > 50:
                await update.message.reply_text("⚠️ Message threshold must be between 2 and 50")
                return
            
            if time_window < 1 or time_window > 60:
                await update.message.reply_text("⚠️ Time window must be between 1 and 60 seconds")
                return
            
            await self.db.set_chat_config(
                update.effective_chat.id,
                flood_threshold=threshold,
                flood_time_window=time_window
            )
            
            await update.message.reply_text(
                f"✅ Flood limit set to {threshold} messages per {time_window} seconds"
            )
        except ValueError:
            await update.message.reply_text("❌ Please provide valid numbers")
    
    async def show_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current chat configuration"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        config = await self.db.get_chat_config(update.effective_chat.id)
        
        hours = config['ban_duration'] // 3600
        minutes = (config['ban_duration'] % 3600) // 60
        time_str = f"{hours}h {minutes}m" if hours else f"{minutes}m"
        
        ai_status = "✅ Enabled" if config['enable_ai_moderation'] else "❌ Disabled"
        
        message = f"""
⚙️ **Chat Configuration**

📊 **Moderation Settings:**
• Warning Limit: {config['warn_limit']} warnings
• Ban Duration: {time_str}
• AI Moderation: {ai_status}

🌊 **Flood Protection:**
• Threshold: {config['flood_threshold']} messages
• Time Window: {config['flood_time_window']} seconds
• Auto-delete Spam: {'✅ Yes' if config['auto_delete_spam'] else '❌ No'}

💡 **Tip:** Use /help to see all available commands
        """
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def set_rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set chat rules"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        if not context.args:
            await update.message.reply_text(
                "Usage: /setrules <rules text>\n"
                "Example: /setrules No spam, be respectful, no NSFW content"
            )
            return
        
        rules = ' '.join(context.args)
        await self.db.set_chat_config(update.effective_chat.id, rules=rules)
        await update.message.reply_text("✅ Chat rules updated!")
    
    async def show_rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show chat rules"""
        config = await self.db.get_chat_config(update.effective_chat.id)
        
        if config['rules']:
            await update.message.reply_text(f"📜 **Chat Rules:**\n\n{config['rules']}", parse_mode='Markdown')
        else:
            await update.message.reply_text("📜 No rules have been set yet. Admins can use /setrules to add them.")
    
    async def get_user_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get statistics for a user"""
        if not await self.is_admin(update, context):
            await update.message.reply_text("❌ This command is only for admins.")
            return
        
        # Check if replying to a message or user ID provided
        target_user = None
        target_username = "Unknown"
        
        if update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user.id
            target_username = update.message.reply_to_message.from_user.username or \
                            update.message.reply_to_message.from_user.first_name
        elif context.args and len(context.args) == 1:
            try:
                target_user = int(context.args[0])
            except ValueError:
                await update.message.reply_text("❌ Please provide a valid user ID or reply to a message")
                return
        else:
            await update.message.reply_text(
                "Usage: Reply to a user's message with /userstats\n"
                "or: /userstats <user_id>"
            )
            return
        
        stats = await self.db.get_user_stats(target_user, update.effective_chat.id)
        warnings = await self.db.get_warnings(target_user, update.effective_chat.id)
        
        ban_status = "🚫 Banned" if stats['is_banned'] else "✅ Active"
        
        message = f"""
📊 **User Statistics**

👤 User: @{target_username} (ID: {target_user})
⚠️ Warnings: {stats['warnings']}
🔒 Status: {ban_status}

**Recent Warnings:**
"""
        
        if warnings:
            for i, warn in enumerate(warnings[:5], 1):
                message += f"\n{i}. {warn['reason']} - {warn['timestamp']}"
        else:
            message += "\nNo warnings"
        
        await update.message.reply_text(message, parse_mode='Markdown')

