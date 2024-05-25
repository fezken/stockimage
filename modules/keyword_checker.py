from modules.network_module import NetworkModule
from config import BASE_URL
from utils.file_utils import FileUtils
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Tuple, Union

class KeywordChecker(NetworkModule):
    def __init__(self) -> None:
        super().__init__(BASE_URL)

    async def get_adobe_stock_results(self, session: aiohttp.ClientSession, keyword: str, category: str, generative_ai: bool) -> Tuple[int, str, str, str]:
        base_url = f"{self.base_url}?filters%5Bcontent_type%3Aimage%5D=1&k={keyword}&safe_search=1"
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

        if response_text is None:
            return timestamp, keyword, "Error fetching the URL", category

        soup = BeautifulSoup(response_text, 'html.parser')
        outer_span = soup.find('span', class_="js-search-results")
        if outer_span:
            h1 = outer_span.find('h1', class_="no-margin")
            if h1:
                strong_tag = h1.find('strong')
                if strong_tag:
                    result_text = strong_tag.get_text()
                    match = re.search(r'(\d[\d\s]*)', result_text)
                    if match:
                        number_of_results = re.sub(r'\s+', '', match.group(1))  # Remove all whitespace
                        return timestamp, keyword, number_of_results, category
                    else:
                        return timestamp, keyword, "Number not found in the text.", category
                else:
                    return timestamp, keyword, "Strong tag not found.", category
            else:
                return timestamp, keyword, "H1 tag not found.", category
        else:
            return timestamp, keyword, "Outer span not found.", category

    async def process_keywords(self, keywords: List[str], category: str, generative_ai: bool) -> List[Tuple[int, str, str, str]]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for keyword in keywords:
                if category == 'both':
                    tasks.append(self.get_adobe_stock_results(session, keyword, 'photos', generative_ai))
                    tasks.append(self.get_adobe_stock_results(session, keyword, 'illustrations', generative_ai))
                else:
                    tasks.append(self.get_adobe_stock_results(session, keyword, category, generative_ai))
            results = await asyncio.gather(*tasks)
            return results

    def check_keywords(self, keywords_string: str, category: str = 'both', generative_ai: bool = False) -> str:
        keywords = [keyword.strip() for keyword in keywords_string.split(',')]
        results = asyncio.run(self.process_keywords(keywords, category, generative_ai))
        headers = ['Timestamp', 'Keyword', 'Search Results', 'Category']
        filename = 'keyword_search_results.csv' if not generative_ai else 'keyword_search_results_generative_ai.csv'
        FileUtils.save_results_to_csv(results, headers, filename)
        return "CSV file updated with search results."
