# Reddit Job Monitor

A Python bot that monitors specified subreddits for job postings and sends notifications to Telegram.

## Overview

This script continuously monitors job-related subreddits for new posts containing specific keywords like "hiring" or "task". When it finds relevant posts from authors with sufficient karma, it formats the information and sends it to a Telegram chat via a bot.

## Features

- Monitors multiple subreddits simultaneously
- Filters posts by keywords in the title
- Verifies poster credibility by checking author karma
- Formats post details for Telegram including links to the original post
- Prevents duplicate notifications
- Error handling with Telegram notifications when issues occur

## Requirements

- Python 3.6+
- praw (Python Reddit API Wrapper)
- python-dotenv
- requests

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/airdward/reddit_scraper.git
   cd reddit_scraper
   ```

2. Install required packages:
   ```
   pip install -r req.txt
   ```

3. Create a `.env` file in the project directory with the following variables:
   ```
   CLIENT_ID=your_reddit_client_id
   CLIENT_SECRET=your_reddit_client_secret
   USERNAME=your_reddit_username
   PASSWORD=your_reddit_password
   TELEGRAM_KEY=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   ```

## Setup Instructions

### Reddit API Credentials
1. Go to https://www.reddit.com/prefs/apps
2. Click "create app" at the bottom
3. Fill in the required information:
   - Name: job_scraper (or any name you prefer)
   - Select "script"
   - Description: Optional
   - About URL: Optional
   - Redirect URI: http://localhost:8080
4. Click "create app"
5. Note the client ID (the string under the app name) and client secret

### Telegram Bot Setup
1. Message @BotFather on Telegram
2. Send the command `/newbot`
3. Follow the instructions to create a new bot
4. Note the bot token provided
5. Start a chat with your bot or add it to a group
6. Get the chat ID by:
   - For direct messages: Message the bot, then visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - For groups: Add the bot to the group, send a message in the group, then check the same URL

## Usage

Run the script:
```
python reddit_scraper.py
```

The script will:
- Start monitoring the specified subreddits
- Send a confirmation message to your Telegram chat
- Run continuously, checking for new posts every 15 minutes (900 seconds)
- Send notifications when new relevant posts are found

## Configuration

You can modify these parameters in the script:
- `subreddits`: List of subreddits to monitor
- `min_author_karma`: Minimum combined karma required for post authors
- `title_keywords`: Keywords to look for in post titles
- `limit`: Number of recent posts to check in each subreddit
- `check_interval`: Time between checks in seconds (default: 900 seconds/15 minutes)


## Disclaimer

This tool is for educational purposes only. Be sure to comply with Reddit's API terms of service and respect rate limits.