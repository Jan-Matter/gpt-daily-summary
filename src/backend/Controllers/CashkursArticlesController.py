from pathlib import Path
import asyncio
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.backend.Controllers.DocumentDBController import DocumentDBController
from src.backend.Scrapers.CashkursArticleScraper import CashkursArticleScraper
from src.backend.Controllers.GPTChatController import GPTChatController

class CashkursArticlesController:

    def __init__(self):
        self.__documentdb_controller = DocumentDBController()
        self.__scraper = None
        self.__gpt_controller = GPTChatController()

    def get_articles(self):
        return self.__documentdb_controller.get_collection_documents('cashkurs_articles')

    async def refresh_articles(self):
        articles = self.__documentdb_controller.get_collection_documents('cashkurs_articles')
        existing_articles = {article['title'] for article in articles}
        self.__scraper = CashkursArticleScraper(existing_articles)
        new_articles = await self.__scraper.scrap_new_articles()
        for key, article in new_articles.items():
            self.__gpt_controller.init_chat(article['title'])
            text_for_summary = article['text'][:4000]
            article['summary'] = await self.__gpt_controller.send_message(article['title'], f"Please summarize the text in around 20 sentences. Write your summary in German!.: {text_for_summary}")
            self.__documentdb_controller.store_document('cashkurs_articles', article['title'], article)

async def main():
    controller = CashkursArticlesController()
    await controller.refresh_articles()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    #controller = CashkursArticlesController()
    #articles = controller.get_articles()
    #print(articles)