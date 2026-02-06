from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'discord_bot_dashboard_secret'

DB_PATH = os.environ.get('BOT_DB_PATH', '../data/bot.db')
LOG_PATH = os.environ.get('BOT_LOG_PATH', '../logs/bot.log')

def get_db():
    if os.path.exists(DB_PATH):
        return sqlite3.connect(DB_PATH)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/proposals')
def get_proposals():
    db = get_db()
    if not db:
        return jsonify([])
    c = db.cursor()
    c.execute('SELECT * FROM proposals ORDER BY created_at DESC LIMIT 20')
    proposals = c.fetchall()
    db.close()
    return jsonify(proposals)

@app.route('/api/leaderboard')
def get_leaderboard():
    db = get_db()
    if not db:
        return jsonify([])
    c = db.cursor()
    c.execute('SELECT user_id, username, xp, messages, reactions FROM user_stats ORDER BY xp DESC LIMIT 50')
    users = c.fetchall()
    db.close()
    return jsonify(users)

@app.route('/api/logs')
def get_logs():
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'bot.log')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            lines = f.readlines()[-100:]
        return jsonify(lines)
    return jsonify([])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
