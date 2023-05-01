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
cashkurs_controller= CashkursArticlesController()
gpt_controller = GPTChatController()
list_articles = cashkurs_controller.get_articles()
articles = {article["title"]: article for article in cashkurs_controller.get_articles()}
bot_id = "U055J9C6D1T"



@app.route("/api/cashkurs", methods=["GET", "POST"])
async def cashkurs():
    if request.method == "POST":
        body = await request.json
        print(body)
        try:
            messages = slack_connector.get_messages(os.environ["SLACK_CASHKURS_CHANNEL_ID"])
            question = body["event"]["text"]
            event_ts = body["event"]["event_ts"]
            if body["event"].get("user") == bot_id:
                return {"message": "Bot message"}
            
            for message in messages:
                if message.get("latest_reply") == event_ts:
                    thread_ts = message.get("thread_ts")
                    original_title = message.get("blocks")[0].get("elements")[0].get("elements")[0].get("text")
                    for title, article in articles.items():
                        #check if strings match roughly
                        if len(title) > 10 and title[2:10] in original_title:
                            original_text = article["text"]
                            break
                        
                    try:
                        await gpt_controller.init_chat(original_title)
                        await gpt_controller.send_message(original_title, original_text)
                    except:
                        pass
                    response = await gpt_controller.send_message(original_title, question)
                    slack_connector.send_message(os.environ["SLACK_CASHKURS_CHANNEL_ID"], response, thread_ts)
            return {"message": "Success"}
        except Exception as e:
            return {"message": f"Failed: {e}"}
    elif request.method == "GET":
        return {"message": "Hello world!"}
    
if __name__ == "__main__":
    app.run()