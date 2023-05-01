from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from datetime import date
import asyncio
import sys
import os

load_dotenv(find_dotenv())



sys.path.append(str(Path(__file__).parent.parent.parent))
from src.backend.Controllers.CashkursArticlesController import CashkursArticlesController
from src.backend.Connectors.SlackConnector import SlackConnector

if __name__ == '__main__':
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    cashkurs_channel_id = os.environ["SLACK_CASHKURS_CHANNEL_ID"]
    cashkurs_articles_controller = CashkursArticlesController()
    slack_connector  = SlackConnector(slack_token)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(cashkurs_articles_controller.refresh_articles())
    
    articles = cashkurs_articles_controller.get_articles()
    for article in articles:
        if article["date"] == date.today().strftime('%Y-%m-%d'):
            message = f"""
                *{article["title"]}*

    {article["summary"]}

    Full article: {article["link"]}
            """
            slack_connector.send_message(cashkurs_channel_id, message)

