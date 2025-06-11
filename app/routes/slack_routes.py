import json
from datetime import datetime
from flask import jsonify, request, Blueprint
from app.utils.counter import get_applied_count, increment_applied_count, reset_applied_count
from app.services.slack_service import update_message, send_job_alert, send_daily_report

# Create a Blueprint for Slack routes
slack_bp = Blueprint('slack', __name__)

@slack_bp.route('/actions', methods=['POST'])
def slack_actions():
    """
    Handle Slack interactive actions (button clicks)
    """
    try:
        payload = request.form['payload']
        data = json.loads(payload)
        action_id = data['actions'][0]['action_id']
        
        # Extract needed data from the payload
        channel_id = data['channel']['id']
        message_ts = data['message']['ts']

        # Check if the action was the 'Apply' button
        if action_id == "apply_button":
            user_id = data['user']['id']  # User who clicked the button
            
            # Increment the applied count
            applied_count = increment_applied_count()

            # Update the message in Slack - removes the button
            result = update_message(channel_id, message_ts, user_id, applied_count)
            
            if result["success"]:
                return jsonify({"text": "Applied!"})
            else:
                return jsonify({"text": result["error"]})
                
        return '', 200
    except Exception as e:
        return jsonify({"text": f"Error: {str(e)}"}), 500

@slack_bp.route('/send_alert', methods=['GET'])
def send_alert():
    """
    Send a job alert message with an Apply button
    """
    result = send_job_alert()
    
    if result["success"]:
        return f"Message posted successfully! {result['response']['message']['ts']}"
    else:
        return f"Error sending message: {result['error']}"

@slack_bp.route('/daily_report', methods=['GET'])
def daily_report():
    """
    Send a daily report of job applications and reset the counter
    """
    # Get the current count before resetting
    applied_count = get_applied_count()
    today_date = datetime.now().strftime("%B %d, %Y")  # Get today's date
    
    # Send the daily report
    result = send_daily_report(applied_count, today_date)
    
    # Reset the counter after sending the report
    reset_applied_count()
    
    if result["success"]:
        return f"Daily report sent successfully and counter reset to 0! {result['response']['message']['ts']}"
    else:
        return f"Error sending daily report: {result['error']}" 