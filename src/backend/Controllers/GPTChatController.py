from pathlib import Path
import asyncio
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.backend.Connectors.GPTConnector import GPTConnector

class GPTChatController:

    def __init__(self):
        self.__gpt_connector = GPTConnector()
        self.__chats = {}
    
    def init_chat(self, chat_title):
        if chat_title in self.__chats:
            raise Exception("Chat already exists")
        
        self.__chats[chat_title] = {
            "title": chat_title,
            "messages": []
        }
    
    async def send_message(self, title, message):
        if title not in self.__chats:
            raise Exception("Chat does not exist")
        
        message_dict = {"role": "user", "content": message}
        self.__chats[title]["messages"].append(message_dict)
        response = await self.__gpt_connector.get_chat_respone(self.__chats[title]["messages"])
        response_dict = {"role": "assistant", "content": response}
        self.__chats[title]["messages"].append(response_dict)

        return response
    
async def main1():
    controller = GPTChatController()
    controller.init_chat("test")
    print(await controller.send_message("test", "How old was princess diana when she died?"))
    print(await controller.send_message("test", "How did it happen?"))

async def main2():
    controller = GPTChatController()
    controller.init_chat("test")
    print(await controller.send_message("test", "How old was princess diana when she died?"))
    print(await controller.send_message("test", "How did it happen?"))
    

async def main3():
    controller = GPTChatController()
    controller.init_chat("test")
    print(await controller.send_message("test", "How old was princess diana when she died?"))
    print(await controller.send_message("test", "How did it happen?"))
    


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    try:
        loop.create_task(main1())
        loop.create_task(main2())
        loop.create_task(main3())
        pending = asyncio.all_tasks(loop)
        group = asyncio.gather(*pending, return_exceptions=True)
        results = loop.run_until_complete(group)
    except KeyboardInterrupt:
        pass

