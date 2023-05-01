from quart import Quart, request
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import sys
import os

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.backend.Controllers.CashkursArticlesController import CashkursArticlesController
from src.backend.Connectors.SlackConnector import SlackConnector

load_dotenv(find_dotenv())

#def check_signing():



app = Quart(__name__)

slack_connector = SlackConnector(os.environ["SLACK_BOT_TOKEN"])
cashkurs_connector = CashkursArticlesController()


@app.route("/api/cashkurs", methods=["GET", "POST"])
async def cashkurs():
    if request.method == "POST":
        body = await request.json
        print(body)
        messages = slack_connector.get_messages(os.environ["SLACK_CASHKURS_CHANNEL_ID"])
        text = body["text"]
        output = [message for message in messages if message["latest_reply"] == body["event_ts"]]
        print(output)
        if "challenge" in body:
            return {"challenge": body["challenge"]}
        return {"message": "Hello world!"}
    elif request.method == "GET":
        return {"message": "Hello world!"}
    
if __name__ == "__main__":
    app.run()