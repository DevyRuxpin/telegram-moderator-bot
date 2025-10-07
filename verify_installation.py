#!/usr/bin/env python3
"""
Quick verification script - checks if bot is ready to run
Run this before starting the bot to verify everything is set up correctly
"""
import sys
import os

def check_mark(condition):
    return "✅" if condition else "❌"

def main():
    print("\n" + "="*60)
    print("  TELEGRAM BOT - INSTALLATION VERIFICATION")
    print("="*60 + "\n")
    
    all_ok = True
    
    # Check 1: Python version
    print("1. Checking Python version...")
    py_version = sys.version_info
    py_ok = py_version.major == 3 and py_version.minor >= 11
    print(f"   {check_mark(py_ok)} Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    if not py_ok:
        print("   ⚠️  Python 3.11+ recommended")
        all_ok = False
    
    # Check 2: Required files exist
    print("\n2. Checking project files...")
    required_files = [
        'bot.py',
        'database.py',
        'ai_moderator.py',
        'admin_commands.py',
        'config.py',
        'requirements.txt',
        '.env.example'
    ]
    
    for file in required_files:
        exists = os.path.exists(file)
        print(f"   {check_mark(exists)} {file}")
        if not exists:
            all_ok = False
    
    # Check 3: Environment file
    print("\n3. Checking configuration...")
    env_exists = os.path.exists('.env')
    print(f"   {check_mark(env_exists)} .env file exists")
    if not env_exists:
        print("   ⚠️  Run: cp .env.example .env")
        all_ok = False
    
    if env_exists:
        with open('.env', 'r') as f:
            content = f.read()
            has_token = 'BOT_TOKEN=' in content
            token_configured = 'your_bot_token_here' not in content
            
            print(f"   {check_mark(has_token)} BOT_TOKEN variable present")
            print(f"   {check_mark(token_configured)} BOT_TOKEN configured")
            
            if not token_configured:
                print("   ⚠️  Edit .env and add your bot token from @BotFather")
                all_ok = False
    
    # Check 4: Dependencies
    print("\n4. Checking dependencies...")
    dependencies = [
        ('telegram', 'python-telegram-bot'),
        ('aiosqlite', 'aiosqlite'),
        ('dotenv', 'python-dotenv'),
        ('better_profanity', 'better-profanity'),
        ('textblob', 'textblob'),
    ]
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - Not installed")
            print(f"      Run: pip install {package_name}")
            all_ok = False
    
    # Check 5: Import bot modules
    print("\n5. Checking bot modules...")
    modules = [
        'config',
        'database',
        'ai_moderator',
        'admin_commands'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}.py")
        except Exception as e:
            print(f"   ❌ {module}.py - {str(e)}")
            all_ok = False
    
    # Summary
    print("\n" + "="*60)
    if all_ok:
        print("  ✅ VERIFICATION PASSED")
        print("="*60)
        print("\n🎉 Your bot is ready to run!")
        print("\nNext steps:")
        print("  1. Make sure you've configured .env with your bot token")
        print("  2. Run: python bot.py")
        print("  3. Add bot to your Telegram group")
        print("  4. Make bot an admin")
        print("  5. Test with /start command")
        print("\n📚 See TESTING.md for comprehensive testing guide")
        return 0
    else:
        print("  ❌ VERIFICATION FAILED")
        print("="*60)
        print("\n⚠️  Please fix the issues above before running the bot.")
        print("\nQuick fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Create .env: cp .env.example .env")
        print("  • Add bot token to .env file")
        print("\n📚 See README.md for detailed setup instructions")
        return 1

if __name__ == '__main__':
    sys.exit(main())

