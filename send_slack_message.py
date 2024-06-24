import requests
import os

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

def send_slack_message(message, target):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        json={"channel": target, "text": message},
        headers={"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-Type": "application/json"}
    )

    if response.status_code != 200 or not response.json().get('ok'):
        print(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
        raise Exception(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    else:
        print(f"Message sent to Slack successfully: {message}")
