import pytest
import os
import sys
import sqlite3
import shutil
from unittest.mock import MagicMock

# Add project root to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database

@pytest.fixture
def temp_db(tmp_path):
    """
    Fixture to create a temporary database for testing.
    This ensures tests don't touch the production database.
    """
    # Create a temporary directory for the DB
    db_dir = tmp_path / "data"
    db_dir.mkdir()
    db_path = db_dir / "bot.db"
    
    # Mock the database path in the database module
    original_db_path = database.DB_PATH
    database.DB_PATH = str(db_path)
    
    # Initialize the database
    database.init_db()
    
    yield
    
    # Teardown: Restore original path (cleanup happens automatically by tmp_path)
    database.DB_PATH = original_db_path
    
@pytest.fixture
def mock_bot():
    """
    Fixture to create a mock bot instance.
    """
    bot = MagicMock()
    bot.user.name = "TestBot"
    bot.user.id = 123456789
    return bot
