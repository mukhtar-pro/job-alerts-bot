from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.config import SLACK_BOT_TOKEN, JOB_ALERTS_CHANNEL, DAILY_REPORT_CHANNEL, DAILY_TARGET_COUNT

# Initialize the Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

def update_message(channel_id, message_ts, user_id, applied_count):
    """
    Update a message after a user clicks the Apply button.
    
    Args:
        channel_id (str): The Slack channel ID
        message_ts (str): The message timestamp to update
        user_id (str): The ID of the user who clicked the button
        applied_count (int): The current count of applications
        
    Returns:
        dict: The Slack API response or error message
    """
    # Calculate percentage progress
    progress_percentage = min(100, round((applied_count / DAILY_TARGET_COUNT) * 100, 1))
    
    # Get current time for the confirmation
    from datetime import datetime
    current_time = datetime.now().strftime("%I:%M %p")  # e.g., "10:45 AM"
    current_date = datetime.now().strftime("%B %d, %Y")  # e.g., "July 12, 2023"
    
    try:
        # Update the message without the button - more seamless markdown
        response = client.chat_update(
            channel=channel_id,
            ts=message_ts,
            text=f"Job Application Marked as Applied",
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Job Application Confirmed",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":white_check_mark: *Application marked as completed*\n• User: <@{user_id}>\n• Time: {current_time}\n• Date: {current_date}"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Today's Progress:*\n{applied_count}/{DAILY_TARGET_COUNT} applications"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Completion:*\n{progress_percentage}%"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Keep up the great work! Each application increases your chances of landing an interview."
                        }
                    ]
                }
            ]
        )
        return {"success": True, "response": response}
    except SlackApiError as e2:
        return {"success": False, "error": f"Failed to update message: {e2.response['error']}"}

def send_job_alert():
    """
    Send a job alert message with an Apply button to the job alerts channel.
    
    Returns:
        dict: The Slack API response or error message
    """
    try:
        response = client.chat_postMessage(
            channel=JOB_ALERTS_CHANNEL,
            text="Job Application Reminder",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":bell: *Job Application Reminder* :bell:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Time to apply for a job! Regular applications increase your chances of landing interviews."
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Today's goal: *{DAILY_TARGET_COUNT} applications*"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "I've Applied!",
                                "emoji": True
                            },
                            "action_id": "apply_button",
                            "style": "primary"
                        }
                    ]
                }
            ]
        )
        return {"success": True, "response": response}
    except SlackApiError as e:
        error_message = f"Error sending message: {e.response['error']}"
        return {"success": False, "error": error_message}

def send_daily_report(applied_count, today_date):
    """
    Send a daily report of job applications to the daily report channel.
    
    Args:
        applied_count (int): The count of applications marked as applied
        today_date (str): The formatted date string
        
    Returns:
        dict: The Slack API response or error message
    """
    # Calculate percentage of target achieved
    achievement_percentage = min(100, round((applied_count / DAILY_TARGET_COUNT) * 100, 1))
    
    # Determine status emoji based on achievement
    if achievement_percentage >= 100:
        status_emoji = ":star2:"
        status_text = "Goal achieved! Excellent work!"
    elif achievement_percentage >= 75:
        status_emoji = ":star:"
        status_text = "Great progress today!"
    elif achievement_percentage >= 50:
        status_emoji = ":white_check_mark:"
        status_text = "Good effort, halfway there!"
    elif achievement_percentage >= 25:
        status_emoji = ":hourglass:"
        status_text = "Getting started, keep going!"
    else:
        status_emoji = ":warning:"
        status_text = "More effort needed tomorrow."
    
    try:
        response = client.chat_postMessage(
            channel=DAILY_REPORT_CHANNEL,
            text=f"Daily Job Application Report - {today_date}",
            blocks=[
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"Daily Job Application Report - {today_date}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{status_emoji} *{applied_count}/{DAILY_TARGET_COUNT}* applications completed today ({achievement_percentage}%)"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": status_text
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Daily Goal:* {DAILY_TARGET_COUNT} applications"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Completion:* {achievement_percentage}%"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "The counter has been reset for tomorrow."
                        }
                    ]
                }
            ]
        )
        return {"success": True, "response": response}
    except SlackApiError as e:
        error_message = f"Error sending daily report: {e.response['error']}"
        return {"success": False, "error": error_message} 