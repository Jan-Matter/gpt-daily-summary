from slack_sdk import WebClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class SlackConnector:

    def __init__(self, token):
        self.__slack_client = WebClient(token=token)
    
    def send_message(self, channel_id, message):
        api_response = self.__slack_client.chat_postMessage(
        channel= channel_id,
        text=message
        )
        return api_response
    
    def get_messages(self, channel_id):
        return self.__slack_client.conversations_history(channel=channel_id, limit=100)["messages"]


if __name__ == '__main__':
    token = os.environ["SLACK_BOT_TOKEN"]
    channel_id = os.environ["SLACK_CASHKURS_CHANNEL_ID"]
    slack_connector = SlackConnector(token)
    print(slack_connector.get_messages(channel_id))
