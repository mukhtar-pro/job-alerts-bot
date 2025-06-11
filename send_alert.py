import requests
import sys
import time
from datetime import datetime

def send_job_alert():
    """
    Send a job alert to the Slack channel by calling the API endpoint
    """
    try:
        # Call the /slack/send_alert endpoint
        response = requests.get("http://localhost:5000/slack/send_alert")
        print(response.text)
        return True
    except Exception as e:
        print(f"Error sending alert: {e}")
        return False

def send_daily_report():
    """
    Send a daily report of job applications by calling the API endpoint
    This also resets the counter for the next day
    """
    try:
        # Call the /slack/daily_report endpoint
        response = requests.get("http://localhost:5000/slack/daily_report")
        print(response.text)
        return True
    except Exception as e:
        print(f"Error sending daily report: {e}")
        return False

def clear_screen():
    """Clear the console screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display the main menu"""
    clear_screen()
    current_time = datetime.now().strftime("%I:%M:%S %p")
    current_date = datetime.now().strftime("%B %d, %Y")
    
    print("\n======================================")
    print(f"    JOB ALERTS SLACK BOT - RUNNING")
    print(f"    {current_date} | {current_time}")
    print("======================================\n")
    print("Choose an action:")
    print("1. Send job application reminder")
    print("2. Send daily report (will reset counter)")
    print("3. Auto-send mode (sends reminders at intervals)")
    print("Ctrl+C to force quit at any time\n")

def auto_send_mode():
    """
    Automatically send job reminders at regular intervals
    """
    interval_minutes = 0
    
    while True:
        clear_screen()
        print("\n======================================")
        print("    AUTO-SEND MODE CONFIGURATION")
        print("======================================\n")
        
        try:
            interval_minutes = int(input("Enter minutes between reminders (5-120): "))
            if 5 <= interval_minutes <= 120:
                break
            else:
                print("Please enter a value between 5 and 120 minutes.")
                time.sleep(2)
        except ValueError:
            print("Please enter a valid number.")
            time.sleep(2)
    
    # Convert to seconds
    interval_seconds = interval_minutes * 60
    sent_count = 0
    
    try:
        while True:
            clear_screen()
            current_time = datetime.now().strftime("%I:%M:%S %p")
            
            print("\n======================================")
            print("    AUTO-SEND MODE RUNNING")
            print(f"    Interval: {interval_minutes} minutes")
            print(f"    Reminders sent: {sent_count}")
            print(f"    Current time: {current_time}")
            print("======================================\n")
            print("Sending job application reminder...")
            
            if send_job_alert():
                sent_count += 1
                print(f"Reminder #{sent_count} sent successfully!")
            else:
                print("Failed to send reminder. Will try again next interval.")
            
            print(f"\nNext reminder will be sent in {interval_minutes} minutes.")
            print("Press Ctrl+C to return to the main menu.\n")
            
            # Countdown timer
            for remaining in range(interval_seconds, 0, -1):
                mins, secs = divmod(remaining, 60)
                timer = f"{mins:02d}:{secs:02d} until next reminder"
                print(timer, end="\r")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\nReturning to main menu...")
        time.sleep(1)
        return

if __name__ == "__main__":
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                print("\nSending job alert...")
                send_job_alert()
                print("\nPress Enter to continue...")
                input()
            
            elif choice == "2":
                print("\nSending daily report and resetting counter...")
                confirm = input("This will reset your application count. Continue? (y/n): ")
                if confirm.lower() == 'y':
                    send_daily_report()
                else:
                    print("Operation cancelled.")
                print("\nPress Enter to continue...")
                input()
            
            elif choice == "3":
                auto_send_mode()
            
            else:
                print("Invalid option. Please choose 1, 2, or 3.")
                time.sleep(1)
    
    except KeyboardInterrupt:
        clear_screen()
        print("\n======================================")
        print("    JOB ALERTS SLACK BOT - STOPPED")
        print("======================================\n")
        print("The script has been manually terminated.")
        print("Thank you for using Job Alerts Slack Bot!\n")
        sys.exit(0)