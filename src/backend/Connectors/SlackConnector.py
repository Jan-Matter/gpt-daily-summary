from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class SlackConnector:

    def __init__(self, token):
        self.__slack_client = WebClient(token=token)
        self.__slack_event_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events")
    
    def send_message(self, channel_id, message):
        api_response = self.__slack_client.chat_postMessage(
        channel= channel_id,
        text=message
        )
        return api_response


if __name__ == '__main__':
    token = os.environ["SLACK_BOT_TOKEN"]
    channel_id = os.environ["SLACK_CASHKURS_CHANNEL_ID"]
    slack_connector = SlackConnector(token)
    print(slack_connector.send_message(channel_id, "Hello! :tada:"))
