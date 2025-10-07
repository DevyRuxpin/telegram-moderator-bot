"""
Comprehensive test suite for Telegram Moderator Bot
Run this to verify all core functionality works correctly
"""
import asyncio
import sys
from datetime import datetime

# Test imports
try:
    from config import Config
    from database import Database
    from ai_moderator import AIContentModerator
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)


class BotTester:
    """Comprehensive bot testing suite"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
    
    def test(self, name: str, condition: bool, details: str = ""):
        """Run a single test"""
        self.tests_run += 1
        if condition:
            self.passed += 1
            status = "✅ PASS"
        else:
            self.failed += 1
            status = "❌ FAIL"
        
        print(f"{status} - {name}")
        if details and not condition:
            print(f"     Details: {details}")
    
    def section(self, title: str):
        """Print section header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")
        print(f"  TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {self.tests_run}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        
        success_rate = (self.passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Bot is fully functional!")
            return True
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Please review.")
            return False


async def run_tests():
    """Run all tests"""
    tester = BotTester()
    
    # =================================================================
    # TEST 1: Configuration Tests
    # =================================================================
    tester.section("1. Configuration Tests")
    
    # Test config module
    tester.test(
        "Config module loads",
        hasattr(Config, 'BOT_TOKEN'),
        "Config class should have BOT_TOKEN attribute"
    )
    
    tester.test(
        "Default warn limit is set",
        Config.DEFAULT_WARN_LIMIT > 0,
        f"Expected > 0, got {Config.DEFAULT_WARN_LIMIT}"
    )
    
    tester.test(
        "Default ban duration is set",
        Config.DEFAULT_BAN_DURATION > 0,
        f"Expected > 0, got {Config.DEFAULT_BAN_DURATION}"
    )
    
    tester.test(
        "Database path is configured",
        len(Config.DATABASE_PATH) > 0,
        "Database path should not be empty"
    )
    
    # =================================================================
    # TEST 2: Database Tests
    # =================================================================
    tester.section("2. Database Tests")
    
    # Create test database
    test_db = Database('test_bot.db')
    
    try:
        await test_db.initialize()
        tester.test("Database initialization", True)
    except Exception as e:
        tester.test("Database initialization", False, str(e))
        return tester.summary()
    
    # Test warning operations
    try:
        warning_id = await test_db.add_warning(
            user_id=12345,
            chat_id=67890,
            username="testuser",
            reason="Test warning",
            warned_by=99999
        )
        tester.test("Add warning to database", warning_id > 0)
    except Exception as e:
        tester.test("Add warning to database", False, str(e))
    
    try:
        warnings = await test_db.get_warnings(12345, 67890)
        tester.test("Retrieve warnings from database", len(warnings) > 0)
    except Exception as e:
        tester.test("Retrieve warnings from database", False, str(e))
    
    try:
        count = await test_db.get_warning_count(12345, 67890)
        tester.test("Get warning count", count == 1, f"Expected 1, got {count}")
    except Exception as e:
        tester.test("Get warning count", False, str(e))
    
    # Test ban operations
    try:
        ban_id = await test_db.add_ban(
            user_id=12345,
            chat_id=67890,
            username="testuser",
            reason="Test ban",
            banned_by=99999,
            duration=3600
        )
        tester.test("Add ban to database", ban_id > 0)
    except Exception as e:
        tester.test("Add ban to database", False, str(e))
    
    try:
        is_banned = await test_db.is_banned(12345, 67890)
        tester.test("Check ban status", is_banned == True)
    except Exception as e:
        tester.test("Check ban status", False, str(e))
    
    # Test chat configuration
    try:
        config = await test_db.get_chat_config(67890)
        tester.test("Get chat config (defaults)", config is not None)
        tester.test(
            "Default warn limit in config",
            config['warn_limit'] == Config.DEFAULT_WARN_LIMIT
        )
    except Exception as e:
        tester.test("Get chat config", False, str(e))
    
    try:
        await test_db.set_chat_config(67890, warn_limit=5, ban_duration=7200)
        config = await test_db.get_chat_config(67890)
        tester.test("Update chat config", config['warn_limit'] == 5)
        tester.test("Config persists", config['ban_duration'] == 7200)
    except Exception as e:
        tester.test("Update chat config", False, str(e))
    
    # Test message tracking
    try:
        await test_db.track_message(12345, 67890)
        await test_db.track_message(12345, 67890)
        count = await test_db.get_recent_message_count(12345, 67890, 60)
        tester.test("Message tracking works", count >= 2, f"Expected >= 2, got {count}")
    except Exception as e:
        tester.test("Message tracking", False, str(e))
    
    # Test user stats
    try:
        stats = await test_db.get_user_stats(12345, 67890)
        tester.test("Get user stats", 'warnings' in stats and 'is_banned' in stats)
        tester.test("User stats accuracy", stats['warnings'] >= 1)
    except Exception as e:
        tester.test("Get user stats", False, str(e))
    
    # Cleanup
    try:
        cleared = await test_db.clear_warnings(12345, 67890)
        tester.test("Clear warnings", cleared >= 0)
    except Exception as e:
        tester.test("Clear warnings", False, str(e))
    
    # =================================================================
    # TEST 3: AI Moderator Tests
    # =================================================================
    tester.section("3. AI Content Moderation Tests")
    
    ai_mod = AIContentModerator()
    
    # Test profanity detection
    try:
        result = ai_mod.analyze_message("This is a clean message")
        tester.test("Clean message detection", not result['should_flag'])
    except Exception as e:
        tester.test("Clean message detection", False, str(e))
    
    try:
        result = ai_mod.analyze_message("fuck shit damn")
        tester.test("Profanity detection", result['has_profanity'])
        tester.test("Profanity flags message", result['should_flag'])
    except Exception as e:
        tester.test("Profanity detection", False, str(e))
    
    # Test spam detection
    try:
        spam_msg = "AAAAAAAAAA " * 10 + "http://spam.com " * 5
        result = ai_mod.analyze_message(spam_msg)
        tester.test("Spam detection", result['is_spam'])
    except Exception as e:
        tester.test("Spam detection", False, str(e))
    
    # Test URL spam
    try:
        url_spam = "Check http://link1.com and http://link2.com and http://link3.com"
        result = ai_mod.analyze_message(url_spam)
        tester.test("URL spam detection", result['is_spam'])
    except Exception as e:
        tester.test("URL spam detection", False, str(e))
    
    # Test toxic content
    try:
        toxic_msg = "I hate you, you should kill yourself"
        result = ai_mod.analyze_message(toxic_msg)
        tester.test("Toxic content detection", result['is_toxic'] or result['should_flag'])
    except Exception as e:
        tester.test("Toxic content detection", False, str(e))
    
    # Test flood detection
    try:
        is_flood = ai_mod.check_user_behavior(
            message_count=10,
            time_window=5,
            threshold=5
        )
        tester.test("Flood detection (positive)", is_flood == True)
        
        is_not_flood = ai_mod.check_user_behavior(
            message_count=3,
            time_window=10,
            threshold=5
        )
        tester.test("Flood detection (negative)", is_not_flood == False)
    except Exception as e:
        tester.test("Flood detection", False, str(e))
    
    # Test confidence scoring
    try:
        result = ai_mod.analyze_message("fuck spam http://test.com AAAAA")
        tester.test(
            "Confidence scoring",
            0 <= result['confidence'] <= 1,
            f"Confidence should be 0-1, got {result['confidence']}"
        )
    except Exception as e:
        tester.test("Confidence scoring", False, str(e))
    
    # =================================================================
    # TEST 4: Integration Tests
    # =================================================================
    tester.section("4. Integration Tests")
    
    # Test warning -> ban flow
    try:
        # Clear previous data
        await test_db.clear_warnings(99999, 11111)
        
        # Add warnings up to limit
        config = await test_db.get_chat_config(11111)
        warn_limit = config['warn_limit']
        
        for i in range(warn_limit):
            await test_db.add_warning(99999, 11111, "testuser", f"Warning {i+1}", 88888)
        
        count = await test_db.get_warning_count(99999, 11111)
        tester.test(
            "Warning accumulation",
            count == warn_limit,
            f"Expected {warn_limit}, got {count}"
        )
        
        # At this point, bot should trigger ban
        tester.test(
            "Warning limit reached (ban trigger point)",
            count >= warn_limit
        )
    except Exception as e:
        tester.test("Warning -> Ban flow", False, str(e))
    
    # Test AI -> Warning -> Ban flow
    try:
        # Simulate multiple violations
        violations = [
            "fuck you asshole",
            "SPAM SPAM http://spam.com",
            "shit damn hell"
        ]
        
        flagged_count = 0
        for msg in violations:
            result = ai_mod.analyze_message(msg)
            if result['should_flag']:
                flagged_count += 1
        
        tester.test(
            "AI detects multiple violations",
            flagged_count >= 2,
            f"Expected >= 2, got {flagged_count}"
        )
    except Exception as e:
        tester.test("AI violation detection", False, str(e))
    
    # =================================================================
    # TEST 5: Data Persistence Tests
    # =================================================================
    tester.section("5. Data Persistence Tests")
    
    try:
        # Add data
        await test_db.add_warning(77777, 88888, "persist_test", "Test", 11111)
        
        # Create new db instance (simulates bot restart)
        test_db2 = Database('test_bot.db')
        await test_db2.initialize()
        
        # Verify data persists
        count = await test_db2.get_warning_count(77777, 88888)
        tester.test("Data persists across restarts", count > 0)
    except Exception as e:
        tester.test("Data persistence", False, str(e))
    
    # =================================================================
    # TEST 6: Error Handling Tests
    # =================================================================
    tester.section("6. Error Handling Tests")
    
    # Test empty message handling
    try:
        result = ai_mod.analyze_message("")
        tester.test("Empty message handling", result is not None)
    except Exception as e:
        tester.test("Empty message handling", False, str(e))
    
    # Test None message handling
    try:
        result = ai_mod.analyze_message(None)
        tester.test("None message handling", result is not None)
    except Exception as e:
        tester.test("None message handling", False, str(e))
    
    # Test invalid user IDs
    try:
        warnings = await test_db.get_warnings(-1, -1)
        tester.test("Invalid user ID handling", isinstance(warnings, list))
    except Exception as e:
        tester.test("Invalid user ID handling", False, str(e))
    
    # =================================================================
    # Cleanup
    # =================================================================
    print("\n" + "="*60)
    print("  Cleaning up test database...")
    print("="*60)
    
    import os
    try:
        if os.path.exists('test_bot.db'):
            os.remove('test_bot.db')
            print("✅ Test database cleaned up")
    except Exception as e:
        print(f"⚠️  Could not remove test database: {e}")
    
    # Print summary
    return tester.summary()


async def main():
    """Main test runner"""
    print("\n" + "="*60)
    print("  TELEGRAM MODERATOR BOT - TEST SUITE")
    print("  Testing all core functionality...")
    print("="*60)
    
    success = await run_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

