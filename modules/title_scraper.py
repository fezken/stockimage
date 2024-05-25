from modules.network_module import NetworkModule
from config import BASE_URL
from utils.file_utils import FileUtils
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Tuple, Optional

class TitleScraper(NetworkModule):
    def __init__(self) -> None:
        super().__init__(BASE_URL)

    async def get_adobe_stock_titles(self, session: aiohttp.ClientSession, keyword: str, page: int, sort: str, category: str, generative_ai: bool) -> List[Tuple[int, str, int, int, str, str]]:
        base_url = f"{self.base_url}?filters%5Bcontent_type%3Aimage%5D=1&k={keyword}&order={sort}&safe_search=1&search_page={page}&get_facets=0"
        if category == 'photos':
            url = base_url + "&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=0"
        elif category == 'illustrations':
            url = base_url + "&filters%5Bcontent_type%3Aphoto%5D=0&filters%5Bcontent_type%3Aillustration%5D=1"
        else:  # both
            url = base_url + "&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1"
        
        if generative_ai:
            url += "&filters%5Bgentech%5D=only"

        response_text = await self.fetch(session, url)
        timestamp = int(datetime.now().timestamp())
        
        titles = []
        if response_text:
            soup = BeautifulSoup(response_text, 'html.parser')
            results = soup.find_all('div', class_='search-result-cell')
            for idx, result in enumerate(results, start=1):
                thumb_frame = result.find('a', class_='js-search-result-thumbnail')
                if thumb_frame:
                    meta_tag = thumb_frame.find('meta', itemprop='name')
                    if meta_tag:
                        title = meta_tag.get('content', '').strip()
                        titles.append((timestamp, keyword, page, idx, title, category))
        
        return titles

    async def scrape_titles(self, keywords: List[str], pages: List[int], sort: str, category: str, generative_ai: bool) -> List[Tuple[int, str, int, int, str, str]]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for keyword in keywords:
                for page in pages:
                    if category == 'both':
                        tasks.append(self.get_adobe_stock_titles(session, keyword, page, sort, 'photos', generative_ai))
                        tasks.append(self.get_adobe_stock_titles(session, keyword, page, sort, 'illustrations', generative_ai))
                    else:
                        tasks.append(self.get_adobe_stock_titles(session, keyword, page, sort, category, generative_ai))
            results = await self.process_tasks(tasks)
            flattened_results = [title for sublist in results for title in sublist]
            return flattened_results

    def scrape_titles_to_csv(self, keywords_string: str, pages_string: str, sort: str = "nb_downloads", category: str = "both", generative_ai: bool = False) -> str:
        keywords = [keyword.strip() for keyword in keywords_string.split(',')]
        if not pages_string:
            pages = [1]  # Default to page 1 if no input
        elif '-' in pages_string:
            start_page, end_page = map(int, pages_string.split('-'))
            pages = list(range(start_page, end_page + 1))
        else:
            pages = [int(pages_string)]
        
        print(f"Scraping titles for keywords: {keywords}, pages: {pages}, sort: {sort}, category: {category}, generative AI: {generative_ai}")
        
        titles = asyncio.run(self.scrape_titles(keywords, pages, sort, category, generative_ai))
        headers = ['Timestamp', 'Keyword', 'Page', 'Result Number', 'Title', 'Category']
        filename = 'titles.csv' if not generative_ai else 'titles_generative_ai.csv'
        FileUtils.save_results_to_csv(titles, headers, filename)
        
        print(f"Titles scraped: {titles}")
        
        return "CSV file updated with titles."
