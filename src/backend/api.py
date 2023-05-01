from quart import Quart, request
from dotenv import load_dotenv, find_dotenv
import hmac
import os

load_dotenv(find_dotenv())

#def check_signing():



app = Quart(__name__)

@app.route("/api/cashkurs/", methods=["GET", "POST"])
async def cashkurs():
    if request.method == "POST":
        body = await request.json
        print(body)
        return {"message": "Hello world!"}
    elif request.method == "GET":
        return {"message": "Hello world!"}
    
if __name__ == "__main__":
    app.run()