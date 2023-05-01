from quart import Quart, request
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import sys
import os

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.backend.Controllers.CashkursArticlesController import CashkursArticlesController
from src.backend.Connectors.SlackConnector import SlackConnector
from src.backend.Controllers.GPTChatController import GPTChatController

load_dotenv(find_dotenv())

#def check_signing():



app = Quart(__name__)

slack_connector = SlackConnector(os.environ["SLACK_BOT_TOKEN"])
cashkurs_connector = CashkursArticlesController()
gpt_controller = GPTChatController()
articles = {article["title"]: article for article in cashkurs_connector.get_articles()}



@app.route("/api/cashkurs", methods=["GET", "POST"])
async def cashkurs():
    if request.method == "POST":
        body = await request.json
        try:
            messages = slack_connector.get_messages(os.environ["SLACK_CASHKURS_CHANNEL_ID"])
            question = body["event"]["text"]
            print(question)
            event_ts = body["event"]["event_ts"]
            for message in messages:
                if message.get("latest_reply") == event_ts:
                    print(message)
                    thread_ts = message.get("thread_ts")
                    print(thread_ts)
                    original_title = message.get("blocks")[0].get("elements")[0].get("elements")[0].get("text")
                    print(original_title)
                    for title, article in articles:
                        #check if strings match roughly (levenshtein distance)
                        if title[2:10] in original_title:
                            original_text = article["text"]
                            break
                    print(original_text)
                        
                    try:
                        await gpt_controller.init_chat(original_title)
                        await gpt_controller.send_message(original_title, original_text)
                    except:
                        pass
                    response = await gpt_controller.send_message(original_title, question)
                    print(response)
                    slack_connector.send_message(os.environ["SLACK_CASHKURS_CHANNEL_ID"], response, thread_ts)
            return {"message": "Success"}
        except Exception as e:
            return {"message": f"Failed: {e}"}
    elif request.method == "GET":
        return {"message": "Hello world!"}
    
if __name__ == "__main__":
    app.run()