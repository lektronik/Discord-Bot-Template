import sqlite3
import os
import logging

logger = logging.getLogger('discord_bot.database')

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'bot.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            author_id INTEGER NOT NULL,
            author_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            yes_votes INTEGER DEFAULT 0,
            no_votes INTEGER DEFAULT 0,
            message_id INTEGER
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            vote TEXT NOT NULL,
            voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (proposal_id) REFERENCES proposals(id),
            UNIQUE(proposal_id, user_id)
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            messages INTEGER DEFAULT 0,
            reactions INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized")

def create_proposal(title, description, author_id, author_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO proposals (title, description, author_id, author_name)
        VALUES (?, ?, ?, ?)
    ''', (title, description, author_id, author_name))
    proposal_id = c.lastrowid
    conn.commit()
    conn.close()
    return proposal_id

def get_proposals(status='active'):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM proposals WHERE status = ? ORDER BY created_at DESC', (status,))
    proposals = c.fetchall()
    conn.close()
    return proposals

def record_vote(proposal_id, user_id, vote):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO votes (proposal_id, user_id, vote) VALUES (?, ?, ?)
        ''', (proposal_id, user_id, vote))
        
        if vote == 'yes':
            c.execute('UPDATE proposals SET yes_votes = yes_votes + 1 WHERE id = ?', (proposal_id,))
        else:
            c.execute('UPDATE proposals SET no_votes = no_votes + 1 WHERE id = ?', (proposal_id,))
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def has_voted(proposal_id, user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT 1 FROM votes WHERE proposal_id = ? AND user_id = ?', (proposal_id, user_id))
    result = c.fetchone() is not None
    conn.close()
    return result

def update_user_stats(user_id, username, messages=0, reactions=0):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO user_stats (user_id, username, messages, reactions, xp)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            messages = user_stats.messages + excluded.messages,
            reactions = user_stats.reactions + excluded.reactions,
            xp = user_stats.xp + (excluded.messages * 10) + (excluded.reactions * 5),
            last_active = CURRENT_TIMESTAMP
    ''', (user_id, username, messages, reactions, messages * 10 + reactions * 5))
    conn.commit()
    conn.close()

def get_leaderboard(limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT user_id, username, xp, messages, reactions
        FROM user_stats
        ORDER BY xp DESC
        LIMIT ?
    ''', (limit,))
    users = c.fetchall()
    conn.close()
    return users

def get_user_rank(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(*) + 1 FROM user_stats WHERE xp > (
            SELECT COALESCE(xp, 0) FROM user_stats WHERE user_id = ?
        )
    ''', (user_id,))
    rank = c.fetchone()[0]
    c.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return rank, user

init_db()
