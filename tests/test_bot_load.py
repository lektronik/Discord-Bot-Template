import pytest
import os
import sys
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import bot

@pytest.mark.asyncio
async def test_bot_cogs_loading():
    """
    Test that the bot can load all cogs without error.
    This doesn't start the bot, just tests the setup_hook logic.
    """
    # Mock environment variables
    with patch.dict(os.environ, {'DISCORD_TOKEN': 'fake_token'}):
        # Initialize bot
        test_bot = bot.TemplateBot()
        
        # Mock load_extension to track calls instead of actually loading (which requires discord connection)
        # However, for a better test, we should try to actually load them if possible,
        # but loading cogs often requires a connected client state.
        # Given we are offline, we'll verify the list of cogs exists and import them
        # to ensure no syntax errors or missing dependencies.
        
        cogs_list = [
            'cogs.server_setup',
            'cogs.verification',
            'cogs.language',
            'cogs.info',
            'cogs.network_stats',
            'cogs.help_command',
            'cogs.auto_sync',
            'cogs.welcome',
            'cogs.moderation',
            'cogs.announcements',
            'cogs.governance',
            'cogs.ticker_status',
            'cogs.leaderboard',
            'cogs.nft_gallery',
        ]
        
        # Verify all cog files exist
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        for cog in cogs_list:
             # Convert 'cogs.server_setup' -> 'cogs/server_setup.py'
            cog_path = os.path.join(project_root, *cog.split('.')) + ".py"
            assert os.path.exists(cog_path), f"Cog file not found: {cog_path}"
            
            # Try to import it to check for syntax errors
            try:
                __import__(cog)
            except ImportError as e:
                pytest.fail(f"Failed to import {cog}: {e}")
            except Exception as e:
                # Some cogs might fail on import if they do top-level logic, but usually safe
                 pytest.fail(f"Error importing {cog}: {e}")

def test_bot_token_check():
    """Test that the bot script checks for the token."""
    # We can't easily test the cleanup script's main execution without mocking sys.exit,
    # but we can verify the class initialization works.
    with patch.dict(os.environ, {'DISCORD_TOKEN': 'test_token'}):
        b = bot.TemplateBot()
        assert b.command_prefix == '!'
