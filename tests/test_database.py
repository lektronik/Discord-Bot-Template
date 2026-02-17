import pytest
import sqlite3
import database

def test_init_db(temp_db):
    """Test that database tables are created successfully."""
    conn = database.get_connection()
    c = conn.cursor()
    
    # Check if tables exist
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in c.fetchall()}
    
    assert 'proposals' in tables
    assert 'votes' in tables
    assert 'user_stats' in tables
    conn.close()

def test_create_and_get_proposal(temp_db):
    """Test creating a proposal and retrieving it."""
    proposal_id = database.create_proposal(
        title="Test Proposal",
        description="This is a test",
        author_id=123,
        author_name="TestUser"
    )
    
    assert proposal_id is not None
    
    proposals = database.get_proposals()
    assert len(proposals) == 1
    
    p = proposals[0]
    # Check columns based on schema: 
    # id, title, description, author_id, author_name, created_at, status, yes, no, msg_id
    assert p[1] == "Test Proposal"
    assert p[2] == "This is a test"
    assert p[3] == 123
    assert p[4] == "TestUser"
    assert p[6] == "active"
    assert p[7] == 0 # yes_votes
    assert p[8] == 0 # no_votes

def test_record_vote(temp_db):
    """Test voting on a proposal."""
    proposal_id = database.create_proposal("Vote Test", "Desc", 123, "User")
    
    # Test Yes vote
    success = database.record_vote(proposal_id, 456, 'yes')
    assert success is True
    
    # Check updated counts
    proposals = database.get_proposals()
    assert proposals[0][7] == 1 # yes_votes
    assert proposals[0][8] == 0 # no_votes
    
    # Verify has_voted
    assert database.has_voted(proposal_id, 456) is True
    assert database.has_voted(proposal_id, 789) is False

def test_double_vote_prevention(temp_db):
    """Test that a user cannot vote twice on the same proposal."""
    proposal_id = database.create_proposal("Double Vote", "Desc", 111, "User")
    
    # First vote
    assert database.record_vote(proposal_id, 222, 'yes') is True
    
    # Second vote (should fail due to UNIQUE constraint)
    assert database.record_vote(proposal_id, 222, 'no') is False
    
    # Verify counts didn't change for the second vote
    proposals = database.get_proposals()
    assert proposals[0][7] == 1
    assert proposals[0][8] == 0

def test_user_stats_update(temp_db):
    """Test updating user statistics."""
    user_id = 999
    username = "StatsUser"
    
    # Initial update
    database.update_user_stats(user_id, username, messages=5, reactions=2)
    
    # Verify initial stats
    # XP = messages*10 + reactions*5 = 50 + 10 = 60
    rank, user = database.get_user_rank(user_id)
    assert user[1] == username
    assert user[2] == 5 # messages
    assert user[3] == 2 # reactions
    assert user[5] == 60 # xp
    
    # Update again (incremental)
    database.update_user_stats(user_id, username, messages=2, reactions=1)
    
    # Verify updated stats
    # New messages = 5+2=7, New reactions = 2+1=3
    # New XP = 60 + (2*10+1*5) = 60 + 25 = 85
    _, user = database.get_user_rank(user_id)
    assert user[2] == 7
    assert user[3] == 3
    assert user[5] == 85

def test_leaderboard(temp_db):
    """Test leaderboard ranking."""
    database.update_user_stats(1, "User1", messages=10) # 100 XP
    database.update_user_stats(2, "User2", messages=20) # 200 XP
    database.update_user_stats(3, "User3", messages=5)  # 50 XP
    
    leaderboard = database.get_leaderboard(limit=3)
    
    assert len(leaderboard) == 3
    assert leaderboard[0][0] == 2 # User2 (Highest XP)
    assert leaderboard[1][0] == 1 # User1
    assert leaderboard[2][0] == 3 # User3
