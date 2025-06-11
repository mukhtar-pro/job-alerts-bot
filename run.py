import os
from app import create_app
from app.config import DEBUG, PORT, SLACK_BOT_TOKEN, JOB_ALERTS_CHANNEL, DAILY_REPORT_CHANNEL, DAILY_TARGET_COUNT

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Print essential startup information
    print("\n===== Job Alerts Slack Bot =====")
    print(f"Server running on port: {PORT}")
    print(f"Daily application target: {DAILY_TARGET_COUNT}")
    
    # Mask token for security in logs
    if SLACK_BOT_TOKEN:
        token_preview = f"{SLACK_BOT_TOKEN[:5]}...{SLACK_BOT_TOKEN[-5:]}" if len(SLACK_BOT_TOKEN) > 10 else "**INVALID TOKEN**"
        print(f"Using Slack token: {token_preview}")
        # Print token length to verify we have the full token
        print(f"Token length: {len(SLACK_BOT_TOKEN)} characters")
    else:
        print("WARNING: Slack token not set!")
    
    print("================================\n")
    
    # Run the Flask application - bind to 0.0.0.0 for deployment environments
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT) 