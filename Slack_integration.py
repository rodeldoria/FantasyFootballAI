import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

def send_slack_message(message):
    if SLACK_WEBHOOK_URL is None:
        raise ValueError("SLACK_WEBHOOK_URL is not set")
    
    payload = {
        "text": message
    }
    
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise Exception(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    else:
        print(f"Message sent to Slack successfully: {message}")

# Example usage
if __name__ == "__main__":
    send_slack_message("Hello, this is a test message from Python!")
