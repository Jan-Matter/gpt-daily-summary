from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from pyppeteer import launch
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
import sys
import os
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from src.backend.Scrapers.BaseArticleScraper import BaseArticleScraper

#load dotenv
load_dotenv(find_dotenv())

class CashkursArticleScraper(BaseArticleScraper):

    def __init__(self, existing_articles):
        self.__existing_articles = existing_articles
        self.__new_articles = {}
        self.__page = None
    
    @property
    def new_articles(self):
        return self.__new_articles

    async def scrap_new_articles(self):
        await self.init_page()
        await self.__scrap_articles_on_page()
        return self.__new_articles

    async def init_page(self):
        self.__page = await (await launch(headless=True, args=['--no-sandbox'])).newPage() # defaultViewport={'width': 1000, 'height': 800},
        self.__page.setDefaultNavigationTimeout(100000)
        await self.__page.goto("https://www.cashkurs.com/login")
        await self.__login()
    
    async def __login(self):
        await self.__page.waitForSelector("#username")
        await self.__page.type("#username", os.environ["CASHKURS_USERNAME"])
        await self.__page.waitForSelector("#password")
        await self.__page.type("#password", os.environ["CASHKURS_PASSWORD"])
        await self.__page.click("#c70 > div > form > div:nth-child(5) > input")
        await self.__page.goto("https://www.cashkurs.com/?id=360")
    
    async def __scrap_articles_on_page(self):
        await asyncio.sleep(3)
        elements = await self.__page.querySelectorAll('a.read-more.pull-right')
        for element in elements:
            link = await self.__page.evaluate('(element) => element.href', element)
            article = await self.__scrap_article(link)
            article["link"] = link
            if article["title"] in self.__existing_articles or article["date"] < "2023-04-27":
                return
            self.__new_articles[article["title"]] = article
        #goto next page
        self.__page.waitForSelector("li.next")
        await self.__page.click("li.next")
        await self.__scrap_articles_on_page()
    
    async def __scrap_article(self, link):
        #async get text content of page with link using aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                await asyncio.sleep(0.5)
                html = await response.text()
                soup = bs(html, 'html.parser')
                text = self.get_text_from_html(soup)
                article = {
                    "title": soup.find("div", {"class": "col-xs-12 col-sm-12 col-md-10 col-md-offset-1"}).find("h1").text.strip(),
                    "text": text,
                    "date": soup.find('time')["datetime"],
                    "author": soup.find("span", {"class": "author-name"}).text.strip(),
                }
                return article

    def get_text_from_html(self, soup):
        text = " ".join([token.strip() for token in soup.get_text().split()])
        return text



async def main():
    scraper = CashkursArticleScraper({})
    await scraper.scrap_new_articles()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())


