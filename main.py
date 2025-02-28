import praw
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent='job_scraper',
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),

)

def send_posts_to_telegram(reddit, subreddit_names, telegram_bot_token, telegram_chat_id,
                           min_author_karma=200, title_keywords=["hiring", "task"],
                           limit=50, check_interval=3600):

    # Track posts we've already sent to avoid duplicates
    sent_posts = set()

    # Function to send a message to Telegram
    def send_telegram_message(message):
        telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(telegram_url, data=payload)
        return response.json()

    # Initial message to confirm the bot is running
    send_telegram_message("🤖 *Reddit Monitor Started*\nWatching for posts with author karma > "
                          f"{min_author_karma} and keywords: {', '.join(title_keywords)}")

    # Main monitoring loop
    while True:
        try:
            print(f"Checking subreddits at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")

            for subreddit_name in subreddit_names:
                print(f"Scanning r/{subreddit_name}...")
                subreddit = reddit.subreddit(subreddit_name)

                # Check new submissions
                for submission in subreddit.new(limit=limit):
                    # Skip if we've already processed this post
                    if submission.id in sent_posts:
                        continue

                    # Check if title contains any of the keywords
                    title_lower = submission.title.lower()
                    if any(keyword.lower() in title_lower for keyword in title_keywords):
                        # Check if author exists and has sufficient karma
                        if submission.author is not None:
                            author_karma = submission.author.link_karma + submission.author.comment_karma

                            if author_karma > min_author_karma:
                                # Create message for Telegram
                                message = (
                                    f"*New Post in r/{subreddit_name}*\n\n"
                                    f"*Title:* {submission.title}\n"
                                    f"*Author:* u/{submission.author.name} (Karma: {author_karma})\n"
                                    f"*Score:* {submission.score} | *Comments:* {submission.num_comments}\n"
                                    f"*Posted:* {datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                                    f"[View on Reddit](https://www.reddit.com{submission.permalink})"
                                )

                                # Send to Telegram
                                print(f"Sending post {submission.id} to Telegram...")
                                response = send_telegram_message(message)

                                if response.get('ok'):
                                    # Add to sent posts
                                    sent_posts.add(submission.id)
                                    print(f"Successfully sent post {submission.id}")
                                else:
                                    print(f"Failed to send post {submission.id}: {response}")

                print(f"Finished scanning r/{subreddit_name}")

            # Limit the size of sent_posts to avoid memory issues in long runs
            if len(sent_posts) > 1000:
                sent_posts = set(list(sent_posts)[-1000:])

            print(f"Sleeping for {check_interval} seconds...")
            time.sleep(check_interval)

        except Exception as e:
            error_message = f"❌ *Error:* {str(e)}\nMonitor will try again in {check_interval} seconds."
            print(error_message)
            send_telegram_message(error_message)
            time.sleep(check_interval)


if __name__ == "__main__":

   #Telegram bot credentials
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_KEY")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    # Subreddits to monitor
    subreddits = ['hiring', 'forhire', 'donedirtcheap', 'freelance_forhire']

    # Start monitoring
    send_posts_to_telegram(
        reddit=reddit,
        subreddit_names=subreddits,
        telegram_bot_token=TELEGRAM_BOT_TOKEN,
        telegram_chat_id=TELEGRAM_CHAT_ID,
        min_author_karma=200,
        title_keywords=["hiring", "task"],
        limit=50,
        check_interval=900
    )