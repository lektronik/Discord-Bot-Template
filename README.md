# 🤖 Generic Bot Template

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-5865F2.svg)](https://discordpy.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A **feature-rich** Discord bot template with 16+ features including governance voting, leaderboards, network stats, moderation tools, and an admin dashboard.

---

## ✨ Features

| Category | Features |
|----------|----------|
| **🏛️ Governance** | DAO voting, persistent proposals, SQLite storage |
| **🏆 Engagement** | XP leaderboard, message tracking, reaction rewards |
| **📊 Stats** | Live network stats from API, auto-refresh |
| **🛡️ Moderation** | Purge, slowmode, spam filter |
| **🌐 Multi-Language** | English, Greek, Spanish, Russian, Japanese |
| **📢 Announcements** | Rich embed broadcasts |
| **🎫 Verification** | Button-based member verification |
| **📈 Dashboard** | Flask admin panel |

---

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/lektronik/Discord-Bot-Template.git
cd Discord-Bot-Template
```

### 2. Install
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure
```bash
cp .env.example .env
# Edit .env and add your DISCORD_TOKEN
```

### 4. Run
```bash
python bot.py
```

---

## 📋 Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!setup_server` | Auto-configure channels | Admin |
| `!stats` | Network statistics | All |
| `!leaderboard` | Top members by XP | All |
| `!rank` | Your stats | All |
| `!propose "Title" desc` | Create vote | Admin |
| `!proposals` | List all votes | All |
| `!announce msg` | Broadcast message | Admin |
| `!purge N` | Delete N messages | Admin |
| `!help` | Show all commands | All |

---

## 📁 Project Structure

```
├── bot.py              # Entry point
├── database.py         # SQLite layer
├── cogs/
│   ├── governance.py   # DAO voting
│   ├── leaderboard.py  # XP tracking
│   ├── moderation.py   # Admin tools
│   ├── network_stats.py# API integration
│   └── ...             # 10 more cogs
└── dashboard/
    └── app.py          # Flask admin panel
```

---

## ⚙️ Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | ✅ | Your bot token |
| `API_BASE_URL` | ❌ | Optional API endpoint |
| `WEBSITE_URL` | ❌ | Optional website link |

### Discord Developer Portal

Enable these **Privileged Intents**:
- ✅ Presence Intent
- ✅ Server Members Intent
- ✅ Message Content Intent

---

## 🤝 Contributing

Pull requests welcome! Please read the contributing guidelines first.

## 📄 License

MIT License - feel free to use and modify!

---

<p align="center">
  <b>⭐ Star this repo if you find it useful!</b>
</p>

---

## 🧪 Testing

This project uses `pytest` for testing.

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run tests
```bash
pytest
```
