import os
from dotenv import load_dotenv

# Load environment variables from .env file
if os.environ.get("FLASK_ENV") == "development":
    load_dotenv()

# Slack configuration
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
JOB_ALERTS_CHANNEL = os.getenv('JOB_ALERTS_CHANNEL')
DAILY_REPORT_CHANNEL = os.getenv('DAILY_REPORT_CHANNEL')

# File storage settings
COUNT_FILE = 'applied_count.txt'

# Application settings
DAILY_TARGET_COUNT = int(os.getenv('DAILY_TARGET_COUNT', 60))  # Target number of applications per day

# Flask settings
DEBUG = True
PORT = 5000 