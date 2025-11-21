Deployment In Termux 🔥 
# 🚀 OSINET_MAX — Termux Installation Guide (Beginner Friendly)

This guide explains how to install and run the **OSINET_MAX Telegram bot** on **Termux**, step by step — simple, clean, and error-free.

---

## 📦 Requirements
Before starting, install **Termux** (latest version from F-Droid recommended).

---

## 🟦 STEP 1 — Install Required Packages

```bash
pkg update && pkg upgrade
pkg install python git
pip install --upgrade pip

🟩 STEP 2 — Download the Bot

cd ~
git clone https://github.com/Itsunknownme/OSINET_MAX.git
cd OSINET_MAX

🟨 STEP 3 — Install Dependencies

pip install -r requirements.txt

STEP 4 — Create .env File (Important)
nano .env

Paste and modify your values:
Copy code

BOT_TOKEN=1234567890:ABCDEF-YOUR-TOKEN
ADMIN_ID=5633810208
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW=60
DATABASE_FILE=bot_data.db
USERS_FILE=users.json
REQUEST_TIMEOUT=10
MAX_RETRIES=3
ENABLE_OCR=false
ENABLE_IMAGE_PROCESSING=true
LOG_LEVEL=INFO
LOG_FILE=bot.log

Save: CTRL + X → Y → ENTER

🟥 STEP 5 — Replace config.py
cat > config.py

"""
Configuration module for the Telegram bot
Handles all configuration settings and environment variables
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class for bot settings"""

    def init(self):
        # Bot configuration
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', '')
        self.ADMIN_ID = os.getenv('ADMIN_ID', '')

        # Validate BOT_TOKEN
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")

        # Validate ADMIN_ID
        if not self.ADMIN_ID or not self.ADMIN_ID.isdigit():
            raise ValueError("ADMIN_ID must be a numeric Telegram user ID")
        else:
            self.ADMIN_ID = int(self.ADMIN_ID)

        # 🚫 No required channels
        self.REQUIRED_CHANNELS = []

        # Rate limiting settings
        self.RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '5'))
        self.RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))  # seconds

        # Database settings
        self.DATABASE_FILE = os.getenv('DATABASE_FILE', 'bot_data.db')
        self.USERS_FILE = os.getenv('USERS_FILE', 'users.json')

        # Scraping settings
        self.REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
        self.MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

        # Feature flags
        self.ENABLE_OCR = os.getenv('ENABLE_OCR', 'false').lower() == 'true'
        self.ENABLE_IMAGE_PROCESSING = os.getenv('ENABLE_IMAGE_PROCESSING', 'true').lower() == 'true'

        # Logging settings
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

    def get_user_agent(self) -> str:
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

    def get_request_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": self.get_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

CTRL + D to Save


STEP 6 — Export Values (Only Once Per Session)
Copy code
Bash
export BOT_TOKEN="your-bot-token-here"
export ADMIN_ID=your-telegram-id-here

🌄STEP 7 — Run the Bot
Copy code
Bash
python main.py
Expected output:
Copy code

Bot started...
Application started

🎉 Done!
Your bot is now running successfully.

#----------------------------------#

---

🟪 RUN BOT 24/7 IN BACKGROUND (PM2 / SCREEN / NOHUP)

Choose any one method below based on your preference.


---

💠 METHOD 1 — Run 24/7 using PM2 (Recommended)

📥 Install Node.js & PM2

pkg install nodejs -y
npm install pm2 -g

▶ Start the bot

pm2 start main.py --interpreter=python

🔄 Auto-restart on crash

pm2 startup
pm2 save

📌 Useful Commands

Description	Command

Show running processes	pm2 list
Restart bot	pm2 restart main
Stop bot	pm2 stop main
Logs	pm2 logs



---

💠 METHOD 2 — Run 24/7 using screen

(Perfect for simple background execution)

📥 Install screen

pkg install screen -y

▶ Start bot inside screen

screen -S osinet
python main.py

🔙 Detach screen (bot keeps running)

CTRL + A + D

♻ Reopen screen

screen -r osinet

❌ Kill screen session

screen -X -S osinet kill


---

💠 METHOD 3 — Run 24/7 using nohup

(Simplest)

▶ Run the bot

nohup python main.py &

📄 View logs

tail -f nohup.out


---

🧠 Which Should You Choose?

Method	Best For	Pros

PM2	Long-term stable bots	Auto-restart, crash protection, logs
Screen	Beginners, simple control	Easy resume & monitoring
Nohup	Quick background	Lightweight



---

🎯 Example Recommended Setup

Most users should use PM2:

pkg install nodejs
npm install pm2 -g
pm2 start main.py --interpreter=python
pm2 save
pm2 startup


---

🧰 Extra — Auto Restart Script (Optional)

Create start.sh:

cat > start.sh << 'EOF'
#!/bin/bash
while true
do
  python main.py
  echo "Bot crashed! Restarting in 3 seconds..."
  sleep 3
done
EOF

Make it executable:

chmod +x start.sh

Run:

./start.sh


---

🟢 Done — Bot Now Runs 24/7 Automatically 🎉

#----------------------------------#
## Deploy Via Buttons

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/gajendrajangid83/OSINET_MAX)

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?button-url=https://github.com/xpingpongx/Extractor-V3&template=https://github.com/gajendrajangid83/OSINET_MAX)

# Telegram Phone Tracer & Vehicle Lookup Bot

A comprehensive Telegram bot that provides phone number tracing and vehicle registration lookup services with advanced image processing capabilities.

## Features

### 🔍 Phone Tracing
- Comprehensive phone number lookup using multiple sources
- Support for international and local number formats
- Detailed information extraction including carrier, location, and more
- Rate limiting to prevent abuse

### 🚗 Vehicle Lookup
- Vehicle registration number lookup for Indian vehicles
- Comprehensive RTO database with detailed information
- State and district identification
- Vehicle type classification

### 📸 Image Processing
- EXIF data extraction from images
- GPS coordinate extraction and mapping
- OCR text extraction (optional)
- Support for multiple image formats

### 👥 User Management
- User activity tracking and statistics
- Membership verification for required channels
- Admin controls and broadcasting
- Comprehensive logging system

### 🛡️ Security Features
- Rate limiting to prevent spam
- Input validation and sanitization
- Secure environment variable handling
- Error handling and logging

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Admin user ID

### 2. Environment Variables
Create a `.env` file or set the following environment variables:

```bash
# Required
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_admin_user_id

# Optional Configuration
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW=60
REQUEST_TIMEOUT=10
MAX_RETRIES=3

# Feature Flags
ENABLE_OCR=true
ENABLE_IMAGE_PROCESSING=true

# Database
DATABASE_FILE=bot_data.db
USERS_FILE=users.json

# Logging
LOG_LEVEL=INFO
LOG_FILE=bot.log
