import os
import requests

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

def send_slack_message(message, target):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://slack.com/api/chat.postMessage", json={"channel": target, "text": message}, headers=headers)
    
    if response.status_code != 200:
        print(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
        raise Exception(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")
    else:
        print(f"Message sent to Slack successfully: {message}")

def search_slack(query):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    response_users = requests.get("https://slack.com/api/users.list", headers=headers)
    users = response_users.json().get('members', [])

    response_channels = requests.get("https://slack.com/api/conversations.list", headers=headers)
    channels = response_channels.json().get('channels', [])

    results = {
        "users": [user for user in users if query.lower() in user['name'].lower()],
        "channels": [channel for channel in channels if query.lower() in channel['name'].lower()]
    }
    
    return results
