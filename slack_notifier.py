import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackNotifier:
    def __init__(self):
        self.client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

    def send_message(self, agent_name: str, message: str, channel: str = "#general"):
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=f"Agent: {agent_name}\nMessage: {message}"
            )
            return response
        except SlackApiError as e:
            print(f"Error sending message to Slack: {e.response['error']}")
            return None
