from abc import ABC, abstractmethod
from pyppeteer import launch

class BaseArticleScraper(ABC):

    def __init__(self, existing_articles):
        self.__existing_articles = existing_articles
        self.__new_articles = {}
        self.__page = None
    
    @property
    def new_articles(self):
        return self.__new_articles

    @abstractmethod
    async def scrap_new_articles(self):
        pass

    @abstractmethod
    async def init_page(self):
        pass