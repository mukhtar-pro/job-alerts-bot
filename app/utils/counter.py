import os
from app.config import COUNT_FILE

def get_applied_count():
    """
    Read the current application count from the file.
    Returns 0 if the file doesn't exist.
    """
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            count = int(f.read().strip())  # Read the current count
        return count
    else:
        return 0  # Return 0 if file doesn't exist

def increment_applied_count():
    """
    Increment the application count and save it to the file.
    Returns the new count after incrementing.
    """
    applied_count = get_applied_count()
    applied_count += 1  # Increment the count
    with open(COUNT_FILE, 'w') as f:
        f.write(str(applied_count))  # Update the count in the file
    return applied_count 

def reset_applied_count():
    """
    Reset the application count to zero.
    This is typically called after sending the daily report.
    """
    with open(COUNT_FILE, 'w') as f:
        f.write('0')  # Reset count to zero
    return 0 