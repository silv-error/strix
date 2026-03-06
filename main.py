"""
Auto-Kick Bot - Main Entry Point
A Discord bot that automatically kicks members who don't verify within a set time.
"""
import os
import sys
from dotenv import load_dotenv
import discord

# Load environment variables
load_dotenv()

# Import bot components
from src.bot import create_bot
from src.events import setup_member_events
from src.commands import register_slash_commands, register_prefix_commands
from src.tasks import scan_existing_members
from src.config import UNVERIFIED_ROLE_NAME, KICK_AFTER_MINUTES, CHECK_INTERVAL_MINUTES


def main():
    """Main entry point for the bot"""
    
    # Get bot token
    if len(sys.argv) > 1:
        TOKEN = sys.argv[1]
    else:
        TOKEN = os.getenv('DISCORD_BOT_TOKEN')
        
        if not TOKEN:
            print("❌ ERROR: No bot token provided!")
            print("Usage: python main.py YOUR_BOT_TOKEN")
            print("Or set DISCORD_BOT_TOKEN environment variable")
            sys.exit(1)
    
    # Create bot instance
    bot = create_bot()
    
    # Register events
    setup_member_events(bot)
    
    # Register commands
    register_slash_commands(bot)
    register_prefix_commands(bot)
    
    # Setup ready event
    @bot.event
    async def on_ready():
        print('=' * 50)
        print(f'✅ Bot is ready! Logged in as {bot.user.name} (ID: {bot.user.id})')
        print(f'📊 Connected to {len(bot.guilds)} server(s)')
        print(f'🎯 Default role: {UNVERIFIED_ROLE_NAME}')
        print(f'⏱️  Default kick timer: {KICK_AFTER_MINUTES} minutes')
        print(f'🔄 Check interval: {CHECK_INTERVAL_MINUTES} minutes')
        print('💡 Use /setup or !setup to configure settings')
        print('💡 Use /help or !autokick_help for all commands')
        print('=' * 50)
        
        # Scan existing members
        await scan_existing_members(bot)
    
    # Start the bot
    print("🚀 Starting Auto-Kick Bot...")
    print("📁 File structure: Organized")
    print("⚙️  Configuration: config.py")
    print("🔧 Utilities: utils/")
    print("🎮 Commands: commands/")
    print("📡 Events: events/")
    print("⏰ Tasks: tasks.py")
    print()
    
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\n\n👋 Bot shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()